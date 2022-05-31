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
import re
import zipfile, traceback
import subprocess

from datetime import datetime

def load_combo(combo, items):
    combo.blockSignals(True)
    combo.clear()
    for item in items:
        combo.addItem(item["name"], userData = item)
    combo.blockSignals(False)
    return combo

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

def fcount(path):
    """ Counts the number of files in a directory """
    count = 0
    if not os.path.exists(path):
        return count

    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)): 
            count += 1
        if os.path.isdir(os.path.join(path, f)): 
            if not f in [ ".source", ".history"]:
                count += 1

    return count        

def fcount_name(path, name):
    """ Counts the number of files in a directory """
    count = 0
    if not os.path.exists(path):
        return count

    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)) and name.lower() in f.lower(): 
            count += 1
        if os.path.isdir(os.path.join(path, f)) and name.lower() in f.lower(): 
            if not f in [ ".source", ".history"]:
                count += 1

    return count        


def open_folder(directory):
    file_info = QtCore.QFileInfo(directory)
    if file_info.isDir():
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(directory))
    else:
        write_log("[ERROR] Invalid directory path: {0}".format(directory))

def resolve_content_path(path, local):
    try:
        if path:
            if "/mnt/content/productions" in path:
                path = path.replace('/mnt/content/productions', local)
                return os.path.normpath(path)
        return os.path.normpath(path)
    except:
        traceback.print_exc(file=sys.stdout)          

    return path

def set_target(file_item, local_root):
    if "file_path" in file_item:
        path = file_item["file_path"]
    else:
        path = file_item["path"]

    path = resolve_content_path(path, local_root)

    if not "file_name" in file_item or not file_item["file_name"]:
        return file_item

    if not path.endswith(file_item["file_name"]):
        path = "{}/{}".format(path, file_item["file_name"])

    file_item["target_path"] = os.path.normpath(path)
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

#
# force write_log to be thread safe,
# one line of output, newline appended, flush output
# 
def write_log(*args):
    log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    log += "\n"
    print(log, flush=True, end='')

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
    # type: (float) -> str
    if bytes > 1000000 * 1000:
        return '%.1f GB' % (bytes / 1000.0 / 1000.0 / 1000)
    elif bytes > 1000 * 1000:
        return '%.1f MB' % (bytes / 1000.0 / 1000)
    elif bytes > 10 * 1000:
        return '%i kB' % (bytes / 1000)
    elif bytes > 1000:
        return '%.1f kB' % (bytes / 1000.0)
    else:
        return '%i bytes' % bytes
        
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

def extract_archive(prog_name, archive, directory, extract_mode = "x"):

    if prog_name and len(prog_name) > 0:
        if os.path.exists(prog_name) and os.path.isfile(prog_name):
            return external_extract(prog_name, archive, directory, extract_mode=extract_mode)
    else:
        try:
            os.chdir(directory)
            with zipfile.ZipFile(archive, 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                zipObj.extractall()
                #shutil.unpack_archive(archive)        
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            return False
            # extract all items in 64bit
    # open zip file in read binary

def scan_archive(archive):
    try:
        # os.chdir(directory)
        with zipfile.ZipFile(archive, 'r') as zipObj:
            # Return a list of the files in the archive
            return zipObj.filelist
    except:
        traceback.print_exc(file=sys.stdout)
        return False
        # extract all items in 64bit
# open zip file in read binary    

# extract archive using 7zip
def external_extract(program, archive, directory, extract_mode = "x" ):
    #
    ## Usage: 7z <command> [<switches>...] <archive_name> [<file_names>...] [@listfile]
    
    # <Commands>
    # a : Add files to archive
    # b : Benchmark
    # d : Delete files from archive
    # e : Extract files from archive (without using directory names)
    # h : Calculate hash values for files
    # i : Show information about supported formats
    # l : List contents of archive
    # rn : Rename files in archive
    # t : Test integrity of archive
    # u : Update files to archive
    # x : eXtract files with full paths

    # <Switches>
    # -bs{o|e|p}{0|1|2} : set output stream for output/error/progress line
    # -bt : show execution time statistics
    # -i[r[-|0]]{@listfile|!wildcard} : Include filenames
    # -m{Parameters} : set compression Method
    #     -mmt[N] : set number of CPU threads
    #     -mx[N] : set compression level: -mx1 (fastest) ... -mx9 (ultra)
    # -o{Directory} : set Output directory
    # -p{Password} : set Password
    # -r[-|0] : Recurse subdirectories
    # -sa{a|e|s} : set Archive name mode
    # -spd : disable wildcard matching for file names
    # -spe : eliminate duplication of root folder for extract command
    # -spf : use fully qualified file paths
    # -ssc[-] : set sensitive case mode
    # -sse : stop archive creating, if it can't open some input file
    # -ssw : compress shared files
    # -stl : set archive timestamp from the most recently modified file
    # -stm{HexMask} : set CPU thread affinity mask (hexadecimal number)
    # -stx{Type} : exclude archive type
    # -t{Type} : Set type of archive
    # -u[-][p#][q#][r#][x#][y#][z#][!newArchiveName] : Update options
    # -v{Size}[b|k|m|g] : Create volumes
    # -w[{path}] : assign Work directory. Empty path means a temporary directory
    # -x[r[-|0]]{@listfile|!wildcard} : eXclude filenames
    # -y : assume Yes on all queries
    try:
        #drive_name = directory[:1]
        #os.chdir("{}:".format(drive_name))
        os.chdir(directory)

        with subprocess.Popen([program, extract_mode, "-y", archive], stdout=subprocess.PIPE) as proc:
            print(proc.stdout.read().splitlines())

        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False
        # extract all items in 64bit
    # open zip file in read binary

def external_compress(program, archive, directory, compress_level = "-mx0" ):
    try:
        ## 7za a -t7z files.7z *.txt
        #drive_name = directory[:1]
        #os.chdir("{}:".format(drive_name))
        cwd = os.getcwd()
        try:
            os.chdir(directory)
            # proc = subprocess.Popen(cmd, shell = True, stderr=subprocess.PIPE)
            proc = subprocess.Popen([program, "a", archive, "{}/*.exr".format(directory), compress_level], shell = True, stderr=subprocess.PIPE)

            while True:
                output = proc.stderr.read(1)
                try:
                    log = output.decode('utf-8')
                    if log == '' and proc.poll() != None:
                        break
                    else:
                        sys.stdout.write(log)
                        sys.stdout.flush()
                except:
                    print("Byte Code Error: Ignoring")
                    print(traceback.format_exc())
                # continue
        except:
            print(traceback.format_exc())
        finally:
            os.chdir(cwd)        

        # print("{} {} {} {} {}/*.exr".format(program, "a", compress_level, archive, directory))
        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False    

## zip_directory("C:/Work/testdir")