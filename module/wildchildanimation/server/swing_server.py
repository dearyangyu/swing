# -*- coding: utf-8 -*-
import os
import shutil
import argparse
import json

import zipfile

from wildchildanimation.gui.background_workers import WorkingFileUploader
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import write_log

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    qtMode = 1

import sys
import traceback
import time
import gazu
import subprocess

from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
class SwingServer(QtCore.QObject):

    ENCODE_DIR = "H:\\Encodes"

    SUPPRESS_LINES = [
        r"Unrecognized node type 'nodeGraphEditorInfo';",
        r"Unrecognized node type 'Redshift",
        r'Plug-in, "redshift4maya"',
        r"Warning: Frame rate mismatch",
        r"Imported animation keys may not match scene frames and become fractional",
        r"You must either select the affected nodes or specify them on the command line",
        r":redshiftOptions.postEffects' already has an incoming connection",
        r"':defaultArnoldDisplayDriver.message' is already connected",
        r"Result: Warning: handled a NAN float",
        r"Errors have occurred while reading this scene that may result in data loss",
        r"pymel : WARNING : found new MPx classes",
        r"pymel.core : INFO : Updating pymel with pre-loaded plugins",
        r"Warning: line 1: filePathEditor: Attribute",
        r"qt.svg: Cannot open file ':/expression.svg'",
        r"RuntimeError: file <maya console> line 1: Plug-in",
        r"Could not find file: aiRectangleAreaLight.xml",
        r"Errors loading XML",
        r"Attempting to read fragment XML code from: aiRectangleAreaLight.xml",
        r"Begin attempted read of a shade fragment XML file",
        r"###############################################################################",
        r"-------------------------------------------------------------------------------",
        r"End attempted read of fragment XML.",
        r"filePathEditorRegistryPrefs.mel",
        r"Undo:",
        r"anim_export::was in Root",
        r"anim_export::Already in Root",
        r"maya\FBX\Logs\2020.2.3\maya2022exp.log",
        r"translateXtranslateYtranslateZrotateXrotateYrotateZparentConstraint"
    ]

    def __init__(self, server, project, user, password):
        self.swing_settings = SwingSettings.get_instance()

        self.server = server
        self.project_name = project
        self.user = user
        self.password = password

        self.connected = False
        self.gazu_client = None
        self.running = False    
        self.log = []

    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        gazu.set_host("{}/api".format(self.server))
        try:
            self.gazu_client = gazu.log_in(self.user, password)
            self.connected = True
            self.user_email = self.user
            self.project = gazu.project.get_project_by_name(self.project_name)
            self.swing_root = self.swing_settings.swing_root()

            if not self.project:
                write_log("error: Project {} not found".format(self.project_name))
                return False            

            # check shot cache
            self.cache = gazu.task.get_task_type_by_name("Cache")
            if not self.cache:
                write_log("error: Task Type {} not found".format("Cache"))
                return False   

            # check a3 
            self.a3 = gazu.task.get_task_type_by_name("A3")
            if not self.a3:
                write_log("error: Task Type {} not found".format("A3"))
                return False  

            # check a2 
            self.a2 = gazu.task.get_task_type_by_name("A2")
            if not self.a2:
                write_log("error: Task Type {} not found".format("A2"))
                return False  

            # check a1 
            self.a1 = gazu.task.get_task_type_by_name("A1")
            if not self.a1:
                write_log("error: Task Type {} not found".format("A1"))
                return False 

            self.final = gazu.task.get_task_status_by_name("Final") 
            if not self.final:
                write_log("error: Task Status 'Final' not found")
                return False   

            self.wip = gazu.task.get_task_status_by_name("Work In Progress") 
            if not self.wip:
                write_log("error: Task Status 'WIP' not found")
                return False                   

            self.wfa = gazu.task.get_task_status_by_name("Waiting for Approval") 
            if not self.wfa:
                write_log("error: Task Status 'WFA' not found")
                return False                                                                                      

            self.export = gazu.task.get_task_status_by_name("Export") 
            if not self.export:
                write_log("error: Task Status 'Export' not found")
                return False  

            self.review = gazu.task.get_task_status_by_name("Retake") 
            if not self.review:
                write_log("error: Task Status 'Retake' not found")
                return False                                               

            self.render_status = gazu.task.get_task_status_by_name("Render") 
            if not self.render_status:
                write_log("error: Task Status 'Render' not found")
                return False                   

            write_log("connected to {} as {}".format(self.project_name, self.user))
        except:
            return False

        return True   

    def start(self):
        if self.connect_to_server():
            self.running = True
            self.run()

    def run(self):
        while self.running:
            try:
                self.process()
                self.flush_output()
            except:
                write_log("exception running swing server")
                traceback.print_exc(file=sys.stdout)

            # sleep 5 mins
            time.sleep(5 * 60)

    def zip_dir(self, path, zipfile):
        for root, _, files in os.walk(path):
            for file in files:
                zipfile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))        

    def remove_dir(self, dir):
        write_log("removing dir {}".format(dir))
        shutil.rmtree(dir)

    def server_log(self, text):
        log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
        log += " {}".format(text)

        self.log.append(log.strip())          
        print(log)       

    # scan through project working files, if task type found, call anim-export on it
    # will first download project file to local working dir
    # will then run anim_update on the project
    # will run anim_export passing in the project_name to strip from file name
    # lastly will zip and upload cache to kitsu
    def cache_working_files(self, episode_name, working_files, cache_task, completed_status, task_type):
        SUPPRESS_LINES = True

        files = []
        for item in working_files:
            file_item = {}
            file_item["working_file"] = working_files[item]
            file_item["updated_at"] = working_files[item]["updated_at"]
            files.append(file_item)

        project_files = sorted(files, key=lambda d: time.strptime(d['updated_at'], r'%Y-%m-%dT%H:%M:%S'), reverse=True)            

        self.log = []
        self.server_log("Exporting {}".format(episode_name))

        for item in project_files:
            wf = item["working_file"]

            if wf["name"].lower().endswith(".ma"):
                working_file_path = wf["path"]
                task_name = "{}_".format(task_type["name"].replace("-", "_")).lower()

                working_file_path = os.path.normpath(working_file_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))    

                if not wf["name"] in working_file_path:
                    wf = os.path.join(working_file_path, wf["name"])

                project_path = os.path.normpath(wf.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))

                self.server_log("Exporting {}".format(project_path))

                if not os.path.exists(project_path) and os.path.isfile(project_path):
                    self.server_log("error: file not found: {}".format(project_path))
                    continue
                #

                if project_path.startswith("Z:\\"):
                    working_path = os.path.normpath(project_path.replace("Z:\\productions", self.swing_root))
                elif project_path.startswith("V:\\"):
                    working_path = os.path.normpath(project_path.replace("V:\\productions", self.swing_root))
                elif project_path.startswith("T:\\"):
                    working_path = os.path.normpath(project_path.replace("T:\\productions", self.swing_root))

                if not os.path.exists(os.path.dirname(working_path)):
                    os.makedirs(os.path.dirname(working_path))

                cache_dir = os.path.join(os.path.dirname(working_path), "cache")                    
                if os.path.exists(cache_dir):
                    try:
                        os.remove(cache_dir)    
                        self.server_log("removed old cache dir: {}".format(cache_dir))
                    except:
                        self.server_log("error removing old cache dir: {}".format(cache_dir))                        
                        print(traceback.format_exc())   

                    target = "{}/{}".format(os.path.dirname(working_path), "shot_cache.zip")
                    try:
                        if os.path.exists(target):
                            os.remove(target)    
                            self.server_log("removed old shot_cache: {}".format(target))
                    except:
                        self.server_log("error removing shot_cache: {}".format(target))                        
                        print(traceback.format_exc())                                            

                shutil.copy2(project_path, working_path)
                try:
                    # run anim update on the project file
                    command_line = 'Z:\\env\\wca\\swing\\swing-main\\bin\\anim_update_maya_2023.bat'
                    self.server_log("running: {} {} {} {} {} {}".format(cache_task["project"]["name"], cache_task["episode"]["name"], cache_task["sequence"]["name"], cache_task["entity"]["name"], command_line, item))

                    time_start = datetime.now()
                    suppress_count = 0

                    proc = subprocess.Popen([command_line, working_path], shell = False, stdout=subprocess.PIPE)
                    while True:
                        show_line = True
                        output = proc.stdout.readline()
                        # output = proc.stdout.read(1)
                        try:
                            log = output.decode('utf-8')
                            if log == '' and proc.poll() != None:
                                break
                            elif "#done#" in log:
                                self.server_log("Script is #done#")    
                                break
                            else:
                                if SUPPRESS_LINES: 
                                    for item in SwingServer.SUPPRESS_LINES:
                                        if item in log:
                                            suppress_count += 1
                                            show_line = False
                                            break

                                if show_line:
                                    # sys.stdout.write(log)
                                    log = log.strip()
                                    if log != '':
                                        self.server_log(log)

                                sys.stdout.flush()
                        except:
                            self.server_log("Byte Code Error: Ignoring")
                            print(traceback.format_exc())
                        # continue

                    time_end = datetime.now()
                    try:
                        self.server_log("anim update completed in {}, suppressed {} lines of warning".format((time_end - time_start), suppress_count))
                    except:
                        print(traceback.format_exc())

                    # run shot cache on the project file                                          
                    command_line = 'Z:\\env\\wca\\swing\\swing-main\\bin\\shot_cache_maya_2023.bat'
                    self.server_log("running: {} {} {} {}".format(command_line, working_path, episode_name, task_name))

                    time_start = datetime.now()     
                    suppress_count = 0                                   

                    proc = subprocess.Popen([command_line, working_path, episode_name, task_name], shell = False, stdout=subprocess.PIPE)
                    while True:
                        show_line = True
                        #output = proc.stdout.read(1)
                        output = proc.stdout.readline()
                        try:
                            log = output.decode('utf-8')
                            if log == '' and proc.poll() != None:
                                break
                            elif "#done#" in log:
                                self.server_log("Script is #done#")    
                                break
                            else:
                                if SUPPRESS_LINES: 
                                    for item in SwingServer.SUPPRESS_LINES:
                                        if item in log:
                                            suppress_count += 1
                                            show_line = False
                                            break                                        

                                if show_line:
                                    # sys.stdout.write(log)
                                    log = log.strip()
                                    if log != '':
                                        self.server_log(log)
                                sys.stdout.flush()
                        except:
                            self.server_log("Byte Code Error: Ignoring")
                            print(traceback.format_exc())
                        # continue


                    time_end = datetime.now()
                    try:
                        self.server_log("shot cache completed in {}, suppressed {} lines of warning".format((time_end - time_start), suppress_count))
                    except:
                        print(traceback.format_exc())

                    self.flush_output()

                    log_out = os.path.join(os.path.dirname(working_path), "cache", "swing_export.log")
                    with open(log_out, 'w') as f:
                        for item in self.log:
                            f.write("%s\n" % item.strip())
                    f.close()

                    time_start = datetime.now()                    

                    if os.path.exists(cache_dir):
                        target = "{}/{}".format(os.path.dirname(working_path), "shot_cache.zip")
                    
                        try:
                            if os.path.exists(target):
                                os.remove(target)

                            self.server_log("zipping: {}".format(target))
                            with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
                                try:
                                    self.zip_dir(cache_dir, archive)
                                    self.remove_dir(cache_dir)
                                finally:
                                    archive.close()  
                        except:                                
                            traceback.print_exc(file=sys.stdout)
                            return False 
                        self.flush_output()

                        edit_api = "{}/edit".format(self.server)  

                        self.server_log("uploading: {}".format(target))
                        worker = WorkingFileUploader(self, edit_api, cache_task, target, "cache", "Maya", comment="Generated Shot Cache" , mode = "wip", file_model = None, task_status = completed_status["id"], archive_name = "shot_cache.zip")                            
                        worker.run()

                        time_end = datetime.now()
                        self.server_log("zip and uploaded completed in {}".format(time_end - time_start))

                        self.flush_output()
                    else:
                        # set task to error
                        comment_text = "Error generating shot_cache for task"
                        gazu.task.add_comment(cache_task, self.review, comment_text)


                    self.server_log("finished: {} {} {} {} {} {}".format(cache_task["project"]["name"], cache_task["episode"]["name"], cache_task["sequence"]["name"], cache_task["entity"]["name"], command_line, item))
                    self.server_log("******************************************************************************************")
                   
                    return True
                except:
                    traceback.print_exc(file=sys.stdout)
                    return False                    

                # call anim cache
        return True

    def flush_output(self):
        try:
            sys.stdout.write('')
            sys.stdout.flush() 
        except:
            pass

    def process(self):
        write_log("process::start")

        gazu.set_host("{}/api".format(self.server))
        gazu.log_in(self.user, password)        

        tasks = gazu.task.all_tasks_for_task_status(self.project, self.cache, self.export)
        #
        # check for any shot cache tasks
        if len(tasks) > 0:
            write_log("process::checking {} for {} shots".format(self.cache["name"].lower(), len(tasks)))
            write_log(r"**************************************************")

            # sort tasks by shot priority
            for t in tasks:
                t["priority"] = 0

                shot = gazu.shot.get_shot(t["entity_id"])
                if "data" in shot:
                    try:
                        if "priority" in shot["data"]:
                            t["priority"] = shot["data"]["priority"]
                    except:
                        write_log("process::priority: No priority to set")

            tasks = sorted(tasks, key=lambda d: d['priority'], reverse=True) 

            for task_id in tasks:
                shot_cache_task = gazu.task.get_task(task_id)

                if not shot_cache_task["task_status_id"] == self.export["id"]:
                    task_details = "{} episode {} shot {} {} status {}".format(self.project["name"], shot_cache_task["episode"]["name"], shot_cache_task["sequence"]["name"], shot_cache_task["entity"]["name"], shot_cache_task["task_status"]["name"])
                    write_log("skipping {}".format(task_details))                    
                    continue

                shot = gazu.shot.get_shot(shot_cache_task["entity"]["id"])
                episode = gazu.shot.get_episode(shot["episode_id"])

                episode_details = episode["name"].split("_")
                if len(episode_details) == 2:
                    episode_name = "{}_".format(episode_details[1].lower())
                else:
                    episode_name = "{}_".format("".join(episode_details).lower())

                if not episode_name.startswith(self.project["code"]):
                    episode_name = "{}_{}".format(self.project["code"], episode_name)

                task_type = self.a3
                shot_task = gazu.task.get_task_by_entity(shot, task_type)

                project_files = gazu.files.get_last_working_files(shot_task)
                if len(project_files) > 0:
                    # fix start task - gazu.task.start_task(shot_cache_task)
                    gazu.task.add_comment(shot_cache_task, self.wip)
                    if self.cache_working_files(episode_name, project_files, shot_cache_task, self.final, task_type):
                        continue
                        # return True

                task_type = self.a2
                shot_task = gazu.task.get_task_by_entity(shot, task_type)

                project_files = gazu.files.get_last_working_files(shot_task)
                if len(project_files) > 0:
                    # fix start task - gazu.task.start_task(shot_cache_task)
                    gazu.task.add_comment(shot_cache_task, self.wip)
                    if self.cache_working_files(episode_name, project_files, shot_cache_task, self.wip, task_type):
                        continue
                        #return True

                task_type = self.a1
                shot_task = gazu.task.get_task_by_entity(shot, task_type)

                project_files = gazu.files.get_last_working_files(shot_task)
                if len(project_files) > 0:
                    # fix start task - gazu.task.start_task(shot_cache_task)
                    gazu.task.add_comment(shot_cache_task, self.wip)
                    if self.cache_working_files(episode_name, project_files, shot_cache_task, self.wip, task_type):
                        continue
                        #return True

                write_log("process::{} {} {} {} {} ({})".format(self.project_name, shot["episode_name"], shot["sequence_name"], shot["name"], self.export["name"], len(project_files)))    
                self.flush_output() 

        write_log("process::done")       

    def stop(self):
        self.running = False

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Swing::Cache Service - Settings"
    )

    parser.add_argument("-c", "--config", help="Config File", action="store")
    args = parser.parse_args()
    config_file = args.config

    if not os.path.exists(config_file):
        print("Config file not found: {}".format(config_file))
        sys.exit(1)

    config_json = json.load(open(config_file))

    server = config_json["server"]
    project = config_json["project"]
    user = config_json["user"]
    password = config_json["password"]

    # Add arguments for the sequence parser
    try:
        write_log("SwingServer::start")

        server = SwingServer(server = server, project = project, user = user, password = password)
        server.start()
        write_log("SwingServer::done")
    except:
        traceback.print_exc()
    # Process the args using the argument execution functions        
    sys.exit(0)