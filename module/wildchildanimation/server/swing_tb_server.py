# -*- coding: utf-8 -*-

# Scan Kitsu for Tasks set to Render
# For each task, check for a working file (priority Anim-Final > Anim-Animation > Anim-Block)
# First project archive found, download and extract local
# Open Toon Boom scene file, set export settings to Scene = Rec.709 2.4, all other nodes set to 'Use Scene Settings'
# Export Scene to PNG
# Compress and Upload PNG's to Kitsu
# 
# Last updated: 2023/09/07
#
import os
import json
import shutil
import argparse
import subprocess
import zipfile
import re

from glob import glob

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import extract_archive
from wildchildanimation.gui.swing_utils import write_log
from wildchildanimation.gui.swing_utils import zip_dir_contents
from wildchildanimation.unreal.swing_unreal_loader import SwingUE
from wildchildanimation.gui.background_workers import WorkingFileUploader

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
class TBServer(QtCore.QObject):

    JS_COLOUR_SPACE = "Z:/env/wca/swing/swing-main/module/wildchildanimation/toonboom/scripts/js/update_colour_space.js"
    JS_COLOUR_SPACE_METHOD = "set_write_node"

    def __init__(self, server, project, user, password, shared_root, toonboom):
        self.swing_settings = SwingSettings.get_instance()

        self.server = server
        self.project_name = project
        self.user = user
        self.password = password
        self.shared_root = shared_root
        self.toonboom = toonboom

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
            self.project = gazu.project.get_project_by_name(self.project_name)
            self.swing_root = self.swing_settings.swing_root()

            if not self.project:
                write_log("error: Project {} not found".format(self.project_name))
                return False            

            #######################################################################################
            # TASK TYPES
            #

            # check renders task
            self.breakout_task_type = gazu.task.get_task_type_by_name("Breakout")
            if not self.breakout_task_type:
                write_log("error: Task Type {} not found".format("Breakout"))
                return False   

            self.render_task = gazu.task.get_task_type_by_name("Renders")
            if not self.render_task:
                write_log("error: Task Type {} not found".format("Renders"))
                return False   
            
            # check a3 - Anim-Final
            self.anim_final = gazu.task.get_task_type_by_name("Anim-Final")
            if not self.anim_final:
                write_log("error: Task Type {} not found".format("Anim-Final"))
                return False  

            # check a2 - Anim-Animation
            self.anim_animation = gazu.task.get_task_type_by_name("Anim-Animation")
            if not self.anim_animation:
                write_log("error: Task Type {} not found".format("Anim-Animation"))
                return False  

            # check a1 - Anim-Block
            self.anim_block = gazu.task.get_task_type_by_name("Anim-Block")
            if not self.anim_block:
                write_log("error: Task Type {} not found".format("Anim-Block"))
                return False             

            #######################################################################################
            # STATUS TYPES
            #

            # final
            self.final = gazu.task.get_task_status_by_name("Final (Client Approved)") 
            if not self.final:
                write_log("error: Task Status 'Final not found")
                return False   

            # wip 
            self.wip = gazu.task.get_task_status_by_name("Work in Progress") 
            if not self.wip:
                write_log("error: Task Status 'WIP' not found")
                return False                   

            # wfa
            self.wfa = gazu.task.get_task_status_by_name("Waiting for Approval") 
            if not self.wfa:
                write_log("error: Task Status 'WFA' not found")
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

            # sleep 10 mins
            time.sleep(10 * 60)

    def remove_dir(self, dir):
        write_log("removing dir {}".format(dir))
        shutil.rmtree(dir)            

    def server_log(self, text):
        log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
        log += " {}".format(text)

        self.log.append(log.strip())          
        print(log)       

    def flush_output(self):
        try:
            sys.stdout.write('')
            sys.stdout.flush() 
        except:
            pass

    def process_task(self, episode_name, working_files, render_task, completed_status, task_type, shot_task):
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

            if wf["name"].lower().endswith(".zip") or wf["name"].lower().endswith("7z"):
                working_file_path = wf["path"]
                working_file_path = os.path.normpath(working_file_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))    

                if not wf["name"] in working_file_path:
                    wf = os.path.join(working_file_path, wf["name"])

                project_path = os.path.normpath(wf.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))

                self.server_log("Processing {}".format(project_path))

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

                export_dir = os.path.join(os.path.dirname(working_path), "export")                    
                if os.path.exists(export_dir):
                    try:
                        os.remove(export_dir)    
                        self.server_log("removed old export_dir dir: {}".format(export_dir))
                    except:
                        self.server_log("error removing old export_dir dir: {}".format(export_dir))                        
                        print(traceback.format_exc())   
                else:
                    os.makedirs(export_dir)                                           

                ## Export Zip to local working folder 
                extract_archive(SwingSettings.get_instance().bin_7z(), project_path, export_dir)

                # scan project for TB project files, order by date, get newest one
                file_list = []
                for item in glob("{}/**/*.xstage".format(export_dir), recursive=True):
                    file_info = {
                        "file": item,
                        "modified": os.path.getmtime(item)
                    }
                    file_list.append(file_info)

                if len(file_list) == 0:
                    gazu.task.add_comment(render_task, self.review, "Error: Project Files for {} not found, searching previous task".format(task_type["name"]))
                    write_log("error: no TB project files found in {}".format(export_dir))
                    return False

                if len(file_list) > 1:
                    write_log("Multiple TB project files found: {}".format(len(file_list)))

                file_list = sorted(file_list, key=lambda d: d['modified'], reverse=True)            

                for item in file_list:
                    self.process_scene(item["file"], render_task, completed_status, shot_task)
                    break # only process the first file

                break # only process the first file
        return True
    
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

    # Function rename file to match regular expression %04d
    def rename_png_files(self, export_dir):
        for filename in os.listdir(export_dir):
            src, ext = os.path.splitext(filename)
            src = src.split("_")
            target = F"{src[0]}_{src[1]}_{src[2]}.{src[3]}{ext}"

            src = os.path.join(export_dir, filename)
            target = os.path.join(export_dir, target)

            os.rename(src, target)
            print("{} -> {}".format(src, target))
        return True     
    
    def encode_export(self, export_dir, render_task, media_file, shot_task):
        ffmpeg_cmd = self.swing_settings.bin_ffmpeg()
        frame_rate = self.project["fps"]

        shot_name = self.extract_numbers(render_task["entity"]["name"])
        sequence_name = self.extract_numbers(render_task["sequence"]["name"])
        episode_name = self.extract_numbers(render_task["episode"]["name"].split("_")[-1])
        project_code = render_task["project"]["code"]   

        node_name = F"{project_code}{episode_name}_{sequence_name}_{shot_name}"   

        breakout_task = self.get_shot_task(shot_task["entity_id"], self.breakout_task_type["name"])

        audio_breakout_files = gazu.files.get_working_files_for_task(breakout_task)
        audio_breakout_files = sorted(audio_breakout_files, key=lambda x: x["updated_at"], reverse=True)     

        shot_task = gazu.task.get_task(shot_task["id"])   

        title = F"{project_code}{episode_name}_{sequence_name}_{shot_name} - {shot_task['task_type']['name']}" 
        artist = None
        for person in shot_task["persons"]:
            if person["last_name"] != "Admin":
                artist = F"{person['first_name']} {person['last_name']}"
                break

        audio_path = None
        if len(audio_breakout_files) >= 1:
            audio_file = audio_breakout_files[0]
            if audio_file:
                audio_path = os.path.join(os.path.normpath(audio_file["path"].replace("/mnt/content/productions", SwingSettings.get_instance().shared_root())), audio_file["name"])

        # self.rename_png_files(export_dir)
        ffmpeg_cmd += r' -y -framerate {0} -i "{1}" '.format(frame_rate, os.path.join(export_dir, F'{node_name}_%04d.png'))        

        if audio_path:
            ffmpeg_cmd += f'-i "{audio_path}" -c:v copy -c:a aac'

        filters = []
        text_graph = ''

        if artist:
            title = "{}: {}".format(title, artist).upper()

        filters.append(r"drawtext=font=Consolas: fontsize=24: fontcolor=white: x=(w-text_w)/2: y=20: text='{}' ".format(title.strip(), 24))

        # Timecode Burn-In
        filters.append(r"drawtext=font=Consolas: fontsize=24: fontcolor=white: x=5: y=20: timecode='00\:00\:00\:00': r={}: ".format(frame_rate))
        filters.append(r"drawtext=font=Consolas: fontsize=24: fontcolor=white: x=(w-text_w)-5: y=20: start_number=1: text='%{frame_num}' ")

        for i in range(len(filters)):
            text_graph += filters[i]
            if i < len(filters) - 1:
                text_graph += ', '

        if len(text_graph) > 0:
            ffmpeg_cmd += r' -vf "{}"'.format(text_graph)

        ffmpeg_cmd += r' -c:v libx264 '

        if audio_path:
            ffmpeg_cmd += r' -filter_complex "[1:0] apad" -shortest' 

        ## ffmpeg_cmd += " -vf scale=1920:1080 "     
        ffmpeg_cmd += r' "{0}"'.format(media_file)   

        write_log("encoding: {}".format(ffmpeg_cmd))
        write_log("***************************************************************************************************")

        proc = subprocess.Popen(ffmpeg_cmd, shell = False, stdout=subprocess.PIPE)
        while True:
            #output = proc.stdout.read(1)
            output = proc.stdout.readline()
            try:
                log = output.decode('utf-8')
                if log == '' and proc.poll() != None:
                    break
                else:
                    print(log)
            except:
                write_log("Byte Code Error: Ignoring")
                print(traceback.format_exc())
            # continue    
            # 
        self.server_log("--------------------------------------------------------------------------------")#     
        return media_file          

    
    def process_scene(self, scene_file, render_task, completed_status, shot_task):
        # Update Colour Space in TB Scene
        write_log("processing::TB project dir {}".format(os.path.dirname(scene_file)))
        write_log("processing::TB scene file {}".format(os.path.basename(scene_file)))

        time_start = datetime.now()  

        batch = "-batch"
        debug = "-debug"
        compile = "-compile"

        proc = subprocess.Popen([self.toonboom, scene_file, batch, debug, compile, TBServer.JS_COLOUR_SPACE], shell = False, stdout=subprocess.PIPE)
        while True:
            #output = proc.stdout.read(1)
            output = proc.stdout.readline()
            try:
                show_line = True                
                log = output.decode('utf-8')
                if log == '' and proc.poll() != None:
                    break
                else:
                    if SwingUE.SUPPRESS_LINES: 
                        for item in SwingUE.SUPPRESS_LINES:
                            if item in log:
                                suppress_count += 1
                                show_line = False
                                break

                    if show_line:
                        # sys.stdout.write(log)
                        log = log.strip()
                        if log != '':
                            self.server_log(log)
            except:
                print(traceback.format_exc())
            # continue  

        export_name = self.render_scene(scene_file, render_task)
        if not export_name:
            gazu.task.add_comment(render_task, self.review, "Error: Could not render out scene: {}".format(scene_file))                            
            self.server_log("error **********************************: renders not found: {}".format(export_dir))
            return False        
        
        output_files = gazu.files.all_output_files_for_entity(render_task["entity_id"], task_type=render_task["task_type_id"])

        export_dir = os.path.join(os.path.dirname(scene_file), export_name)

        if not os.path.exists(export_dir):
            self.server_log("error: *********************************: export dir not found: {}".format(export_dir))            
            return False
        
        count = None
        target = "{}/{}".format(os.path.dirname(os.path.dirname(scene_file)), F"{export_name}_v{len(output_files)+1}.zip")
        try:
            # remove old zip if exists
            if os.path.exists(target):
                os.remove(target)

            self.server_log("zipping: {}".format(target))
            with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
                try:
                    count = zip_dir_contents(export_dir, archive)
                finally:
                    archive.close()  

        except:                                
            traceback.print_exc(file=sys.stdout)
            return False 
        self.flush_output()

        edit_api = "{}/edit".format(self.server)  

        self.server_log("uploading: {}".format(target))
        worker = WorkingFileUploader(self, edit_api, render_task, target, export_name, "Toon Boom", comment=F"RenderPub: {os.path.basename(scene_file)}", mode = "render", task_status = completed_status["id"], archive_name = target)                            
        worker.run()

        media_file = "{}/{}".format(os.path.dirname(os.path.dirname(scene_file)), F"{export_name}_v{len(output_files)+1}.mp4")

        if count > 0:
            preview = self.encode_export(export_dir, render_task, media_file, shot_task)
            if preview:
                comment = gazu.task.add_comment(render_task, self.wfa, "Render Preview: {}".format(os.path.basename(scene_file)))
                gazu.task.add_preview(render_task, comment, media_file, normalize_movie=False)

        time_end = datetime.now()
        self.server_log("zip and uploaded completed in {}".format(time_end - time_start))
        self.server_log("--------------------------------------------------------------------------------")

        self.flush_output()   
        return True

    def extract_numbers(self, input_string):
        numbers = re.findall(r'\d+', input_string)

        # Join the extracted numbers into a single string
        return ''.join(numbers).zfill(3)     
    
    # scan all nodes in TB project, return first WRITE_NODE
    #
    def get_write_node(self, node_list):
        for n in node_list:
            if n.type == "WRITE":
                return n
        return None

    def render_scene(self, scene_file, render_task):
        HARMONY_INSTALL = os.path.dirname(self.toonboom)
        HARMONY_WIN64_LIB = rF"{HARMONY_INSTALL}/python-packages"

        exported_path = None

        shot_name = self.extract_numbers(render_task["entity"]["name"])
        sequence_name = self.extract_numbers(render_task["sequence"]["name"])
        episode_name = self.extract_numbers(render_task["episode"]["name"].split("_")[-1])
        project_code = render_task["project"]["code"]

        if sys.platform == "win32":
            write_log("Loading Windows Path: {}".format(HARMONY_WIN64_LIB))
            HARMONY_PATH = HARMONY_WIN64_LIB
        #HARMONY_PATH = 

        #Extend the environment's path, in order to find the installed Harmony Python module
        if not HARMONY_PATH in sys.path: sys.path.append(HARMONY_PATH)
        from ToonBoom import harmony #Import the Harmony Module        

        harmony.open_project(scene_file)    
        try:
            sess = harmony.session()                                     #Get access to the Harmony session, this class.

            proj = sess.project                                          #Get the active session's currently loaded project.
            render_handler = proj.create_render_handler()                #The new render handler that has been generated; will not have any changes from other handlers.
            render_handler.blocking = True                               #This handler will block the main application. Optional.
            scn = proj.scene

            node = self.get_write_node(scn.nodes)
            #node_split = os.path.basename(scene_file).split("_")
            #node_name = "Top/{}_{}_{}".format(node_split[0], node_split[1], node_split[2])
            node_name = F"{project_code}{episode_name}_{sequence_name}_{shot_name}"

            ## override for re-use assets
            if node_name == "tg000_000_000":
                node_name = F'{render_task["episode"]["name"].lower()}'

            if not node:
                gazu.task.add_comment(render_task, self.review, "Error: Write Node not found in TB scene: {}".format(scene_file))                
                write_log("error ********************************** write node not found")
                return False
            else:
                write_log("Found Node: {}".format(node_name))

            write_log("Rendering: {}".format(node))
            if node:
                drawing_name = r"{}_export/{}_".format(node_name, node_name)

                set_drawing_name = False
                set_export_to_movie = False
                set_color_space = False

                for attribute in node.attributes:           
                    try:
                        # Get available attributes on the node.
                        if attribute.keyword == "DRAWING_NAME":
                            attribute.set_text_value(0, drawing_name)
                            set_drawing_name = True
                            write_log("setting node {} DRAWING_NAME: {}".format(node, drawing_name))
                            continue

                        if attribute.keyword == "EXPORT_TO_MOVIE":                            
                            attribute.set_value(0, "false")
                            set_export_to_movie = True
                            write_log("setting node {} EXPORT_TO_MOVIE {}".format(node, "False"))                           
                            continue

                        if attribute.keyword == "COLOR_SPACE":
                            attribute.set_text_value(0, "Rec.709 2.4")
                            set_color_space = True
                            write_log("setting node {} COLOR_SPACE: {}".format(node, "Rec.709 2.4"))                                                        
                            continue

                    except:
                        write_log("error ********************************** : could not set write node settings")
                        print(traceback.format_exc())                        
                        return False
                    
                if not set_drawing_name and set_color_space and set_export_to_movie:
                    write_log("error ********************************** : could not set write node settings, please check scene {}".format(scene_file))
                    return False
                    
                render_handler.node_add(node)                            #The render handler will render any nodes added to it.
                render_handler.render()                                  #In the case of write nodes, the write node's parameters will define the settings of the exported frame.
                exported_path = r"{}{}_{}_{}_export".format(project_code, episode_name, sequence_name, shot_name)

            write_log("Render completed")   
        finally:
            harmony.close_project()
        return exported_path


    def process(self):
        write_log("process::start")

        gazu.set_host("{}/api".format(self.server))
        gazu.log_in(self.user, password)        

        tasks = gazu.task.all_tasks_for_task_status(self.project, self.render_task, self.render_status)
        #
        # check for any shot cache tasks
        if len(tasks) > 0:
            write_log("process::checking {} for {} shots".format(self.render_task["name"].lower(), len(tasks)))
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
                render_export_task = gazu.task.get_task(task_id)

                ## prio some episodes
                ##if render_export_task["episode"]["name"] != "tg_2d_ep311":
                ##    continue

                if not render_export_task["task_status_id"] == self.render_status["id"]:
                    task_details = "{} episode {} shot {} {} status {}".format(self.project["name"], render_export_task["episode"]["name"], render_export_task["sequence"]["name"], render_export_task["entity"]["name"], render_export_task["task_status"]["name"])
                    write_log("skipping {}".format(task_details))                    
                    continue

                shot = gazu.shot.get_shot(render_export_task["entity"]["id"])
                episode = gazu.shot.get_episode(shot["episode_id"])

                episode_details = episode["name"].split("_")
                if len(episode_details) == 2:
                    episode_name = "{}_".format(episode_details[1].lower())
                elif len(episode_details) == 3:
                    episode_name = "{}_".format(episode["name"].lower())
                elif len(episode_details) == 4:
                    episode_name = episode["name"] ## override for re-use episodes
                else:
                    write_log("Error: Unknown episode name convention: {}".format(episode["name"]))

                if not episode_name.startswith(self.project["code"]):
                    episode_name = "{}_{}".format(self.project["code"], episode_name)

                task_type = self.anim_final
                shot_task = gazu.task.get_task_by_entity(shot, task_type)

                project_files = gazu.files.get_last_working_files(shot_task)
                if len(project_files) > 0:
                    gazu.task.add_comment(render_export_task, self.wip)
                    if self.process_task(episode_name, project_files, render_export_task, self.wfa, task_type, shot_task):
                        continue
                        # return True

                task_type = self.anim_animation
                shot_task = gazu.task.get_task_by_entity(shot, task_type)

                project_files = gazu.files.get_last_working_files(shot_task)
                if len(project_files) > 0:
                    gazu.task.add_comment(render_export_task, self.wip)
                    if self.process_task(episode_name, project_files, render_export_task, self.wfa, task_type, shot_task):
                        gazu.task.add_comment(render_export_task, self.review, "Warning: Anim-Animation scene found, please check Anim-Final files")
                        continue
                        #return True

                task_type = self.anim_block
                shot_task = gazu.task.get_task_by_entity(shot, task_type)

                project_files = gazu.files.get_last_working_files(shot_task)
                if len(project_files) > 0:
                    gazu.task.add_comment(render_export_task, self.wip)
                    if self.process_task(episode_name, project_files, render_export_task, self.wfa, task_type, shot_task):
                        gazu.task.add_comment(render_export_task, self.review, "Warning: Anim-Block scene found, please check Anim-Final files")
                        continue
                        #return True

                write_log("process::{} {} {} {} {} ({})".format(self.project_name, shot["episode_name"], shot["sequence_name"], shot["name"], self.render_status["name"], len(project_files)))    
                self.flush_output() 

        write_log("process::done")    

    def stop(self):
        self.running = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Swing::TB Service - Settings"
    )

    parser.add_argument("-c", "--config", help="Config File", action="store")
    args = parser.parse_args()
    config_file = args.config

    if not os.path.exists(config_file):
        print("Config file not found: {}".format(config_file))
        sys.exit(1)

    # Read Setings override from supplied config file
    config_json = json.load(open(config_file))

    server = config_json["server"]
    project = config_json["project"]
    user = config_json["user"]
    password = config_json["password"]
    shared_root = config_json["shared_root"]
    toonboom = config_json["toonboom"]

    write_log("TBServer::start")
    server = TBServer(server = server, project = project, user = user, password = password, shared_root = shared_root, toonboom = toonboom)
    server.start()
    write_log("TBServer::done")
