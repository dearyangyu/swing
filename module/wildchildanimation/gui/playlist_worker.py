import os
import traceback
import shutil

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
from wildchildanimation.gui.swing_utils import extract_archive, scan_archive
from wildchildanimation.gui.background_workers import FileDownloader

class WorkerSignal(QtCore.QObject):

    # setting up custom signal
    done = pyqtSignal(object)        
    progress = pyqtSignal(object)

class PlaylistWorker(QtCore.QRunnable):

    mode = "Download"

    def __init__(self, parent, item, target, skip_existing = True, extract_zips = True, params = {}):
        super(PlaylistWorker, self).__init__(self, parent)
        self.parent = parent
        self.item = item
        self.target = target

        self.skip_existing = skip_existing
        self.extract_zips = extract_zips
        self.check_archives = True
        self.params = params
        self.callback = WorkerSignal()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        try:
            local_path = self.item["path"]
            #edit_root = SwingSettings.get_instance().edit_root()
            test_path = local_path.replace("/mnt/content/productions", "Z://productions")

            if os.path.exists(test_path):
                self.mode = "Copy"
        except:
            traceback.print_exc()
            self.mode = "Download"

    def progress(self, status):
        # print("progress: {}".format(status))
        status["item"] = self.item

        self.callback.progress.emit(status)

    def done(self):
        # print("done: {}".format(self.item))

        results = {
            "status": "ok",
            "message": "done",
            "item": self.item,
            "target": self.target,
        }
        self.callback.done.emit(results)

    def run(self):
        edit_api = "{}/edit".format(SwingSettings.get_instance().swing_server())

        output_dir = "{}\\{}\\{}\\{}\\{}_{}_{}".format(self.target, self.item["ep"], self.item["sq"], self.item["sh"], self.item["sq"], self.item["sh"], self.item["name"])
        target = os.path.join(output_dir, self.item["output_file_name"])

        target_dir = os.path.dirname(self.target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        #if not target_dir.exists():
        #    target_dir.mkdir(parents=True)

        if os.path.exists(target):
            if self.skip_existing:
                results = {
                    "status": "skipped",
                    "message": "skipped",
                    "item": self.item,
                    "target": self.target,
                }
                self.callback.done.emit(results)                
                return

        fn, ext = os.path.splitext(self.item["output_file_name"])
        if ext in StudioInterface.UNARCHIVE_TYPES:
            if os.path.exists(os.path.join(output_dir, fn)):
                if self.skip_existing:
                    results = {
                        "status": "skipped",
                        "message": "skipped",
                        "item": self.item,
                        "target": self.target,
                    }
                    self.callback.done.emit(results)                
                    return

        if self.mode == "Download":
            url = "{}/api/output_file/{}".format(edit_api, self.item["output_file_id"])

            # if we are downloading zips, store it in an archive folder
            #if os.path.splitext(self.item["output_file_name"])[1] in StudioInterface.UNARCHIVE_TYPES:

            worker = FileDownloader(self, self.item["output_file_id"], url, target, skip_existing = self.skip_existing, extract_zips = self.extract_zips)
            worker.callback = self.callback

            self.threadpool.start(worker)
        else:
            local_path = self.item["path"]
            #edit_root = SwingSettings.get_instance().edit_root()
            source = local_path.replace("/mnt/content/productions", "Z://productions")

            if os.path.exists(source):
                fn, ext = os.path.splitext(self.item["output_file_name"])

                if ext in StudioInterface.UNARCHIVE_TYPES:
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
                    #            "item": self.item,
                    #            "target": output_dir,
                    #        }
                    #        self.callback.done.emit(results)                
                    #        return                        

                    if os.path.exists(output_dir):
                        if self.skip_existing:
                            results = {
                                "status": "skipped",
                                "message": "skipped",
                                "item": self.item,
                                "target": output_dir,
                            }
                            self.callback.done.emit(results)                
                            return
                        
                    print("Extracting {}".format(source))

                    results = {
                        "status": "Busy",
                        "message": "Extracting",
                        "file_id": self.item["output_file_id"],
                        "item": self.item,
                        "target": output_dir,
                    }
                    self.progress(results)

                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    if extract_archive(SwingSettings.get_instance().bin_7z(), source, output_dir, extract_mode = "e"):
                        results = {
                            "status": "Done",
                            "message": "Success",
                            "item": self.item,
                            "target": output_dir,
                        }
                        self.callback.done.emit(results)
                        print("Extract complete {}".format(output_dir))
                else:
                    if os.path.exists(target):
                        if self.skip_existing:
                            results = {
                                "status": "skipped",
                                "message": "skipped",
                                "item": self.item,
                                "target": self.target,
                            }
                            self.callback.done.emit(results)                
                            return

                    print("Copying {}".format(source))
                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))
                    shutil.copyfile(source, target)

            results = {
                "status": "Complete",
                "message": "Done",
                "item": self.item,
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





