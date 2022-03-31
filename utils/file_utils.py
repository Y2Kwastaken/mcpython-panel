import requests
import os
import zipfile

from internals.error_manager import FileInstallException

SCRIPTS = os.getcwd() + "/scripts"
INSTALLS = os.getcwd() + "/installs"
SERVERS = os.getcwd() + "/servers"

def download(link, name=None, return_json=False, no_download=False):
    '''
    Downloads a file form the internet using the basic-installer.sh script
    More details about this script in the file itself
    '''

    wd = chdir(INSTALLS)
    data = requests.get(link)

    if not no_download:
        if name == None:
            name = link.split('/')[-1] 
        
        with open(name, 'wb') as f:
            f.write(data.content)
        os.chdir(wd)

    if data.status_code == 404:
        raise FileInstallException(link, data.status_code, data.reason)

    if return_json:
        return data.status_code, data.json()
    
    return data.status_code


def chdir(dir):
    '''
    A better version of os.chdir
    '''
    wd = os.getcwd()
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f'created directory at {dir}')
        os.chdir(dir)
    else:
        os.chdir(dir)
    return wd

def unzip(path, file_name, dest=None):
    with zipfile.ZipFile(path+"/"+file_name, 'r') as zip_ref:
        if dest == None:
            zip_ref.extractall(path)   
        else:
            zip_ref.extractall(dest) 


def getserver(servertype):
    wd = chdir(INSTALLS)

    for file in os.listdir():
        if servertype.lower() in file.lower():
           os.chdir(wd)
           return os.path.basename(file)
    
    os.chdir(wd)


def lastlines(fname, N):
    assert N >= 0
    pos = N + 1
    lines = []
    with open(fname) as f:
        # loop which runs
        # until size of list
        # becomes equal to N
        while len(lines) <= N:
            try:
                f.seek(-pos, 2)
            except IOError:
                f.seek(0)
                break
            finally:
                lines = list(f)
            pos *= 2
    return lines[-N:]