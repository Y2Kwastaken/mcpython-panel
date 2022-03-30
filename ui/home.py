from internals.server_installer import create_server
from utils.cosmetics import cfiglet, cinput, cprint
from ui.server_manager import server_manager
from ui.create import create
import utils.utils as utils
import sys
import os
import traceback


home_choices = {
    '1': ["Server Manager: ", server_manager],
    '2': ["Creation Tools: ", create],
    '3': ["Exit", sys.exit],
}

def home():    
    running = True

    while running:
        os.system("clear")
        cfiglet('&5', "Minecraft Panel")
        cprint("&fGithub Repository: &3https://github.com/Y2Kwastaken/python-panel")

        # Prints All The Arguments
        utils.print_arguments(home_choices)

        option = cinput("&2Choose an option: ")
        try:
            home_choices[option][1]()
        except Exception:
            traceback.print_exc()
            cprint("&4A Serious Error Occurred while running that command")
            cprint("&4If you are not make sure you are entering the numerator")