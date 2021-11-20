# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import gazu
import json
import sys
import os

import requests
import zipfile

from requests_toolbelt import (
    MultipartEncoder,
    MultipartEncoderMonitor
)

import urllib

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSignal
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import write_log, resolve_content_path, extract_archive
from wildchildanimation.gui.swing_updater import update

class LoadedSignal(QtCore.QObject):
    loaded = pyqtSignal(object)        

class VersionCheck(QtCore.QRunnable):

    def __init__(self, parent):
        super(VersionCheck, self).__init__(self, parent)
        self.callback = LoadedSignal()

    def run(self):
        try:
            QtCore.QThread.sleep(5) 
            req = urllib.request.urlopen('https://raw.githubusercontent.com/wildchild-animation/swing/main/module/swing.version')
            version = req.read().decode("utf-8")
            self.callback.loaded.emit(version)
        except:
            traceback.print_exc(file=sys.stdout)
        # done

class SwingUpdater(QtCore.QRunnable):

    def __init__(self, parent, install_dir):
        super(SwingUpdater, self).__init__(self, parent)
        self.install_dir = install_dir
        self.callback = LoadedSignal()

    def run(self):
        try:
            update(self.install_dir)
        except:
            traceback.print_exc(file=sys.stdout)
        # done        


'''
    Loads all open projects, all episodes per project, all task types and softwares
'''
class ProjectLoaderThread(QtCore.QRunnable):

    def __init__(self, parent):
        super(ProjectLoaderThread, self).__init__(self, parent)
        self.callback = LoadedSignal()

    def run(self):
        results = {}
        try:
            try:
                #projects = gazu.project.all_open_projects()
                projects = ProjectEpisodeLoader().run()
                task_types = gazu.task.all_task_types()
                task_status = gazu.task.all_task_statuses()
                software = gazu.files.all_softwares()

                results["projects"] = projects
                results["task_status"] = task_status
                results["task_types"] = task_types
                results["software"] = software

            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            self.callback.loaded.emit(results)
        return results
            

class ProjectHierarchyLoaderThread(QtCore.QRunnable):

    def __init__(self, parent, project):
        super(ProjectHierarchyLoaderThread, self).__init__(self, parent)
        self.project = project
        self.callback = LoadedSignal()        

    def run(self):
        results = {}

        episodes = []
        task_types = []

        if not self.project:
            return False
        try:
            try:
                task_types = gazu.task.all_task_types()
                status_codes = gazu.task.all_task_statuses()
                
                # find all episodes for selected project
                episode_list = gazu.shot.all_episodes_for_project(self.project)

                # if no eps, fake a default
                if len(episode_list) == 0:

                    episode = {
                        "name": "All",
                        "id": 0,
                        "sequences": gazu.shot.all_sequences_for_project(self.project)
                    }
                    episodes.append(episode)

                    # and grab all task types
                    #for item in gazu.task.all_task_types():
                    #    task_types.append(item)
                    
                else:
                    # else run through all eps
                    for ep in episode_list:
                        # grab all sequences for that ep
                        ep["sequences"] = gazu.shot.all_sequences_for_episode(ep)

                        # grab all shots
                        for seq in ep["sequences"]:
                            seq["shots"] = gazu.shot.all_shots_for_sequence(seq)

                        # grab task types
                        #ep["task_types"] = gazu.task.all_task_types_for_episode(ep)
                        #for item in ep["task_types"]:
                        #    # unique 
                        #    if not item in task_types:
                        #        task_types.append(item)

                        episodes.append(ep)
                    # scan eps for seq, shot and task type

                results["episodes"] = episodes
                results["task_types"] = task_types
                results["status_codes"] = status_codes
            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            self.callback.loaded.emit(results)

