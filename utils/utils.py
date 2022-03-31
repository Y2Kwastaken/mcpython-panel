from re import L
from utils.cosmetics import cinput, cprint
import utils.file_utils as fu
import os
import time
import subprocess

def follow(server_name, log="latest.log"):
    '''generator function that yields new lines in a file
    '''

    with open(f'{fu.SERVERS}/{server_name}/logs/{log}') as l:

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

def server_input(user_input, server_name):
    subprocess.call(['screen', '-S', f'{server_name}', '-X', 'stuff', f'{user_input}\015'])


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
    '''
    dirs = []
    for dir in os.listdir(fu.SERVERS):
        if os.path.isdir(fu.SERVERS+"/"+dir):
            dirs.append(dir)
    return dirs