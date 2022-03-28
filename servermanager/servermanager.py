from typing import final
import utils.file_utils as fu
from utils.cosmetics import cprint, cinput
import subprocess
import os
import re


def list_servers():
    wd = fu.chdir(fu.SERVERS)

    cprint("&6A List Of All Your Servers: ")
    cprint("&8---------------------------------")
    for server in os.listdir():
        type = "unkown"
        version = "unkown"

        if os.path.isfile(os.getcwd()+"/"+server+"/info.txt"):      
            with open(os.getcwd()+"/"+server+"/info.txt", 'r') as f:
                for line in f.readlines():
                    if "type=" in line:
                        type = line.replace("type=", "").replace("\n", "")
                    elif "version=" in line:
                        version = line.replace("version=", "").replace("\n", "")

        cprint(f'&3{server}:&e{version}:&c{type}')

    os.chdir(wd)

def start_server(take_over=False):

    server_name = cinput("&7What is the name of the server you want to start: ")

    if not os.path.isdir(fu.SERVERS+"/"+server_name):
        cprint("&cThat is not a server")
        return

    if server_running(server_name):
        cprint("&cThat server is already running")
        return
    
    wd = fu.chdir(fu.SERVERS+"/"+server_name)

    if not take_over:
        os.system(f'screen -S {server_name} -d -m ./start.sh')
    else:
        os.system('./start,sh')
    os.chdir(wd)


def stop_server():

    server_name = cinput("&7What is the name of the server you want to stop: ")

    if not server_running(server_name):
        cprint("&cThat server is not running so it can not be stopped")
    
    wd = fu.chdir(fu.SCRIPTS)

    try:
        server = subprocess.check_output(['./server_status.sh', f'{server_name}'])
        
        pid = re.sub('(?=[.]).*', '', str(server))
        pid = re.sub('[^0-9]', '', pid)
        
        subprocess.call(['screen', '-XS', f'{pid}', 'quit'])
        cprint("&aStopped the server")
    except Exception:
        cprint("&cCould not stop the server")
    finally:
        os.chdir(wd)

def server_running(server_name):
    '''
    Returns true if the server is already running
    Precondition: Server Name must be valid
    '''

    wd = fu.chdir(fu.SCRIPTS)

    try:
        subprocess.check_output(['./server_status.sh', f'{server_name}'])
        return True
    except:
        return False
    finally:
        os.chdir(wd)