class EntityFileLoaderOld(QtCore.QRunnable):

    def __init__(self, parent, project_nav, entity, working_dir, scan_cast = False):
        super(EntityFileLoaderOld, self).__init__(self, parent)
        self.nav = project_nav
        self.entity = entity
        self.working_dir = working_dir
        self.callback = LoadedSignal()    
        self.scan_cast = scan_cast

    def find_item(self, data_list, item):
        for i in data_list:
            if i["id"] == item:
                return i
        return None            

    def run(self):
        try:
            results = {
                "output_files": [],
                "working_files": []
            }                        

            try:
                task_types = self.nav.get_task_types()
                print("Loading files for {}".format(self.entity["name"]))
                
                #for item in casting:
                #    file_list += reportdata.load_working_files(item["asset_id"])            
                
                output_files = []
                output_file_list = gazu.files.all_output_files_for_entity(self.entity)

                working_files = []
                working_file_list = gazu.files.get_all_working_files_for_entity(self.entity)

                if self.scan_cast:
                    if "Shot" in self.entity["type"]:
                        shot = gazu.shot.get_shot(self.entity["id"])
                        casting = gazu.casting.get_shot_casting(shot)
                    else:
                        asset = gazu.asset.get_asset(self.entity["id"])
                        casting = gazu.casting.get_asset_casting(asset)

                    for item in casting:
                        for file_item in gazu.files.all_output_files_for_entity(item["asset_id"]):
                            if file_item not in output_file_list:
                                output_file_list.append(file_item)
                        for file_item in gazu.files.get_all_working_files_for_entity(item["asset_id"]):
                            if file_item not in working_file_list:
                                working_file_list.append(file_item)

                # check task types
                for file_item in output_file_list:
                    task_type = self.find_item(task_types, file_item["task_type_id"])
                    if task_type:
                        file_item["task_type"] = task_type
                        file_item["status"] = ""
                        output_files.append(file_item)

                for file_item in working_file_list:
                    task = gazu.task.get_task(file_item["task_id"])
                    task_type = self.find_item(task_types, task["task_type"]["id"])
                    if task_type:
                        file_item["task_type"] = task_type
                        file_item["status"] = ""
                        working_files.append(file_item)

                results = {
                    "entity": self.entity,
                    "output_files": output_files,
                    "working_files": working_files
                }                        
            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            self.callback.loaded.emit(results)                        
              
class AssetTypeLoaderThread(QtCore.QRunnable):

    def __init__(self, parent, project_id):
        super(AssetTypeLoaderThread, self).__init__(self, parent)
        self.project_id = project_id
        self.callback = LoadedSignal()        

    def run(self):
        results = gazu.asset.all_asset_types_for_project(gazu.project.get_project(self.project_id))

        self.callback.loaded.emit(results)        

class AssetLoaderThread(QtCore.QRunnable):

    def __init__(self, parent, project_id, asset_type):
        super(AssetLoaderThread, self).__init__(self, parent)
        self.project_id = project_id
        self.asset_type = asset_type
        self.callback = LoadedSignal()        

    def run(self):
        self.project = gazu.project.get_project(self.project_id)

        if self.asset_type:
            results = gazu.asset.all_assets_for_project_and_type(self.project, self.asset_type)
        else:
            results = gazu.asset.all_assets_for_project(self.project)

        self.callback.loaded.emit(results)          

class EntityLoaderThread(QtCore.QRunnable):

    def __init__(self, parent, entity_id):
        super(EntityLoaderThread, self).__init__(self, parent)
        self.entity_id = entity_id
        self.callback = LoadedSignal()        

    def run(self):
        results = {}
        entity = gazu.entity.get_entity(self.entity_id)

        results["entity"] = entity
        results["task_types"] = gazu.task.all_task_types()
        results["type"] = entity["type"]
        results["history"] = []

        if entity["type"] == "Shot":
            results["item"] = gazu.shot.get_shot(self.entity_id)
            results["project"] = gazu.project.get_project(results["item"]["project_id"])
            results["url"] = gazu.shot.get_shot_url(results["item"])
            results["casting"] = gazu.casting.get_shot_casting(results["item"])
            
            results["tasks"] = gazu.task.all_tasks_for_shot(self.entity_id)
            for task in results['tasks']:
                results["history"].append(gazu.task.get_last_comment_for_task(task))
        else:
            results["item"] = gazu.asset.get_asset(self.entity_id)
            results["project"] = gazu.project.get_project(results["item"]["project_id"])
            results["url"] = gazu.asset.get_asset_url(results["item"])
            results["casting"] = gazu.casting.get_asset_casting(results["item"])

            results["tasks"] = gazu.task.all_tasks_for_asset(self.entity_id)
            for task in results['tasks']:
                results["history"].append(gazu.task.get_last_comment_for_task(task))

        self.callback.loaded.emit(results)      

