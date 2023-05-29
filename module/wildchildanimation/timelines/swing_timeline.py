# -*- coding: utf-8 -*-
# Management GUI for Editorial
#
# - Scan XML to update shots and frame ranges in Kitsu
# - Cut video file into shots
# - Export separate audio files for shots
# 

import traceback
import sys
import os
import gazu
import datetime
import opentimelineio as otio
import io
import re

import xml.etree.ElementTree as ET

# Qt High DPI 
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2.QtCore import Signal as pyqtSignal    
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtCore import pyqtSignal    
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.background_workers import WorkingFileUploader
from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.timelines.swing_timeline_dialog  import Ui_SwingTimelineDialog

from wildchildanimation.gui.swing_tables import CheckBoxDelegate, human_size

import gspread

'''
    Swing Timelines class
    ################################################################################
'''

class CommandRunnerSignal(QtCore.QObject):
    signal = pyqtSignal(object)    

class CommandRunner(QtCore.QRunnable):

    def __init__(self, label, command_line):
        super(CommandRunner, self).__init__(self, None)
        self.label = label
        self.command_line = command_line
        self.callback = CommandRunnerSignal()        

    def run(self):
        time_start = datetime.now()

        proc = subprocess.Popen(args = self.command_line, shell = False, stdout=subprocess.PIPE)
        while True:
            output = proc.stdout.read()
            # output = proc.stdout.read(1)
            try:
                log = output.decode('utf-8')
                if log == '' and proc.poll() != None:
                    break
                else:
                    # sys.stdout.write(log)
                    log = log.strip()
                    if log != '':
                        self.callback.signal.emit(log)

                    sys.stdout.flush()
            except:
                print(traceback.format_exc())
            # continue

        time_end = datetime.now()
        try:
            self.callback.signal.emit("{} completed in {}".format(self.label, (time_end - time_start)))
        except:
            print(traceback.format_exc())     

