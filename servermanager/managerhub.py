from utils.cosmetics import cprint, cinput
import servermanager.servermanager as sm

def hub():
    commands()

    running = True

    while running:
        user_input = cinput("&7Choose an option from above: ")

        if user_input == "status":
            print("status")
        elif user_input == "start":
            sm.start_server()
        elif user_input == "start takeover":
            sm.start_server(take_over=True)
        elif user_input == "stop":
            sm.stop_server()
        elif user_input == "list":
            sm.list_servers()
        elif user_input == "help":
            commands()
        elif user_input == "exit":
            running = False
        else:
            cprint("&cThat wasn't a valid option try again")


def commands():
    cprint('''&5
     ____                             __  __                                   
    / ___|  ___ _ ____   _____ _ __  |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
    \___ \ / _ \ '__\ \ / / _ \ '__| | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
     ___) |  __/ |   \ V /  __/ |    | |  | | (_| | | | | (_| | (_| |  __/ |   
    |____/ \___|_|    \_/ \___|_|    |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                                                               |___/  
    ''')

    cprint('''
    &6Manager Commands
    &8----------------------------
    &ahelp: displays this
    &astatus: shows status of all servers
    &astart: start's a server of your choice
    &astart takeover: start's a server, but takes over the panel until the server is stopped
    &4stop: stop's a server of your choice
    &alist: list's all servers you currently have
    &4exit: exits the server manager area
    ''')