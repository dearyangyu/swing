import traceback
import gazu
import sys
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
        productions = []
        try:
            try:
                write_log("ProjectLoaderThread", "load")
                productions = gazu.project.all_open_projects()
            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            write_log("ProjectLoaderThread", "done")
            self.loaded.emit(productions)

class EpisodeLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project):
        QtCore.QThread.__init__(self, parent)
        self.project = project

    def run(self):
        results = gazu.shot.all_episodes_for_project(self.project)

        self.loaded.emit(results)

class AssetTypeLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project):
        QtCore.QThread.__init__(self, parent)
        self.project = project

    def run(self):
        results = gazu.asset.all_asset_types_for_project(self.project)

        self.loaded.emit(results)        

class SequenceLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project, episode):
        QtCore.QThread.__init__(self, parent)
        self.project = project
        self.episode = episode

    def run(self):
        if (self.episode):
            results = gazu.shot.all_sequences_for_episode(self.episode)
        else:
            results = gazu.shot.all_sequences_for_project(self.project)

        self.loaded.emit(results)

class ShotLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, project, sequence):
        QtCore.QThread.__init__(self, parent)
        self.project = project
        self.sequence = sequence

    def run(self):
        results = gazu.shot.all_shots_for_sequence(self.sequence)

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

class FileDownloader(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, url, target, email, password):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.url = url
        self.target = target
        self.email = email
        self.password = password
    
    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            print("FileDownloader", "interrupted")

    def run(self):
        write_log("Downloading {} to {}".format(self.url, self.target))

        params = { 
            "username": email,
            "password": password
        }        

        rq = requests.post(self.url, data = params)
        if rq.status_code == 200:
            with open(target, 'wb') as out:
                for bits in rq.iter_content():
                    out.write(bits)        

        results = {
            "status": rq.status_code,
            "file": target
        }
        self.loaded.emit(results)        
        write_log("Downloaded {} to {}".format(self.url, self.target))