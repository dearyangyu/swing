# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re
import copy

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance 
    import PySide2.QtUiTools as QtUiTools
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.background_workers import *

from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.loader_dialog import Ui_LoaderDialog

from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

'''
    Load Asset class
    ################################################################################
'''

class LoaderDialogGUI(QtWidgets.QDialog, Ui_LoaderDialog):

    def __init__(self, parent = None, handler = None, entity = None):
        super(LoaderDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.handler = handler
        self.entity = entity
        self.shot = None
        self.asset = None
        self.url = None
        self.threadpool = QtCore.QThreadPool.globalInstance()

        loader = EntityLoaderThread(self, self.entity["id"])
        loader.callback.loaded.connect(self.entity_loaded)
        self.threadpool.start(loader)

        self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        self.toolButtonWorkingDir.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        self.toolButtonWorkingDir.clicked.connect(self.select_wcd)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

        self.setWorkingDir(load_settings("projects_root", os.path.expanduser("~")))

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

    def entity_loaded(self, data):
        self.type = data["type"]
        self.project = data["project"]

        self.shot = None
        self.asset = None

        self.project_name = None
        self.episode_name = None
        self.sequence_name = None
        self.shot_name = None
        self.asset_name = None
        self.task_type_name = None
        self.asset_type_name = None

        sections = []
        if self.type == "Shot":
            self.setWindowTitle("swing: import shot")
            self.shot = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]
                
            if "episode_name" in self.shot:
                self.episode_name = self.shot["episode_name"]
                #sections.append(self.episode_name)

            if "sequence_name" in self.shot:
                self.sequence_name = self.shot["sequence_name"]
                #sections.append(self.sequence_name)

            self.shot_name = self.shot["name"] 
            sections.append(self.shot_name)

            #if "task_type" in self.task:
            #    self.task_type_name = self.task["task_type"]["name"]
            #    sections.append(self.task_type_name)

            self.lineEditEntity.setText(friendly_string("_".join(sections)))

            self.textEditShotInfo.setText(self.shot["description"])

            self.lineEditFrameIn.setText(self.shot["frame_in"])
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText(self.shot["frame_out"])
            self.lineEditFrameOut.setEnabled(False)            

            if self.shot["nb_frames"] and len(self.shot["nb_frames"] > 0):
                self.lineEditFrameCount.setText()
            else:
                text = ""
            self.lineEditFrameCount.setText(text)                
            self.lineEditFrameCount.setEnabled(False)                          
        else:
            self.setWindowTitle("swing: import asset")
            self.asset = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]

            if "asset_type_name" in self.asset:
                self.asset_type_name = self.asset["asset_type_name"].strip()
                #sections.append(self.asset_type_name)                 

            self.asset_name = self.entity["name"].strip() 
            sections.append(self.asset_name)

            #if "task_type" in self.task:
            #    self.task_type_name = self.task["task_type"]["name"]
            #    sections.append(self.task_type_name)               

            #sections.append(self.entity["name"].strip())

            self.lineEditEntity.setText(friendly_string("_".join(sections)))
            self.textEditShotInfo.setText(self.asset["description"].strip())

            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)

            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)

        namespace = friendly_string("_".join(sections).lower().strip())
        #if self.asset_type_name:
        #    namespace = self.asset_type_name
        #elif self.asset_name:
        #    namespace = self.asset_name
        #elif self.task_type_name:
        #    namespace = self.task_type_name
        #elif self.shot_name:
        #    namespace = self.shot_name
        #else:
        #    namespace = "_ns"

        self.lineEditNamespace.setText(namespace)
        self.toolButtonWeb.setEnabled(self.url is not None)
        self.setEnabled(True)

    def load_files(self, file_list, selected_file = None):
        index = 0
        selected_index = 0

        self.files = []
        self.comboBoxWorkingFile.clear()
        for item in file_list:
            self.files.append(copy.copy(item))
            self.comboBoxWorkingFile.addItem(item["name"])
            
            if selected_file and selected_file == item:
                selected_index = index
            index += 1

        if selected_file:
            self.comboBoxWorkingFile.setCurrentIndex(selected_index)

    def set_selected(self, file_item):
        index = 0
        while index < len(self.files):
            if file_item["id"] == self.files[index]["id"]:
                self.comboBoxWorkingFile.setCurrentIndex(index)
                break
            index += 1

    def setWorkingDir(self, working_dir):
        self.working_dir = working_dir
        self.lineEditWorkingDir.setText(self.working_dir)

    def close_dialog(self):
        self.close()

    def select_wcd(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if (q):
            self.setWorkingDir(q[0][1])

    def append_status(self, status_message, error = None):
        cursor = QtGui.QTextCursor(self.textEditStatus.document()) 

        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        cursor.insertHtml(text)

    def file_loaded(self, results):
        status = results["status"]
        message = results["message"]
        size = results["size"]
        row = results["file_id"]
        file_name = results["target"]
        working_dir = results["working_dir"]
        self.append_status(message, "error" in status)

        # call maya handler: import into existing workspace
        try:
            #
            # import referenes
            # 
            if self.checkBoxReferences.checkState() == QtCore.Qt.Checked:

                # see if we know a namespace
                if self.checkBoxNamespace.checkState() == QtCore.Qt.Checked:
                    namespace = self.lineEditNamespace.text()
                else:
                    namespace = self.lineEditEntity.text()

                # loop through spinbox counter
                for ref in range(self.spinBoxReferenceCount.value()):
                    ref_str = str(ref).zfill(4)
                    ref_namespace = "{0}_{1}".format(namespace, ref_str)

                    self.append_status("Adding reference {}".format(file_name))
                    if (self.handler.import_reference(source = file_name, working_dir = working_dir, namespace = ref_namespace)):
                        self.append_status("Added {0}".format(ref_namespace))
                    else:
                        self.append_status("Import error", True)
            else:
                self.append_status("Loading file {}".format(file_name))
                if (self.handler.load_file(source = file_name, working_dir = working_dir)):
                    self.append_status("Loading done")
                else:
                    self.append_status("Loading error", True)

        except:
            traceback.print_exc(file=sys.stdout)          

        self.append_status("{}".format(message))
        self.set_ui_enabled(True)

    def file_loading(self, result):
        message = result["message"]
        size = result["size"]
        row = result["file_id"]
        file_name = result["target"]

        self.append_status("{} {}".format(message, human_size(size)))

    def set_ui_enabled(self, status):
        self.comboBoxWorkingFile.setEnabled(status)
        self.lineEditEntity.setEnabled(status)
        self.lineEditFrameIn.setEnabled(status)
        self.lineEditFrameOut.setEnabled(status)
        self.lineEditWorkingDir.setEnabled(status)
        self.toolButtonWorkingDir.setEnabled(status)
        self.checkBoxSkipExisting.setEnabled(status)

        self.checkBoxSkipExisting.setEnabled(status)
        self.checkBoxExtractZips.setEnabled(status)
        self.pushButtonImport.setEnabled(status)
        self.pushButtonCancel.setEnabled(status)

    def process(self):
        #self.threadpool = QtCore.QThreadPool()
        self.textEditStatus.clear()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.set_ui_enabled(False)
        self.process_count = 0

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')
        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)

        # download the currently selected file
        item = self.files[self.comboBoxWorkingFile.currentIndex()]
        row = 0
        if "WorkingFile" in item["type"]:
            #target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
            url = "{}/api/working_file/{}".format(edit_api, item["id"])
            target = set_target(item, self.working_dir)

            worker = FileDownloader(self, self.working_dir, item["id"], url, item["target_path"], email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)

            self.process_count += 1
            self.threadpool.start(worker)
            self.append_status("Downloading {} to {}".format(item["name"], item["target_path"]))
            #file_item["status"] = "Busy"
        else:
            #target = os.path.normpath(os.path.join(self.working_dir, item["name"]))
            url = "{}/api/output_file/{}".format(edit_api, item["id"])
            target = set_target(item, self.working_dir)

            worker = FileDownloader(self, self.working_dir, item["id"], url,  item["target_path"], email, password, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)
            
            self.process_count += 1
            self.threadpool.start(worker)
            self.append_status("Downloading {} to {}".format(item["name"], item["target_path"]))
        # file type
    # process
