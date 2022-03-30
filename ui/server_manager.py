from multiprocessing import Manager
import traceback
import utils.utils as utils
import os
from internals.manager import Manager
from utils.cosmetics import cfiglet, cinput, cprint


def server_manager():
    os.system('clear')
    manager_choices = {}

    num = 1
    for server in utils.get_all_servers():
        manager_choices[str(num)] = [server , Manager]
        num+=1
    
    running = True    
    while running:
        cfiglet('&5', "Server Manager")
        # Prints All The Arguments
        utils.print_arguments(manager_choices)

        option = cinput("&2Choose an option: ")
        try:

            # Attemps To Interface With The
            manager = manager_choices[option][1](server_name=manager_choices[option][0])
            manager.hub()
        except Exception:
            running = False
        os.system("clear")