class TaskFileInfoThread(QtCore.QRunnable):

    def __init__(self, parent, task, project_root):
        super(TaskFileInfoThread, self).__init__(self, parent)
        self.parent = parent
        self.task = task
        self.project_root = project_root
        self.callback = LoadedSignal()        
    
    def run(self):
        task = gazu.task.get_task(self.task)

        if task["entity_type"]["name"] == "Shot":
            entity = gazu.shot.get_shot(task["entity_id"])
        else:
            entity = gazu.asset.get_asset(task["entity_id"])
        
        project = task["project_id"]
        task_dir = gazu.files.build_working_file_path(task)
        wf = gazu.files.get_last_working_files(task)

        results = {
            "task": task,
            "working_files": wf,
            "entity": entity,
            "task_dir": task_dir,
            "project_dir": resolve_content_path(task_dir, self.project_root),
            "project": project
        }

        self.callback.loaded.emit(results)        
        return results

class ToDoLoader(QtCore.QRunnable):

    def __init__(self, project_id, episode_id, is_done = False):
        super(ToDoLoader, self).__init__(self)
        self.settings = SwingSettings.get_instance()
        self.request_url = "{}/edit/api/task_list".format(self.settings.swing_server())
        self.callback = LoadedSignal()    
        self.project_id = project_id
        self.episode_id = episode_id
        self.is_done = is_done

    def run(self):
        params = { 
            "username": self.settings.swing_user(),
            "password": self.settings.swing_password(),
            "episode_id": self.episode_id,
            "project_id": self.project_id,
            "is_done": self.is_done
        }             

        results = []
        rq = requests.post(self.request_url, data = params)
        if rq.status_code == 200:
            found = rq.json()
            for item in found:
                results.append(item)

        self.callback.loaded.emit(results)                        
        return results               

class TaskLoaderThread(QtCore.QRunnable):

    ALL_TASKS = False

    def __init__(self, parent, project_id, episode_id, parent_id, task_types = [], status_types = []):
        super(TaskLoaderThread, self).__init__(self, parent)
        self.parent = parent

        self.project_id = project_id
        self.episode_id = episode_id
        self.parent_id = parent_id
        self.task_types = task_types
        self.status_types = status_types

        self.settings = SwingSettings.get_instance()
        self.callback = LoadedSignal()        

    #def due_date(self, elem):
    #    if "due_date" in elem and elem["due_date"]:
    #        return arrow.get(elem["due_date"], "YYYY-MM-DDTHH:mm:ss")
    #    return 0

    def is_found(self, data_list, item):
        for i in data_list:
            if i["id"] == item:
                return True
        return False

    def run(self):
        results = {}
        tasks = []

        task_list = ToDoLoader(self.project_id, self.episode_id).run()    
        
        task_types = {}
        if self.task_types:
            for item in self.task_types:
                task_types[item["id"]] = item

        task_status = {}
        if self.status_types:
            for item in self.status_types:
                task_status[item["id"]] = item

        for item in task_list:
            task = gazu.task.get_task(item["task_id"])

            if len(task_types) > 0 and task["task_type_id"] not in task_types:
                continue

            if len(task_status) > 0 and task["task_status_id"] not in task_status:
                continue

            if self.parent_id:
                if task["entity"]["id"] != self.parent_id:
                    continue

            task["task_dir"] = gazu.files.build_working_file_path(task)
            task["project_dir"] = resolve_content_path(task["task_dir"], SwingSettings.get_instance().swing_root())
        
            tasks.append(task)

        if self.episode_id and self.episode_id != 'All':
            results["episode"] = gazu.shot.get_episode(self.episode_id)
        else:
            results["episode"] = { "id": "all", "name": "All" }

        results["tasks"] = tasks

        self.callback.loaded.emit(results)
        return results

class SoftwareLoader(QtCore.QRunnable):

    def __init__(self, parent):
        super(SoftwareLoader, self).__init__(self, parent)
        self.parent = parent
        self.callback = LoadedSignal()        

    def run(self):
        software = gazu.files.all_softwares()

        results = {
            "software": software
        }
        self.callback.loaded.emit(results)        

        return results

class TaskTypeLoader(QtCore.QRunnable):

    def __init__(self, parent):
        super(TaskTypeLoader, self).__init__(self, parent)
        self.parent = parent
        self.callback = LoadedSignal()        

    def run(self):
        items = gazu.task.all_task_types()
        results = {
            "results": items
        }
        self.callback.loaded.emit(results)  
        return results

