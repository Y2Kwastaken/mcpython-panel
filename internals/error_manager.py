from utils.cosmetics import cprint
import traceback as tback
import os

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
    

    def print_stack_trace(self, exception: Exception):
        if not self.feedback:
            return

        if self.debugmode:
            self.clear()
            cprint("&4ERROR OCCURED")
            cprint("&4-------------------------")
            tback.print_exc()
            cprint("&4-------------------------")
        else:
            cprint("&4"+str(type(exception).__name__))
            cprint("&4"+str(exception.args))
        self.pause_panel()


    def pause_panel(self):
        if self.pause:
            input("Press Enter To Continue...")


    def clear(self):
        # Time differential on tests
        #os.system("clear") -> 0.0015304088592529297
        #print(\033c) -> 3.075599670410156e-05
        # Using a faster method leads to smoother and quick transitions from panel screen
        print("\033c")


class InvalidVersionException(Exception):

    def __init__(self, servertype, version):
        self.message = f'There is no version: {version} for servertype: {servertype}'
        super().__init__(self.message)


class FileInstallException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BuildToolsException(Exception):

    def __init__(self, error):
        super().__init__(error)
