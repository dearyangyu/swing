# -*- coding: utf-8 -*-
_VERSION = "1.00"

import argparse
import platform

import sys
sys.path.append("./module")

import os
from pprint import pprint

swing_repo = 'wildchild-animation/swing'

# local import wildchildanimation module by adding to the path
WCA_ROOT = "C:/WCA"

def split_path(path):
     return os.path.splitdrive(path)

def get_git_version(path = ''):
    cmd = '{}git --version'.format(path)
    try:
        p = os.popen(cmd)
        s = p.read()
        p.close()    
        return s
    except:
        return None

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

def git_clone(dir):
    drive, tail = split_path(dir)
    cmd = '{} && cd {} && git clone https://github.com/{}'.format(drive, dir, swing_repo)
    print(cmd)

    p = os.popen(cmd)
    s = p.read()
    p.close()

    pprint(s)    

def git_pull(dir):
    drive, tail = split_path(dir)    
    cmd = '{} && cd {} && git pull'.format(drive, dir)
    print(cmd)    

    p = os.popen(cmd)
    s = p.read()
    p.close()

    pprint(s)    

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
    cmd = '{} && cd {} && "env/Scripts/activate" && pip install -r swing/requirements.txt'.format(drive, dir)
    print(cmd)    

    p = os.popen(cmd)
    s = p.read()
    p.close()   

    pprint(s)

def get_swing_version(dir):
    drive, tail = split_path(dir)        
    #  c:; cd 'c:\DEV\Github\wca-maya'; & 'c:\DEV\Github\wca-maya\venv\Scripts\python.exe' 'c:\Users\pniemandt\.vscode\extensions\ms-python.python-2021.5.842923320\pythonFiles\lib\python\debugpy\launcher' '1778' '--' 'c:\DEV\Github\wca-maya\plugin\treehouse\swing_desktop.py' 
    cmd = '{} &&  cd {}/swing && "{}/env/Scripts/activate" && python {}/swing/plugin/treehouse/swing_desktop.py'.format(drive, dir, dir, dir)
    print(cmd)

    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()   

    pprint(s)

def setup_windows(install_dir):
    # make sure we have default directories
    check_or_create_dir(install_dir)

    repo = "{}/swing".format(install_dir)

    # change to download as zip
    return False
    if not os.path.exists(repo):
        print("{}: No repo found, creating".format(repo))
        git_clone(install_dir)
    else:
        print("{}: Repo found, updating".format(repo))
        git_pull(repo)

    venv = "{}/env".format(install_dir)

    if not os.path.exists(venv):
        print("{}: Python virtual env not found, creating".format(install_dir))
        create_venv(install_dir)

    update_requirements(install_dir)
    get_swing_version(install_dir)

def update(working_dir):
    print("treehouse: swing updater v{}".format(_VERSION))

    if working_dir is None:
        install_dir = WCA_ROOT
    else:
        install_dir = working_dir
    print("path: {}".format(install_dir))

    git_version = get_git_version()
    if not git_version:
        print("Pleasure ensure git is installed and in your path")
        exit(-1)
    else:
        print("Found {}".format(git_version))

    python_version = get_python_version()
    if not git_version:
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