class StatusTypeLoader(QtCore.QRunnable):

    def __init__(self, parent):
        super(StatusTypeLoader, self).__init__(self, parent)
        self.parent = parent
        self.callback = LoadedSignal()        

    def run(self):
        items = gazu.task.all_task_statuses()
        results = {
            "results": items
        }
        self.callback.loaded.emit(results)                   
        return results

class DownloadSignal(QtCore.QObject):

    # setting up custom signal
    done = pyqtSignal(object)        
    progress = pyqtSignal(object)

class FileDownloader(QtCore.QRunnable):

    def __init__(self, parent, file_id, url, target, skip_existing = True, extract_zips = False, params = {}):
        super(FileDownloader, self).__init__(self, parent)
        self.parent = parent
        self.file_id = file_id
        self.url = url
        self.target = target

        self.skip_existing = skip_existing
        self.extract_zips = extract_zips
        self.params = params
        self.callback = DownloadSignal()

    def progress(self, count):
        results = {
            "status": "ok",
            "message": "downloading",
            "file_id": self.file_id,
            "target": self.target,
            "size": count
        }
        self.callback.progress.emit(results)

    def run(self):
        filename, file_extension = os.path.splitext(os.path.basename(self.target))
        working_dir = os.path.dirname(self.target)

        ###
        # check if the file exists
        #
        if self.skip_existing:
            # check if the target 
            if os.path.exists(self.target):
                write_log("Target exists {}".format(self.target))

                size = os.path.getsize(self.target)                
                status = {
                    "status": "skipped",
                    "message": "Skipped existing file",
                    "file_id": self.file_id,
                    "target": self.target,
                    "working_dir": working_dir,
                    "size": size
                }
                self.callback.done.emit(status)
                return

            if os.path.exists(os.path.join(working_dir, filename)):
                write_log("Working path exists {}".format(os.path.join(working_dir, filename)))

                if os.path.isfile(os.path.join(working_dir, filename)):
                    size = os.path.getsize(self.target)                
                    status = {
                        "status": "skipped",
                        "message": "Skipped existing file",
                        "file_id": self.file_id,
                        "target": self.target,
                        "working_dir": working_dir,
                        "size": size
                    }
                else:
                    status = {
                        "status": "skipped",
                        "message": "Skipped existing directory",
                        "file_id": self.file_id,
                        "target": self.target,
                        "working_dir": working_dir
                    }                    
                self.callback.done.emit(status)
                return                
        ###

        self.params["username"] = SwingSettings.get_instance().swing_user()
        self.params["password"] = SwingSettings.get_instance().swing_password()

        if not os.path.exists(working_dir):
            try:
                os.makedirs(working_dir)   
                print("Made dir: {}".format(os.path.dirname(working_dir)))
            except:
                pass

        count = 0
        rq = requests.post(self.url, data = self.params, stream = True)
        if rq.status_code == 200:
            with open(self.target, 'wb') as out:
                # download in 1 MB chunks
                for bits in rq.iter_content(1024 * 1024):
                    out.write(bits)        
                    count += len(bits)
                    self.progress(count)
        else:
            status = {
                "status": "error",
                "message": "Error downloading file",
                "file_id": self.file_id,
                "target": self.target,
                "working_dir": working_dir,
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
        if self.extract_zips and file_extension.lower() in  [ ".zip", ".rar" ]:
            zip_root = os.path.normpath(os.path.join(working_dir, filename))

            status = {
                "status": "ok",
                "message": "Extracting zip",
                "file_id": self.file_id,
                "target": zip_root,
                "working_dir": working_dir,
                "size": size
            }   
            self.callback.progress.emit(status)
            # def makedirs(name, mode=0o777, exist_ok=False):
            try:
                os.makedirs(zip_root)
            except:
                pass

            if extract_archive(SwingSettings.get_instance().bin_7z(), self.target, zip_root):
                status = {
                    "status": "ok",
                    "message": "Extracted zip",
                    "file_id": self.file_id,
                    "target": zip_root,
                    "working_dir": working_dir,
                    "size": size
                }   
                self.callback.progress.emit(status)  
            else:
                status = {
                    "status": "error",
                    "message": "Error extracting zip",
                    "file_id": self.file_id,
                    "target": zip_root,
                    "working_dir": working_dir,
                    "size": size
                }   
                self.callback.progress.emit(status)                               

        status = {
            "status": "ok",
            "message": "Download complete",
            "file_id": self.file_id,
            "target": self.target,
            "working_dir": working_dir,
            "size": size            
        }

        write_log("Download complete: {}".format(self.target))
        self.callback.done.emit(status)        


##############################################################################################################################################################################################

class UploadSignal(QtCore.QObject):

    # setting up custom signal
    done = pyqtSignal(object)        
    progress = pyqtSignal(object)



##############################################################################################################################################################################################
# https://github.com/vsoch/django-nginx-upload/blob/master/push.py
#
_READ_SIZE = 1024 * 1024.0

def create_callback(encoder, upload_signal, source):
    encoder_len = int(encoder.len / _READ_SIZE)
    
    upload_signal.progress.emit({
        "status": "ok",
        "message": "[0 of %s MB]" % (encoder_len),
        "source": source
    })

    def callback(monitor):
        bytes_read = int(monitor.bytes_read / _READ_SIZE)
        upload_signal.progress.emit({
            "status": "ok",
            "message": "[%s of %s MB]" % (bytes_read, encoder_len),
            "source": source
        })
    return callback

class SwingCompressor(QtCore.QRunnable):

    def __init__(self, directory, model, target = 'out.zip'):
        super(SwingCompressor, self).__init__(self)
        self.source = directory
        self.model = model
        self.target = target
        
        self.callback = UploadSignal()

    def zip_dir(self, path, zipfile):
        for root, dirs, files in os.walk(path):
            for file in files:
                zipfile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))        

    def run(self):
        if not os.path.isdir(self.source):
            print("Source {} not a directory".format(self.source))
            return

        if os.path.exists(self.target):
            os.remove(self.target)
            #print("Target exists: {}".format(self.target))
            #return

        current_dir = os.getcwd()
        try:
            #os.chdir(self.source)

            root = self.source

            exclude = [ ".", "..", "./", root, os.path.basename(self.source), os.path.basename(self.target) ]

            with zipfile.ZipFile(self.target, 'w', zipfile.ZIP_DEFLATED) as archive:

                for item in os.listdir(self.source):
                    item_path = os.path.join(self.source, item)
                    
                    if self.model.checkState(self.model.index(item_path)) == QtCore.Qt.Checked:
                        # print("{} Added {} {}".format(item, os.path.join(root, item), root))

                        if any(os.path.basename(item) in ext for ext in exclude):
                        #if item in exclude:
                            print("{} Skipped".format(item_path))
                            continue

                        if os.path.isdir(item_path):
                            self.zip_dir(item_path, archive)
                        else:
                            archive.write(item_path, item)

                        self.callback.progress.emit("{} Added {} {}".format(item, os.path.join(root, item), root))
                archive.close()
        finally:
            pass
            #os.chdir(current_dir)

        self.callback.done.emit(self.target)


