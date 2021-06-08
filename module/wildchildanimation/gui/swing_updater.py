# -*- coding: utf-8 -*-
_VERSION = "1.00"

import argparse
import platform

import sys
sys.path.append("./module")

import os
from pprint import pprint

import zipfile

# python 3
if sys.version_info[0] >= 3:
    import urllib.request as request    
else:
    import urllib as request

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
    print("Creating python virtual env")
    drive, tail = split_path(dir)        
    cmd = '{} && cd {} && python -m venv env'.format(drive, dir)

    p = os.popen(cmd)
    s = p.read()
    p.close()    

    pprint(s)

def update_requirements(dir):
    print("Updating requirements.txt")
    drive, tail = split_path(dir)        
    cmd = '{} && cd {} && "env/Scripts/activate" && pip install -r swing/swing-main/requirements.txt'.format(drive, dir)

    p = os.popen(cmd)
    s = p.read()
    p.close()   

def get_swing_release():
    url = 'https://raw.githubusercontent.com/wildchild-animation/swing/main/module/swing.version'
    res = request.urlopen(url)
    dat = res.read()
    tex = dat.decode('utf-8')
    return tex

def run_swing_standalone(dir):
    drive, tail = split_path(dir)        
    cmd = '{} &&  cd {}/swing/swing-main && "{}/env/Scripts/activate" && python {}/swing/swing-main/module/wildchildanimation/plugin/swing_desktop.py'.format(drive, dir, dir, dir)

    p = os.popen(cmd)
    s = p.read()
    p.close()   

def download_latest(dir):
    print("Downloading release")
    check_or_create_dir(dir)

    target = "{}/swing-main.zip".format(dir)
    request.urlretrieve(SWING_DOWNLOAD, target)

    return True

def extract_latest(download_dir, module_dir):
    print("Extracting release")
    check_or_create_dir(module_dir)
    with zipfile.ZipFile("{}/swing-main.zip".format(download_dir), 'r') as zf:
        zf.extractall(module_dir)
    
    return True

def setup_windows(working_dir):
    # make sure we have default directories
    check_or_create_dir(working_dir)

    venv_dir = "{}/env".format(working_dir)

    if not os.path.exists(venv_dir):
        create_venv(working_dir)

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
    else:
        print("Not implemented yet")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help = "Target dir", default = None, action='store')

    args = parser.parse_args()
    update(args.dir)
