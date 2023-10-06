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

from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
class SwingEncoder(QtCore.QObject):

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

            # check renders
            self.render = gazu.task.get_task_type_by_name("Renders")
            if not self.render:
                write_log("error: Task Type {} not found".format("Renders"))
                return False                   

            # check renders
            self.fx = gazu.task.get_task_type_by_name("Fx")
            if not self.fx:
                write_log("error: Task Type {} not found".format("Fx"))
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

            self.wfa = gazu.task.get_task_status_by_name("Waiting for Approval") 
            if not self.wfa:
                write_log("error: Task Status 'WFA' not found")
                return False                                                                                      

            self.export = gazu.task.get_task_status_by_name("Export") 
            if not self.export:
                write_log("error: Task Status 'Export' not found")
                return False  

            self.review = gazu.task.get_task_status_by_name("Review") 
            if not self.review:
                write_log("error: Task Status 'Review' not found")
                return False                                               

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

    def render_encode(self, task_list, task_type):
        self.log = []
        for task in task_list:
            task = gazu.task.get_task(task["id"])

            if not task["task_status_id"] == self.render_status["id"]:
                task_details = "{} episode {} shot {} {} status {}".format(self.project["name"], task["episode"]["name"], task["sequence"]["name"], task["entity"]["name"], task["task_status"]["name"])

                write_log("skipping {}".format(task_details))
                continue    

            shot = gazu.shot.get_shot(task["entity_id"])
            seq = gazu.entity.get_entity(shot["parent_id"])
            ep = gazu.entity.get_entity(seq["parent_id"])

            item_name = "{} {} {} {}".format(self.project["name"], ep["name"], seq["name"], shot["name"])
            
            #self.server_log("Render Encode: {} {} {} {}".format(self.project["name"], ep["name"], seq["name"], shot["name"]))
            output_files = gazu.files.get_last_output_files_for_entity(task["entity_id"], task_type=task_type)
            ##output_files = sorted(output_files, key=lambda d: time.strptime(d['updated_at'], r'%Y-%m-%dT%H:%M:%S'))            

            output_files = sorted(output_files, key=lambda d: d["name"], reverse=True)

            for f in output_files:
                artist = gazu.person.get_person(f["person_id"])
                print("{} {}".format(item_name, f["name"]), artist["full_name"])
                gazu.task.start_task(task)
                
                media_file = self.encode_and_upload(task, f, shot, seq, ep, artist)
                if media_file:
                    comment = gazu.task.add_comment(task["id"], self.wfa)
                    gazu.task.add_preview(task["id"], comment, media_file)
                    break
                    
                    # upload preview
                    # continue

    def encode_and_upload(self, task, render_archive, shot, seq, ep, artist):
        media_file = friendly_string("{}_{}_{}_{}".format(self.project["code"], ep["name"], seq["name"], shot["name"]))
        media_dir = os.path.join(self.ENCODE_DIR, media_file)

        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        source = render_archive["path"]
        if not source.endswith(render_archive["name"]):
            source = os.path.join(render_archive["path"], render_archive["name"])

        source = source.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())

        print("temp folder {} source archive {} ".format(media_dir, source))            

        if os.path.isfile(source):
            if extract_archive(SwingSettings.get_instance().bin_7z(), source, media_dir, extract_mode = "e"):
                media_file = friendly_string("{}_{}_{}_{}".format(self.project["code"], ep["name"], seq["name"], shot["name"]))
                media_file += ".mov"

                temp_dir = os.path.join(media_dir, "encode")

                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)                
                
                convert = SwingConvert(media_file, media_dir, temp_dir, caption = "{}_{}_{}_{}".format(self.project["code"], ep["name"], seq["name"], shot["name"]), artist=artist["full_name"], album=self.project["name"])
                media_file = convert.exr_to_png_mp4_convert()

                return media_file


    def flush_output(self):
        try:
            sys.stdout.write('')
            sys.stdout.flush() 
        except:
            pass

    def process(self):
        write_log("process::start")

        tasks = gazu.task.all_tasks_for_task_status(self.project, self.render, self.render_status)
        #
        # check for any render tasks
        if len(tasks) > 0:
            write_log("process::checking {} for {} shots".format(self.render["name"].lower(), len(tasks)))
            write_log(r"**************************************************")
            self.render_encode(tasks, self.render)

        tasks = gazu.task.all_tasks_for_task_status(self.project, self.fx, self.render_status)
        #
        # check for any fx tasks
        if len(tasks) > 0:
            write_log("process::checking {} for {} shots".format(self.fx["name"].lower(), len(tasks)))
            write_log(r"**************************************************")
            self.render_encode(tasks, self.fx)            

        write_log("process::done")       

    def stop(self):
        self.running = False

if __name__ == "__main__":
    write_log("SwingEncoder::start")
    #server = SwingEncoder(project_name = "Wind in the Willows")

    ##server = SwingEncoder(project_name = "Attack of the Killer Bunny S1")

    server = SwingEncoder(project_name = "Wind in the Willows")
    server.start()
    write_log("SwingEncoder::done")