class WorkingFileUploader(QtCore.QRunnable):

    def __init__(self, parent, edit_api, task, source, file_name, software_name, comment = '', mode = "working", file_model = None, task_status = None):
        super(WorkingFileUploader, self).__init__(self, parent)
        self.threadpool = QtCore.QThreadPool.globalInstance()        
        self.parent = parent
        self.url = edit_api
        self.mode = mode
        self.source = source
        self.file_name = file_name
        self.task = task
        self.task_status = task_status
        self.software_name = software_name
        self.comment = comment

        self.swing_settings = SwingSettings.get_instance()

        self.email = self.swing_settings.swing_user()
        self.password = self.swing_settings.swing_password()

        self.file_model = file_model
        self.callback = UploadSignal()

    def process_upload(self):
        # source_name, source_ext = os.path.splitext(self.source)

        # /edit/logon 
        logon_url = "{}/login/".format(self.url)
        client = requests.session()

        # Retrieve the CSRF token first
        client.get(logon_url).cookies
        csrf = client.get(logon_url).cookies['csrftoken']

        login_data = dict(username=self.email, password=self.password, csrfmiddlewaretoken=csrf, next='/')
        r = client.post(logon_url, data=login_data, headers=dict(Referer=logon_url))

        upload_to = os.path.basename(self.source)

        encoder = MultipartEncoder(fields = { 
            "task_id": self.task["id"],
            "user_id": self.email,
            "task_status": self.task_status,
            "software": self.software_name,
            "mode": self.mode,
            "file_name": upload_to,
            "comment": self.comment,
            "csrfmiddlewaretoken": csrf,
            'input_file': (upload_to, open(self.source, 'rb'), 'rb')
        })

        encoder._read = encoder.read
        encoder.read = lambda size: encoder._read(int(_READ_SIZE))

        progress_callback = create_callback(encoder, self.callback, self.source)
        monitor = MultipartEncoderMonitor(encoder, progress_callback)
        headers = {'Content-Type': monitor.content_type }

        upload_url = "{}/api/upload/".format(self.url)
        try:
            r = client.post(upload_url, data=monitor, headers=headers, auth=(self.email, self.password))
            self.callback.done.emit({
                "status": "ok",
                "source": self.source,
                "message": "upload complete"
            })
            message = r.json()['message']
            # print('\n[Return status {0} {1}]'.format(r.status_code, message))
        except KeyboardInterrupt:
            print('\nUpload cancelled.')
        except Exception as e:
            print(e)
            self.callback.done.emit({
                "status": "error",
                "source": self.source,
                "message": "error uploading {}".format(e)
            })            
        return True

    def compress_dir(self):
        #v = 0
        #target = "{}_v{}".format(os.path.dirname(self.source), '{}'.format(v).zfill(3))
        #while os.path.exists(target):
        #    v += 1
        #    target = "{}_v{}".format(os.path.dirname(self.source), '{}'.format(v).zfill(3))
        baseline = os.path.basename(self.source)
        target = "{}/{}_{}.zip".format(os.path.dirname(self.source), baseline, self.mode)

        zipper = SwingCompressor(self.source, self.file_model, target=target)
        zipper.run()
        self.source = target

        self.callback.progress.emit({
            "status": "zipped",
            "source": self.source,
            "message": "created {}".format(target)
        })                            

        self.process_upload()

    def run(self):
        if os.path.isdir(self.source) and self.file_model:
            self.compress_dir()
        else:
            self.process_upload()

