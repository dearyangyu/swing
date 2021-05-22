# -*- coding: utf-8 -*-
_VERSION = "1.00"

import argparse
import platform

import os

from pprint import pprint

github_api_key = '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'
swing_repo = 'wildchild-animation/swing'

# local import wildchildanimation module by adding to the path
WCA_ROOT = "C:/WCA"

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

def git_clone(install_dir):
    cmd = 'cd {} && git clone https://github.com/wildchild-animation/swing'.format(install_dir)
    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()

def git_pull(repo):
    cmd = 'cd {} && git pull'.format(repo)

    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()

def create_venv(venv):
    cmd = 'cd {} && python -m venv env'.format(venv)

    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()    

    pprintv(s)

def update_requirements(dir):
    cmd = 'cd {} && "env/Scripts/activate" && pip install -r swing/requirements.txt'.format(dir)

    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()   

    pprint(s)

def get_swing_version(dir):
    cmd = 'cd {} && "env/Scripts/activate" && python swing/plugin/treehouse/swing_desktop.py'.format(dir)

    #'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()   

    pprint(s)

def setup_windows(install_dir):

    # make sure we have default directories
    check_or_create_dir(install_dir)

    repo = "{}/swing".format(install_dir)

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

def main(args):
    print("treehouse: swing updater v{}".format(_VERSION))

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

    if args.dir is None:
        install_dir = WCA_ROOT
    else:
        install_dir = dir

    if "Windows" in platform.platform():
        setup_windows(install_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help = "Target dir", default = None, action='store')

    main(parser.parse_args())