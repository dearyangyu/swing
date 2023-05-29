# -*- coding: utf-8 -*-
import os
import shutil

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import extract_archive

from wildchildanimation.gui.swing_utils import write_log, dir_count
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
import subprocess

from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
class RenderServer(QtCore.QObject):

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

            #######################################################################################
            # TASK TYPES
            #                    
            self.lighting_task_type = gazu.task.get_task_type_by_name("Li")
            if not self.lighting_task_type:
                write_log("error: Task Type {} not found".format("Li"))
                return False   

            # check ue import
            self.look_dev_task_type = gazu.task.get_task_type_by_name("Ld")
            if not self.look_dev_task_type:
                write_log("error: Task Type {} not found".format("Ld"))
                return False             

            #######################################################################################
            # STATUS TYPES
            #

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

            # retake
            self.retake = gazu.task.get_task_status_by_name("Retake") 
            if not self.retake:
                write_log("error: Task Status 'Retake' not found")
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

    def unreal_render(self, render_task):
        SUPPRESS_LINES = True

        sections = []

        if "Shot" == render_task["entity_type"]["name"]:
            sections.append(render_task["task_type"]["name"])
            sections.append(render_task["episode"]["name"])
            sections.append(render_task["sequence"]["name"])
            sections.append(render_task["entity"]["name"])

        elif "Asset" == render_task["entity_type"]["name"]:
            sections.append(render_task["task_type"]["name"])
            sections.append(render_task["entity"]["name"])
        else:
            sections.append(render_task["task_type"]["name"])
            sections.append(render_task["entity_type"]["name"])
            sections.append(render_task["entity"]["name"])        

        self.log = []
        self.server_log("Rendering {}".format("/".join(sections)))

        task_data = render_task["data"]

        output_dir = task_data["render_output_dir"]
        output_dir = os.path.normpath(os.path.join(output_dir, "/".join(sections)))

        if not os.path.exists(output_dir):
            version = 1
        else:
            version = dir_count(output_dir)
        
        output_dir = os.path.join(output_dir, "v{}".format(version))

        os.makedirs(output_dir, mode=0o777, exist_ok = True)

        editor_cmd = self.swing_settings.bin_ue_editor()
        unreal_project = self.swing_settings.ue_project_root()

        unreal_map = task_data["unreal_map"]
        unreal_lvl = task_data["unreal_level"]
        unreal_preset = task_data["unreal_preset"]

        proc = subprocess.Popen([editor_cmd, unreal_project, unreal_map, "-game", "-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor",
            "-ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor", 
            '-LevelSequence="{}"'.format(unreal_lvl),
            "-windowed", "-ResX=1920", "-ResY=1080",
            "-OutputDir={}".format(output_dir),
            "-log"
        ], shell = False, stdout=subprocess.PIPE)
        
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
                        for item in RenderServer.SUPPRESS_LINES:
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


        # "C:\\Program Files\\Epic Games\\UE_5.2\\Engine\\Binaries\\Win64\\UnrealEditor-Cmd.exe" 
        #  "C:\Productions\sdmp\ue\sdmp_build_5_1_001\sdmp_build_5_1_001.uproject" 
        #   lv_turntable_default 
        #   -game -MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor 
        #   -ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor 
        #   -LevelSequence="/Game/Turntable/ls_turntable_HeroPupA" 
        #   -windowed -ResX=1920 -ResY=1080 -OutputDir=C:/Renders/SDMP/HeroPupA -log        

        return False
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
        # UE RENDER
        #
        task_types = [ self.look_dev_task_type, self.lighting_task_type ]

        for task_type in task_types:
            tasks = gazu.task.all_tasks_for_task_status(project = self.project, task_type = task_type, task_status = self.render_status)
            if len(tasks) > 0:
                write_log("process::checking {} for {} renders".format(task_type["name"], len(tasks)))
                write_log(r"**************************************************")

                for task in tasks:
                    if self.unreal_render(gazu.task.get_task(task["id"])):
                        gazu.task.add_comment(task["id"], self.wfa)
                    self.flush_output() 

        write_log("process::done")       

    def stop(self):
        self.running = False

if __name__ == "__main__":
    write_log("RenderServer::start")

    server = RenderServer(project_name = "WCA")
    server.start()
    write_log("RenderServer::done")
