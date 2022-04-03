from internals.error_manager import Panel_Feedback
from utils.cosmetics import cinput, cprint, cfiglet
from utils.killable_thread import thread_with_trace
import utils.file_utils as fu
import utils.utils as utils
import subprocess
import time
import os
import re
    
proxies = ['BungeeCord', 'Waterfall']

class Manager:

    def __init__(self, server_name: str, feedback: Panel_Feedback):
        self.server_name: str = server_name
        self.feedback: Panel_Feedback = feedback
        self.choices: dict = {
            '1': ["Start", self.start_server],
            '2': ["Stop", self.stop_server],
            '3': ["Restart", self.restart_server],
            '4': ["Information", self.server_information],
            '5': ["View", self.view_server],
            '6': ["Exit", False],
        }
        self.info = {}
        with open(fu.SERVERS+f'/{self.server_name}/info.txt', 'r') as f:
            for line in f.readlines():
                larr = line.split("=")
                self.info[larr[0]] = larr[1].replace("\n", "")

    
    def hub(self):
        
        running = True
        while running:
            self.feedback.clear()
            cfiglet('&5', self.server_name)
            utils.print_arguments(self.choices)
            
            option = cinput("&2Choose an option: ")

            try:
                action_name = self.choices[option][0]

                if action_name == "Exit":
                    running = False
                    return

                self.choices[option][1]()
                self.feedback.pause_panel()
            except KeyError as ke:
                self.feedback.print_stack_trace(ke)
            self.feedback.clear()
    
    
    def server_running(self):
        '''
        Returns true if the server is already running
        Precondition: Server Name must be valid
        '''

        wd = fu.chdir(fu.SCRIPTS)

        try:
            subprocess.check_output(['./server_status.sh', f'{self.server_name}'])
            return True
        except:
            return False
        finally:
            os.chdir(wd)

    
    def start_server(self):

        if not os.path.isdir(fu.SERVERS+"/"+self.server_name):
            cprint("&cThat is not a server")
            return

        if self.server_running():
            cprint("&cThat server is already running")
            return
        
        wd = fu.chdir(fu.SERVERS+"/"+self.server_name)

        os.system(f'screen -S {self.server_name} -d -m ./start.sh')
        
        os.chdir(wd)
        cprint("&aStarted The Server")
    

    def stop_server(self):

        if not self.server_running():
            cprint("&cThat server is not running so it can not be stopped")
            return
        
        wd = fu.chdir(fu.SCRIPTS)

        try:
            server = subprocess.check_output(['./server_status.sh', f'{self.server_name}'])
            pid = re.sub('(?=[.]).*', '', str(server))
            pid = re.sub('[^0-9]', '', pid)
            
            subprocess.call(['screen', '-XS', f'{pid}', 'quit'])
            cprint("&aStopped the server")
        except Exception:
            cprint("&cCould not stop the server")
        finally:
            os.chdir(wd)
    

    def restart_server(self):
        if self.server_running():
            self.stop_server()
            time.sleep(5)
            self.start_server()
        else:
            self.start_server()


    def server_information(self):
        
        for k in self.info:
            cprint("&e"+k+"="+self.info[k])
        cprint("&erunning="+str(self.server_running()))

    def view_server(self):
        #screen -S myScreen -X eval 'stuff "save-all\015"'
        #from utils.serverutils import follow, server_input
        #import threading

        #x = threading.Thread(target=lambda: follow("paper_test"))
        #x.start()
        #server_input("paper_test")
        #print("exited")
        server_view = thread_with_trace(target=self.follow)
        server_view.start()

        running = True
        while running:
            user_input = input()
            if user_input == "exit":
                running = False
            else:
                self.server_input(user_input)

        server_view.kill()
        server_view.join(timeout=0.05)


    def server_input(self, user_input):
        subprocess.call(['screen', '-S', f'{self.server_name}', '-X', 'stuff', f'{user_input}\015'])

    def follow(self):
        '''
        generator function that yields new lines in a file
        '''        
        relative_log_location = "logs/latest.log"
        
        if self.info['type'] in proxies:
            relative_log_location = "proxy.log.0"

        with open(f'{fu.SERVERS}/{self.server_name}/{relative_log_location}') as l:

            # seek the end of the file
            l.seek(0, os.SEEK_END)
            
            # start infinite loop
            while True:
                # read last line of file
                line = l.readline()        # sleep if file hasn't been updated
                if not line:
                    time.sleep(0.1)
                    continue

                cprint(line.replace("\n", ""))