class SwingTimelineDialog(QtWidgets.QDialog, Ui_SwingTimelineDialog):

    ALLOWED_MOVIE_EXTENSION = [
        ".avi",
        ".m4v",
        ".mkv",
        ".mov",
        ".mp4",
        ".webm",
        ".wmv",
    ]    

    PLAYLIST_FILE = "swing-playlist.json"

    working_dir = None
    
    def __init__(self, parent = None):
        super(SwingTimelineDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)
        self.read_settings()        

        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.toolButtonSelectEDLFile.clicked.connect(self.select_edl_file)
        self.toolButtonSelectSource.clicked.connect(self.select_source)

        set_button_icon(self.pushButtonSelectAll, "../resources/fa-free/solid/plus.svg")
        self.pushButtonSelectAll.clicked.connect(self.select_all)

        self.pushButtonSelectNone.clicked.connect(self.select_none)
        set_button_icon(self.pushButtonSelectNone, "../resources/fa-free/solid/minus.svg")

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)

        self.pushButtonUpdateKitsu.clicked.connect(self.update_kitsu)
        self.pushButtonUpdateTrackingSheet.clicked.connect(self.update_tracking_sheet)

        self.pushButtonExtractVideo.clicked.connect(self.extract_video)
        self.pushButtonExtractAudio.clicked.connect(self.extract_audio)
        self.pushButtonExtractImages.clicked.connect(self.extract_images)

        self.pushButtonRunAll.clicked.connect(self.run_all)

        #self.tableView.doubleClicked.connect(self.file_table_double_click)
        #self.checkBoxSequences.clicked.connect(self.update_tree)

        #self.lineEditSearch.textChanged.connect(self.search)
        self._createContextMenu()

        self.pushButtonScanEDL.clicked.connect(self.scan_edl)
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(self.spinBoxThreadCount.value())
        self.busy_count = 0

        self.spinBoxThreadCount.valueChanged.connect(self.thread_count_changed)

        self.load_project_data()

    def enable_controls(self, is_enabled):
        self.pushButtonCancel.setEnabled(is_enabled)
        self.pushButtonRunAll.setEnabled(is_enabled)
                
        self.pushButtonExtractVideo.setEnabled(is_enabled)
        self.pushButtonExtractAudio.setEnabled(is_enabled)
        self.pushButtonExtractImages.setEnabled(is_enabled)

        self.pushButtonUpdateKitsu.setEnabled(is_enabled)

        self.pushButtonSelectNone.setEnabled(is_enabled)
        self.pushButtonSelectAll.setEnabled(is_enabled)
        self.spinBoxThreadCount.setEnabled(is_enabled)
        self.pushButtonScanEDL.setEnabled(is_enabled)

        self.lineEditEDLFile.setEnabled(is_enabled)
        self.lineEditSource.setEnabled(is_enabled)
        self.toolButtonSelectEDLFile.setEnabled(is_enabled)
        self.toolButtonSelectSource.setEnabled(is_enabled)

        self.comboBoxEpisode.setEnabled(is_enabled)
        self.comboBoxProject.setEnabled(is_enabled)

        self.checkBoxUploadMedia.setEnabled(is_enabled)
        self.pushButtonUpdateTrackingSheet.setEnabled(is_enabled)

    def thread_count_changed(self):
        self.threadpool.setMaxThreadCount(self.spinBoxThreadCount.value())

    def load_project_data(self):
        connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password())

        self.projects = gazu.project.all_open_projects()

        self.comboBoxProject.blockSignals(True)
        self.comboBoxProject.clear()

        for item in self.projects:
            self.comboBoxProject.addItem(item["name"], userData = item)
        self.comboBoxProject.blockSignals(False)

        if len(self.projects) > 0:
            self.project_changed(self.comboBoxProject.currentIndex())     

        self.episodes = None

    def project_changed(self, index):
        project = self.comboBoxProject.itemData(index)

        if not project:
            write_log("Error: No open project could be loaded, please check settings")
            write_log("Server: {}".format(SwingSettings.get_instance().swing_server()))
            write_log("Artist: {}".format(SwingSettings.get_instance().swing_user()))

            return False
        
        self.episodes = gazu.shot.all_episodes_for_project(project)
        
        self.comboBoxEpisode.clear()
        self.comboBoxEpisode.blockSignals(True)

        # Add Main Pack Episode placeholder for Asset Tasks
        for item in self.episodes:
            self.comboBoxEpisode.addItem(item["name"], userData = item)
            
        self.comboBoxEpisode.blockSignals(False)   

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings("WCA", self.__class__.__name__)
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("edl_file", self.lineEditEDLFile.text())
        self.settings.setValue("source_file", self.lineEditSource.text())
        self.settings.setValue("thread_count", self.spinBoxThreadCount.value())

        if self.checkBoxUploadMedia.isChecked():
            self.settings.setValue("upload_media", "True")
        else:
            self.settings.setValue("upload_media", "False")

        #self.settings.setValue("extract_zip", self.checkBoxExtractZip.isChecked())
        #self.settings.setValue("software", self.comboBoxSoftware.currentText())
        #self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        #self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()
        self.settings.sync()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings("WCA", self.__class__.__name__)
        self.settings.beginGroup(self.__class__.__name__)
        
        self.project_root = self.settings.value("projects_root", os.path.expanduser("~"))
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.lineEditEDLFile.setText(self.settings.value("edl_file", ""))
        self.lineEditSource.setText(self.settings.value("source_file", ""))
        self.spinBoxThreadCount.setValue(self.settings.value("thread_count", 3))
        self.checkBoxUploadMedia.setChecked(self.settings.value("upload_media", "True") == "True")

        #self.checkBoxSequences.setChecked(self.is_setting_selected(self.settings, "show_sequences"))
        #self.checkBoxExtractZip.setChecked(self.is_setting_selected(self.settings, "extract_zip"))        
        ##self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))
        self.settings.endGroup()        

    def is_setting_selected(self, settings, value):
        val = settings.value(value, True)
        return val == 'true'        

    def search(self):
        text = self.lineEditSearch.text()
        if len(text) and self.proxy:
            self.proxy.setFilterFixedString(text)

    def close_dialog(self):
        self.write_settings()
        self.close()        

    def select_all(self):
        self.model.select_all()
        self.tableView.update()        

    def select_none(self):
        self.model.select_none()
        self.tableView.update()     

    def _loadActionIcon(self,  action_text, resource_string):
        action = QtWidgets.QAction(self)
        action.setText(action_text)

        resource_file = resource_path(resource_string)
        if os.path.exists(resource_file):
            pm = QtGui.QPixmap(resource_file)
            pm = pm.scaledToHeight(14)

            icon = QtGui.QIcon(pm)            
            action.setIcon(icon)

        return action           

    def file_table_double_click(self, index):
        self.filesOpenDirectory()

    def _createContextMenu(self):
        # File actions
        self.actionViewKitsu = self._loadActionIcon("&View in Kitsu", "../resources/fa-free/solid/info-circle.svg")
        self.actionViewKitsu.setStatusTip("Open Shot in Kitsu")
        self.actionViewKitsu.triggered.connect(self.viewInKitsu)

        self.actionOpenDirectory = self._loadActionIcon("&Open Explorer", "../resources/fa-free/solid/folder.svg")
        self.actionOpenDirectory.setStatusTip("View File Explorer")
        self.actionOpenDirectory.triggered.connect(self.filesOpenDirectory)   

        self.actionCheckSelected = self._loadActionIcon("&Select", "../resources/fa-free/solid/plus.svg")
        self.actionCheckSelected.setStatusTip("Mark selected items")
        self.actionCheckSelected.triggered.connect(self.checkSelected)   

        self.actionUncheckSelected = self._loadActionIcon("&Unselect", "../resources/fa-free/solid/minus.svg")
        self.actionUncheckSelected.setStatusTip("Unmark selected items")
        self.actionUncheckSelected.triggered.connect(self.uncheckSelected)   

        self.tableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableView.addAction(self.actionViewKitsu)
        self.tableView.addAction(self.actionOpenDirectory)  
        self.tableView.addAction(self.actionCheckSelected)  
        self.tableView.addAction(self.actionUncheckSelected)   

    def checkSelected(self):
        self.checkItems(True)

    def uncheckSelected(self):
        self.checkItems(False)

    def checkItems(self, select):
        idx = self.tableView.selectedIndexes()
        
        for index in idx:
            row_index = index.row()
            try:
                # self.selected_file = self.proxy.data[row_index]  
                self.proxy.setData(self.proxy.index(row_index, ShotListModel.COL_SELECT), select, QtCore.Qt.EditRole)
            except:
                traceback.print_exc()
                return None                    

    def viewInKitsu(self):
        idx = self.tableView.selectedIndexes()
        for index in idx:
            row_index = index.row()
            try:
                self.selected_file = self.proxy.data(self.proxy.index(row_index, 0), QtCore.Qt.UserRole)                
                # self.selected_file = self.proxy.items[row_index]  
                tasks = gazu.task.all_tasks_for_entity_and_task_type(self.selected_file["entity_id"], self.selected_file["task_type_id"])
                if len(tasks) > 0:
                    task = tasks[0]
                    task_url = gazu.task.get_task_url(task)
                    if task_url:
                        self.open_url(task_url)
                        return True

                    
            except:
                traceback.print_exc()
                return None         

    def filesOpenDirectory(self):
        editorial_folder = self.lineEditFolder.text()
        if not (self.tableView.selectedIndexes()):
            return False

        idx = self.tableView.selectedIndexes()
        for index in idx:
            row_index = index.row()
            try:
                # self.selected_file = self.proxy.items[row_index]                
                self.selected_file = self.proxy.data(self.proxy.index(row_index, 0), QtCore.Qt.UserRole)                

                fn, ext = os.path.splitext(self.selected_file["output_file_name"])
                item_name = os.path.normcase("{}_{}_{}".format(self.selected_file["ep"], self.selected_file["sq"], self.selected_file["sh"]))
                output_name = os.path.normcase("{}/{}{}".format(item_name, item_name, ext))

                # D:\Productions\editorial\wotw\wotw_edit\wip\101_ALICKOFPAINT\sc010\sh010\sc010_sh010_Anim-Animation\witw_101_alickofpaint_sc010_sh010_anim_animation_v004.mp4

                file_path = os.path.dirname(os.path.join(editorial_folder, output_name))

                #output_dir = "{}/{}".format(self.lineEditFolder.text(), self.episode["name"])
                #file_path = os.path.normpath(os.path.join(output_dir, self.selected_file["output_file_name"]))

                if os.path.isdir(file_path):
                    #reply = QtWidgets.QMessageBox.question(self, 'File found:', 'Would you like to open the existing folder?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    #if reply == QtWidgets.QMessageBox.Yes:
                    open_folder(file_path)
                    return True       

            except:
                traceback.print_exc()
                return None    
            
    def read_fps(self):
        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        return float(self.project["fps"])        
            
    def read_timeline(self):
        #self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        #frame_rate = self.read_fps()
