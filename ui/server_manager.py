from multiprocessing import Manager
import traceback
from internals.error_manager import Panel_Feedback
import utils.utils as utils
import os
from internals.manager import Manager
from utils.cosmetics import cfiglet, cinput, cprint


def server_manager(feedback: Panel_Feedback):
    manager_choices = {}

    num = 1
    for server in utils.get_all_servers():
        manager_choices[str(num)] = [server , Manager]
        num+=1
    
    manager_choices[str(num)] = ["Exit", False]
    running = True    
    while running:
        feedback.clear()

        cfiglet('&5', "Server Manager")
        # Prints All The Arguments
        utils.print_arguments(manager_choices)

        option = cinput("&2Choose an option: ")
        try:
            action_name = manager_choices[option][0]

            if action_name == "Exit":
                running = False
                return 

            manager = manager_choices[option][1](server_name=action_name, feedback=feedback)
            manager.hub()
        except KeyError as ke:
            feedback.print_stack_trace(ke)
        
        feedback.clear()
