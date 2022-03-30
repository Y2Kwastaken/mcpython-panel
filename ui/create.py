from utils.cosmetics import cfiglet, cinput
from internals.server_installer import create_server
import utils.utils as utils
import os

create_choices = {
    '1': ["Create Server: ", create_server],
}

def create():    
    running = True

    while running:
        os.system("clear")
        cfiglet('&5', "Creation Tools")

        # Prints All The Arguments
        utils.print_arguments(create_choices)

        option = cinput("&2Choose an option: ")
        try:
            create_choices[option][1]()
        except Exception:
            running = False
        os.system("clear")
