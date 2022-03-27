import requests
import os
import zipfile

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
        if servertype in file:
           os.chdir(wd)
           return os.path.basename(file)
    
    os.chdir(wd)