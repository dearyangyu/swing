# -*- coding: utf-8 -*-
_VERSION = "1.00"

import argparse
import platform

import sys
sys.path.append("./module")

import os
from pprint import pprint

import requests
import zipfile

SWING_DOWNLOAD = "https://github.com/wildchild-animation/swing/archive/refs/heads/main.zip"

# local import wildchildanimation module by adding to the path
WCA_ROOT = "C:/WCA"

def split_path(path):
     return os.path.splitdrive(path)

def get_python_version(path = ''):
    cmd = '{}python --version'.format(path)
    try:
        p = os.popen(cmd)
        s = p.read()
        p.close()    
        return s
    except:
        return None     

def check_or_create_dir(dir):
    if not os.path.exists(dir):
        print("Creating new directory: {}".format(dir))  
        os.makedirs(dir)
    else:
        print("Found directory {}".format(dir))

def create_venv(dir):
    drive, tail = split_path(dir)        
    cmd = '{} && cd {} && python -m venv env'.format(drive, dir)
    print(cmd)

    p = os.popen(cmd)
    s = p.read()
    p.close()    

    pprint(s)

def update_requirements(dir):
    drive, tail = split_path(dir)        
    cmd = '{} && cd {} && "env/Scripts/activate" && pip install -r swing/swing-main/requirements.txt'.format(drive, dir)
    print(cmd)    

    p = os.popen(cmd)
    s = p.read()
    p.close()   

    pprint(s)

def get_swing_release():
    req = requests.get('https://raw.githubusercontent.com/wildchild-animation/swing/main/module/swing.version')
    return req.text

def run_swing_standalone(dir):
    drive, tail = split_path(dir)        
    #  c:; cd 'c:\DEV\Github\wca-maya'; & 'c:\DEV\Github\wca-maya\venv\Scripts\python.exe' 'c:\Users\pniemandt\.vscode\extensions\ms-python.python-2021.5.842923320\pythonFiles\lib\python\debugpy\launcher' '1778' '--' 'c:\DEV\Github\wca-maya\plugin\treehouse\swing_desktop.py' 
    cmd = '{} &&  cd {}/swing && "{}/env/Scripts/activate" && python {}/swing/swing-main/plugin/treehouse/swing_desktop.py'.format(drive, dir, dir, dir)
    print(cmd)

    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()   

    pprint(s)

def download_latest(dir):
    check_or_create_dir(dir)

    req = requests.get(SWING_DOWNLOAD, stream = True)
    with open("{}/swing-main.zip".format(dir), 'wb') as fd:
        for chunk in req.iter_content(chunk_size = 1024):
            fd.write(chunk)
    return True

def extract_latest(download_dir, module_dir):
    check_or_create_dir(module_dir)
    with zipfile.ZipFile("{}/swing-main.zip".format(download_dir), 'r') as zf:
        zf.extractall(module_dir)
    
    return True

def setup_windows(working_dir):
    # make sure we have default directories
    check_or_create_dir(working_dir)

    install_dir = "{}/installs".format(working_dir)
    if not os.path.exists(install_dir):
        download_latest(install_dir)

    module_path = "{}/swing".format(working_dir)
    if not os.path.exists(module_path):
        check_or_create_dir(module_path)
        extract_latest(install_dir, module_path)

    version_path = "{}/swing/swing-main/module/swing.version".format(working_dir)
    if not os.path.exists(module_path):
        download_latest(install_dir)
        extract_latest(install_dir, module_path)

    local_version = open(version_path, 'r').read()
    release_version = get_swing_release()

    if not local_version == release_version:
        download_latest(install_dir)
        extract_latest(install_dir, module_path)
    else:
        print("Swing up to date")

    update_requirements(working_dir)
    run_swing_standalone(working_dir)

def update(working_dir):
    print("treehouse: swing updater v{}".format(_VERSION))

    if working_dir is None:
        install_dir = WCA_ROOT
    else:
        install_dir = working_dir
    print("path: {}".format(install_dir))

    python_version = get_python_version()
    if not python_version:
        print("Pleasure ensure python is in your path")
        exit(-2)
    else:
        print("Found {}".format(python_version))        

    if "Windows" in platform.platform():
        setup_windows(install_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help = "Target dir", default = None, action='store')

    args = parser.parse_args()
    update(args.dir)
