from internals.error_manager import Panel_Feedback
from utils.cosmetics import cfiglet, cinput
from internals.server_installer import create_server
import utils.utils as utils

create_choices = {
    '1': ["Create Server: ", create_server],
    '2': ["Exit", False],
}

def create(feedback: Panel_Feedback):    
    running = True

    while running:
        feedback.clear()
        cfiglet('&5', "Creation Tools")

        # Prints All The Arguments
        utils.print_arguments(create_choices)

        option = cinput("&2Choose an option: ")
        try:
            action_name = create_choices[option][0]

            if action_name == "Exit":
                running = False
                return
            
            create_choices[option][1](feedback=feedback)
        except KeyError as ke:
            feedback.print_stack_trace(ke)
        feedback.clear()