class ShotCreatorSignal(QtCore.QObject):

    # setting up custom signal
    results = pyqtSignal(object) 

class ShotCreator(QtCore.QRunnable):

    def __init__(self, parent, project, episode, sequence, shot_list):
        super(ShotCreator, self).__init__(self, parent)
        self.parent = parent

        # expecting gazu entities
        self.project = project
        self.episode = episode
        self.sequence = sequence

        # expecting breakout format json
        self.shot_list = shot_list
        self.callback = ShotCreatorSignal()

        self.force_preview = False

    def get_shot_task(self, shot, task_type_name, task_status):
        
        tasks = gazu.task.all_tasks_for_shot(shot)
        for t in tasks:
            if t["task_type_name"] == task_type_name and t["task_status_name"] == task_status["name"]:
                    return t
        return False        

    def run(self):
        settings = SwingSettings.get_instance()
        email = settings.swing_user()
        password = settings.swing_password()
        server = settings.swing_server()

        edit_api = "{}/edit".format(server)       

        force_preview = True                               

        sequence = gazu.shot.get_sequence(self.sequence["id"])
        if not sequence:
            results = {
                "status": "Error",
                "message": "Sequence not found"
            }
            self.callback.results.emit(results)
            return False

        #task_type = gazu.task.get_task_type_by_name("Layout")
        #todo: fix case insensitive search on gazu.task.get_task_type_by_name
        task_type = gazu.task.get_task_type("821d35d1-819f-475c-90ee-47bce5839a28")
        if not task_type:
            results = {
                "status": "Error",
                "message": "Task type Layout not found"
            }        
            self.callback.results.emit(results)
            return False

        task_status = gazu.task.get_task_status_by_name("Todo")
        if not task_status:
            results = {
                "status": "Error",
                "message": "Task status Todo not found"
            }        
            self.callback.results.emit(results)
            return False   

        software = gazu.files.get_software_by_name("Maya 2020")
        if not software:
            results = {
                "status": "Error",
                "message": "Software Maya 2020 not found in Kitsu config"
            }        
            self.callback.results.emit(results)
            return False                         

        person = gazu.person.get_person_by_email(email)            
        if not person:
            results = {
                "status": "Error",
                "message": "Person Maya 2020 not found in Kitsu config"
            }        
            self.callback.results.emit(results)
            return False           

        for item in self.shot_list:
            number = str(item["shot_number"])
            shot_name = "{}".format(number.zfill(3))

            shot = gazu.shot.get_shot_by_name(sequence, shot_name)
            results = {
                "status": "OK", 
                "message": "Checking shot {0}".format(shot_name),
            }        
            self.callback.results.emit(results)                

            if not shot:
                shot = gazu.shot.new_shot(self.project, sequence, shot_name)

                results = {
                    "status": "OK", 
                    "message": "Created new shot {0}".format(shot_name),
                }        
                self.callback.results.emit(results)     

            if "project_file_name" in item:
                file_name = item["project_file_name"]
                file_path = item["project_file_path"]
                
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    task = self.get_shot_task(shot, task_type["name"], task_status)
                    if not task:
                        task = gazu.task.new_task(shot, task_type, task_status = task_status, assigner = None, assignees = None)
                    working_files = gazu.files.get_working_files_for_task(task)

                    if len(working_files) == 0 or True:
                        source = file_path
                        if os.path.exists(source):
                            file_base = os.path.basename(source)
                            file_path = os.path.dirname(source)

                            worker = WorkingFileUploader(self, edit_api, task, source, file_base, software["name"], "Breakout file", mode = "working")
                            ##self.threadpool.start(worker)                        
                            worker.run()

                            results = {
                                "status": "OK", 
                                "message": "Uploaded file {0}".format(source),
                            }                              

                        self.callback.results.emit(results)                
            ### project working file

            # add playblast to Layout task if Layout task doesn't exist or is set to Todo
            if "playblast_file_name" in item:
                file_name = item["playblast_file_name"]
                file_path = item["playblast_file_path"]
                
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    task = self.get_shot_task(shot, task_type["name"], task_status)
                    if not task:
                        task = gazu.task.new_task(shot, task_type, task_status = task_status, assigner = None, assignees = None)                    
                    previews = gazu.files.get_all_preview_files_for_task(task)

                    if len(previews) == 0 or force_preview:
                        source = file_path
                        if os.path.exists(source):
                            file_base = os.path.basename(source)
                            file_path = os.path.dirname(source)
                            file_name, file_ext = os.path.splitext(file_base)                

                            # self.threadpool.start(worker)                        
                            worker = WorkingFileUploader(self, edit_api, task, source, file_base, software["name"], "Breakout file", mode = "preview")
                            ##self.threadpool.start(worker)                                                    
                            worker.run()

                            results = {
                                "status": "OK", 
                                "message": "Uploaded file {0}".format(source),
                            }  

                            self.callback.results.emit(results)      
            ### add playblast movie

            # check timings
            data = {}
            if "nb_frames" in item and item["nb_frames"]:
                data["nb_frames"] = item["nb_frames"]

            if "in" in item and item["in"]:
                data["frame_in"] = item["in"]

            if "out" in item and item["out"]:
                data["frame_out"] = item["out"]

            if len(data.keys()) > 0:
                gazu.shot.update_shot_data(shot, data)
            ### update timings

            results = {
                "status": "OK", 
                "message": "Processed shot {0}".format(shot_name),
            }        
            self.callback.results.emit(results)                                        

        results = {
            "status": "OK", 
            "message": "Create shots success",
        }        

        self.callback.results.emit(results)
        return True        

