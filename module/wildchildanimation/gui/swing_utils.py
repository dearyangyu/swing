# -*- coding: utf-8 -*-
'''
    Utility functions
'''
# ==== auto Qt load ====
try:
    from PySide2 import QtCore, QtGui
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtGui

import sys
import gazu
import keyring
import os
import os.path
import re
import zipfile

from datetime import datetime

def get_platform():
    platforms = {
        'linux': 'Linux',
        'mac': 'OS X',
        'win': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

def fakestr(*args):
    return args[0]

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def open_folder(directory):
    file_info = QtCore.QFileInfo(directory)
    if file_info.isDir():
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(directory))
    else:
        write_log("[ERROR] Invalid directory path: {0}".format(directory))

def set_target(file_item, local_root):
    path = file_item["path"]
    path = path.replace("/mnt/content/productions", local_root)

    if not path.endswith(file_item["name"]):
        path = "{}/{}".format(path, file_item["name"])

    file_item["target_path"] = path
    return file_item
 
def load_settings(key, default):
    settings = QtCore.QSettings()    
    return settings.value(key, default)

def save_settings(key, val):
    settings = QtCore.QSettings()    
    settings.setValue(key, val)
    settings.sync()
    return settings.value(key)    

def save_password(service, key, val):
    try: 
        keyring.set_password(service, key, val)
    except:
        setpassword(service, key, val)

def load_keyring(key, val, default):
    try:
        result = keyring.get_password(key, val)
        if result == None:
            keyring.set_password(key, val, default)
            result = keyring.get_password(key, val)
        return result
    except:
        return getpassword(key, val)


## apple mac keyring override
def getpassword(service, account):

    def decode_hex(s):
        s = eval('"' + re.sub(r"(..)", r"\x\1", s) + '"')
        if "" in s: s = s[:s.index("")]
        return s

    cmd = ' '.join([
        "/usr/bin/security",
        " find-generic-password",
        "-g -s '%s' -a '%s'" % (service, account),
        "2>&1 >/dev/null"
    ])
    p = os.popen(cmd)
    s = p.read()
    p.close()
    m = re.match(r"password: (?:0x([0-9A-F]+)\s*)?\"(.*)\"$", s)
    if m:
        hexform, stringform = m.groups()
        if hexform:
            return decode_hex(hexform)
        else:
            return stringform


def setpassword(service, account, password):
    cmd = 'security add-generic-password -U -a %s -s %s -p %s' % (account, service, password)
    p = os.popen(cmd)
    s = p.read()
    p.close()

def write_log(*args):
    log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)

def friendly_string(string):
    return re.sub('\W+','_', str(string).strip())

def resource_path(resource):
    base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, resource)

def my_date_format(date):
    if isinstance(date, str):
        if len(date) == 19: # YYYY-MM-DDTHH:MM:SS
            dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
    try:
        result = date.strftime("%Y-%m-%d %H:%M:%S")    
    except:
        result = date

    return result

def human_size(bytes):
    if bytes < 1024:
        return "{} bytes".format(bytes)
    
    bytes /= 1024
    if bytes < 1024:
        return "{:.2f} Kb".format(bytes)
    
    bytes /= 1024
    if bytes < 1024:
        return "{:.2f} Mb".format(bytes)
    
    bytes /= 1024
    if bytes < 1024:
        return "{:.2f} Gb".format(bytes)
    
    bytes /= 1024
    if bytes < 1024:
        return "{:.2f} Tb".format(bytes)

    # really ?     
    return "{:.2f}".format(bytes)   

def resource_path(resource):
    base_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(base_path, resource)    


def set_button_icon(button, resource_string):
    resource_string = resource_path(resource_string)

    pm = QtGui.QPixmap(resource_string)
    pm = pm.scaledToHeight(18)        

    icon = QtGui.QIcon(pm)
    button.setIcon(icon)
    return button

def connect_to_server(email, password): 
    server = load_settings('server', 'https://example.company.com')
    gazu.set_host("{}/api".format(server))
    try:
        gazu.log_in(email, password)
    except:
        return False

    return True        
 
# Declare the function to return all file paths of the particular directory
def retrieve_file_paths(dirName):
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in os.walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    # return all paths
    return filePaths

def zip_directory(dir_name):

    # Call the function to retrieve all files and folders of the assigned directory
    filePaths = retrieve_file_paths(dir_name)

    # printing the list of all files to be zipped
    write_log("Zipping {0} files in {1}".format(len(filePaths), dir_name))

    # writing files to a zipfile
    zip_file = zipfile.ZipFile(dir_name + '.zip', 'w')
    with zip_file:
        # writing each file one by one
        for file in filePaths:
            zip_file.write(file)
        zip_file.close()

    write_log("Created {0}.zip".format(dir_name))
    return 


## zip_directory("C:/Work/testdir")