#        timeline = otio.adapters.read_from_file(
#            self.lineEditEDLFile.text(),
#            rate = frame_rate,
#            ignore_timecode_mismatch = True,
#        )            
#        timeline.global_start_time = otio.opentime.from_timecode("00:58:00:00", frame_rate)     
        #timeline = otio.adapters.read_from_file(self.lineEditEDLFile.text())
        #return timeline   

        tree = ET.parse(self.lineEditEDLFile.text())
        return tree.getroot()
    
    def shot_selected(self, shot_name):
        for x in range(self.tableView.model().rowCount()):
            rowIndex = self.tableView.model().index(x, 0)
            item = self.proxy.data(rowIndex, QtCore.Qt.UserRole)    

            item_name = "{}_{}".format(item["sequence_name"], item["name"])
            if shot_name == item_name:
                return item["selected"]
        return False

    def read_timecodes(self, clip):
        frame_in = int(clip.find('start').text)
        frame_out = int(clip.find('end').text)
        frame_count = frame_out - frame_in

        ## seconds
        seqStart = 1 / self.read_fps() * frame_in
        seqEnd = 1 / self.read_fps() * frame_out

        start_time = datetime.fromtimestamp(seqStart).strftime('%H:%M:%S.%f')
        end_time = datetime.fromtimestamp(seqEnd).strftime('%H:%M:%S.%f')        

        #start_time = otio.opentime.to_time_string(otio.opentime.RationalTime(frame_in, self.read_fps())) ## 00:00:50.28
        ##end_time = otio.opentime.to_time_string(otio.opentime.RationalTime(frame_in, self.read_fps())) ## 00:00:50.28

        return start_time, end_time, frame_count
            
    def scan_edl(self):
        # self.write_settings()
        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)
        
        self.shots = gazu.shot.all_shots_for_episode(self.episode)
        self.shot_map = {}

        for shot_id in self.shots:
            shot = gazu.shot.get_shot(shot_id["id"])

            if not "nb_frames" in shot:
                shot["nb_frames"] = None
                
            shot["frame_count_changed"] = False
            shot["frame_out_changed"] = False
            shot["edl_status"] = ""

            sequence_name = shot["sequence_name"].lower()
            shot_name = shot["name"].lower()

            key = "{}_{}".format(sequence_name, shot_name)

            if not key in self.shot_map:
                self.shot_map[key] = shot

        all_shots = []

        try:
            timeline = self.read_timeline()
        except otio.exceptions.OTIOError:
            raise Exception("Failed to parse EDL file.")
        
        for clip in timeline.iter('clipitem'):
            name, extension = os.path.splitext(clip.find('name').text)

            if extension not in SwingTimelineDialog.ALLOWED_MOVIE_EXTENSION:
                continue

            if not name.lower().startswith("sc"):
                continue 

            start_time, end_time, frame_count = self.read_timecodes(clip)            

            shot_id = None
            matched_values = name.lower().split("_")

            shot_info = {
                "sequence_name": matched_values[0],
                "shot_name": matched_values[1]
            }                    

            key = "{}_{}".format(shot_info["sequence_name"], shot_info["shot_name"])
            all_shots.append(key)

            if not key in self.shot_map:
                self.shot_map[key] =  {
                    "id": None,
                    "name": shot_info["shot_name"],
                    "sequence_name": shot_info["sequence_name"],
                    "new_shot": True,
                    "nb_frames": None,
                    "frame_in": None,
                    "frame_out": None,
                    "data": {
                        "frame_in": None,
                        "frame_out": None
                    },
                    "edl_status": "New Shot",
                    "start_time": None,
                    "end_time": None,
                    "canceled": False
                }
            
            shot = self.shot_map[name]

            shot["start_time"] = start_time
            shot["end_time"] = end_time

            shot["frame_count_changed"] = not shot["nb_frames"] or (frame_count != shot["nb_frames"])
            if shot["frame_count_changed"]:
                shot["nb_frames"] = frame_count

                if len(shot["edl_status"]) > 0:
                    shot["edl_status"] += ", "

                shot["edl_status"] = shot["edl_status"] + "# Frames changed"

            frame_out = frame_count - 1
            shot["frame_out_changed"] = not shot["data"]["frame_out"] or (frame_out != int(shot["data"]["frame_out"]))
            if shot["frame_out_changed"]:
                shot["data"]["frame_in"] = 0
                shot["data"]["frame_out"] = frame_out

        for k in self.shot_map:
            if not k in all_shots:
                self.shot_map[k]["edl_status"] = ShotListModel.SHOT_CUT

        self.update_model(self.shot_map)

    def extract_video(self):
        #edl_string = self.hack_edl(self.lineEditEDLFile.text())
        #
        #try:
        #    timeline = otio.adapters.read_from_string(edl_string, "cmx_3600", rate = self.project["fps"], ignore_timecode_mismatch = True, )            
        #except otio.exceptions.OTIOError:
        #    raise Exception("Failed to parse EDL file.")

        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)          

        try:
            timeline = self.read_timeline()
        except otio.exceptions.OTIOError:
            raise Exception("Failed to parse EDL file.")        
        
        name, _ = os.path.splitext(self.lineEditEDLFile.text())  
        source = self.lineEditSource.text()
        target_dir = os.path.join(os.path.dirname(name), name)
        prefix = os.path.basename(name).lower().split("_")[0]

        ffmpeg = SwingSettings.get_instance().bin_ffmpeg()

        ##if os.path.exists(target_dir):
        ##    raise Exception("Target directory already exists: {}".format(target_dir))
        
        ##os.makedirs(target_dir, mode=0o775, exist_ok=False)
        os.makedirs(target_dir, mode=0o775, exist_ok=True)

        ##  00:58:00:00 00:58:10:02 01:00:00:00 01:00:10:02
        for clip in timeline.iter('clipitem'):
            name, extension = os.path.splitext(clip.find('name').text)

            if extension not in SwingTimelineDialog.ALLOWED_MOVIE_EXTENSION:
                continue

            if not name.lower().startswith("sc"):
                continue 

            if not self.shot_selected(name):
                continue
            
            start_time, end_time, frame_count = self.read_timecodes(clip)            

            print("{} {} -> {}".format(name, start_time, end_time))  
            output = "{}/{}_{}/video/{}_{}.mp4".format(target_dir, prefix, name, prefix, name)  

            if not os.path.exists(os.path.dirname(output)):
                os.makedirs(os.path.dirname(output))                    

            try:
                ##command = ffmpeg + " -y -i " + source + " -ss  " + start_time + " -to " + end_time + " -c:v libx264 -crf 30 -an " + output
                command = ffmpeg + " -y -ignore_chapters 1 -i " + source + " -start_number 0" + " -ss  " + start_time + " -to " + end_time + " " + output
                # command = ffmpeg + " -y -i " + source + " -ss  " + start_time + " -to " + end_time + " -acodec copy -vcodec copy " + output                        

                self.run_command("{}: Video, Frame Count {}".format(name, frame_count), command)
                self.busy_count += 1
            except:
                traceback.print_exc() 
   
        self.enable_controls(self.busy_count == 0)
        ##self.textEditLog.append("Exporting Video: {}".format(self.busy_count))

    def extract_audio(self):
        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)    

        try:
            timeline = self.read_timeline()
        except otio.exceptions.OTIOError:
            raise Exception("Failed to parse EDL file.")    
        
        name, _ = os.path.splitext(self.lineEditEDLFile.text())  
        source = self.lineEditSource.text()
        target_dir = os.path.join(os.path.dirname(name), name)
        prefix = os.path.basename(name).lower().split("_")[0]

        ffmpeg = SwingSettings.get_instance().bin_ffmpeg()

        ##if os.path.exists(target_dir):
        ##    raise Exception("Target directory already exists: {}".format(target_dir))
        
        ##os.makedirs(target_dir, mode=0o775, exist_ok=False)
        os.makedirs(target_dir, mode=0o775, exist_ok=True)

        ##  00:58:00:00 00:58:10:02 01:00:00:00 01:00:10:02
        for clip in timeline.iter('clipitem'):
            name, extension = os.path.splitext(clip.find('name').text)

            if extension not in SwingTimelineDialog.ALLOWED_MOVIE_EXTENSION:
                continue

            if not name.lower().startswith("sc"):
                continue 

            if not self.shot_selected(name):
                continue            
            
            start_time, end_time, frame_count = self.read_timecodes(clip)            

            print("{} {}:{}".format(name, start_time, end_time))  
            output = "{}/{}_{}/audio/{}_{}.wav".format(target_dir, prefix, name, prefix, name)  

            if not os.path.exists(os.path.dirname(output)):
                os.makedirs(os.path.dirname(output))

            try:
                command = ffmpeg + " -y -ignore_chapters 1 -i " + source + " -start_number 0" + " -ss  " + start_time + " -to " + end_time + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + output                
