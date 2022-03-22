import subprocess
import os
import zipfile

INSTALL_SCRIPT = os.getcwd() + "/python_panel/utility_scripts"
INSTALLS = os.getcwd() + "/python_panel/installs"
UTILITY_SCRIPTS = os.getcwd() + "/python_panel/utility_scripts"

def download(link):
    '''
    Downloads a file form the internet using the basic-installer.sh script
    More details about this script in the file itself
    '''
    wd = chdir(INSTALL_SCRIPT)
    subprocess.call([f'./basic-installer.sh', link])
    os.chdir(wd)

def chdir(dir, credir=True):
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