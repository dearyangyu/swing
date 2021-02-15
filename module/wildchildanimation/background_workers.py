import traceback
import gazu
import sys
import os
import requests

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from QtCore import pyqtSignal

from datetime import datetime

def write_log(*args):
    log = "{}: StudioAPI".format(datetime.now().strftime("%d/%m%Y %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    print(log)

class ProjectLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)

    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            write_log("ProjectLoaderThread", "interrupted")

    def run(self):
        write_log("ProjectLoaderThread", "start")
        results = {}
        try:
            try:
                write_log("ProjectLoaderThread", "load")
                projects = gazu.project.all_open_projects()
                task_types = gazu.task.all_task_types()

                results["projects"] = projects
                results["task_types"] = task_types

            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            write_log("ProjectLoaderThread", "done")
            self.loaded.emit(results)

class ProjectHierarchyLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project):
        QtCore.QThread.__init__(self, parent)
        self.project = project

    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            write_log("ProjectHierarchyLoaderThread", "interrupted")

    def run(self):
        write_log("ProjectHierarchyLoaderThread", "start")
        try:
            try:
                episodes = gazu.shot.all_episodes_for_project(self.project)
                if len(episodes) == 0:
                    episode = {
                        "name": "All",
                        "id": 0,
                        "sequences": gazu.shot.all_sequences_for_project(self.project)
                    }
                    episodes = [ episode ]
                else:
                    for ep in episodes:
                        ep["sequences"] = gazu.shot.all_sequences_for_episode(ep)

                for ep in episodes:
                    for seq in ep["sequences"]:
                        seq["shots"] = gazu.shot.all_shots_for_sequence(seq)

                results = {
                    "results": episodes
                }                        
            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            write_log("ProjectHierarchyLoaderThread", "done")
            self.loaded.emit(episodes)

class EntityFileLoader(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, entity):
        QtCore.QThread.__init__(self, parent)
        self.entity = entity

    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            write_log("EntityFileLoader", "interrupted")

    def run(self):
        write_log("EntityFileLoader", "start")
        try:
            results = {
                "output_files": [],
                "working_files": []
            }                        

            try:
                if self.entity["type"] == "Shot":
                    casting = gazu.casting.get_shot_casting(self.entity)
                else:
                    casting = gazu.casting.get_asset_casting(self.entity)
                    
                #for item in casting:
                #    file_list += reportdata.load_working_files(item["asset_id"])            

                output_files = gazu.files.all_output_files_for_entity(self.entity)
                working_files = gazu.files.get_all_working_files_for_entity(self.entity)

                # load casted files
                for item in casting:

                    for file_item in gazu.files.all_output_files_for_entity(item["asset_id"]):
                        if file_item not in output_files:
                            output_files.append(file_item)

                    for file_item in gazu.files.get_all_working_files_for_entity(item["asset_id"]):
                        if file_item not in working_files:
                            working_files.append(file_item)

                results = {
                    "output_files": output_files,
                    "working_files": working_files
                }                        
            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            write_log("EntityFileLoader", "done")
            self.loaded.emit(results)                        
              
class AssetTypeLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project):
        QtCore.QThread.__init__(self, parent)
        self.project = project

    def run(self):
        results = gazu.asset.all_asset_types_for_project(self.project)

        self.loaded.emit(results)        

class AssetLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project, asset_type):
        QtCore.QThread.__init__(self, parent)
        self.project = project
        self.asset_type = asset_type

    def run(self):
        results = gazu.asset.all_assets_for_project_and_type(self.project, self.asset_type)

        self.loaded.emit(results)          

class TaskLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project, email):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.project = project
        self.email = email
    
    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            print("TaskLoaderThread", "interrupted")

    #def due_date(self, elem):
    #    if "due_date" in elem and elem["due_date"]:
    #        return arrow.get(elem["due_date"], "YYYY-MM-DDTHH:mm:ss")
    #    return 0

    def run(self):
        person = gazu.person.get_person_by_email(self.email)
        tasks = gazu.task.all_tasks_for_person(person)
        results = []
        for item in tasks:
            if item["project_id"] == self.project["id"]:
                results.append(item)
        self.loaded.emit(results)

class DownloadSignal(QtCore.QObject):

    # setting up custom signal
    done = QtCore.Signal(object)        
    progress = QtCore.Signal(object)

class FileDownloader(QtCore.QRunnable):

    def __init__(self, parent, index, url, target, email, password, skip_existing = True, extract_zips = False):
        QtCore.QRunnable.__init__(self, parent)
        self.parent = parent
        self.index = index
        self.url = url
        self.target = target
        self.email = email
        self.password = password
        self.callback = DownloadSignal()
    
    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            print("FileDownloader", "interrupted")

    def progress(self, index, count):
        results = {
            "status": "downloading",
            "index": index,
            "count": count
        }
        self.callback.progress.emit(results)

    def run(self):
        write_log("Downloading {} to {}".format(self.url, self.target))

        params = { 
            "username": self.email,
            "password": self.password
        }        

        if os.path.exists(self.target):
            status = "skipped"
        else:
            it = 0
            count = 0
            rq = requests.post(self.url, data = params)
            if rq.status_code == 200:
                with open(self.target, 'wb') as out:
                    for bits in rq.iter_content():
                        out.write(bits)        
                        count += len(bits)

                        #if it % 1024 == 0:
                        #    self.progress(self.index, count)
                        it += 1
            status = "Downloaded"

        size = os.path.getsize(self.target)

        results = {
            "status": status,
            "size": size,
            "index": self.index,
            "file": self.target
        }
        self.callback.done.emit(results)        
        write_log("Downloaded {} to {}".format(self.url, self.target))