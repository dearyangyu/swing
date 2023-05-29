from functools import reduce
import os as os
import pymel.core as pm

source_images = os.path.join(pm.workspace.getcwd(), 'sourceimages')
print(source_images)

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    
    return dir

def get_directory_structure_with_files(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir that includes files
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    
    return dir

def get_project_folder(location  = ''):
    path = os.path.join(pm.workspace.getPath(), location)
    
    return(path)
