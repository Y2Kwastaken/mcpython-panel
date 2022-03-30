from xmlrpc import server
from utils.cosmetics import cprint, cinput, cfiglet
import utils.file_utils as fu
import utils.utils as utils
import os
import subprocess
import shutil
import traceback as tb

BUILDTOOLS_PATH = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/{project}/versions/{version}"
PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"
BUNGEE_LATEST = "https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar"
BUNGEE_BUILD = "https://ci.md-5.net/job/BungeeCord/{build}/artifact/bootstrap/target/BungeeCord.jar"


def papermc_api(project: str, version: str):
    response_code, json_response = fu.download(PAPER_V2_API_VERSION.format(project=project, version=version), return_json=True, no_download=True)

    if response_code == 404:
        cprint("&cAn error occured when installing please try again later")
        return
    
    build = str(json_response["builds"][len(json_response["builds"])-1])

    download_url = PAPER_V2_API.format(project=project, version=version, build=build, download=project+"-"+version+"-"+build+".jar")
    
    cprint("&aBeginning install of &b"+download_url)
    response_code = fu.download(download_url)

    if response_code == 404:
        cprint("&4An Error Occurred while installing your server please try again")
        return False
    else:
        cprint("&aSuccessfully installed your server")


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


def bungee(build: str):
    '''
    Installs a build of bungee
    '''
    if build.lower() != "latest":
        fu.download(BUNGEE_BUILD.format(build=build))
        return
    fu.download(BUNGEE_LATEST)


create_server_choices = {
    '1': ['Paper', papermc_api],
    '2': ['Spigot', spigot],
    '3': ['Bungee', bungee],
    '4': ['Waterfall', papermc_api],
}

def create_server():
    '''
    Runs Throguh Creating a server
    '''
    running = True
    while running:
        os.system("clear")
        cfiglet('&5', "Server Creator")
        
        utils.print_arguments(create_server_choices)

        options = cinput("&2Choose an option: ")
        
        try:
            type = create_server_choices[options][0]
            print(type)
            if type == "Bungee" or type == "Waterfall":
                proxy_setup(create_server_choices[options][1], type)
            else:
                version = cinput("&cInput a version: ")
                server_setup(create_server_choices[options][1], type, version)
        except:
            #Uncomment below for debug
            #tb.print_exc()
            #utils.stall()
            running = False


def proxy_setup(download, proxytype: str):
    version = "unkown"
    if proxytype.lower() == "bungee":
        cprint("&cWarning a build is not the same as a version\nto see all bungee builds go to the link below\nhttps://ci.md-5.net/job/BungeeCord/")
        cprint("input latest to get the latest build")
        build = cinput("&cInput a build: ")
        bungee(build)
    elif proxytype.lower() == "waterfall":
        cprint("&cWarning while you may beable to get older versions of waterfall upto 1.11")
        cprint("&cI caution you to always get the latest version. proxies support multiple minecraft versions")
        version = cinput("&cInput a version: ")
        papermc_api("waterfall", version)
    else:
        cprint("&cThat proxytype does not exist")
        utils.stall()
        return
    
    basic_setup(proxytype, version, eula=False)


def server_setup(download, servertype: str, version: str):

    if servertype.lower() == "spigot":
       download(version)
    elif servertype.lower() == "paper":
        download(servertype.lower(), version)
    else:
        cprint("&cThat servertype does not exist")
        utils.stall()
        return
    basic_setup(servertype, version)


def basic_setup(servertype: str, version: str, eula=True):
    servername = cinput("&3What do you want to name the server: ")
    
    wd = fu.chdir(fu.SERVERS)
    os.mkdir(servername)
    
    server = fu.getserver(servertype.lower())
    shutil.move(fu.INSTALLS + "/" + server, fu.SERVERS + "/"+servername+"/"+"server.jar")

    minram = cinput("&7What is the minimum amount of ram (for this server) in megabytes: ")
    maxram = cinput("&7What is the max amount of ram (for this server) in megabytes: ")
    
    # java -Xms2G -Xmx2G -jar paper.jar --nogui
    with open(servername+"/start.sh", "w") as f:
        f.write('#! /bin/sh\n')
        f.write(f'java -jar -Xms{minram}M -Xmx{maxram}M -jar server.jar')
        if servertype == "paper":
            f.write(" --nogui")
        f.close() 
    
    if eula:
        with open(servername+"/eula.txt", "w") as f:
            f.write("eula=true")
    
    with open(servername+"/info.txt", "w") as f:
        f.write("type="+servertype+"\n")
        f.write("version="+version+"\n")

    subprocess.call(['chmod', '+x', f'{servername}/start.sh'])
    os.chdir(wd)
    
    
