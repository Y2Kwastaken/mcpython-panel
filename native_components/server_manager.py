from asyncio import start_server
from utils.file_utils import CONFIG, chdir
from utils.cosmetics import cprint
from utils.panel_utils import Panel_Interface
import os
import shlex
import subprocess

class ServerPanel():

    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.choices = {
            '1': ["Start", self.start_server]
        }
        self.panel = Panel_Interface(self.choices, self.name, "&2")
    
    
    def display(self):
        self.panel.launch()
    

    def start_server(self):
        wd = chdir(self.path)
        p = subprocess.Popen(['./start.sh'], start_new_session=True)
        os.chdir(wd)
        self.panel.feedback.pause_panel()


def fetch_servers(choices: dict):
    serverloc = CONFIG.get("serverloc")
    if not os.path.exists(serverloc):
        cprint(
            f'''
            &cYou don't have any servers yet create servers using 
            the server creator or change the paths in the config.yml
            your config location is: {os.getcwd() + "/configs/config.yml"}
            ''')

    count = 1
    # serverloc servers
    for server in os.listdir(serverloc):
        choices[str(count)] = [server, ServerPanel(serverloc+"/"+server).display]
        count += 1
    
    # External Servers not in serverloc
    external_servers = CONFIG.get("external_servers")
    if external_servers is None:
        pass
    else:
        for server in external_servers:
            choices[str(count)] = [os.path.basename(server), ServerPanel(server).panel]
            count +=1


def on_call(headPanel: Panel_Interface):
    choices = {}
    fetch_servers(choices)
    panel = Panel_Interface(choices, "Server Manager", "&b", "An Example Panel")
    panel.launch()
    