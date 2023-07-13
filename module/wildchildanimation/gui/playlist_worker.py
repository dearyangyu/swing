import os
import sys
import traceback
import shutil
import subprocess
from datetime import datetime

from wildchildanimation.studio.studio_interface import StudioInterface

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSignal
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import extract_archive, scan_archive, fcount
from wildchildanimation.gui.background_workers import FileDownloader

class WorkerSignal(QtCore.QObject):

    # setting up custom signal
    done = pyqtSignal(object)        
    progress = pyqtSignal(object)

class PlaylistWorker(QtCore.QRunnable):

    mode = "Download"

    ## list the contents of the archive, checking for sub directories
    ## default to listing all sub directories, if none found, assume content is in top level of archive
    ## returns a line item: '2023-07-05 11:23:20           83119208     79872331  60 files'
    def check_archive_files(self, archive_name):
        program = SwingSettings.get_instance().bin_7z()
        extract_mode = 'l'
        output_contents = r"*\*"

        print(F"swing::list archive -> {program} {extract_mode} {archive_name}")

        proc = subprocess.Popen([program, extract_mode, archive_name, output_contents], shell = False, stdout=subprocess.PIPE)
        while True:
            output = proc.stdout.readline()
            try:
                log = output.decode('utf-8')
                if log == '' and proc.poll() != None:
                    break
                else:
                    line = log.strip()
                    if "files" in line.lower():
                        return line

            except:
                print(traceback.format_exc())
            # continue

        return None
    
    def extract_zip_contents(self, archive, directory):
        try:
            #drive_name = directory[:1]
            #os.chdir("{}:".format(drive_name))
            if not os.path.exists(directory):
                os.makedirs(directory)

            os.chdir(directory)

            program = SwingSettings.get_instance().bin_7z()
            extract_mode = 'e'

            time_start = datetime.now()   

            #
            # Extract first folder in .tpl to top level directory
            # this is to cater for the directory being zipped as top level, vs. the content of the directory being zipped
            # 7zip
            # -- working_folder.tpl
            # ---- folder_contents
            #

            if " 0 files" in self.check_archive_files(archive):
                ## if no files found in sub directory, extract root content
                output_contents = r"*"
            else:
                ## if no files found in sub directory, extract sub dir content
                output_contents = r"*\*"

            print(F"Swing::Extracting -> {program} {extract_mode} -y {archive} {output_contents}")

            proc = subprocess.Popen([program, extract_mode, "-y", archive, output_contents], shell = False, stdout=subprocess.PIPE)
            while True:
                output = proc.stdout.readline()
                try:
                    log = output.decode('utf-8')
                    if log == '' and proc.poll() != None:
                        break
                    else:
                        print(log.strip())
                except:
                    print(traceback.format_exc())
                # continue

            time_end = datetime.now()
            try:
                print(r"swing: extracting {} completed in {}".format(directory, (time_end - time_start)))
                print(r"")
            except:
                print(traceback.format_exc())

            return True
        except:
            traceback.print_exc(file=sys.stdout)
            return False            


    def __init__(self, parent, item, target, extract_zips = True, params = {}):
        super(PlaylistWorker, self).__init__(self, parent)
        self.parent = parent
        self.selected_file = item
        self.target = target
        self.skip_existing = False

        self.extract_zips = extract_zips
        self.check_archives = True
        self.params = params
        self.callback = WorkerSignal()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        try:
            local_path = self.selected_file["path"]
            #edit_root = SwingSettings.get_instance().edit_root()
            test_path = local_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())

            if os.path.exists(test_path):
                self.mode = "Copy"
        except:
            traceback.print_exc()
            self.mode = "Download"

    def progress(self, status):
        # print("progress: {}".format(status))
        status["item"] = self.selected_file

        self.callback.progress.emit(status)

    def done(self):
        # print("done: {}".format(self.selected_file))

        results = {
            "status": "ok",
            "message": "done",
            "item": self.selected_file,
            "target": self.target,
        }
        self.callback.done.emit(results)

    def run(self):
        edit_api = "{}/edit".format(SwingSettings.get_instance().swing_server())

        ##output_dir = "{}\\{}\\{}\\{}\\{}_{}_{}".format(self.target, self.selected_file["ep"], self.selected_file["sq"], self.selected_file["sh"], self.itselected_file["sq"], self.selected_file["sh"], self.selected_file["name"])

        fn, ext = os.path.splitext(self.selected_file["output_file_name"])
        item_name = os.path.normcase("{}_{}_{}".format(self.selected_file["ep"], self.selected_file["sq"], self.selected_file["sh"]))
        output_name = os.path.normcase("{}/{}{}".format(item_name, item_name, ext))

        target = os.path.join(self.target, output_name)

        target_dir = os.path.dirname(target)
        if os.path.exists(target_dir):
            for item in os.listdir(target_dir):
                old_file = os.path.join(target_dir, item)
                if os.path.isfile(old_file):
                    print("swing::playlist: removing {}".format(old_file))
                    os.remove(old_file)
                    ## pass
        else:
        # if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        fn, ext = os.path.splitext(self.selected_file["output_file_name"])

        is_archive = False
        for item in StudioInterface.UNARCHIVE_TYPES:
            if item in ext:
                is_archive = True

        if is_archive:
            if os.path.exists(os.path.join(target, fn)):
                if self.skip_existing:
                    results = {
                        "status": "skipped",
                        "message": "skipped",
                        "item": self.selected_file,
                        "target": self.target,
                    }
                    self.callback.done.emit(results)                
                    return

        if self.mode == "Download":
            url = "{}/api/output_file/{}".format(edit_api, self.selected_file["output_file_id"])

            # if we are downloading zips, store it in an archive folder
            #if os.path.splitext(self.selected_file["output_file_name"])[1] in StudioInterface.UNARCHIVE_TYPES:

            worker = FileDownloader(self, self.selected_file["output_file_id"], url, target, skip_existing = self.skip_existing, extract_zips = self.extract_zips)
            worker.callback = self.callback

            self.threadpool.start(worker)
        else:
            local_path = self.selected_file["path"]
            #edit_root = SwingSettings.get_instance().edit_root()
            source = local_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())

            if not self.selected_file["output_file_name"] in source:
                source = "{}/{}".format(source, self.selected_file["output_file_name"])

            versions = [ ".7zv1", ".7zv2", ".7zv3", ".7zv4", ".7zv5", ".7zv6", ".7zv7", ".7zv8", ".7zv9"]

            for item in versions:
                if item in source:
                    source = source.replace(item, ".7z")
                    break

            if os.path.exists(source):
                fn, ext = os.path.splitext(self.selected_file["output_file_name"])

                # if ext in StudioInterface.UNARCHIVE_TYPES:
                if is_archive:
                    #target = os.path.normpath(os.path.join(self.target, fn))

                    #
                    # $todo: check that archive contains valid files, not project files
                    #
                    #if not media_in_archive(source):
                    #    if self.check_archives:
                    #        print("Invalid media found in archive {}".format(source))
                    #        results = {
                    #            "status": "skipped",
                    #            "message": "invalid files in archive",
                    #            "item": self.selected_file,
                    #            "target": output_dir,
                    #        }
                    #        self.callback.done.emit(results)                
                    #        return                        

                    if os.path.exists(target_dir) and fcount(target_dir) > 0:
                        if self.skip_existing:
                            results = {
                                "status": "skipped",
                                "message": "skipped",
                                "item": self.selected_file,
                                "target": target_dir,
                            }
                            self.callback.done.emit(results)                
                            return
                        
                    print("swing::playlist: extracting {}".format(source))
                    print("swing::playlist: target {}".format(target_dir))

                    results = {
                        "status": "Busy",
                        "message": "Extracting",
                        "file_id": self.selected_file["output_file_id"],
                        "item": self.selected_file,
                        "target": self.target,
                    }
                    self.progress(results)

                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)

                    extract_mode = 'e'

                    if '.zip' in source:
                        extract_mode = 'x'

                    # if extract_archive(SwingSettings.get_instance().bin_7z(), source, target_dir, extract_mode = extract_mode):
                    if self.extract_zip_contents(source, target_dir):
                        results = {
                            "status": "Done",
                            "message": "Success",
                            "item": self.selected_file,
                            "target": target_dir,
                        }
                        self.callback.done.emit(results)
                        print("swing::playlist: extract complete {}".format(target_dir))
                        print("------------------------------------")

                        #Todo: Check if people uploaded as a zip folder, check sub folders
                        #if fcount(target_dir) == 1:
                        #    directory_contents = os.listdir(target_dir)
                        #    for item in directory_contents:
                        #        if os.path.isdir(item):
                        #            print("Found subdir {}".format(item))
                else:
                    print("swing::playlist: copying {}->{}".format(source, target))

                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))
                    shutil.copyfile(source, target)

            results = {
                "status": "Complete",
                "message": "Done",
                "item": self.selected_file,
                "target": self.target,
            }

            self.callback.done.emit(results)                

'''
    Check zip contains only images or movie files
'''
def media_in_archive(archive):
    file_list = scan_archive(archive)

    for item in file_list:
        fn, ext = os.path.splitext(item.filename)
        if not ext in [ ".png", ".jpg", ".mov", ".mp4" ]:
            return False
    return True





