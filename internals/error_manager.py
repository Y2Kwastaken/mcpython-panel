from http import HTTPStatus, server
from re import L
from utils.cosmetics import cprint
from utils.file_utils import download
import traceback as tback

class Panel_Feedback:

    SERVERTYPES = {
        'spigot-domain': ['spigot', 'bungee'],
        'papermc-domain': ['paper', 'waterfall'],
    }
    PAPER_API = "https://papermc.io/api/v2/projects/{project}"

    def __init__(self, debugmode, feedback, pause):
        self.debugmode = debugmode
        self.feedback = feedback
        self.pause = pause
    

    def print_stack_trace(self, exception: Exception, limited: bool=False):
        if not limited:
            cprint("&4ERROR OCCURED")
            cprint("&4-------------------------")
            cprint('&4'+tback.extract_stack)
            cprint("&4-------------------------")
        else:
            cprint("&4ERROR OCCURED")
            cprint("&4Cuase: "+exception.__cause__)
        self.pause_panel()


    def pause_panel(self):
        if self.pause:
            input("Press Enter To Continue...")
    

    def check_version(self, servertype: str, version: str):
        servertype=servertype.lower()
        '''
        Precondition: servertype must be valid
        '''
        if servertype in self.SERVERTYPES['spigot-domain']:
            if servertype == "bungee":
                '''do stuff'''
            else:
                '''get versions'''
        elif servertype in self.SERVERTYPES['papermc-domain']:
            '''
            Get Valid Project Versions
            '''
            response_code, json_response = download(self.PAPER_API.format(project=servertype))

            if response_code == 404:
                raise HTTPNotFound
            
            if version not in json_response['versions']:
                raise InvalidVersionException
            


class InvalidVersionException(Exception):

    def __init__(self, servertype, version):
        self.servertype = servertype
        self.version = version
        self.message = f'There is no version: {version} for servertype: {servertype}'
        super().__init__(self.message)


class HTTPNotFound(Exception):
    
    def __init__(self):
        super().__init__("404 Error Request Not Found")
