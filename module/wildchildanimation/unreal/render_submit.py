# -- coding: utf-8 --
import sys
import os
import gazu

from glob import glob

UNREAL_LOADED = False
try:
    import unreal
    UNREAL_LOADED = True
    unreal.log("Running in Unreal")
except:
    UNREAL_LOADED = False

import json
import traceback

from datetime import datetime

try:
    from PySide2 import QtCore, QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.unreal.gui.render_submit_dialog import Ui_RenderSubmit
from wildchildanimation.gui.swing_utils import connect_to_server, set_button_icon


class RenderSubmitDialog(QtWidgets.QDialog, Ui_RenderSubmit):

    VERSION = "0.1"    

    def __init__(self, parent = None):
        super(RenderSubmitDialog, self).__init__(parent) # Call the inherited classes __init__ method    

        self.setupUi(self)
        self.setWindowTitle("Render Submission")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.swing_settings = SwingSettings.get_instance()  

        self.read_settings()   
        self.refresh_all()

        self.toolButtonRefreshKitsuProject.clicked.connect(self.refresh_projects)
        self.toolButtonRefreshKitsuTask.clicked.connect(self.project_changed)

        self.toolButtonMap.clicked.connect(self.select_map_folder)
        self.toolButtonRefreshMapAsset.clicked.connect(self.refresh_maps)

        self.toolButtonSequence.clicked.connect(self.select_level_sequence)
        self.toolButtonRefreshSequenceAsset.clicked.connect(self.refresh_levels)

        self.toolButtonOutput.clicked.connect(self.select_output_dir)

        self.comboBoxKitsuProject.currentIndexChanged.connect(self.project_changed)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonSubmit.clicked.connect(self.submit_render)

        set_button_icon(self.toolButtonRefreshKitsuProject, "../resources/fa-free/solid/sync-solid.svg")        
        set_button_icon(self.toolButtonRefreshKitsuTask, "../resources/fa-free/solid/sync-solid.svg")                        
        set_button_icon(self.toolButtonRefreshMapAsset, "../resources/fa-free/solid/sync-solid.svg")        
        set_button_icon(self.toolButtonRefreshSequenceAsset, "../resources/fa-free/solid/sync-solid.svg")   
        set_button_icon(self.toolButtonRefreshPresets, "../resources/fa-free/solid/sync-solid.svg")   


        if UNREAL_LOADED:         
            unreal.log("{}: v{} Created".format(self.__class__.__name__, self.VERSION))  
        
    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.lineEditUEProject.setText(self.swing_settings.ue_project_root())

        self.lineEditMapDir.setText(self.settings.value("unreal_map_dir", ""))
        if self.refresh_maps():
            item = self.settings.value("unreal_map_selection", "")
            self.comboBoxMapAsset.setCurrentIndex(self.comboBoxMapAsset.findText(item))

        self.lineEditSequenceDir.setText(self.settings.value("unreal_level_sequence", ""))
        if self.refresh_levels():
            item = self.settings.value("unreal_level_selection", "")
            self.comboBoxSequenceAsset.setCurrentIndex(self.comboBoxSequenceAsset.findText(item))

        if self.refresh_presets():
            item = self.settings.value("unreal_preset", "")
            self.comboBoxPreset.setCurrentIndex(self.comboBoxPreset.findText(item))

        self.lineEditOutputDir.setText(self.settings.value("render_output_dir", ""))                        

        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.settings.endGroup()   

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("unreal_map_dir", self.lineEditMapDir.text())
        self.settings.setValue("unreal_map_selection", self.comboBoxMapAsset.currentText())        

        self.settings.setValue("unreal_level_sequence", self.lineEditSequenceDir.text())
        self.settings.setValue("unreal_level_selection", self.comboBoxSequenceAsset.currentText())        

        self.settings.setValue("unreal_preset", self.comboBoxPreset.currentText())    

        self.settings.setValue("render_output_dir", self.lineEditOutputDir.text())                
        
        self.settings.endGroup()        

    def close_dialog(self):
        self.write_settings()
        self.close() 

    def submit_render(self):
        self.write_settings()

        task = self.comboBoxKitsuTask.currentData(QtCore.Qt.UserRole)

        task_data = {}
        task_data["unreal_project"] = self.lineEditUEProject.text()
        task_data["unreal_map"] = self.comboBoxMapAsset.currentText()
        task_data["unreal_level"] = self.comboBoxSequenceAsset.currentText()
        task_data["unreal_preset"] = self.comboBoxPreset.currentText()
        task_data["render_output_dir"] = self.lineEditOutputDir.text()

        task_render_status = gazu.task.get_task_status_by_name("Render")

        gazu.task.update_task_data(task, task_data)
        gazu.task.add_comment(task, task_render_status, 'Render Submit {}'.format(datetime.now()))

        QtWidgets.QMessageBox.information(self, 'Render Submit', 'Task submitted for Render')   

        #print(task)
        #print(task_data)
        ##gazu.task.update_task_data(task, task_data)
        
    def select_folder(self, caption, working_dir = None):
        return QtWidgets.QFileDialog.getExistingDirectory(self, caption, working_dir)
    
    def select_map_folder(self):
        cwd = self.lineEditMapDir.text()
        if cwd == '':
            cwd = os.getcwd()

        folder = self.select_folder("Select Map folder", cwd)
        if folder:
            self.lineEditMapDir.setText(os.path.normpath(folder))
            self.refresh_maps()

    def refresh_maps(self):
        directory = self.lineEditMapDir.text()
        if not os.path.exists(directory):
            return False
        
        self.comboBoxMapAsset.clear()
        
        files = glob("{}/*/**.umap".format(directory), recursive=True)
        for f in files:
            self.comboBoxMapAsset.addItem(os.path.normpath(f))

        return True

    def select_level_sequence(self):
        cwd = self.lineEditSequenceDir.text()
        if cwd == '':
            cwd = os.getcwd()

        folder = self.select_folder("Select Map folder", cwd)
        if folder:
            self.lineEditSequenceDir.setText(os.path.normpath(folder))
            self.refresh_levels()        

    def refresh_levels(self):
        directory = self.lineEditSequenceDir.text()
        if not os.path.exists(directory):
            return False
        
        self.comboBoxSequenceAsset.clear()
        
        files = glob("{}/**/ls_*.uasset".format(directory), recursive=True)
        for f in files:
            self.comboBoxSequenceAsset.addItem(os.path.normpath(f))

        return True  

    def select_output_dir(self):
        cwd = self.lineEditOutputDir.text()
        if cwd == '':
            cwd = os.getcwd()

        folder = self.select_folder("Select Output folder", cwd)
        if folder:
            self.lineEditOutputDir.setText(os.path.normpath(folder))

    def refresh_presets(self):
        project = self.lineEditUEProject.text()
        if not os.path.exists(project):
            return False
        
        project_directory = os.path.dirname(project)
        preset_directory = os.path.join(project_directory, 'Content', 'RenderSettings')

        if os.path.exists(preset_directory):
            self.comboBoxPreset.clear()
            
            files = glob("{}/**/*.uasset".format(preset_directory), recursive=True)
            for f in files:
                self.comboBoxPreset.addItem(os.path.normpath(f))  

        return True    

    def project_changed(self):
        project = self.comboBoxKitsuProject.currentData(QtCore.Qt.UserRole)
        person = gazu.person.get_person_by_email(SwingSettings.get_instance().swing_user())
        tasks = gazu.task.all_tasks_for_person(person)

        self.comboBoxKitsuTask.clear()

        for task in tasks:
            if task["project_id"] == project["id"]:

                if "Shot" == task["entity_type_name"]:
                    task_description = "{}: {} / {} / {}".format(task["task_type_name"], task['episode_name'], task['sequence_name'], task['entity_name'])
                elif "Asset" == task["entity_type_name"]:
                    task_description = "{}: {} / {} / {}".format(task["task_type_name"], task['task_type_for_entity'], task['entity_name'], task['entity_name'])
                else:
                    task_description = "{}: {} / {} / {}".format(task["task_type_name"], task["task_type_for_entity"], task["entity_type_name"], task['entity_name'])

                self.comboBoxKitsuTask.addItem(task_description, userData = task)

    def refresh_projects(self):
        if not connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password()):
            return False
        
        self.comboBoxKitsuProject.clear()

        projects = gazu.project.all_open_projects()
        for p in projects:
            #self.comboBoxShot.addItem(name, userData = item) 
            self.comboBoxKitsuProject.addItem(p["name"], userData = p) #role=Qt.UserRole

        self.project_changed()
        
    def refresh_all(self):
        self.refresh_maps()
        self.refresh_levels()
        self.refresh_presets()
        self.refresh_projects()

    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)

    dialog = RenderSubmitDialog()
    dialog.show()

    sys.exit(app.exec_())    

            