#                command = ffmpeg + " -y -i " + source + " -ss  " + start_time + " -to " + end_time + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + output
                
                self.run_command("{}: Audio, Frame Count {}".format(name, frame_count), command)
                self.busy_count  += 1
            except:
                traceback.print_exc()    

        self.enable_controls(self.busy_count == 0)
        ##self.textEditLog.append("Exporting Audio: {}".format(self.busy_count))         

    def extract_images(self):
        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)    

        try:
            timeline = self.read_timeline()
        except otio.exceptions.OTIOError:
            raise Exception("Failed to parse EDL file.")    
        
        name, _ = os.path.splitext(self.lineEditEDLFile.text())  
        source = self.lineEditSource.text()
        target_dir = os.path.join(os.path.dirname(name), name)
        prefix = os.path.basename(name).lower().split("_")[0]

        ffmpeg = SwingSettings.get_instance().bin_ffmpeg()

        ##if os.path.exists(target_dir):
        ##    raise Exception("Target directory already exists: {}".format(target_dir))
        
        ##os.makedirs(target_dir, mode=0o775, exist_ok=False)
        os.makedirs(target_dir, mode=0o775, exist_ok=True)

        ##  00:58:00:00 00:58:10:02 01:00:00:00 01:00:10:02
        ##  00:58:00:00 00:58:10:02 01:00:00:00 01:00:10:02
        for clip in timeline.iter('clipitem'):
            name, extension = os.path.splitext(clip.find('name').text)

            if extension not in SwingTimelineDialog.ALLOWED_MOVIE_EXTENSION:
                continue

            if not name.lower().startswith("sc"):
                continue 
            
            if not self.shot_selected(name):
                continue            
            
            start_time, end_time, frame_count = self.read_timecodes(clip)            

            print("{} {}:{}".format(name, start_time, end_time))  
            output = "{}/{}_{}/images/{}_{}.%04d.jpg".format(target_dir, prefix, name, prefix, name)  

            if not os.path.exists(os.path.dirname(output)):
                os.makedirs(os.path.dirname(output))

            try:
                command = ffmpeg + " -y -ignore_chapters 1 -i " + source + " -start_number 0" + " -ss  " + start_time + " -to " + end_time + " " + output                        
                
                self.run_command("{}: Images, Frame Count {}".format(name, frame_count), command)                        
                self.busy_count  += 1                        
            except:
                traceback.print_exc()    

        self.enable_controls(self.busy_count == 0)

    def run_command(self, label, command_line):
        runner = CommandRunner(label, command_line)
        runner.callback.signal.connect(self.command_callback)

        self.threadpool.start(runner)

    def run_all(self):
        self.busy_count = 0

        self.extract_video()
        self.extract_audio()
        self.extract_images()

    def command_callback(self, data):
        self.textEditLog.append(data)
        self.busy_count -= 1

        if self.busy_count == 0:
            self.enable_controls(True)
            self.textEditLog.append("All exports completed")  

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

    def update_kitsu(self): 
        name, _ = os.path.splitext(self.lineEditEDLFile.text())  
        target_dir = os.path.join(os.path.dirname(name), name)
        prefix = os.path.basename(name).lower().split("_")[0]

        if not self.model:
            QtWidgets.QMessageBox.information("Please load and scan an EDL first")
            return False

        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)  

        server = SwingSettings.get_instance().swing_server()
        edit_api = "{}/edit".format(server)                     

        connect_to_server("showadmin@wildchildanimation.com", "Monday@01")

        task_types = gazu.task.all_task_types_for_project(self.project)
        layout_task_type = None
        for t in task_types:
            if t["name"].lower() == 'layout':
                layout_task_type = t
                break

        if not layout_task_type:
            QtWidgets.QMessageBox.information("Layout task type not found")
            return False
        
        task_status_todo = gazu.task.get_task_status_by_name("Todo")       
        if not task_status_todo:
            QtWidgets.QMessageBox.information("Todo task status not found")
            return False             

        person = gazu.person.get_person_by_email("showadmin@wildchildanimation.com")            
        if not person:
            QtWidgets.QMessageBox.information("Show Admin user not found")
            return False            

        for x in range(self.tableView.model().rowCount()):
            rowIndex = self.tableView.model().index(x, 0)
            item = self.proxy.data(rowIndex, QtCore.Qt.UserRole)    

            if item["selected"]:
                item_name = "{}_{}".format(item["sequence_name"], item["name"])
                self.textEditLog.append("Checking shot: {}".format(item_name))  

                print("Checking Kitsu: {} {} {}".format(self.project["name"], self.episode["name"], item_name))

                if "new_shot" in item and item["new_shot"]:
                    print("Creating new shot: {} {} {}".format(self.project["name"], self.episode["name"], item_name))

                sequence = gazu.shot.get_sequence_by_name(self.project, item["sequence_name"].lower(), self.episode)               
                if not sequence:
                    print("Creating new sequence: {} {}".format(self.episode["name"], item["sequence_name"]))
                    sequence = gazu.shot.new_sequence(self.project, item["sequence_name"].lower(), self.episode)

                shot = gazu.shot.get_shot_by_name(sequence, item["name"].lower())
                if not shot:
                    frame_in = 0

                    if "nb_frames" in item and item["nb_frames"]:
                        nb_frames = item["nb_frames"]
                    else:
                        nb_frames = None

                    if "frame_out" in item and item["frame_out"]:
                        frame_out = item["frame_out"]
                    else:
                        if nb_frames and nb_frames > 0:
                            frame_out = nb_frames - 1

                    if not nb_frames:
                        frame_in = None

                    shot = gazu.shot.new_shot(self.project, sequence, item["name"].lower(), nb_frames=nb_frames, frame_in=frame_in, frame_out=frame_out)

                task = self.get_shot_task(shot, layout_task_type["name"])
                if not task:
                    task = gazu.task.new_task(shot, layout_task_type, task_status = task_status_todo, assigner = None, assignees = None)

                if item["edl_status"] == ShotListModel.SHOT_CUT:
                    # gazu.task.add_comment(task, layout_task_type, "Shot cut from edit")
                    gazu.shot.remove_shot(shot)
                    print("Removed Shot from Kitsu: {} {} {}".format(self.project["name"], self.episode["name"], item_name))

                    continue

                if not shot["nb_frames"] or shot["nb_frames"] != item["nb_frames"]:
                    shot["nb_frames"] = item["nb_frames"]
                    shot = gazu.shot.update_shot(shot)

                update_shot = False

                shot_data = shot["data"]
                if not "frame_in" in shot_data or not shot_data["frame_in"] == 0:
                    shot_data["frame_in"] = 0
                    update_shot = True                    

                if not "frame_out" in shot_data or not shot_data["frame_out"] == item["data"]["frame_out"]:
                    shot_data["frame_out"] = item["data"]["frame_out"]
                    update_shot = True

                if update_shot:                    
                    shot = gazu.shot.update_shot_data(shot, shot_data)
                    print("Updated Shot Data: {} {} {}".format(self.project["name"], self.episode["name"], item_name))                    

                if self.checkBoxUploadMedia.isChecked():
                    video_preview = "{}/{}_{}/video/{}_{}.mp4".format(target_dir, prefix, item_name, prefix, item_name)  
                    audio_file = "{}/{}_{}/audio/{}_{}.wav".format(target_dir, prefix, item_name, prefix, item_name)  

                    if os.path.exists(video_preview):
                        print("Uploading preview {}".format(video_preview))

                        worker = WorkingFileUploader(self, edit_api, task, video_preview, item_name, "Video", "Breakout file", mode = "preview")
                        worker.run()                        

                    if os.path.exists(audio_file):
                        print("Uploading audio: {}".format(audio_file))

                        worker = WorkingFileUploader(self, edit_api, task, audio_file, item_name, "Audio", "Breakout file", mode = "working")
                        worker.run()  

        self.textEditLog.append("Update shot completed")
        return True
    
    def update_tracking_sheet(self):
        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)    

        ## sort table by name
        self.tableView.sortByColumn(ShotListModel.COL_NAME, QtCore.Qt.AscendingOrder)             

        gc = gspread.service_account(filename='./treehouse-gsuite-dcad9a674b8c.json')     
        spreadsheet_name = self.project["code"].upper() + " | Frame Ranges"

        sh = gc.open(spreadsheet_name)

        worksheet_list = sh.worksheets()

        worksheet = None
        for item in worksheet_list:
            if item.title == self.episode["name"]:
                worksheet = item
                break

        if not worksheet:
            worksheet = sh.add_worksheet(title=self.episode["name"], rows=500, cols=20)

        batch_update = [] # batch list update

        ## Add / Update Header
        row = 1
        cell_range = "A{}:F{}".format(1, row)

        batch = {
            "range": cell_range,
            "values": [ [
                "Sequence", 
                "Shot", 
                "Frame Count", 
                "Status", 
                'Updated: {}'.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")), 
                "Source: {}".format(os.path.basename(self.lineEditSource.text())) ] 
            ]
        }
        batch_update.append(batch)
        row += 1       

        for x in range(self.tableView.model().rowCount()):
            rowIndex = self.tableView.model().index(x, 0)
            item = self.proxy.data(rowIndex, QtCore.Qt.UserRole)                

            cell_range = "A{}:$D{}".format(row, row)

            if item["nb_frames"]:
                frame_count = item["nb_frames"]
            else:
                frame_count = ""

            batch = {
                "range": cell_range,
                "values": [ [item['sequence_name'], item['name'], frame_count, item["edl_status"]] ]
            }

            batch_update.append(batch)
            row += 1
        try:
            worksheet.batch_update(batch_update)
        except:
            print(traceback.format_exc())                

        self.textEditLog.append("Update shot completed")
        return True          

    def set_selection(self, project, episode):
        self.project = project
        self.set_episode(episode)

    def set_project_episode(self, project_id, episode_id, task_types):
        self.project_id = project_id
        self.episode_id = episode_id
        self.task_types = task_types

        self.refresh_playlists()

    def refresh_playlists(self):
        pass

    def get_playlist_file_name(self):
        pass
        # return os.path.join(self.lineEditFolder.text(), PlaylistDialog.PLAYLIST_FILE)

    def select_edl_file(self):
        file_name = self.lineEditEDLFile.text()
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Select EDL File", file_name, "EDL (*.edl);; XML (*.xml);; All Files (*.*)")
        if q:
            self.lineEditEDLFile.setText(q[0])

    def select_source(self):
        file_name = self.lineEditSource.text()
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Select Video File", file_name, "Video (*.mov);(*.mp4); All Files (*.*)")
        if q:
            self.lineEditSource.setText(q[0])

    def update_model(self, shot_data):
        self.project = self.comboBoxProject.currentData(QtCore.Qt.UserRole)
        self.episode = self.comboBoxEpisode.currentData(QtCore.Qt.UserRole)    

        self.model = ShotListModel(self.project, self.episode, shot_data)

        self.proxy = QtCore.QSortFilterProxyModel()
        self.proxy.setFilterKeyColumn(-1) # Search all columns.
        self.proxy.setSourceModel(self.model)
        self.proxy.setDynamicSortFilter(True)

        self.tableView.setModel(self.proxy)

        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(True)

        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.tableView.setColumnWidth(ShotListModel.COL_SELECT, 40)
        self.tableView.setColumnWidth(ShotListModel.COL_NAME, 200)
        self.tableView.setColumnWidth(ShotListModel.COL_STATUS, 120)

        self.tableView.sortByColumn(ShotListModel.COL_NAME, QtCore.Qt.AscendingOrder) 

        checkboxDelegate = CheckBoxDelegate()
        self.tableView.setItemDelegateForColumn(0, checkboxDelegate)  

        for i in range(self.model.rowCount()):
            self.tableView.resizeRowToContents(i)

        return True

