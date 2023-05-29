# -*- coding: utf-8 -*-
import os
import shutil

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import extract_archive

from wildchildanimation.gui.swing_utils import write_log
from wildchildanimation.unreal.swing_unreal_loader import SwingUE

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

from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
class UEServer(QtCore.QObject):

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

            #######################################################################################
            # TASK TYPES
            #

            # check shot cache
            self.shot_cache = gazu.task.get_task_type_by_name("Shot_Cache")
            if not self.shot_cache:
                write_log("error: Task Type {} not found".format("Anim-Block"))
                return False   

            # check ue import
            self.ue_import = gazu.task.get_task_type_by_name("UE_Import")
            if not self.ue_import:
                write_log("error: Task Type {} not found".format("UE_Import"))
                return False 

            #######################################################################################
            # STATUS TYPES
            #

            # final
            self.final = gazu.task.get_task_status_by_name("Final (Client Approved)") 
            if not self.final:
                write_log("error: Task Status 'Final (Client Approved)' not found")
                return False   

            # wip 
            self.wip = gazu.task.get_task_status_by_name("Work in Progress") 
            if not self.wip:
                write_log("error: Task Status 'WIP' not found")
                return False                   

            # wfa
            self.wfa = gazu.task.get_task_status_by_name("Waiting for Approval") 
            if not self.wfa:
                write_log("error: Task Status 'WIP' not found")
                return False                                                                                      

            # export
            self.export = gazu.task.get_task_status_by_name("Export") 
            if not self.export:
                write_log("error: Task Status 'Export' not found")
                return False  

            # review
            self.review = gazu.task.get_task_status_by_name("Review") 
            if not self.review:
                write_log("error: Task Status 'Review' not found")
                return False                                               

            # render 
            self.render_status = gazu.task.get_task_status_by_name("Render") 
            if not self.render_status:
                write_log("error: Task Status 'Render' not found")
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

    def remove_dir(self, dir):
        write_log("removing dir {}".format(dir))
        shutil.rmtree(dir)            

    def server_log(self, text):
        log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
        log += " {}".format(text)

        self.log.append(log.strip())          
        print(log)       

    def unreal_import(self, episode_name, output_files, shot_cache_task, completed_status, task_type):
        #     SwingUE().swing_ue_import(dir = SOURCE_DIR,  episode="110_nursetoad")
        SUPPRESS_LINES = True

        self.log = []
        self.server_log("Exporting {}".format(episode_name))

        for of in output_files:

            if of["name"].lower().endswith(".zip") or of["name"].lower().endswith("7z"):
                source_file_path = of["path"]
                #task_name = "{}_".format(task_type["name"].replace("-", "_")).lower()

                source_file_path = os.path.normpath(source_file_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))    

                if not of["name"] in source_file_path:
                    source_file_path = os.path.join(source_file_path, of["name"])

                source_path = os.path.normpath(source_file_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))
                target_path = os.path.normpath(source_file_path.replace(SwingSettings.get_instance().shared_root(), self.swing_root))

                self.server_log("Exporting {} to {}".format(source_path, target_path))

                if not os.path.exists(source_path) and os.path.isfile(source_path):
                    self.server_log("error: file not found: {}".format(source_path))
                    continue
                #

                cache_dir = os.path.join(os.path.dirname(target_path), "shot_cache")                    
                if os.path.exists(cache_dir):
                    try:
                        os.remove(cache_dir)    
                        self.server_log("removed old cache dir: {}".format(cache_dir))
                    except:
                        self.server_log("error removing old cache dir: {}".format(cache_dir))                        
                        print(traceback.format_exc())   
                else:
                    os.makedirs(cache_dir)

                if extract_archive(SwingSettings.get_instance().bin_7z(), source_path, cache_dir):
                    try:
                        self.server_log("Processing shot_cache for UE Import")
                        try:
                            # call ue batch import  
                            time_start = datetime.now()                             
                            try:
                                abc_cache_dir = os.path.join(cache_dir, "cache")

                                if not os.path.exists(abc_cache_dir):
                                    abc_cache_dir = os.path.join(cache_dir)
                                self.server_log("ABC_CACHE_DIR :{}".format(abc_cache_dir))

                                SwingUE().swing_ue_import(ue_editor = SwingSettings.get_instance().bin_ue_editor(), project_path = SwingSettings.get_instance().ue_project_root(), 
                                    episode=episode_name, dir = abc_cache_dir, log_dir = os.path.dirname(target_path))

                                time_end = datetime.now()

                                self.server_log("shot cache completed in {}".format((time_end - time_start)))
                            except:
                                print(traceback.format_exc())

                            self.flush_output()

                            log_out = os.path.join(os.path.dirname(cache_dir), "swing_ue_import.log")
                            with open(log_out, 'w') as f:
                                try:
                                    for item in self.log:
                                        f.write("%s\n" % item.strip())
                                finally:
                                    f.close()

                            ##self.server_log("finished: {} {} {} {} {} {}".format(shot_cache_task["project"]["name"], shot_cache_task["episode"]["name"], shot_cache_task["sequence"]["name"], shot_cache_task["entity"]["name"], command_line, item))
                            self.server_log("******************************************************************************************")
                        
                            return True
                        except:
                            traceback.print_exc(file=sys.stdout)


                            return False                    
                    finally:
                        ##try:
                            ## if os.path.exists(cache_dir):
                            ##    self.remove_dir(cache_dir)
                        ##except:
                        ##    self.server_log("Directory {} in use, delete manually".format(cache_dir))
                        pass
                        # remove cache dir


                    # end finally

                # call ue batch import
        return True

    def flush_output(self):
        try:
            sys.stdout.write('')
            sys.stdout.flush() 
        except:
            pass

    def process(self):
        write_log("process::start")

        ###########################################################################################
        #
        # UE IMPORT
        #
        # tasks = gazu.task.all_tasks_for_task_status(self.project, self.ue_import, self.export)    
        tasks = gazu.task.all_tasks_for_task_status(self.project, self.ue_import, self.export)[:10]
        if len(tasks) > 0:
            write_log("process::checking {} for {} shots".format(self.ue_import["name"].lower(), len(tasks)))
            write_log(r"**************************************************")

            # sort tasks by shot priority
            for t in tasks:
                t["priority"] = 0

                shot = gazu.shot.get_shot(t["entity_id"])
                if "data" in shot:
                    if "priority" in shot["data"]:
                        t["priority"] = shot["data"]["priority"]            

            for task_id in tasks:
                ue_import_task = gazu.task.get_task(task_id)

                # enable for production
                #if not ue_import_task["task_status_id"] == self.export["id"]:
                #    write_log("skipping task {} not available, task in use or in error".format(ue_import_task["id"]))
                #    continue

                shot = gazu.shot.get_shot(ue_import_task["entity"]["id"])
                episode = gazu.shot.get_episode(shot["episode_id"])
                output_files = gazu.files.get_last_output_files_for_entity(shot, task_type=self.shot_cache)
                if len(output_files) > 0:
                    gazu.task.start_task(ue_import_task)                    
                    if self.unreal_import(episode["name"].lower(), output_files, ue_import_task, self.wip, self.ue_import):
                        gazu.task.add_comment(ue_import_task["id"], self.wfa)
                        continue
                        #return True

                write_log("process::{} {} {} {} {} ({})".format(self.project_name, shot["episode_name"], shot["sequence_name"], shot["name"], self.export["name"], len(output_files)))    
                self.flush_output() 

        write_log("process::done")       

    def stop(self):
        self.running = False

if __name__ == "__main__":
    write_log("UEServer::start")
    #server = UEServer(project_name = "Wind in the Willows")

    ##server = UEServer(project_name = "Attack of the Killer Bunny S1")

    server = UEServer(project_name = "Wind in the Willows")
    server.start()
    write_log("UEServer::done")
