from utils.cosmetics import cprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import utils.file_utils as fu
import os
import subprocess

BUILDTOOLS_PATH = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/paper/versions/{version}"
PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"

def spigot(version):
    '''
    Runs spigots build tools and downloads it if it doesn't exist already
    '''
    wd = fu.chdir(fu.INSTALLS)
    # Installs BuildTools.jar if it doesn't exist
    if not os.path.isfile(os.getcwd() + "/BuildTools.jar"):
        fu.download(BUILDTOOLS_PATH)
    
    if os.path.isfile(fu.INSTALLS + f'/spigot-{version}.jar'):
        cprint("&a Found Server Version: " + f'spigot-{version}.jar')
    else:
        subprocess.call(['java', '-jar', 'BuildTools.jar', f'--rev', f'{version}'])
        cprint("&aFinished installing the spigot server for the version " + str(version))
    os.chdir(wd)            


def paper(version):
    '''
    Installs Paper Using Paper's v2 api
    '''
    response_code, json_response = fu.download(PAPER_V2_API_VERSION.format(version=version), return_json=True, no_download=True)

    if response_code == 404:
        cprint("&4An Error Occurred while fetching version information for your server please try again")
        return False
    
    project_id = json_response["project_id"]
    build = str(json_response["builds"][len(json_response["builds"])-1])

    download_url = PAPER_V2_API.format(project=project_id, version=version, build=build, download=project_id+"-"+version+"-"+build+".jar")
    
    print(download_url)
    response_code = fu.download(download_url)

    if response_code == 404:
        cprint("&4An Error Occurred while installing your server please try again")
        return False
    else:
        cprint("&aSuccessfully installed your paper server")
    
    return True