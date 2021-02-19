import traceback
import gazu
import sys
import os
import requests
import shutil

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
    log = "{}: SWING".format(datetime.now().strftime("%d/%m%Y %H:%M:%S.%f"))
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

class EntityLoaderThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, entity_id):
        QtCore.QThread.__init__(self, parent)
        self.entity_id = entity_id

    def run(self):
        results = {}

        entity = gazu.entity.get_entity(self.entity_id)
        results["entity"] = entity
        results["type"] = entity["type"]

        if entity["type"] == "Shot":
            results["item"] = gazu.shot.get_shot(self.entity_id)
            results["project"] = gazu.project.get_project(results["item"]["project_id"])
            results["url"] = gazu.shot.get_shot_url(results["item"])
            results["casting"] = gazu.casting.get_shot_casting(results["item"])
        else:
            results["item"] = gazu.asset.get_asset(self.entity_id)
            results["project"] = gazu.project.get_project(results["item"]["project_id"])
            results["url"] = gazu.asset.get_asset_url(results["item"])
            results["casting"] = gazu.casting.get_asset_casting(results["item"])

        self.loaded.emit(results)      

class TaskFileInfoThread(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent, task, project_root):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
        self.task = task
        self.project_root = project_root
    
    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            write_log("TaskLoaderThread", "interrupted")

    def run(self):
        task = gazu.task.get_task(self.task)
        project = gazu.project.get_project(self.task["project_id"])
        working_dir = gazu.files.build_working_file_path(task)

        if project["file_tree"]:
            file_tree = project["file_tree"]
            if "working" in file_tree and file_tree["working"]["mountpoint"]:
                mount_point = file_tree["working"]["mountpoint"]
                working_dir = os.path.normpath(working_dir.replace(mount_point, self.project_root))


        results = {
            "task": task,
            "working_dir": working_dir,
            "project": project
        }

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
            write_log("TaskLoaderThread", "interrupted")

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

class SoftwareLoader(QtCore.QThread):
    loaded = pyqtSignal(object)

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent
    
    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            write_log("SoftwareLoader", "interrupted")

    def run(self):
        software = gazu.files.all_softwares()

        results = {
            "software": software
        }
        self.loaded.emit(results)        

class DownloadSignal(QtCore.QObject):

    # setting up custom signal
    done = QtCore.Signal(object)        
    progress = QtCore.Signal(object)

class FileDownloader(QtCore.QRunnable):

    def __init__(self, parent, working_dir, file_id, url, target, email, password, skip_existing = True, extract_zips = False):
        super(FileDownloader, self).__init__(self, parent)
        self.parent = parent
        self.working_dir = working_dir
        self.file_id = file_id
        self.url = url
        self.target = target
        self.email = email
        self.password = password
        self.skip_existing = skip_existing
        self.extract_zips = extract_zips
        self.callback = DownloadSignal()
    
    def __del__(self):
        try:
            if self:
                self.wait()
        except:
            write_log("FileDownloader", "interrupted")

    def progress(self, count):
        results = {
            "message": "downloading",
            "file_id": self.file_id,
            "target": self.target,
            "working_dir": self.working_dir,
            "size": count
        }
        self.callback.progress.emit(results)

    def run(self):
        write_log("Downloading {} to {}".format(self.url, self.target))
        filename, file_extension = os.path.splitext(self.target)

        ###
        if self.skip_existing:
            # check if the target 
            if os.path.exists(self.target):
                write_log("Target exists {}".format(self.target))

                size = os.path.getsize(self.target)                
                status = {
                    "message": "Skipped existing file",
                    "file_id": self.file_id,
                    "target": self.target,
                    "working_dir": self.working_dir,
                    "size": size
                }
                self.callback.done.emit(status)
                return

            if os.path.exists(os.path.join(self.working_dir, filename)):
                write_log("Target exists {}".format(os.path.join(self.working_dir, filename)))

                size = os.path.getsize(self.target)                
                status = {
                    "message": "Skipped existing file",
                    "file_id": self.file_id,
                    "target": self.target,
                    "working_dir": self.working_dir,
                    "size": size
                }
                self.callback.done.emit(status)
                return                

        params = { 
            "username": self.email,
            "password": self.password
        } 

        target_dir = os.path.dirname(self.target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)        

        count = 0
        rq = requests.post(self.url, data = params, stream = True)
        if rq.status_code == 200:
            with open(self.target, 'wb') as out:
                for bits in rq.iter_content(1024 * 1024):
                    out.write(bits)        
                    count += len(bits)
                    self.progress(count)
        else:
            status = {
                "message": "Error downloading file",
                "file_id": self.file_id,
                "target": target_dir,
                "working_dir": self.working_dir,
                "size": 0
            }   
            self.callback.done.emit(status)            
            return False        
                    
        try:
            os.sync()
        except:
            pass

        size = os.path.getsize(self.target)
        ###
        if self.extract_zips and file_extension in [ ".zip" ]:
            zip_root = os.path.normpath(os.path.join(self.working_dir, filename))

            status = {
                "message": "Extracting archive",
                "file_id": self.file_id,
                "target": zip_root,
                "working_dir": self.working_dir,
                "size": size
            }   
            self.callback.progress.emit(status)

            os.makedirs(zip_root, exist_ok=True)
            self.extract_zip(self.target, zip_root)

        status = {
            "message": "Download complete",
            "file_id": self.file_id,
            "target": self.target,
            "working_dir": self.working_dir,
            "size": size            
        }

        self.callback.done.emit(status)        
        write_log("Downloaded {} to {}".format(self.url, self.target))

    def extract_zip(self, archive, directory):
        try:
            os.chdir(directory)
            shutil.unpack_archive(archive)        
        except:
            traceback.print_exc(file=sys.stdout)
            # extract all items in 64bit
        # open zip file in read binary