class ShotListModel(QtCore.QAbstractTableModel):

    COLUMNS = ["", "Name", "Sequence", "Shot", "Frame In", "Frame Out", "# Frames", "Start", "End", "EDL Status", "Cancelled" ]
    items = []

    COL_SELECT = 0

    COL_NAME = 1

    COL_SEQUENCE = 2
    COL_SHOT = 3

    COL_IN = 4
    COL_OUT = 5
    COL_FRAMES = 6

    COL_START = 7
    COL_END = 8

    COL_STATUS = 9

    COL_CANCELLED = 10

    SHOT_CUT = "Shot cut from edit"

    def __init__(self, project, episode, data):
        super(ShotListModel, self).__init__(None)

        self.project = project
        self.episode = episode

        self.items = []
        for val in data.values():
            val["selected"] = True
            self.items.append(val)

    def select_all(self):
        for i in self.items:
            i["selected"] = True
        self.dataChanged.emit(0, len(self.items))

    def select_none(self):
        for i in self.items:
            i["selected"] = False
        self.dataChanged.emit(0, len(self.items))

    def columnCount(self, parent=QtCore.QModelIndex()):
        return ShotListModel.COLUMNS.__len__()

    def data(self, index, role):
        if not index.isValid():
            return None

        col_index = index.column()
        row_index = index.row()

        item = self.items[row_index]

        if role == QtCore.Qt.UserRole:
            return item

        if role == QtCore.Qt.BackgroundColorRole:
            if item["canceled"]:
                return QtGui.QColor.red            
            elif item["frame_count_changed"]:
                return QtGui.QColor("#ffa500") # orange
            elif "edl_status" in item:
                if "new_shot" in item["edl_status"]:
                    return QtGui.QColor("#0000cd") # green
            return None

        elif role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return None

        if ShotListModel.COL_SELECT == col_index:
            return item["selected"] 
        
        elif ShotListModel.COL_NAME == col_index:
            return F'{self.episode["name"]}_{item["sequence_name"]}_{item["name"]}'
        
        elif ShotListModel.COL_SEQUENCE == col_index:
            if "sequence_name" in item:
                return item["sequence_name"]

        elif ShotListModel.COL_SHOT == col_index:
            return item["name"]

        elif ShotListModel.COL_FRAMES == col_index:
            return item["nb_frames"]

        elif ShotListModel.COL_IN == col_index:
            if item["data"] and "frame_in" in item["data"]:
                return item["data"]["frame_in"]

        elif ShotListModel.COL_OUT == col_index:
            if item["data"] and "frame_out" in item["data"]:
                return item["data"]["frame_out"]
        
        elif ShotListModel.COL_START == col_index:
            if "start_time" in item:
                return item["start_time"]
            
        elif ShotListModel.COL_END == col_index:
            if "end_time" in item:
                return item["end_time"]
        
        #elif ShotListModel.COL_NEW_FRAMES == col_index:
        #    return item["nb_frames"]

        #elif ShotListModel.COL_NEW_OUT == col_index:
        #    return item["frame_out"]

        elif ShotListModel.COL_STATUS == col_index:
            if "edl_status" in item:
                return item["edl_status"]
            
        elif ShotListModel.COL_CANCELLED == col_index:
            if item["canceled"]:
                return "Cancelled"

        return None

    def flags(self, index):
        if not index.isValid():
            return 0

        if index.column() == 0:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        else:
            return QtCore.Qt.ItemIsEditable | super(ShotListModel, self).flags(index)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return ShotListModel.COLUMNS[section]

        return None

    def rowCount(self, parent=QtCore.QModelIndex()):

        return len(self.items)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole:
            return False

        col_index = index.column()
        row_index = index.row()

        item = self.items[row_index]            
        if ShotListModel.COL_SELECT == col_index:
            item["selected"] = bool(value)
            self.dataChanged.emit(index, index)
            return True

        return False

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.EditRole):
        if role != QtCore.Qt.EditRole or orientation != QtCore.Qt.Horizontal:
            return False

        result = self.rootItem.setData(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # or in new API
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))      

    test = SwingTimelineDialog(None)
    #test = FileSelectDialog(None, "E:/productions/Tom_Gates_Sky_S02/tg_2d_main/tg_2d_build/tg_2d_ep206/shots/sc100/sh010/anim_block/sc100_sh010_anim_block/")

    #test.pushButtonWorkingFiles.setVisible(True)
    #test.pushButtonOutputFiles.setVisible(True)
    #test.pushButtonZip.setVisible(True)

    test.show()
    sys.exit(app.exec_())