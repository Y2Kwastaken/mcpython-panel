from setup import installer
from utils import file_utils as fu
from utils.cosmetics import cprint, cinput
import os
import subprocess
import shutil


def hub():
    commands()

    running = True

    while running:
        user_input = cinput("&7Choose an option from above: ")

        if user_input == "create server":
            create_server()
            commands()
        elif user_input == "help":
            commands()
        elif user_input == "exit":
            return False
        else:
            cprint("&cThat wasn't a valid option try again")

        
def create_server():
    '''
    Creates A Server
    '''

    valid = False

    while not valid:
        servertype =cinput("&3What type of server do you want [spigot/paper]: ")
        version = cinput("&3What version do you want your server to be: ")
        valid = True
        if servertype == "spigot":
            installer.spigot(version)
            valid = True
        elif servertype == "paper":
            # Check To See If Everything Installed Correctly
            if installer.paper(version):
                valid = True
            else:
                return
        else:
            cprint("&cThat was not a valid option")
    
    servername = cinput("&3What do you want to name the server: ")
    
    wd = fu.chdir(fu.SERVERS)
    os.mkdir(servername)
    
    server = fu.getserver(servertype)
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
    
    with open(servername+"/eula.txt", "w") as f:
        f.write("eula=true")
    
    with open(servername+"/info.txt", "w") as f:
        f.write("type="+servertype+"\n")
        f.write("version="+version+"\n")

    subprocess.call(['chmod', '+x', f'{servername}/start.sh'])
    os.chdir(wd)


def commands():
    '''
    Commands displayed
    '''

    cprint('''
    &b
     ____       _               
    / ___|  ___| |_ _   _ _ __  
    \___ \ / _ \ __| | | | '_ \ 
     ___) |  __/ |_| |_| | |_) |
    |____/ \___|\__|\__,_| .__/ 
                         |_|   
    ''')
    
    cprint('''
    &6Setup Commmands
    &8---------------------------------------
    &ahelp: displays this
    &acreate server: creates a server either paper or spigot
    &4exit: exits the setup area
    ''')