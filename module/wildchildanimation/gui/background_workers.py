# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import gazu
import json
import sys
import os
import requests
import zipfile

from zipfile import ZipFile

from requests_toolbelt.streaming_iterator import StreamingIterator
from requests_toolbelt import (
    MultipartEncoder,
    MultipartEncoderMonitor
)

import urllib
#from url six.moves import urllib

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import extract_archive

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSignal

from wildchildanimation.gui.swing_utils import write_log, resolve_content_path
from wildchildanimation.gui.swing_updater import update
from wildchildanimation.studio_interface import StudioInterface

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

class ProjectLoaderThread(QtCore.QRunnable):

    def __init__(self, parent):
        super(ProjectLoaderThread, self).__init__(self, parent)
        self.callback = LoadedSignal()

    def run(self):
        results = {}
        try:
            try:
                projects = gazu.project.all_open_projects()
                task_types = gazu.task.all_task_types()
                software = gazu.files.all_softwares()

                results["projects"] = projects
                results["task_types"] = task_types
                results["software"] = software

            except:
                traceback.print_exc(file=sys.stdout)
            # done
        finally:
            self.callback.loaded.emit(results)

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
        super(EntityFileLoader, self).__init__(self, parent)
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

    def __init__(self, parent, project):
        super(AssetTypeLoaderThread, self).__init__(self, parent)
        self.project = project
        self.callback = LoadedSignal()        

    def run(self):
        results = gazu.asset.all_asset_types_for_project(self.project)

        self.callback.loaded.emit(results)        

class AssetLoaderThread(QtCore.QRunnable):

    def __init__(self, parent, project, asset_type):
        super(AssetLoaderThread, self).__init__(self, parent)
        self.project = project
        self.asset_type = asset_type
        self.callback = LoadedSignal()        

    def run(self):
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
        project = task["project_id"]
        task_dir = gazu.files.build_working_file_path(task)

        results = {
            "task": task,
            "task_dir": task_dir,
            "project_dir": resolve_content_path(task_dir, self.project_root),
            "project": project
        }

        self.callback.loaded.emit(results)        

class TaskLoaderThread(QtCore.QRunnable):

    ALL_TASKS = False

    def __init__(self, parent, project_nav, email, project_root):
        super(TaskLoaderThread, self).__init__(self, parent)
        self.parent = parent
        self.nav = project_nav
        self.email = email
        self.project_root = project_root
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
        if TaskLoaderThread.ALL_TASKS:
            person = gazu.person.get_person_by_email(self.email)
            task_list = gazu.task.all_tasks_for_person(person)
        else:
            task_list = gazu.user.all_tasks_to_do()

        results = {}
        tasks = []

        current_project = self.nav.get_project()
        current_episode = self.nav.get_episode()
        
        task_types = {}
        for item in self.nav.get_task_types():
            task_types[item["id"]] = item

        task_status = {}
        for item in self.nav.get_task_status():
            task_status[item["id"]] = item

        for item in task_list:
            if not item["project_id"] == current_project["id"]:
                continue

            if item["task_type_id"] in task_types:
                if item["task_status_id"] in task_status:
                    if current_episode and item["episode_id"] != current_episode["id"]:
                        continue
                    ##item["task_url"] = gazu.task.get_task_url(item)
                    tasks.append(item)

        for item in tasks:
            item["task_dir"] = gazu.files.build_working_file_path(item)
            item["project_dir"] = resolve_content_path(item["task_dir"], self.project_root)

        results["project"] = current_project
        results["episode"] = current_episode
        results["tasks"] = tasks

        self.callback.loaded.emit(results)

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

class DownloadSignal(QtCore.QObject):

    # setting up custom signal
    done = pyqtSignal(object)        
    progress = pyqtSignal(object)