class SearchResultSignal(QtCore.QObject):

    # setting up custom signal
    results = pyqtSignal(object)        

class SearchFn(QtCore.QRunnable):

    def __init__(self, parent, list_of_names, project_id, show_hidden = False, task_types = None, status_types = None):
        super(SearchFn, self).__init__(self, parent)
        self.parent = parent

        self.swing_settings = SwingSettings.get_instance()
        self.project_id = project_id

        self.email = self.swing_settings.swing_user()
        self.password = self.swing_settings.swing_password()        
        
        self.search_list = list_of_names
        self.show_hidden = show_hidden
        self.task_types = task_types
        self.status_types = status_types

        self.callback = SearchResultSignal()

    def run(self):
        search_url = "{}/edit/api/search/fn".format(self.swing_settings.swing_server())
        results = []

        user_task_types = []
        if self.task_types:
            for item in self.task_types:
                user_task_types.append(item["id"])
            if len(user_task_types) > 0:
                task_types = ",".join(user_task_types)
        else:
            task_types = None

        count = 0
        for item in self.search_list:
            
            params = { 
                "username": self.email,
                "password": self.password,
                "filename": "%{}%".format(item.strip()),
                "project": self.project_id,
                "task_types": task_types, 
                "task_status": self.status_types,
                "show_hidden": self.show_hidden
            }             

            rq = requests.post(search_url, data = params)
            if rq.status_code == 200:
                found = rq.json()
                for item in found:
                    results.append(item)
            count += 1

        self.callback.results.emit(results)
        return results

