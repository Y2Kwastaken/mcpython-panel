from http import server
from internals.error_manager import BuildToolsException, FileInstallException, InvalidVersionException, Panel_Feedback
from utils.cosmetics import cprint, cinput, cfiglet
import utils.file_utils as fu
import utils.utils as utils
import os
import subprocess
import shutil

BUILDTOOLS_PATH = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
PAPER_V2_API_VERSION = "https://papermc.io/api/v2/projects/{project}/versions/{version}"
PAPER_V2_API = "https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}/downloads/{download}"
BUNGEE_LATEST = "https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar"

BUILDTOOLS_SUCCESS ="Success!"

spigot_provider_dict = {
    "Spigot": BUILDTOOLS_PATH,
    "BungeeCord": BUNGEE_LATEST,
}

def papermc_api(project: str, feedback: Panel_Feedback=None):
    project = project.lower()
    version = cinput("&cInput a version: ")
    
    try:
        _, json_response = fu.download(PAPER_V2_API_VERSION.format(project=project, version=version), return_json=True, no_download=True)
        
        build = str(json_response["builds"][len(json_response["builds"])-1])

        download_url = PAPER_V2_API.format(project=project, version=version, build=build, download=project+"-"+version+"-"+build+".jar")
        
        cprint("&aBeginning install of &b"+download_url)
        fu.download(download_url)

        basic_setup(project, version)
    except FileInstallException as fie:
        if feedback != None:
            feedback.print_stack_trace(fie)


def spigot_provider(project: str, feedback: Panel_Feedback=None):

    try:
        cprint("&3Installing: "+project)
        link = spigot_provider_dict[project]
        fu.download(link)

        eula=False
        version="latest"
        if project == "Spigot":
            eula=True
            version = cinput("&cInput a version: ")

            wd = fu.chdir(fu.INSTALLS)
            subprocess.call(['java', '-jar', 'BuildTools.jar', f'--rev', f'{version}'])

            last_lines = fu.lastlines("BuildTools.log.txt", 10)
            build_success = False
            for line in last_lines:
                if BUILDTOOLS_SUCCESS in line:
                    build_success = True
                    break
            
            if not build_success:
                raise BuildToolsException(last_lines)
            
                
            os.chdir(wd)
        
        basic_setup(project, version, eula=eula)
    except (KeyError, FileInstallException, InvalidVersionException, BuildToolsException) as ke:
        if feedback != None:
            feedback.print_stack_trace(ke)





create_server_choices = {
    '1': ['Paper', papermc_api],
    '2': ['Spigot', spigot_provider],
    '3': ['BungeeCord', spigot_provider],
    '4': ['Waterfall', papermc_api],
    '5': ['Exit', False],
}

def create_server(feedback: Panel_Feedback):
    '''
    Runs Throguh Creating a server
    '''
    running = True
    while running:
        feedback.clear()
        cfiglet('&5', "Server Creator")
        
        utils.print_arguments(create_server_choices)
        options = cinput("&2Choose an option: ")
        
        try:
            
            type = create_server_choices[options][0]

            if type == "Exit":
                running = False
                return

            create_server_choices[options][1](create_server_choices[options][0], feedback)
        except KeyError as ke:
            feedback.print_stack_trace(ke)

        feedback.clear()



def basic_setup(servertype: str, version: str, eula=True):
    servername = cinput("&3What do you want to name the server: ")
    
    wd = fu.chdir(fu.SERVERS)
    
    if not os.path.exists(servername):
        os.mkdir(servername)
    
    server = fu.getserver(servertype.lower())
    print(server)
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
    
    
