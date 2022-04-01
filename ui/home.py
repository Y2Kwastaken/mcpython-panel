from internals.error_manager import Panel_Feedback
from utils.cosmetics import cfiglet, cinput, cprint
from ui.server_manager import server_manager
from ui.create import create
import utils.utils as utils
import subprocess

panel_feedback = Panel_Feedback(debugmode=True, feedback=True, pause=True)


def enter_firewall(feedback: Panel_Feedback):
    # Subprocess spawn prevents sudo from being needed to run entire panel
    # Panel having sudo could cause security issues and permission issues down the line
    subprocess.call(['sudo', '-E', 'python3', 'scripts/firewall.py'])


home_choices = {
    '1': ["Server Manager: ", server_manager],
    '2': ["Creation Tools: ", create],
    '3': ["Firewall Gateway", enter_firewall],
    '4': ["Exit", False],
}

def home():    
    fcol: str = "&5"
    ftext: str = "Minecraft Panel"
    foot: str = "&fRepository: https://github.com/Y2Kwastaken/mcpython-panel"
    utils.create_user_interface(home_choices, panel_feedback, ftext, fcol, foot, panel_feedback)