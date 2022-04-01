from internals.error_manager import Panel_Feedback
from utils.cosmetics import cfiglet, cinput, cprint
import utils.file_utils as fu
import os

def print_arguments(dict: dict, index=0):
    '''
    Prints all arguments from a dictionary
    formated as:
    [key] value[0]
    value must be a list
    '''
    for k, v in dict.items():
        cprint(f'&a[{k}] {v[index]}')


def get_all_servers():
    '''
    Returns a list of all servers
    This assumes all folders are a server
    '''
    dirs = []
    for dir in os.listdir(fu.SERVERS):
        if os.path.isdir(fu.SERVERS+"/"+dir):
            dirs.append(dir)
    return dirs
    

def create_user_interface(choices: dict, feedback: Panel_Feedback, figlet_text: str="Sample", figlet_color: str="&6", footer=None, *args):
    # Creates Loop that can be deactived to terminate the interface
    running = True

    while running:
        # Clears the screen see method for preformance benefits
        feedback.clear()
        
        # Spinning up figlet and print footer if there is one
        cfiglet(figlet_color, figlet_text)
        if footer != None:
            cprint(footer)

        # Prints All Arguments
        print_arguments(choices)

        option = cinput("&2Choose an option: ")
        # Try Except catches all errors and displays them in a readable fassion
        try:
            action_name = choices[option][0]

            if action_name == "Exit":
                running = False
                return
            
            choices[option][1](*args)
        except Exception as e:
            feedback.print_stack_trace(e)
        
        feedback.clear()
