# -*- coding: utf-8 -*-
import os
import shutil
import argparse
import json
import zipfile

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.studio.openexr.swing_convert import SwingConvert

from wildchildanimation.gui.swing_utils import write_log, dir_count, zip_dir_contents
from wildchildanimation.unreal.swing_unreal_loader import SwingUE
from wildchildanimation.gui.background_workers import WorkingFileUploader

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal    
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSignal    
    qtMode = 1

import sys
import traceback
import time
import gazu
import subprocess

from datetime import datetime

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
class ProgressSignal(QtCore.QObject):
    progress = pyqtSignal(object)    

class RenderThread(QtCore.QRunnable):

    def __init__(self, editor_cmd, unreal_project, unreal_map, unreal_lvl, set_frame_range, frame_in, frame_out, shot_prefix, view_res_x, view_res_y, output_dir, unreal_preset, log):
        super(RenderThread, self).__init__()

        self.timer = QtCore.QTimer()
        self.proc = None        

        self.editor_cmd = editor_cmd
        self.unreal_project = unreal_project
        self.unreal_map = unreal_map
        self.unreal_lvl = unreal_lvl
        self.set_frame_range = set_frame_range
        self.frame_in = frame_in
        self.frame_out = frame_out
        self.shot_prefix = shot_prefix
        self.view_res_x = view_res_x
        self.view_res_y = view_res_y
        self.output_dir = output_dir
        self.unreal_preset = unreal_preset
        self.log = log
        self.running = True
        self.callback = ProgressSignal()

    def run(self):
        try:
            try:
                self.proc = subprocess.Popen([self.editor_cmd, self.unreal_project, self.unreal_map, "-game", "-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor", 
                    "-ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor", 
                    "-LevelSequence={}".format(self.unreal_lvl), 
                    "-SetFrames={}".format(self.set_frame_range),
                    "-FrameIn={}".format(self.frame_in), "-FrameOut={}".format(self.frame_out),
                    "-ShotPrefix={}".format(self.shot_prefix),
                    "-windowed", 
                    "-ResX={}".format(self.view_res_x), "-ResY={}".format(self.view_res_y), 
                    "-OutputDir={}".format(self.output_dir), "-RenderPreset={}".format(self.unreal_preset), "-unattended", "-log"], shell = False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
                
                self.callback.progress.emit("Rendering ... ")

                while True:
                    output = self.proc.stdout.readline()
                    try:
                        show_line = True                
                        log = output.decode('utf-8')

                        if log == '' and self.proc.poll() != None:
                            break
                        
                        else:
                            if SwingUE.SUPPRESS_LINES: 
                                for item in SwingUE.SUPPRESS_LINES:
                                    if item in log:
                                        suppress_count += 1
                                        show_line = False
                                        break

                            if show_line:
                                log = log.strip()
                                if log != '':
                                    self.log(log)
                                    self.callback.progress.emit(log)                                    
                    except:
                        print(traceback.format_exc())
                    # continue            
            except:
                traceback.print_exc(file=sys.stdout)
        finally:
            self.running = False            
        # done

class UERenderServer(QtCore.QObject):

    SUPPRESS_LINES = [
    ]    

    def __init__(self, config_file):
        super(UERenderServer, self).__init__()

        self.config_file = config_file

        config_json = json.load(open(config_file))

        self.server = config_json["server"]
        self.project_name = config_json["project"]
        self.user = config_json["user"]
        self.password = config_json["password"]
        self.shared_root = config_json["shared_root"]
        self.swing_settings = SwingSettings.get_instance()

        self.connected = False
        self.gazu_client = None
        self.running = False    
        self.log = []
        self.threadpool = QtCore.QThreadPool()

    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        gazu.set_host("{}/api".format(self.server))
        try:
            self.gazu_client = gazu.log_in(self.user, self.password)
            self.connected = True
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
            
            # check ue import
            self.breakout_task_type = gazu.task.get_task_type_by_name("Breakout")
            if not self.breakout_task_type:
                write_log("error: Task Type {} not found".format("Breakout"))
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

            write_log("connected to {} as {}".format(self.project_name, self.user))
        except:
            return False

        return True   
    
    def parse_sections(self, task):
        sections = []

        if "Shot" == task["entity_type"]["name"]:
            sections.append(task["episode"]["name"])
            sections.append(task["sequence"]["name"])
            sections.append(task["entity"]["name"])
            sections.append(task["task_type"]["name"])

        elif "Asset" == task["entity_type"]["name"]:
            sections.append(task["entity"]["name"])
            sections.append(task["task_type"]["name"])            
        else:
            sections.append(task["entity_type"]["name"])
            sections.append(task["entity"]["name"])        
            sections.append(task["task_type"]["name"])           

        return sections
    
    def describe_sections(self, task, sections):
        prefix = "_".join(sections).replace(" ", "_")
        if not task["project"]["code"] in prefix:
            prefix = (task["project"]["code"] + "_" + prefix)
        return prefix.strip().lower()        

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
        self.log = []

        ## set default frame range
        frame_in = 0
        frame_out = 10

        sections = self.parse_sections(render_task)        

        if "data" in render_task:
            entity_data = render_task["data"]

            if "frame_in" in entity_data:
                frame_in = int(entity_data["frame_in"])

            if "frame_out" in entity_data:
                frame_out = int(entity_data["frame_out"])

        else:
            if "nb_frames" in render_task["entity"]:
                frame_out = int(render_task["entity"]["nb_frames"]) - 1

        set_frame_range = (frame_in * frame_out) > 0
        task_data = render_task["data"]
        output_dir = task_data["render_output_dir"]
        output_dir = os.path.normpath(os.path.join(output_dir, "/".join(sections)))

        if not os.path.exists(output_dir):
            version = 1
        else:
            version = dir_count(output_dir)
            if version == 0:
                version = 1
        
        output_dir = os.path.join(output_dir, "v{}".format(version))

        os.makedirs(output_dir, mode=0o777, exist_ok = True)

        editor_cmd = self.swing_settings.bin_ue_editor()
        if editor_cmd.strip() == "":
            self.server_log("error: editor_cmd not set")
            return False

        unreal_project = self.swing_settings.ue_project_root()
        if unreal_project.strip() == "":
            self.server_log("error: unreal_project not set")
            return False

        unreal_map = task_data["unreal_map"]
        if unreal_map.strip() == "":
            self.server_log("error: unreal_map not set")
            return False

        unreal_lvl = task_data["unreal_level"]
        if unreal_lvl.strip() == "":
            self.server_log("error: unreal_level not set")
            return False

        unreal_preset = task_data["unreal_preset"]
        if unreal_preset.strip() == "":
            self.server_log("error: unreal_preset not set")
            return False

        shot_prefix = self.describe_sections(render_task, sections)

        self.server_log("Rendering {}".format("/".join(sections)))

        view_res_x = 1024
        view_res_y = 768

        time_start = datetime.now()

        ##Editor Commandline:
        ## UnrealEditor-Cmd.exe "E:\SubwaySequencer\SubwaySequencer.uproject" subwaySequencer_P -game 
        # -MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor 
        # -ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor 
        # -LevelSequence="/Game/Sequencer/SubwaySequencerMASTER.SubwaySequencerMASTER" 
        # -windowed -resx=1280 -resy=720 -log

        exec_cmd = ""
        exec_cmd += Fr"{editor_cmd} {unreal_project} {unreal_map} -game -MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor"
        exec_cmd += Fr" -ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor"
        
        exec_cmd += Fr" -LevelSequence={unreal_lvl}"

        exec_cmd += Fr" -SetFrames={set_frame_range}"               
        exec_cmd += Fr" -FrameIn={frame_in}"
        exec_cmd += Fr" -FrameOut={frame_out}"       

        exec_cmd += Fr" -ShotPrefix={shot_prefix}"       
        exec_cmd += Fr" -windowed"
        exec_cmd += Fr" -ResX={view_res_x} -ResY={view_res_y} "
        exec_cmd += Fr" -OutputDir={output_dir} " 
        exec_cmd += Fr" -RenderPreset={unreal_preset} "
        exec_cmd += Fr" -unattended -log"
        self.server_log(F"*** Popen: \n\n{exec_cmd}\n\n***")

        swing_render = RenderThread(editor_cmd, unreal_project, unreal_map, unreal_lvl, set_frame_range, frame_in, frame_out, shot_prefix, view_res_x, view_res_y, output_dir, unreal_preset, self.server_log)
        self.threadpool.start(swing_render)

        timeout = 60 # Max 60 mins
        counter = 0
        while swing_render.running:
            duration = time_end = datetime.now() - time_start

            if counter > timeout:
                self.server_log("**** exceeded render timeout {}: killing render".format(counter))
                swing_render.proc.kill()
                break

            self.server_log("render watchdog {}: still rendering ...".format(duration))
            counter += 1
            time.sleep(60)

        time_end = datetime.now()
        self.server_log("completed in {}".format(time_end - time_start))            

        log_out = os.path.join(os.path.dirname(output_dir), "logs", "ue_render.log")

        self.server_log("Writing log file {}".format(log_out))

        if not os.path.exists(os.path.dirname(log_out)):
            os.mkdir(os.path.dirname(log_out))

        with open(log_out, 'w') as f:
            try:
                for item in self.log:
                    f.write("%s\n" % item.strip())
            finally:
                f.close()    

        return output_dir     

    def flush_output(self):
        try:
            sys.stdout.write('')
            sys.stdout.flush() 
        except:
            pass

    def get_shot_task(self, shot, task_type_name, task_status = None):
        tasks = gazu.task.all_tasks_for_shot(shot)
        for t in tasks:
            if task_status:
                if t["task_type_name"] == task_type_name and t["task_status_name"] == task_status["name"]:
                    return t
            else:
                if t["task_type_name"] == task_type_name:
                    return t

        return False           

    def process(self):
        write_log("process::rendering started")

        ## ensure we are connected
        gazu.set_host("{}/api".format(self.server))
        self.gazu_client = gazu.log_in(self.user, self.password)        

        if not self.gazu_client:
            write_log(F"Error connecting to server: {self.server} as user {self.user}")
            return False

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
                    render_task = gazu.task.get_task(task["id"])

                    if not render_task["task_status_id"] == self.render_status["id"]:
                        write_log("process::skipping task {} - not in render status".format(render_task["name"]))
                        continue

                    gazu.task.add_comment(render_task, self.wip)                    

                    if len(render_task["persons"]) > 0:
                        artist_name = render_task["persons"][0]["full_name"]
                    else:
                        artist_name = "Show Admin"

                    sections = self.parse_sections(render_task)
                    caption = self.describe_sections(render_task, sections)

                    ## Submit to UnrealEditor-Cmd for CLI Rendering using SwingMoviePipelineRuntimeExecutor
                    ## Returns the folder name of the render output, or False if failed
                    render_folder = self.unreal_render(render_task)

                    if not render_folder:
                        write_log("process::render failed for {}".format(render_task["name"]))
                        gazu.task.add_comment(task = render_task, comment = F"Render failed: {caption} - Possible render timeout\nPlease check render logs", task_status = self.retake)                         
                        continue

                    if not os.path.exists(render_folder):
                        write_log("process::render folder not found {}".format(render_folder))
                        gazu.task.add_comment(task = render_task, comment = F"Render folder not found: {caption} - Render output files not found\nPlease check render logs", task_status = self.retake)                         
                        continue

                    ## Count number of output files to calculate version
                    output_files = gazu.files.all_output_files_for_entity(render_task["entity_id"], task_type=render_task["task_type_id"])

                    ## see if we can encode audio
                    audio_path = None

                    ## only do audio if working on shots
                    if "Shot" == render_task["entity_type"]["name"]:
                        breakout_task = self.get_shot_task(render_task["entity_id"], self.breakout_task_type["name"])
                        if breakout_task:
                            audio_breakout_files = gazu.files.get_working_files_for_task(breakout_task)
                            audio_breakout_files = sorted(audio_breakout_files, key=lambda x: x["updated_at"], reverse=True)     

                            if len(audio_breakout_files) > 1:
                                audio_file = audio_breakout_files[0]
                                if audio_file:
                                    audio_path = os.path.join(os.path.normpath(audio_file["path"].replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())), audio_file["name"])
                                    write_log("process::found audio file {}".format(audio_path))
                            #
                        # check for audio

                    media_file = os.path.normpath(os.path.join(render_folder, "..\\", F"{caption}_v{len(output_files)+1}.mp4"))
                    temp_dir = os.path.normpath(os.path.join(render_folder, "..\\", "temp"))

                    ## convert EXR images to png and proxy mp4
                    ## todo: check if not EXR's
                    convert = SwingConvert(media_file = media_file, source_dir = render_folder, temp_dir = temp_dir, caption = caption, artist=artist_name, album=self.project["name"], audio_path = audio_path)
                    media_file = convert.exr_to_png_mp4_convert()

                    ## zip and upload EXR's
                    count = None
                    target = "{}/{}".format(os.path.dirname(os.path.dirname(render_folder)), F"{caption}_v{len(output_files)+1}.zip")
                    try:
                        # remove old zip if exists
                        if os.path.exists(target):
                            os.remove(target)

                        self.server_log("zipping: {}".format(target))
                        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
                            try:
                                count = zip_dir_contents(render_folder, archive)
                            finally:
                                archive.close()  

                        self.server_log("zipped: {} files".format(count))
                    except:                                
                        traceback.print_exc(file=sys.stdout)
                        return False      
                    
                    edit_api = "{}/edit".format(self.server)                          

                    self.server_log("uploading render: {}".format(target))
                    worker = WorkingFileUploader(self, edit_api, render_task, target, caption, "Unreal Engine", comment=F"RenderPub: {caption}", mode = "render", task_status = self.wfa["id"], archive_name = target)                            
                    worker.run()                   

                    ## generate proxy preview
                    if os.path.exists(media_file):
                        self.server_log("uploading preview: {}".format(media_file))                        
                        comment = gazu.task.add_comment(render_task, self.wfa, "")
                        gazu.task.add_preview(render_task, comment, media_file, normalize_movie=False)                            

                    self.flush_output() 
                    self.server_log("render complete: {}".format(caption))                        

        write_log("process::rendering done")       

    def stop(self):
        self.running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Swing::UE Render Server - Settings"
    )

    parser.add_argument("-c", "--config", help="Config File", action="store")
    args = parser.parse_args()
    config_file = args.config

    if not os.path.exists(config_file):
        print("Config file not found: {}".format(config_file))
        sys.exit(1)

    write_log("UERenderServer::start")
    server = UERenderServer(config_file=config_file)
    server.start()
    write_log("UERenderServer::done")    
