# -*- coding: utf-8 -*-

import traceback
import sys
import os
import copy

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

from wildchildanimation.gui.background_workers import EntityLoaderThread, FileDownloader
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.loader_dialog import Ui_LoaderDialog

from wildchildanimation.gui.swing_utils import friendly_string, resolve_content_path, set_button_icon, set_target
from wildchildanimation.gui.swing_tables import human_size

'''
    Load Asset class
    ################################################################################
'''

class LoaderDialogGUI(QtWidgets.QDialog, Ui_LoaderDialog):

    target = None
    working_dir = None

    def __init__(self, parent = None, handler = None, entity = None):
        super(LoaderDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.read_settings()                

        self.handler = handler
        self.entity = entity
        self.shot = None
        self.asset = None
        self.url = None

        self.threadpool = QtCore.QThreadPool.globalInstance()
        if self.entity:
            if isinstance(entity, dict):
                loader = EntityLoaderThread(self, self.entity["id"])
            else:
                loader = EntityLoaderThread(self, self.entity)        

            loader.callback.loaded.connect(self.entity_loaded)
            self.threadpool.start(loader)
            self.set_enabled(False)

        set_button_icon(self.toolButtonWeb, "../resources/fa-free/solid/info-circle.svg")
        self.toolButtonWeb.clicked.connect(self.open_url)
        self.toolButtonWeb.setEnabled(False)

        set_button_icon(self.toolButtonTargetDir, "../resources/fa-free/solid/folder.svg")
        self.toolButtonTargetDir.clicked.connect(self.select_wcd)
        self.comboBoxWorkingFile.currentIndexChanged.connect(self.working_file_changed)

        self.openRb.clicked.connect(self.selection_changed)
        self.importRb.clicked.connect(self.selection_changed)
        self.referenceRb.clicked.connect(self.selection_changed)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

        self.working_dir = SwingSettings.get_instance().swing_root()
        self.set_enabled_handlers(self.is_handled())

    def is_handled(self):
        return self.handler and "Maya" in self.handler.NAME

    def set_enabled_handlers(self, status):
        self.checkBoxForce.setEnabled(status)

        self.openRb.setEnabled(status)
        self.importRb.setEnabled(status)
        self.referenceRb.setEnabled(status)
        self.spinBoxReferenceCount.setEnabled(status)
        self.checkBoxNamespace.setEnabled(status)
        self.lineEditNamespace.setEnabled(status)        

    def set_enabled(self, status):
        self.checkBoxSkipExisting.setEnabled(status)
        self.checkBoxExtractZips.setEnabled(status)

        self.comboBoxWorkingFile.setEnabled(status)
        self.lineEditEntity.setEnabled(status)
        self.lineEditFrameIn.setEnabled(status)
        self.lineEditFrameOut.setEnabled(status)
        self.lineEditFrameCount.setEnabled(status)

        self.lineEditTarget.setEnabled(status)
        self.toolButtonTargetDir.setEnabled(status)

        self.textEditStatus.setEnabled(status)

        self.pushButtonImport.setEnabled(status)
        self.pushButtonCancel.setEnabled(status)        

        # DCC handlers
        if self.is_handled():
            self.set_enabled_handlers(status)
        # DCC

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("skip_existing", self.checkBoxSkipExisting.isChecked())
        self.settings.setValue("extract_zips", self.checkBoxExtractZips.isChecked())

        self.settings.setValue("force_load", self.checkBoxForce.isChecked())
        self.settings.setValue("name_space", self.checkBoxNamespace.isChecked())

        if self.openRb.isChecked():
            self.settings.setValue("load_type", "open")
        elif self.importRb.isChecked():
            self.settings.setValue("load_type", "import")
        else:
            self.settings.setValue("load_type", "reference")

        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        try:
            self.settings = QtCore.QSettings()
            self.settings.beginGroup(self.__class__.__name__)
            
            self.resize(self.settings.value("size", QtCore.QSize(480, 520)))

            self.checkBoxSkipExisting.setChecked(self.settings.value("skip_existing", True, type=bool))
            self.checkBoxExtractZips.setChecked(self.settings.value("extract_zips", True, type=bool))
            self.checkBoxForce.setChecked(self.settings.value("force_load", True, type=bool))
            self.checkBoxNamespace.setChecked(self.settings.value("name_space", True, type=bool))

            load_type = self.settings.value("load_type", "open", type=str)
            if "open" in load_type:
                self.openRb.setChecked(True)
            elif "import" in load_type:
                self.importRb.setChecked(True)
            else:
                self.referenceRb.setChecked(True)

            self.settings.endGroup()              
        except:
            traceback.print_exc(file=sys.stdout)

    def selection_changed(self):
        self.checkBoxNamespace.setEnabled(self.referenceRb.isChecked())       
        self.lineEditNamespace.setEnabled(self.referenceRb.isChecked())       
        self.spinBoxReferenceCount.setEnabled(self.referenceRb.isChecked())

    def working_file_changed(self, index):
        target_dir = self.working_dir
        item = self.comboBoxWorkingFile.itemData(index)

        set_target(item, target_dir)

        if item and target_dir:
            self.lineEditTarget.setText(item['target_path'])

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
            self.setWindowTitle("swing: shot loader")

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

            #if "task_type" in self.task:
            #    self.task_type_name = self.task["task_type"]["name"]
            #    sections.append(self.task_type_name)

            self.lineEditEntity.setText(friendly_string("_".join(sections)))

            self.textEditShotInfo.setText(self.shot["description"])

            self.lineEditFrameIn.setText(self.shot["frame_in"])
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText(self.shot["frame_out"])
            self.lineEditFrameOut.setEnabled(False)            

            if self.shot["nb_frames"] and self.shot["nb_frames"] > 0:
                text = "{} frames".format(self.shot["nb_frames"])
            else:
                text = ""
            self.lineEditFrameCount.setText(text)                

            self.lineEditFrameCount.setEnabled(False)                          
        else:
            self.setWindowTitle("swing: asset loader")

            self.asset = data["item"]
            self.url = data["url"]

            if "code" in self.project:
                self.project_name = self.project["code"]
            else:
                self.project_name = self.project["name"]
            sections.append(self.project_name)                

            if "asset_type_name" in self.asset:
                self.asset_type_name = self.asset["asset_type_name"].strip()
                sections.append(self.asset_type_name)

            try:
                self.asset_name = self.entity["name"].strip() 
                sections.append(self.asset_name)
            except:
                print(self.entity)
                traceback.print_exc()

            self.lineEditEntity.setText(friendly_string("_".join(sections)))
            self.textEditShotInfo.setText(self.asset["description"].strip())

            self.lineEditFrameIn.setText("")
            self.lineEditFrameIn.setEnabled(False)

            self.lineEditFrameOut.setText("")
            self.lineEditFrameOut.setEnabled(False)

            self.lineEditFrameCount.setText("")
            self.lineEditFrameCount.setEnabled(False)

        namespace = friendly_string("_".join(sections).lower().strip())

        self.lineEditNamespace.setText(namespace)
        self.set_enabled(True)

    def load_files(self, file_list, selected_file = None):
        index = 0
        selected_index = 0

        self.files = []
        self.comboBoxWorkingFile.clear()
        for item in file_list:
            set_target(item, self.working_dir)

            self.files.append(copy.copy(item))
            self.comboBoxWorkingFile.addItem(item["file_name"], userData = item)
            
            if selected_file and selected_file == item:
                selected_index = index
            index += 1

        if selected_file:
            self.comboBoxWorkingFile.setCurrentIndex(selected_index)
        else:
            self.comboBoxWorkingFile.setCurrentIndex(0)

    def set_selected(self, file_item):
        index = 0
        while index < len(self.files):
            if file_item["file_id"] == self.files[index]["file_id"]:
                self.comboBoxWorkingFile.setCurrentIndex(index)
                break
            index += 1

    def set_working_dir(self, working_dir):
        self.working_dir = working_dir

        target_dir = self.working_dir
        item = self.comboBoxWorkingFile.currentData()

        if item and target_dir:
            self.lineEditTarget.setText(resolve_content_path(item['file_path'], target_dir))

    def close_dialog(self):
        self.write_settings()
        self.close()

    def select_wcd(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if (q):
            self.set_working_dir(q)

    def set_status_text(self, status_message, error = None):
        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        self.textEditStatus.setText(text)

    def append_status(self, status_message, error = None):
        if error:       
            text = "<span style=' font-weight:100; color:#ff0000;'>{}</span><br/><br/>".format(status_message.strip())
        else:
            text = "<span style=' font-weight:100; '>{}</span><br/><bt/>".format(status_message.strip())

        cursor = QtGui.QTextCursor(self.textEditStatus.document()) 
        cursor.insertHtml(text)

    def file_loading(self, result):
        message = result["message"]
        size = result["size"]
        target = result["target"]

        self.set_status_text("{}: {} {}".format(self.target_name, message, human_size(size)))

    # first download and extract the file
    def process(self):
        #self.threadpool = QtCore.QThreadPool()
        self.set_enabled(False)
        self.textEditStatus.clear()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.process_count = 0

        server = SwingSettings.get_instance().swing_server()
        edit_api = "{}/edit".format(server)

        # download the currently selected file to the item selected in editTarget
        target = self.lineEditTarget.text().strip()

        self.target_path = os.path.split(self.lineEditTarget.text().strip())
        self.target_name = self.target_path[1]

        item = self.files[self.comboBoxWorkingFile.currentIndex()]

        self.mode = 'REMOTE'

        # check if we can load the file directly without having to download it
        # should also work to just reference a file in directly after a search
        #
        if self.is_handled():
            try:
                #edit_root = SwingSettings.get_instance().edit_root()
                test_path = item.replace("/mnt/content/productions", "Z://productions")

                if os.path.exists(test_path):
                    self.mode = "LAN"
            except:
                self.mode = "REMOTE"        

        if self.mode == 'LAN':
            self.labelTarget.setText("Source:")
            self.lineEditTarget.setText(test_path)

            if self.openRb.isChecked():
                # call handler, open downloaded file

                print("Call: Load File ... ")
                self.load_file(test_path, self.target_path)
                
            elif self.importRb.isChecked():
                # call handler importing downloaded file

                print("Call: Import  File ... ")
                self.load_file(test_path, self.target_path)

            else:
                # reference file
                print("Call: Import Ref ... ")
                self.import_ref(test_path, self.target_path)

        else:
            if "library-file" in item['file_type']:
                url = "{}/api/library_file/{}".format(edit_api, item["entity_id"])
                ## set_target(item, self.working_dir)
                worker = FileDownloader(self, item["file_id"], url, target, self.checkBoxSkipExisting.isChecked(), self.checkBoxExtractZips.isChecked(), { "fn": item['file_name'] } )
            elif "working-file" in item["file_type"]:
                #target_name = os.path.normpath(os.path.join(target_name_dir, item["name"]))
                url = "{}/api/working_file/{}".format(edit_api, item["file_id"])
                ## set_target_name(item, target_name_dir)

                worker = FileDownloader(self, item["file_id"], url, target, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())
            else:
                #target_name = os.path.normpath(os.path.join(target_name_dir, item["name"]))
                url = "{}/api/output_file/{}".format(edit_api, item["file_id"])
                ## set_target_name(item, target_name_dir)

                worker = FileDownloader(self, item["file_id"], url,  target, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())
            # file type

            self.append_status("{}: downloading to {}".format(self.target_name, target))

            worker.callback.progress.connect(self.file_loading)
            worker.callback.done.connect(self.file_loaded)
            
            item["status"] = "Busy"    

            ##worker.run() # debug
            self.set_enabled(False)
            self.threadpool.start(worker)
        # if the file is on our local network, just copy / reference it in

    # process

    #
    # we have a file or an archive now, let's see what needs to be done
    #
    def file_loaded(self, results):
        status = results["status"]
        message = results["message"]
        file_name = results["target"]
        working_dir = results["working_dir"]

        try:
            # DCC handlers
            if self.is_handled():
            # call maya handler: import into existing workspace                
                print("Check Handler ... ")
                if self.openRb.isChecked():
                    # call handler, open downloaded file

                    print("Call: Load File ... ")
                    self.load_file(file_name, working_dir)
                    
                elif self.importRb.isChecked():
                    # call handler importing downloaded file

                    print("Call: Import  File ... ")
                    self.import_file(file_name, working_dir)

                else:
                    # reference file
                    print("Call: Import Ref ... ")
                    self.import_ref(file_name, working_dir)
            else:
                self.append_status("{}: {} {}".format(file_name, working_dir, message), "error" in status)

        except:
            traceback.print_exc(file=sys.stdout)          

        self.set_enabled(True)

    def load_file(self, file_name, wcd):
        self.append_status("{}: load_file".format(self.target_name))

        if (self.handler.load_file(source = file_name, working_dir = wcd, force = self.checkBoxForce.isChecked())):
            self.append_status("Loading done")
        else:
            self.append_status("Loading error", True)

    def import_file(self, file_name, wcd):
        self.append_status("{}: import_file".format(self.target_name))
        
        if (self.handler.import_file(source = file_name, working_dir = wcd)):
            self.append_status("Loading done")
        else:
            self.append_status("Loading error", True)

    def import_ref(self, file_name, wcd):
        self.append_status("{}: import_ref".format(self.target_name))

        if self.checkBoxNamespace.checkState() == QtCore.Qt.Checked:
            namespace = self.lineEditNamespace.text()
        else:
            namespace = self.lineEditEntity.text()

        # loop through spinbox counter
        for ref in range(self.spinBoxReferenceCount.value()):
            ref_str = str(ref).zfill(4)
            ref_namespace = "{0}_{1}".format(namespace, ref_str)

            if (self.handler.import_reference(source = file_name, working_dir = wcd, namespace = ref_namespace)):
                self.append_status("{}: added ref {}".format(file_name, ref_namespace))
            else:
                self.append_status("Import error", True)

