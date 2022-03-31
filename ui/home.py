from internals.error_manager import Panel_Feedback
from utils.cosmetics import cfiglet, cinput, cprint
from ui.server_manager import server_manager
from ui.create import create
import utils.utils as utils
import sys
import os


feedback = Panel_Feedback(debugmode=True, feedback=True, pause=True)

home_choices = {
    '1': ["Server Manager: ", server_manager],
    '2': ["Creation Tools: ", create],
    '3': ["Exit", sys.exit],
}

def home():    
    running = True

    while running:
        feedback.clear()
        
        cfiglet('&5', "Minecraft Panel")
        cprint("&fGithub Repository: &3https://github.com/Y2Kwastaken/python-panel")
        # Prints All The Arguments
        utils.print_arguments(home_choices)

        option = cinput("&2Choose an option: ")
        try:
            home_choices[option][1](feedback)
        except KeyError as ke:
            feedback.print_stack_trace(ke)
        
        feedback.clear()
