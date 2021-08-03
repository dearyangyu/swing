# -*- coding: utf-8 -*-
import traceback
import sys
import os
from wildchildanimation.gui.downloads import DownloadDialogGUI
from wildchildanimation.gui.swing_update_task import SwingUpdateTaskDialog

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1


from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import friendly_string, set_button_icon
from wildchildanimation.studio.studio_interface import StudioInterface
from wildchildanimation.gui.background_workers import EntityLoaderThread, TaskFileInfoThread, SoftwareLoader
from wildchildanimation.gui.swing_create_dialog import Ui_SwingCreateDialog

'''
    Ui_SwingCreateDialog class
    ################################################################################
'''

class SwingCreateDialog(QtWidgets.QDialog, Ui_SwingCreateDialog):

    def __init__(self, parent = None, task_id = None, entity_id = None, software_name = None):
        super(SwingCreateDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.set_enabled(False)

        self.software_name = software_name
        self.shot = None
        self.asset = None
        self.url = None

        self.task_id = task_id
        self.entity_id = entity_id

        self.swing_settings = SwingSettings.get_instance()
        self.read_settings()                

        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = EntityLoaderThread(self, self.entity_id)
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)

        loader = TaskFileInfoThread(self, self.task_id, self.swing_settings.swing_root())
        loader.callback.loaded.connect(self.task_loaded)
        self.threadpool.start(loader)

        loader = SoftwareLoader(self)            
        loader.callback.loaded.connect(self.software_loaded)
        self.threadpool.start(loader)

        set_button_icon(self.toolButtonWeb, "../resources/fa-free/solid/info-circle.svg")
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        set_button_icon(self.toolButtonWorkingDir, "../resources/fa-free/solid/folder.svg")
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)

        self.pushButtonCancel.clicked.connect(self.cancel_dialog)
        self.pushButtonImport.clicked.connect(self.close_dialog)

        self.setWorkingDir(self.swing_settings.swing_root())
        self.checkBoxLoadExisting.setChecked(True)
        self.checkBoxLoadExisting.setVisible(False)

        self.lineEditEntity.setEnabled(False)
        self.lineEditAssetType.setEnabled(False)

        # Hide updates
        self.pushButtonUpdate.setVisible(False)
        self.pushButtonUpdate.setEnabled(False)
        self.pushButtonUpdate.clicked.connect(self.on_update)

    def set_enabled(self, enabled):
        self.toolButtonWeb.setEnabled(enabled)
        self.toolButtonWorkingDir.setEnabled(enabled)
        self.comboBoxSoftware.setEnabled(enabled)
        self.radioButtonShot.setEnabled(enabled)
        self.radioButtonAsset.setEnabled(enabled)
        self.pushButtonImport.setEnabled(enabled)
        self.pushButtonUpdate.setEnabled(enabled)

        self.lineEditWorkingDir.setEnabled(enabled)
        self.comboBoxSoftware.setEnabled(enabled)
        self.lineEditFrameIn.setEnabled(enabled)
        self.lineEditFrameOut.setEnabled(enabled)
        self.lineEditFrameCount.setEnabled(enabled)

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()

        self.settings.beginGroup(self.__class__.__name__)
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("software", self.comboBoxSoftware.currentText())
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.default_software = self.settings.value("software", "")

        # self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))
        self.settings.endGroup()             

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

    def software_loaded(self, results):
        self.software = results["software"]

        self.comboBoxSoftware.clear()
        for item in self.software:
            self.comboBoxSoftware.addItem(item["name"], userData = item)

        if not self.default_software == '':
            self.select_software(self.default_software)
        else:
            self.comboBoxSoftware.setCurrentIndex(0)

    def select_software(self, software_name):
        index = self.comboBoxSoftware.findText(software_name)
        if index >= 0:
            self.comboBoxSoftware.setCurrentIndex(index)

    def entity_loaded(self, data):
        self.entity = data["entity"]
        self.type = self.entity["type"]
        self.shot = None
        self.asset = None
        self.project = data["project"]

        self.project_name = self.project["name"]
        self.episode_name = None
        self.sequence_name = None
        self.shot_name = None
        self.asset_name = None
        self.task_type_name = None
        self.asset_type_name = None

        sections = []
        if self.type == "Shot":
            self.setWindowTitle("swing: create new shot")
            self.radioButtonShot.setChecked(True)
            self.shot = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]
            sections.append(self.project_name)
                
            if "episode_name" in self.shot:
                self.episode_name = self.shot["episode_name"]
                sections.append(self.episode_name)

            if "sequence_name" in self.shot:
                self.sequence_name = self.shot["sequence_name"]
                sections.append(self.sequence_name)

            self.shot_name = self.shot["name"] 
            sections.append(self.shot_name)

            if "task_type" in self.task:
                if self.task["task_type"]["short_name"]:
                    sections.append(self.task["task_type"]["short_name"])          
                else:
                    sections.append(self.task["task_type"]["name"])          
                self.task_type_name = self.task["task_type"]["name"]

            self.lineEditEntity.setText(friendly_string("_".join(sections).lower()))
            
            self.lineEditAssetType.setText(self.task_type_name)

            self.lineEditFrameIn.setText(self.shot["frame_in"])
            self.lineEditFrameIn.setEnabled(False)
            self.lineEditFrameOut.setText(self.shot["frame_out"])
            self.lineEditFrameOut.setEnabled(False)            

            if self.shot["nb_frames"] and self.shot["nb_frames"] > 0:
                text = "{}".format(self.shot["nb_frames"])
            else:
                text = ""

            if text == "":
                try:
                    nb_frames = int(self.shot["frame_out"]) - int(self.shot["frame_in"])
                    text = "{}".format(nb_frames)
                except:
                    pass

            self.lineEditFrameCount.setText(text)                
            self.lineEditFrameCount.setEnabled(False)                          
        else:
            self.setWindowTitle("swing: create new asset")
            self.radioButtonAsset.setChecked(True)
            self.asset = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]
            sections.append(self.project_name)  

            if "asset_type_name" in self.asset:
                self.asset_type_name = self.asset["asset_type_name"].strip()
                if self.asset_type_name in StudioInterface.ASSET_TYPE_LOOKUP:
                    sections.append(StudioInterface.ASSET_TYPE_LOOKUP[self.asset_type_name])                     
                else:
                    sections.append(self.asset_type_name)                 

            self.asset_name = self.entity["name"].strip() 
            sections.append(self.asset_name)

            if "task_type" in self.task:
                if self.task["task_type"]["short_name"]:
                    sections.append(self.task["task_type"]["short_name"])          
                else:
                    sections.append(self.task["task_type"]["name"])          
                self.task_type_name = self.task["task_type"]["name"]

            self.lineEditEntity.setText(friendly_string("_".join(sections).lower()))

            self.lineEditAssetType.setText(self.asset_type_name)
            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)
            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)
            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)         

        self.toolButtonWeb.setEnabled(self.url is not None)
        self.set_enabled(True)
        self.setEnabled(True)

    def task_loaded(self, results):
        self.task_info = results
        self.task_dir = results["task_dir"]
        self.task = results["task"]

        if "working_files" in self.task_info:
            self.working_files = self.task_info["working_files"]
            if len(self.working_files) > 0:
                self.pushButtonUpdate.setVisible(True)
                self.pushButtonUpdate.setEnabled(True)
        self.setWorkingDir(results["project_dir"])

    def set_selected(self, file_item):
        index = 0
        while index < len(self.files):
            if file_item["id"] == self.files[index]["id"]:
                self.comboBoxWorkingFile.setCurrentIndex(index)
                break
            index += 1

    def setWorkingDir(self, working_dir):
        self.working_dir = os.path.normpath(working_dir)
        self.lineEditWorkingDir.setText(self.working_dir)

    def close_dialog(self):
        self.write_settings()
        self.accept()
        self.close()

    def cancel_dialog(self):
        self.write_settings()
        self.reject()        
        self.close()

    def select_wcd(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if (q and q[0] != ''): 
            self.working_dir = q[0]
            self.lineEditWorkingDir.setText(self.working_dir)

    def append_status(self, status_message, error = None):
        cursor = QtGui.QTextCursor(self.textEditStatus.document()) 

        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        cursor.insertHtml(text)

    def get_software(self):
        return self.comboBoxSoftware.currentData()

    def get_file_name(self):
        return os.path.normpath("{}{}".format(self.lineEditEntity.text().strip(), self.get_software()["file_extension"]))

    def get_working_dir(self):
        return self.lineEditWorkingDir.text().strip()        

    def get_start_frame(self):
        try:
            frame = int(self.lineEditFrameIn.text().strip())
        except:
            frame = 1
        return frame

    def get_end_frame(self):
        try:
            frame = int(self.lineEditFrameOut.text().strip())
        except:
            frame = 10
        return frame

    def get_frame_rate(self):
        return self.project["fps"]

    def get_ratio(self):
        return self.project["ratio"]

    def get_resolution(self):
        return self.project["resolution"]

    def on_update(self):
        self.updateDialog = SwingUpdateTaskDialog(self, task_info = self.task_info)

        if self.updateDialog.scan_files() > 0:
            self.updateDialog.show()
        else:
            QtWidgets.QMessageBox.information(self, 'Task: Update', 'No updates found')               




"""     def process(self):
        self.append_status("Creating new scene")

        # mode = "working"
        software = self.software[self.comboBoxSoftware.currentIndex()]
        name = "{}{}".format(self.lineEditEntity.text().strip(), software["file_extension"])
        workingDir = self.lineEditWorkingDir.text().strip()

        # only create working files on uploads
        # working_file = gazu.files.new_working_file(self.task, name = name, mode = mode, software = software)

        # call handler
        try:
            self.append_status("Create new project: {} {} {}".format(name, workingDir, software['name']))

            if (self.handler.on_create(source = name, working_dir = workingDir, software = software)):
                QtWidgets.QMessageBox.information(self, 'Swing: Create', 'Created folder {}'.format(workingDir), QtWidgets.QMessageBox.Ok)                        
            else:
                self.append_status("Error creating new scene")

            if self.type == "Shot":
                self.handler.set_globals(project = self.project_name, episode = self.episode_name, sequence = self.sequence_name, task = self.task_type_name, shot = self.shot_name, frame_in = self.lineEditFrameIn.text(), frame_out = self.lineEditFrameOut.text(), frame_count = self.lineEditFrameCount.text())
            else:
                self.handler.set_globals(project = self.project_name, asset_type = self.asset_type_name, task = self.task_type_name, asset = self.asset_name)

            self.append_status("Set globals")
        except:
            traceback.print_exc(file=sys.stdout)          

        self.write_settings()
        self.close()
    # process
 """