class EntityFileLoader(QtCore.QRunnable):

    def __init__(self, parent, entity_id, working_dir, task_types = [], status_types = [], show_hidden = False, scan_cast = False):
        super(EntityFileLoader, self).__init__(self, parent)
        self.entity_id = entity_id
        self.working_dir = working_dir
        self.callback = LoadedSignal()    
        self.scan_cast = scan_cast
        self.show_hidden = show_hidden
        self.task_types = task_types
        self.status_types = status_types

        settings = SwingSettings.get_instance()
        self.email = settings.swing_user()
        self.password = settings.swing_password()
        self.server = settings.swing_server()

        self.edit_api = "{}/edit".format(self.server)
        ##self.edit_api = "http://10.147.19.55:8202/edit"

    def run(self):
        url = "{}/{}/{}".format(self.edit_api, "entity_info", self.entity_id)

        task_types = []
        if self.task_types:
            for item in self.task_types:
                task_types.append(item["id"])

        status_types = []
        if self.status_types: 
            for item in status_types:
                status_types.append(item["id"])            

        params = { 
            "username": self.email,
            "password": self.password,
#            "project": self.entity["project_id"],
            "task_types": json.dumps(task_types), 
            "task_status": json.dumps(status_types),            
            "output": "json",
            "show_casted": self.scan_cast,
            "show_hidden": self.show_hidden
        }             

        results = []
        rq = requests.post(url, data = params)
        if rq.status_code == 200:
            found = rq.json()
            for item in found:
                results.append(item)

        self.callback.loaded.emit(results)                        
        return True               
'''
    Loads all open projects, all episodes per project
'''
class ProjectEpisodeLoader(QtCore.QRunnable):

    def __init__(self):
        super(ProjectEpisodeLoader, self).__init__(self)
        self.settings = SwingSettings.get_instance()
        self.request_url = "{}/edit/api/project_list".format(self.settings.swing_server())
        self.callback = LoadedSignal()    

    def run(self):
        params = { 
            "username": self.settings.swing_user(),
            "password": self.settings.swing_password()
        }             

        results = []
        rq = requests.post(self.request_url, data = params)
        if rq.status_code == 200:
            found = rq.json()
            for item in found:
                results.append(item)

        self.callback.loaded.emit(results)                        
        return results      

class ProjectShotLoader(QtCore.QRunnable):

    def __init__(self, episode_id):
        super(ProjectShotLoader, self).__init__(self)
        self.settings = SwingSettings.get_instance()
        self.request_url = "{}/edit/api/shot_list".format(self.settings.swing_server())
        self.episode_id = episode_id
        self.callback = LoadedSignal()    

    def run(self):
        params = { 
            "username": self.settings.swing_user(),
            "password": self.settings.swing_password(),
            "episode_id": self.episode_id
        }             

        results = []
        rq = requests.post(self.request_url, data = params)
        if rq.status_code == 200:
            found = rq.json()
            for item in found:
                results.append(item)

        self.callback.loaded.emit(results)                        
        return results       

class EntityTagLoader(QtCore.QRunnable):

    def __init__(self, project_id, entity_id, entity_type = None):
        super(EntityTagLoader, self).__init__(self)
        self.settings = SwingSettings.get_instance()
        self.request_url = "{}/edit/api/tags".format(self.settings.swing_server())
        self.project_id = project_id
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.callback = LoadedSignal()    

    def run(self):
        params = { 
            "username": self.settings.swing_user(),
            "password": self.settings.swing_password(),
            "project_id": self.project_id, 
            "entity_id": self.entity_id,
            "entity_type": self.entity_type
        }             

        results = []
        rq = requests.post(self.request_url, data = params)

        if rq.status_code == 200:
            results = rq.json()

        self.callback.loaded.emit(results)                        
        return results       




