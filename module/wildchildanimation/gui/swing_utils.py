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

import gazu
import keyring
import os.path
import re

from datetime import datetime

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def open_folder(directory):
    file_info = QtCore.QFileInfo(directory)
    if file_info.isDir():
        QtGui.QDesktopServices.openUrl(directory)
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

def load_keyring(key, val, default):
    result = keyring.get_password(key, val)
    if result == None:
        keyring.set_password(key, val, default)
        result = keyring.get_password(key, val)
    return result

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
    if len(date) == 19: # YYYY-MM-DDTHH:MM:SS
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return date.strftime("%Y-%m-%d %H:%M:%S")

def my_date_format(date):
    if isinstance(date, str):
        return date

    if len(date) == 19: # YYYY-MM-DDTHH:MM:SS
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    return date.strftime("%Y-%m-%d %H:%M:%S")    

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

def connect_to_server(email, password): 
    server = load_settings('server', 'https://production.wildchildanimation.com')
    gazu.set_host("{}/api".format(server))
    try:
        gazu.log_in(email, password)
    except:
        return False

    return True        