class FileDownloader(QtCore.QRunnable):

    def __init__(self, parent, working_dir, file_id, url, target, skip_existing = True, extract_zips = False, params = {}):
        super(FileDownloader, self).__init__(self, parent)
        self.parent = parent
        self.working_dir = working_dir
        self.file_id = file_id
        self.url = url
        self.target = target

        self.swing_settings = SwingSettings.getInstance()

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
            "working_dir": self.working_dir,
            "size": count
        }
        self.callback.progress.emit(results)

    def run(self):
        filename, file_extension = os.path.splitext(self.target)
        ###
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
                    "working_dir": self.working_dir,
                    "size": size
                }
                self.callback.done.emit(status)
                return

            if os.path.exists(os.path.join(self.working_dir, filename)):
                write_log("Working path exists {}".format(os.path.join(self.working_dir, filename)))

                size = os.path.getsize(self.target)                
                status = {
                    "status": "skipped",
                    "message": "Skipped existing file",
                    "file_id": self.file_id,
                    "target": self.target,
                    "working_dir": self.working_dir,
                    "size": size
                }
                self.callback.done.emit(status)
                return                

        self.params["username"] = self.swing_settings.swing_user()
        self.params["password"] = self.swing_settings.swing_password()

        target_dir = os.path.dirname(self.target)
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)   
                # print("Made dir: {}".format(target_dir))     
            except:
                pass

        count = 0
        rq = requests.post(self.url, data = self.params, stream = True)
        if rq.status_code == 200:
            with open(self.target, 'wb') as out:
                for bits in rq.iter_content(1024 * 1024):
                    out.write(bits)        
                    count += len(bits)
                    self.progress(count)
        else:
            status = {
                "status": "error",
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
        if self.extract_zips and file_extension.lower() in StudioInterface.UNARCHIVE_TYPES:
            zip_root = os.path.normpath(os.path.join(self.working_dir, filename))

            status = {
                "status": "ok",
                "message": "Extracting zip",
                "file_id": self.file_id,
                "target": zip_root,
                "working_dir": self.working_dir,
                "size": size
            }   
            self.callback.progress.emit(status)
            # def makedirs(name, mode=0o777, exist_ok=False):
            try:
                os.makedirs(zip_root)
            except:
                pass

            if extract_archive(self.swing_settings.bin_7z(), self.target, zip_root):
                status = {
                    "status": "ok",
                    "message": "Extracted zip",
                    "file_id": self.file_id,
                    "target": zip_root,
                    "working_dir": self.working_dir,
                    "size": size
                }   
                self.callback.progress.emit(status)  
            else:
                status = {
                    "status": "error",
                    "message": "Error extracting zip",
                    "file_id": self.file_id,
                    "target": zip_root,
                    "working_dir": self.working_dir,
                    "size": size
                }   
                self.callback.progress.emit(status)                               

        status = {
            "status": "ok",
            "message": "Download complete",
            "file_id": self.file_id,
            "target": self.target,
            "working_dir": self.working_dir,
            "size": size            
        }

        write_log("Download complete: {}".format(self.target))
        self.callback.done.emit(status)        


##############################################################################################################################################################################################
##############################################################################################################################################################################################
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

class WorkingFileUploader(QtCore.QRunnable):

    def __init__(self, parent, edit_api, task, source, file_name, software_name, comment, email, password, mode = "working", filter = []):
        super(WorkingFileUploader, self).__init__(self, parent)
        self.parent = parent
        self.url = edit_api
        self.mode = mode
        self.source = source
        self.file_name = file_name
        self.task = task
        self.software_name = software_name
        self.comment = comment
        self.email = email
        self.password = password
        self.filter = filter
        self.callback = UploadSignal()

    def process_upload(self):
        source_name, source_ext = os.path.splitext(self.source)

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
        target = "{}/{}.zip".format(os.path.dirname(self.source), baseline)

        with zipfile.ZipFile(target, 'w') as zip:
            for folder, sub, files in os.walk(self.source):
                for filename in files:
                    if not filename in self.filter:
                        #file_path = os.path.join(folder, filename)
                        zip.write(os.path.join(folder, filename), arcname=os.path.join(folder.replace(self.source, baseline), filename))

                        # zip.write(file_path, os.path.basename(file_path))
                        #ziph.write(os.path.join(root, file), arcname=os.path.join(root.replace(src, ""), file))                        
                        #print("added {}".format(filename))  
                    else:
                        print("skipped {}".format(filename))
            zip.close()

        self.callback.done.emit({
            "status": "new",
            "source": self.source,
            "message": "created {}".format(target)
        })                            

        self.source = target

    def run(self):
        if os.path.isdir(self.source):
            self.compress_dir()

        return self.process_upload()

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
        settings = SwingSettings.getInstance()
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

                            worker = WorkingFileUploader(self, edit_api, task, source, file_base, software["name"], "Breakout file", email, password, mode = "working")
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
                            worker = WorkingFileUploader(self, edit_api, task, source, file_base, software["name"], "Breakout file", email, password,  mode = "preview")
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

    def __init__(self, parent, edit_api, email, password, list_of_names, project_nav, show_hidden = False):
        super(SearchFn, self).__init__(self, parent)
        self.parent = parent
        self.nav = project_nav
        self.url = edit_api
        self.email = email
        self.password = password        
        self.search_list = list_of_names
        self.show_hidden = show_hidden
        self.callback = SearchResultSignal()

    def run(self):
        search_url = "{}/{}".format(self.url, "api/search/fn")
        results = []

        task_types = []
        if self.nav.is_task_types_filtered():
            for item in self.nav.get_task_types():
                task_types.append(item["id"])

        status_types = []
        if self.nav.is_status_types_filtered():
            for item in self.nav.get_task_status():
                status_types.append(item["id"])

        count = 0
        for item in self.search_list:
            
            params = { 
                "username": self.email,
                "password": self.password,
                "filename": "%{}%".format(item.strip()),
                "project": self.nav.get_project()["id"],
                "task_types": task_types, 
                "task_status": status_types,
                "show_hidden": self.show_hidden
            }             

            rq = requests.post(search_url, data = params)
            if rq.status_code == 200:
                found = rq.json()
                for item in found:
                    results.append(item)
            count += 1

        self.callback.results.emit(results)
        return True        

class EntityFileLoader(QtCore.QRunnable):

    def __init__(self, parent, project_nav, entity, working_dir, show_hidden = False, scan_cast = False):
        super(EntityFileLoader, self).__init__(self, parent)
        self.nav = project_nav
        self.entity = entity
        self.working_dir = working_dir
        self.callback = LoadedSignal()    
        self.scan_cast = scan_cast
        self.show_hidden = show_hidden

        settings = SwingSettings.getInstance()
        self.email = settings.swing_user()
        self.password = settings.swing_password()
        self.server = settings.swing_server()

        self.edit_api = "{}/edit".format(self.server)

    def run(self):
        url = "{}/{}/{}".format(self.edit_api, "entity_info", self.entity['id'])

        task_types = []
        if self.nav.is_task_types_filtered():
            for item in self.nav.get_task_types():
                task_types.append(item["id"])

        status_types = []
        if self.nav.is_status_types_filtered():
            for item in self.nav.get_task_status():
                status_types.append(item["id"])            

        params = { 
            "username": self.email,
            "password": self.password,
            "project": self.nav.get_project()["id"],
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