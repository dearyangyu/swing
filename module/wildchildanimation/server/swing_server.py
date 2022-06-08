# -*- coding: utf-8 -*-
import os
import shutil

from _thread import *
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
        r"Warning: file: C:\Users\pniemandt.STUDIO\Documents\maya\2022\prefs\filePathEditorRegistryPrefs.mel"
    ]

    def __init__(self, project_name):
        self.swing_settings = SwingSettings.get_instance()
        self.project_name = project_name
        self.connected = False
        self.gazu_client = None
        self.running = False    
        self.log = []

    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        password = self.swing_settings.swing_password()
        server = self.swing_settings.swing_server()
        email = self.swing_settings.swing_user()

        gazu.set_host("{}/api".format(server))
        try:
            self.gazu_client = gazu.log_in(email, password)
            self.connected = True
            self.user_email = email
            self.project = gazu.project.get_project_by_name(self.project_name)
            self.swing_root = self.swing_settings.swing_root()

            if not self.project:
                write_log("error: Project {} not found".format(self.project_name))
                return False            

            # check shot cache
            self.shot_cache = gazu.task.get_task_type_by_name("Shot_Cache")
            if not self.shot_cache:
                write_log("error: Task Type {} not found".format("Anim-Block"))
                return False   

            # check anim_final 
            self.anim_final = gazu.task.get_task_type_by_name("Anim-Final")
            if not self.anim_final:
                write_log("error: Task Type {} not found".format("Anim-Block"))
                return False  

            # check anim_anim 
            self.anim_anim = gazu.task.get_task_type_by_name("Anim-Animation")
            if not self.anim_anim:
                write_log("error: Task Type {} not found".format("Anim-Block"))
                return False  

            # check anim_block 
            self.anim_block = gazu.task.get_task_type_by_name("Anim-Block")
            if not self.anim_block:
                write_log("error: Task Type {} not found".format("Anim-Block"))
                return False 

            self.final = gazu.task.get_task_status_by_name("Final (Client Approved)") 
            if not self.final:
                write_log("error: Task Status 'Final (Client Approved)' not found")
                return False   

            self.wip = gazu.task.get_task_status_by_name("Work in Progress") 
            if not self.wip:
                write_log("error: Task Status 'WIP' not found")
                return False                                                                                      

            self.export = gazu.task.get_task_status_by_name("Export") 
            if not self.export:
                write_log("error: Task Status 'Export' not found")
                return False  

            self.review = gazu.task.get_task_status_by_name("Review") 
            if not self.review:
                write_log("error: Task Status 'Review' not found")
                return False                                               

            write_log("connected to {} as {}".format(self.project_name, email))
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
        for root, dirs, files in os.walk(path):
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
    def shot_cache_working_files(self, episode_name, working_files, shot_cache_task, completed_status, task_type):
        SUPPRESS_LINES = True

        self.log = []
        self.server_log("Exporting {}".format(episode_name))

        for item in working_files:
            wf = working_files[item]

            if wf["name"].lower().endswith(".ma"):
                working_file_path = wf["path"]
                task_name = "{}_".format(task_type["name"].replace("-", "_")).lower()

                working_file_path = os.path.normpath(working_file_path.replace("/mnt/content/productions", "Z://productions"))    

                if not wf["name"] in working_file_path:
                    wf = os.path.join(working_file_path, wf["name"])

                project_path = os.path.normpath(wf.replace("/mnt/content/productions", "Z://productions"))

                self.server_log("Exporting {}".format(project_path))


                if not os.path.exists(project_path) and os.path.isfile(project_path):
                    self.server_log("error: file not found: {}".format(project_path))
                    continue

                #

                working_path = os.path.normpath(project_path.replace("Z:\\productions", self.swing_root))
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
                    command_line = 'Z:\\env\\wca\\swing\\swing-main\\bin\\anim_update.bat'
                    self.server_log("running: {} {} {} {} {} {}".format(shot_cache_task["project"]["name"], shot_cache_task["episode"]["name"], shot_cache_task["sequence"]["name"], shot_cache_task["entity"]["name"], command_line, item))

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
                    command_line = 'Z:\\env\\wca\\swing\\swing-main\\bin\\shot_cache.bat'
                    self.server_log("running: {} {} {} {}".format(command_line, working_path, episode_name, task_name))

                    time_start = datetime.now()     
                    suppress_count = 0                                   

                    proc = subprocess.Popen([command_line, working_path, episode_name, task_name], shell = False, stdout=subprocess.PIPE)
                    while True:
                        #output = proc.stdout.read(1)
                        output = proc.stdout.readline()
                        try:
                            log = output.decode('utf-8')
                            if log == '' and proc.poll() != None:
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
   
                        server = SwingSettings.get_instance().swing_server()
                        edit_api = "{}/edit".format(server)  

                        self.server_log("uploading: {}".format(target))
                        worker = WorkingFileUploader(self, edit_api, shot_cache_task, target, "cache", "Maya", comment="Generated Shot Cache" , mode = "wip", file_model = None, task_status = completed_status["id"], archive_name = "shot_cache.zip")                            
                        worker.run()

                        time_end = datetime.now()
                        self.server_log("zip and uploaded completed in {}".format(time_end - time_start))

                        self.flush_output()
                    else:
                        # set task to error
                        comment_text = "Error generating shot_cache for task"
                        gazu.task.add_comment(shot_cache_task, self.review, comment_text)


                    self.server_log("finished: {} {} {} {} {} {}".format(shot_cache_task["project"]["name"], shot_cache_task["episode"]["name"], shot_cache_task["sequence"]["name"], shot_cache_task["entity"]["name"], command_line, item))
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

        tasks = gazu.task.all_tasks_for_task_type(self.project, self.shot_cache)

        task_list = []
        for task in tasks:
            if task["id"] not in task_list and task["task_status_id"] == self.export["id"]:
                task_list.append(task["id"])

        # debug
        ##task_id = gazu.task.get_task("3f275458-7747-431a-9c69-31e4608d4154")
        ##task_list = [ task_id ]

        write_log("process::checking {} for {} shots".format(self.shot_cache["name"].lower(), len(task_list)))
        write_log(r"**************************************************")
        for task_id in task_list:
            shot_cache_task = gazu.task.get_task(task_id)

            if not shot_cache_task["task_status_id"] == self.export["id"]:
                write_log("skipping task {} not available, task in use or in error".format(shot_cache_task["id"]))
                continue

            shot = gazu.shot.get_shot(shot_cache_task["entity"]["id"])
            episode = gazu.shot.get_episode(shot["episode_id"])

            episode_details = episode["name"].split("_")
            if len(episode_details) == 2:
                episode_name = "{}_".format(episode_details[1].lower())
            else:
                episode_name = "{}_".format("".join(episode_details).lower())

            task_type = self.anim_final
            shot_task = gazu.task.get_task_by_entity(shot, task_type)
            project_files = gazu.files.get_last_working_files(shot_task)
            if len(project_files) > 0:
                gazu.task.start_task(shot_cache_task)
                if self.shot_cache_working_files(episode_name, project_files, shot_cache_task, self.final, task_type):
                    continue
                    # return True

            task_type = self.anim_anim
            shot_task = gazu.task.get_task_by_entity(shot, task_type)
            project_files = gazu.files.get_last_working_files(shot_task)
            if len(project_files) > 0:
                gazu.task.start_task(shot_cache_task)
                if self.shot_cache_working_files(episode_name, project_files, shot_cache_task, self.wip, task_type):
                    continue
                    #return True

            task_type = self.anim_block
            shot_task = gazu.task.get_task_by_entity(shot, task_type)
            project_files = gazu.files.get_last_working_files(shot_task)
            if len(project_files) > 0:
                if self.shot_cache_working_files(episode_name, project_files, shot_cache_task, self.wip, task_type):
                    gazu.task.start_task(shot_cache_task)
                    continue
                    #return True

            write_log("process::{} {} {} {} {} ({})".format(self.project_name, shot["episode_name"], shot["sequence_name"], shot["name"], self.export["name"], len(project_files)))    
            self.flush_output() 

        write_log("process::done")       


    def stop(self):
        self.running = False

if __name__ == "__main__":
    write_log("SwingServer::start")
    #server = SwingServer(project_name = "Wind in the Willows")

    #server = SwingServer(project_name = "Attack of the Killer Bunny S1")
    server = SwingServer(project_name = "Wind in the Willows")
    server.start()
    write_log("SwingServer::done")
