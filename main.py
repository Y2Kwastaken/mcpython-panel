from importlib import import_module
from utils.file_utils import gather_plugins
from utils.cosmetics import cprint
from utils.panel_utils import Panel_Interface 
import native_components.server_creator as screator
import time

choices = {
    '0': ["Server Creator", screator.onCall]
}

if __name__ == "__main__":
    plugins = gather_plugins()
    start = time.time()*1000

    curdex = len(choices.keys())
    for key in plugins:
        temp_import = import_module("plugins."+plugins[key])
        choices[str(curdex)] = [key, temp_import.onCall]
        curdex+=1
    end = time.time()*1000
    cprint(f'&aLoaded all plugins in {end-start} miliseconds')

    panel = Panel_Interface(choices, "MCAdminPanel", "&4", "A Minecraft Python Administrator panel", "self")
    panel.launch()