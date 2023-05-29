# -*- coding: utf-8 -*-
import os
import shutil

from _thread import *
import zipfile

from wildchildanimation.gui.swing_utils import friendly_string

from wildchildanimation.gui.background_workers import WorkingFileUploader
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.studio.openexr.swing_convert import SwingConvert
from wildchildanimation.gui.swing_utils import extract_archive

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
class LayoutServer(QtCore.QObject):

    ENCODE_DIR = "H:\\Turnover"

    SUPPRESS_LINES = [
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
            self.layout_task = gazu.task.get_task_type_by_name("layout")
            if not self.layout_task:
                write_log("error: Task Type {} not found".format("layout"))
                return False   


            self.final = gazu.task.get_task_status_by_name("Final (Client Approved)") 
            if not self.final:
                write_log("error: Task Status 'Final (Client Approved)' not found")
                return False   

            self.wip = gazu.task.get_task_status_by_name("Work in Progress") 
            if not self.wip:
                write_log("error: Task Status 'WIP' not found")
                return False                   

            self.wfa = gazu.task.get_task_status_by_name("Waiting for Approval") 
            if not self.wfa:
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


    # grab layout scene from kitsu
    # run chainsaw on layout scene
    # run animprep on each shot
    # upload shots to turnover folder
    def layout_turnover(self, episode_name, working_files, shot_cache_task, task_status):
        SUPPRESS_LINES = True

        files = []
        for item in working_files:
            file_item = {}
            file_item["working_file"] = working_files[item]
            file_item["updated_at"] = working_files[item]["updated_at"]
            files.append(file_item)

        project_files = sorted(files, key=lambda d: time.strptime(d['updated_at'], r'%Y-%m-%dT%H:%M:%S'), reverse=True)            

        self.log = []
        self.server_log("Breakout {}".format(episode_name))

        for item in project_files:
            wf = item["working_file"]

            if wf["name"].lower().endswith(".ma"):
                working_file_path = wf["path"]

                working_file_path = os.path.normpath(working_file_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))    

                if not wf["name"] in working_file_path:
                    wf = os.path.join(working_file_path, wf["name"])

                project_path = os.path.normpath(wf.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))

                self.server_log("Breakout {}".format(project_path))

                if not os.path.exists(project_path) and os.path.isfile(project_path):
                    self.server_log("error: file not found: {}".format(project_path))
                    continue
                #

                working_path = os.path.normpath(project_path.replace("Z:\\productions", self.swing_root))
                if not os.path.exists(os.path.dirname(working_path)):
                    os.makedirs(os.path.dirname(working_path))

                shutil.copy2(project_path, working_path)
                try:
                    # run anim update on the project file
                    command_line = 'Z:\\env\\wca\\swing\\swing-main\\bin\\layout_breakout.bat'
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
                                    for item in LayoutServer.SUPPRESS_LINES:
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
                        self.server_log("chainsaw completed in {}, suppressed {} lines of warning".format((time_end - time_start), suppress_count))
                    except:
                        print(traceback.format_exc())

                    self.flush_output()

                    time_start = datetime.now()
                    suppress_count = 0

                    try:
                        file_parts = os.path.basename(working_path).split("_")

                        breakout_zip = os.path.join(os.path.dirname(working_path), "{}_{}_{}_turnover.zip".format(file_parts[1], file_parts[3], file_parts[4]))
                        source_dir = os.path.join(os.path.dirname(working_path), 'breakout')

                        self.server_log("zipping: {}".format(source_dir))
                        with zipfile.ZipFile(breakout_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
                            try:
                                self.zip_dir(source_dir, archive)
                                ## self.remove_dir(breakout_zip)
                            finally:
                                archive.close()  
                    except:                                
                        traceback.print_exc(file=sys.stdout)
                        return False 
                    self.flush_output()

                    server = SwingSettings.get_instance().swing_server()
                    edit_api = "{}/edit".format(server)  

                    self.server_log("uploading: {}".format(breakout_zip))
                    worker = WorkingFileUploader(self, edit_api, shot_cache_task, breakout_zip, "cache", "Maya", comment="Layout Turnover Shots" , mode = "wip", file_model = None, task_status = task_status["id"], archive_name = "turnover.zip")                            
                    worker.run()

                    time_end = datetime.now()
                    self.server_log("zip and uploaded completed in {}".format(time_end - time_start))                    

                    log_out = os.path.join(os.path.dirname(working_path), "swing_breakout.log")
                    with open(log_out, 'w') as f:
                        for item in self.log:
                            f.write("%s\n" % item.strip())
                    f.close()

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

        tasks = gazu.task.all_tasks_for_task_status(self.project, self.layout_task, self.export)
        #
        # check for any shot cache tasks
        if len(tasks) > 0:
            write_log("process::checking {} for {} shots".format(self.layout_task["name"].lower(), len(tasks)))
            write_log(r"**************************************************")

            # sort tasks by shot priority
            for t in tasks:
                t["priority"] = 0

                shot = gazu.shot.get_shot(t["entity_id"])
                if "data" in shot:
                    if "priority" in shot["data"]:
                        t["priority"] = shot["data"]["priority"]

            tasks = sorted(tasks, key=lambda d: d['priority'], reverse=True) 

            for task_id in tasks:
                turnover_task = gazu.task.get_task(task_id)

                if not turnover_task["task_status_id"] == self.export["id"]:
                    task_details = "{} episode {} shot {} {} status {}".format(self.project["name"], turnover_task["episode"]["name"], turnover_task["sequence"]["name"], turnover_task["entity"]["name"], turnover_task["task_status"]["name"])
                    write_log("skipping {}".format(task_details))                    
                    continue

                shot = gazu.shot.get_shot(turnover_task["entity"]["id"])
                episode = gazu.shot.get_episode(shot["episode_id"])

                episode_details = episode["name"].split("_")
                if len(episode_details) == 2:
                    episode_name = "{}_".format(episode_details[1].lower())
                else:
                    episode_name = "{}_".format("".join(episode_details).lower())

                project_files = gazu.files.get_last_working_files(turnover_task)
                if len(project_files) > 0:
                    ##debug - gazu.task.start_task(turnover_task)
                    if self.layout_turnover(episode_name, project_files, turnover_task, self.wfa):
                        continue
                        # return True

                write_log("process::{} {} {} {} {} ({})".format(self.project_name, shot["episode_name"], shot["sequence_name"], shot["name"], self.export["name"], len(project_files)))    
                self.flush_output() 

        write_log("process::done")       

    def stop(self):
        self.running = False

if __name__ == "__main__":
    write_log("LayoutServer::start")
    #server = LayoutServer(project_name = "Wind in the Willows")

    server = LayoutServer(project_name = "Attack of the Killer Bunny S1")

    ## server = LayoutServer(project_name = "Wind in the Willows")
    server.start()
    write_log("LayoutServer::done")
