from utils.cosmetics import cprint, cinput
from setup import setup

def main():
    running = True
    while running:
        running = panel()

def panel():

    commands()
    # Loops Through Options
    while 1:
        user_input = cinput("&7Choose an option from above: ")
        if user_input == "setup":
            setup.hub()
            commands()
        elif user_input == "refresh":
            return True
        elif user_input == "exit":
            return False
        elif user_input == "help":
            commands()
        else:
            cprint("&cThat wasn't an option try again")


def commands():
    '''
    prints commands for the panel
    '''
    cprint('''&a
         __  __ _                            __ _     ____                  _ 
        |  \/  (_)_ __   ___  ___ _ __ __ _ / _| |_  |  _ \ __ _ _ __   ___| |
        | |\/| | | '_ \ / _ \/ __| '__/ _` | |_| __| | |_) / _` | '_ \ / _ \ |
        | |  | | | | | |  __/ (__| | | (_| |  _| |_  |  __/ (_| | | | |  __/ |
        |_|  |_|_|_| |_|\___|\___|_|  \__,_|_|  \__| |_|   \__,_|_| |_|\___|_|

        &fGithub: &3https://github.com/Y2Kwastaken
        &fRepository: &3https://github.com/Reecepbcups/minecraft-panel
        
        ''')

    cprint('''
    &6Panel Commands
    &8----------------------------
    &asetup: brings you to an area for general setup
    &ahelp: displays this
    &crefresh: refreses the panel
    &4exit: exits the panel instance
    ''')

main()