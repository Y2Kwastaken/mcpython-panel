from utils.cosmetics import cinput, cprint, cfiglet
from utils.killable_thread import thread_with_trace
import utils.file_utils as fu
import utils.utils as utils
import subprocess
import time
import os
import re
    
class Manager:

    def __init__(self, server_name):
        self.server_name = server_name
        self.choices = {
            '1': ["Start", self.start_server],
            '2': ["Stop", self.stop_server],
            '3': ["Information", self.server_information],
            '4': ["View", self.view_server]
        }
    
    def hub(self):
        os.system("clear")

        running = True
        while running:
            cfiglet('&5', self.server_name)
            utils.print_arguments(self.choices)
            
            option = cinput("&2Choose an option: ")

            try:
                self.choices[option][1]()
                utils.stall()
            except Exception:
                running = False
            os.system("clear")
    
    
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
    

    def server_information(self):
        
        with open(fu.SERVERS+f'/{self.server_name}/info.txt', 'r') as f:
            for line in f.readlines():
                cprint("&e"+line.replace("\n", ""))
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
                utils.server_input(user_input, self.server_name)

        server_view.kill()
        server_view.join(timeout=0.05)
    

    def follow(self):
        '''
        generator function that yields new lines in a file
        '''        
        with open(f'{fu.SERVERS}/{self.server_name}/logs/latest.log') as l:

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

