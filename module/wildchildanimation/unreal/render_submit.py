# -- coding: utf-8 --
import sys
import os
import gazu
import argparse
import json

UNREAL_LOADED = False
try:
    import unreal
    from wildchildanimation.unreal.unreal_utils import search_assets, list_level_sequences, list_maps    
    UNREAL_LOADED = True
    unreal.log("Running in Unreal")
except:
    UNREAL_LOADED = False

import json
from datetime import datetime

try:
    from PySide2 import QtCore, QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.unreal.gui.render_submit_dialog import Ui_RenderSubmit
from wildchildanimation.gui.swing_utils import set_button_icon, connect_to_server


class RenderSubmitDialog(QtWidgets.QDialog, Ui_RenderSubmit):

    VERSION = "0.6"    

    def __init__(self, parent = None, config_file = None):
        super(RenderSubmitDialog, self).__init__(parent) # Call the inherited classes __init__ method    

        self.setupUi(self)
        self.setWindowTitle("Render Submission")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.config_file = config_file
        self.connected = False

        self.server = None
        self.user = None
        self.password = None

        if self.config_file:
            self.read_config()

        self.swing_settings = SwingSettings.get_instance()  

        self.read_settings() 
        self.refresh_projects()  
        ## self.refresh_all()

        self.toolButtonRefreshKitsuProject.clicked.connect(self.refresh_projects)
        self.toolButtonRefreshKitsuTask.clicked.connect(self.project_changed)

        self.toolButtonUnrealProject.clicked.connect(self.select_project)

        self.toolButtonMap.clicked.connect(self.select_map_folder)
        self.toolButtonRefreshMapAsset.clicked.connect(self.refresh_maps)

        self.toolButtonSequence.clicked.connect(self.select_level_sequence)
        self.toolButtonRefreshSequenceAsset.clicked.connect(self.refresh_levels)

        self.toolButtonPreset.clicked.connect(self.select_render_presets)

        self.toolButtonOutput.clicked.connect(self.select_output_dir)

        self.comboBoxKitsuProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxKitsuTask.currentIndexChanged.connect(self.task_changed)

        self.pushButtonClose.clicked.connect(self.close_dialog)
        self.pushButtonSubmit.clicked.connect(self.submit_render)

        self.spinBoxFrameIn.valueChanged.connect(self.on_frames_changed)
        self.spinBoxFrameOut.valueChanged.connect(self.on_frames_changed)
        self.checkBoxFrameIn.stateChanged.connect(self.on_frames_enabled)

        set_button_icon(self.toolButtonRefreshKitsuProject, "../resources/fa-free/solid/sync-solid.svg")        
        set_button_icon(self.toolButtonRefreshKitsuTask, "../resources/fa-free/solid/sync-solid.svg")                        
        set_button_icon(self.toolButtonRefreshMapAsset, "../resources/fa-free/solid/sync-solid.svg")        
        set_button_icon(self.toolButtonRefreshSequenceAsset, "../resources/fa-free/solid/sync-solid.svg")   
        set_button_icon(self.toolButtonRefreshPresets, "../resources/fa-free/solid/sync-solid.svg")   

        if UNREAL_LOADED:         
            unreal.log("{}: v{} Created".format(self.__class__.__name__, self.VERSION))  

    def read_config(self):
        # Read Setings override from supplied config file
        config_json = json.load(open(self.config_file))

        self.server = config_json["server"]
        self.project_name = config_json["project"]
        self.user = config_json["user"]
        self.password = config_json["password"]
        self.shared_root = config_json["shared_root"]
        
    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.project_name = self.settings.value("kitsu_project", "")                  
        self.lineEditUEProject.setText(self.settings.value("unreal_project", self.swing_settings.ue_project_root()))

        self.lineEditMapDir.setText(self.settings.value("unreal_map_dir", ""))
        if self.refresh_maps():
            item = self.settings.value("unreal_map_selection", "")
            self.comboBoxMapAsset.setCurrentIndex(self.comboBoxMapAsset.findText(item))

        self.lineEditSequenceDir.setText(self.settings.value("unreal_level_sequence", ""))
        if self.refresh_levels():
            item = self.settings.value("unreal_level_selection", "")
            self.comboBoxSequenceAsset.setCurrentIndex(self.comboBoxSequenceAsset.findText(item))

        self.lineEditPresetDir.setText(self.settings.value("unreal_preset_dir", ""))
        if self.refresh_presets():
            item = self.settings.value("unreal_preset", "")
            self.comboBoxPreset.setCurrentIndex(self.comboBoxPreset.findText(item))

        self.checkBoxFrameIn.setChecked(bool(self.settings.value("set_frame_range", False)))
        self.on_frames_enabled()

        self.lineEditOutputDir.setText(self.settings.value("render_output_dir", ""))                        
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.settings.endGroup()   

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("kitsu_project", self.comboBoxKitsuProject.currentText())
        self.settings.setValue("unreal_project", self.lineEditUEProject.text())

        self.settings.setValue("unreal_map_dir", self.lineEditMapDir.text())
        self.settings.setValue("unreal_map_selection", self.comboBoxMapAsset.currentText())        

        self.settings.setValue("unreal_level_sequence", self.lineEditSequenceDir.text())
        self.settings.setValue("unreal_level_selection", self.comboBoxSequenceAsset.currentText())        

        self.settings.setValue("unreal_preset_dir", self.lineEditPresetDir.text())   
        self.settings.setValue("unreal_preset", self.comboBoxPreset.currentText())

        self.settings.setValue("render_output_dir", self.lineEditOutputDir.text())   

        self.settings.setValue("set_frame_range", self.checkBoxFrameIn.isChecked())             
        
        self.settings.endGroup()   

    def on_connect(self):
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        if self.server and self.user and self.password:
            gazu.set_host("{}/api".format(self.server))        
            self.gazu_client = gazu.log_in(self.user, self.password)
        else:#
            if connect_to_server(self.swing_settings.swing_user(), self.swing_settings.swing_password()):
                self.gazu_client = gazu.client

        self.connected = True                
        self.project = gazu.project.get_project_by_name(self.project_name) 

        return self.connected       

    def close_dialog(self):
        self.write_settings()
        self.close() 

    def get_game_path(self, asset_path):
        '''
            Given a Project Path: D:\Productions\prp\prp_build_v002\prp_build_v002.uproject
            And an Asset Path like "D:\Productions\prp\prp_build_v002\Content\cinematics", "D:\Productions\prp\prp_build_v002\Content\cinematics\tests\level_sequence" ]

            Return a Game Path: "/Game/cinematics", "/Game/cinematics/tests/level_sequence"
        
        '''
        game_path = os.path.dirname(self.lineEditUEProject.text())
        game_path = os.path.join(game_path, "Content")
        game_path = os.path.normpath(game_path)

        asset_path = os.path.normpath(asset_path)
        asset_path = asset_path.replace(game_path, "/Game")
        asset_path = asset_path.replace("\\", "/")

        return asset_path
    
    def get_system_path(self, asset_path):
        '''
            Given an Asset Path: "/Game/cinematics", "/Game/cinematics/tests/level_sequence" ]
            And a Project Path: D:\Productions\prp\prp_build_v002\prp_build_v002.uproject

            Return a System Path: D:\Productions\prp\prp_build_v002\Content\cinematics, D:\Productions\prp\prp_build_v002\Content\cinematics\tests\level_sequence
        '''
        project_dir = os.path.dirname(self.lineEditUEProject.text())
        project_dir = os.path.join(project_dir, "Content")
        project_dir = os.path.normpath(project_dir)

        if asset_path.strip() == "":
            return project_dir

        asset_path = os.path.normpath(asset_path)
        asset_path = asset_path.replace("\\Game", project_dir)

        return asset_path

    def select_output_dir(self):
        cwd = self.lineEditOutputDir.text()
        if cwd == '':
            cwd = os.getcwd()

        folder = self.select_folder("Select Output folder", cwd)
        if folder:
            self.lineEditOutputDir.setText(os.path.normpath(folder))

    def project_changed(self):
        project = self.comboBoxKitsuProject.currentData(QtCore.Qt.UserRole)
        person = gazu.person.get_person_by_email(SwingSettings.get_instance().swing_user())
        tasks = gazu.task.all_tasks_for_person(person)

        if not project:
            return False

        self.comboBoxKitsuTask.blockSignals(True)        
        self.comboBoxKitsuTask.clear()

        tasks = sorted(tasks, key=lambda k: F"{k['task_type_name']}_{k['entity_name']}", reverse=False)

        for task in tasks:
            if task["project_id"] == project["id"]:

                if "Shot" == task["entity_type_name"]:
                    task_description = "{}: {} / {} / {}".format(task["task_type_name"], task['episode_name'], task['sequence_name'], task['entity_name'])
                elif "Asset" == task["entity_type_name"]:
                    task_description = "{}: {} / {} / {}".format(task["task_type_name"], task['task_type_for_entity'], task['entity_name'], task['entity_name'])
                else:
                    task_description = "{}: {} / {} / {}".format(task["task_type_name"], task["task_type_for_entity"], task["entity_type_name"], task['entity_name'])

                self.comboBoxKitsuTask.addItem(task_description, userData = task)

        self.comboBoxKitsuTask.blockSignals(False)

    def task_changed(self):
        task = self.comboBoxKitsuTask.currentData(QtCore.Qt.UserRole)

        if not task:
            self.textEditTaskData.clear()
            return False
        
        # make sure we have the latest task data
        task = gazu.task.get_task(task["id"])

        task_data = task["data"]
        if task_data:
            # self.comboBoxMapAsset.setCurrentIndex(self.comboBoxMapAsset.findText(item))

            if "unreal_project" in task_data: self.lineEditUEProject.setText(task_data["unreal_project"])
            if "unreal_map" in task_data: self.comboBoxMapAsset.setCurrentIndex(self.comboBoxMapAsset.findText(task_data["unreal_map"]))
            if "unreal_level" in task_data: self.comboBoxSequenceAsset.setCurrentIndex(self.comboBoxSequenceAsset.findText(task_data["unreal_level"]))
            if "unreal_preset" in task_data: self.comboBoxPreset.setCurrentIndex(self.comboBoxPreset.findText(task_data["unreal_preset"]))
            if "frame_in" in task_data: self.spinBoxFrameIn.setValue(int(task_data["frame_in"]))
            if "frame_out" in task_data: self.spinBoxFrameOut.setValue(int(task_data["frame_out"]))
            if "render_output_dir" in task_data: self.lineEditOutputDir.setText(task_data["render_output_dir"])

            self.textEditTaskData.setText(json.dumps(task_data, indent=4, sort_keys=True))
        else:
            self.textEditTaskData.clear()

        if task["entity"] and task["entity"]["data"]:
            frameIn = None
            frameOut = None
            entity_data = task["entity"]["data"]
            if "frame_in" in entity_data:
                frameIn = int(entity_data["frame_in"])
                self.spinBoxFrameIn.setValue(int(entity_data["frame_in"]))

            if "frame_out" in entity_data:
                frameOut = int(entity_data["frame_out"])
                self.spinBoxFrameOut.setValue(int(entity_data["frame_out"]))

            if frameIn is not None and frameOut is not None:
                self.lineEditTaskFrameRange.setText(F"{frameIn} - {frameOut}")

    def on_frames_changed(self):
        frame_in = self.spinBoxFrameIn.value()
        frame_out = self.spinBoxFrameOut.value()
        frame_count = frame_out - frame_in + 1
        self.spinBoxFrameCount.setValue(frame_count)

    def on_frames_enabled(self):
        self.spinBoxFrameIn.setEnabled(self.checkBoxFrameIn.isChecked())
        self.spinBoxFrameOut.setEnabled(self.checkBoxFrameIn.isChecked())
        self.spinBoxFrameCount.setEnabled(self.checkBoxFrameIn.isChecked())

    def refresh_projects(self):
        if not self.on_connect():
            return False
        
        self.comboBoxKitsuProject.clear()

        projects = gazu.project.all_open_projects()
        for p in projects:
            #self.comboBoxShot.addItem(name, userData = item) 
            self.comboBoxKitsuProject.addItem(p["name"], userData = p) #role=Qt.UserRole
        self.comboBoxKitsuProject.setCurrentIndex(self.comboBoxKitsuProject.findText(self.project_name))            

        self.project_changed()        

    def submit_render(self):
        self.write_settings()

        task = self.comboBoxKitsuTask.currentData(QtCore.Qt.UserRole)

        errors = []
        if self.lineEditUEProject.text() == "":
            errors.append("Unreal Project not set")

        if self.comboBoxSequenceAsset.currentText() == "":
            errors.append("Level Sequence not set")

        if self.comboBoxMapAsset.currentText() == "":
            errors.append("Map not set")

        if self.lineEditOutputDir.text() == "":
            errors.append("Output Directory not set")

        if self.comboBoxPreset.currentText() == "":
            errors.append("Preset not set")

        if len(errors) > 0:
            QtWidgets.QMessageBox.warning(self, 'Render Submit', '\n'.join(errors))
            return False

        task_data = {}
        task_data["unreal_project"] = self.lineEditUEProject.text()
        task_data["unreal_map"] = self.comboBoxMapAsset.currentText()
        task_data["unreal_level"] = self.comboBoxSequenceAsset.currentText()
        task_data["unreal_preset"] = self.comboBoxPreset.currentText()

        if self.checkBoxFrameIn.isChecked():
            task_data["frame_in"] = int(self.spinBoxFrameIn.value())
            task_data["frame_out"] = int(self.spinBoxFrameOut.value())

        task_data["render_output_dir"] = self.lineEditOutputDir.text()

        task_render_status = gazu.task.get_task_status_by_name("Render")

        gazu.task.update_task_data(task, task_data)

        comment_text = F'''
<p><b>Render Submit</b></p>
<p>Map: {task_data["unreal_map"]}</p>
<p>Level: {task_data["unreal_level"]}</p>
<p>Preset: {task_data["unreal_preset"]}</p>
'''
        if self.checkBoxFrameIn.isChecked():
            comment_text += F'<p># Frames: {task_data["frame_out"] - task_data["frame_in"]}</p>'

        gazu.task.add_comment(task, task_render_status, comment_text)

        self.task_changed()
        QtWidgets.QMessageBox.information(self, 'Render Submit', comment_text)

    def select_project(self):
        cwd = self.lineEditUEProject.text()
        if cwd == '':
            cwd = os.getcwd()

        selected_file = QtWidgets.QFileDialog.getOpenFileName(self, "Select UE Project", cwd)            
        if selected_file:
            self.lineEditUEProject.setText(os.path.normpath(selected_file[0]))        
        
    def select_folder(self, caption, working_dir = None):
        return QtWidgets.QFileDialog.getExistingDirectory(self, caption, working_dir)

    def select_level_sequence(self):
        folder = self.select_folder("Select Map folder", self.get_system_path(self.lineEditSequenceDir.text()))
        if folder:
            self.lineEditSequenceDir.setText(self.get_game_path(folder))
            self.refresh_levels()       

    def refresh_levels(self):
        if not UNREAL_LOADED:
            return False        

        item_list = list_level_sequences(package_paths = [self.lineEditSequenceDir.text()])

        if not item_list:
            return False
        
        item_list = sorted(item_list, key=lambda k: k.package_name, reverse=False)

        self.comboBoxSequenceAsset.clear()
        for item in item_list:
            self.comboBoxSequenceAsset.addItem(str(item.package_name))
            ## print(str(item))
            ## self.comboBoxSequenceAsset.addItem(str(F"{item.asset_path}/{item.asset_name}"))
        return True              
    
    def select_map_folder(self):
        folder = self.select_folder("Select Map folder", self.get_system_path(self.lineEditMapDir.text()))
        if folder:
            self.lineEditMapDir.setText(self.get_game_path(folder))
            self.refresh_maps()

    def refresh_maps(self):
        if not UNREAL_LOADED:
            return False
        
        item_list = list_maps(package_paths = [self.lineEditMapDir.text()])

        if not item_list:
            return False

        item_list = sorted(item_list, key=lambda k: k.package_name, reverse=False)

        self.comboBoxMapAsset.clear()
        for item in item_list:
            self.comboBoxMapAsset.addItem(str(item.package_name))
        return True

    def select_render_presets(self):
        folder = self.select_folder("Select Presets folder", self.get_system_path(self.lineEditPresetDir.text()))
        if folder:
            self.lineEditPresetDir.setText(self.get_game_path(folder))
            self.refresh_presets()            

    def refresh_presets(self):
        if not UNREAL_LOADED:
            return False

        item_list = search_assets(class_names = ["MoviePipelinePrimaryConfig"], package_paths=[self.lineEditPresetDir.text()])

        if not item_list:
            return False
        
        item_list = sorted(item_list, key=lambda k: k.package_name, reverse=False)        

        self.comboBoxPreset.clear()
        for item in item_list:
            self.comboBoxPreset.addItem(str(item.package_name))
        return True    
    
    def refresh_all(self):
        self.refresh_projects()

        self.refresh_maps()
        self.refresh_levels()
        self.refresh_presets()

if __name__ == "__main__":
    global app

    parser = argparse.ArgumentParser(
        description="Swing::UE Render Submit - Settings"
    )

    parser.add_argument("-c", "--config", help="Config File", action="store")
    args = parser.parse_args()
    config_file = args.config

    if not os.path.exists(config_file):
        print("Config file not found: {}".format(config_file))
        sys.exit(1)

    app = None
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    dialog = RenderSubmitDialog(config_file=config_file)
    dialog.show()

    sys.exit(app.exec_())    

# Z:\env\wca\swing\swing-main\module\wildchildanimation\unreal\render_submit.py --config=V:/productions/HNL/bin/hnl_server.config.json
# Z:\env\wca\swing\swing-main\module\wildchildanimation\unreal\render_submit.py --config=V:/productions/PRP/bin/prp_server.config.json
