# -*- coding: utf-8 -*-

import traceback
import sys
import os
from shutil import copy2
from PySide2.QtGui import QTextCursor
import gazu
from wildchildanimation.gui.background_workers import FileDownloader

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.maya_resource_loader_dialog import Ui_MayaResourceLoaderDialog

from wildchildanimation.gui.swing_utils import friendly_string, set_button_icon

'''
    Maya Resource Loader
    ################################################################################
'''

class ResourceLoaderDialogGUI(QtWidgets.QDialog, Ui_MayaResourceLoaderDialog):

    def __init__(self, parent, handler, resource, entity, namespace):
        super(ResourceLoaderDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowTitle(u"swing::loader")

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.threadpool = QtCore.QThreadPool.globalInstance()        

        self.labelReferenceSource.setEnabled(False)
        self.spinBoxReferenceCount.setEnabled(False)
        self.checkBoxNamespace.setEnabled(False)
        self.lineEditNamespace.setEnabled(False)

        self.read_settings()                

        self.handler = handler
        self.resource = resource
        self.resource_network_path = None
        self.namespace = namespace

        if isinstance(entity, dict):
            self.entity = entity
        else:
            self.entity = gazu.entity.get_entity(entity)

        set_button_icon(self.toolButtonTargetDir, "../resources/fa-free/solid/folder.svg")
        self.toolButtonTargetDir.clicked.connect(self.select_wcd)

        self.working_dir = SwingSettings.get_instance().swing_root()

        self.check_network()
        # self.check_working_folder()
        self.load_entity()

        self.rbImportSource.clicked.connect(self.selection_changed)
        self.rbOpenSource.clicked.connect(self.selection_changed)
        self.rbReferenceSource.clicked.connect(self.selection_changed)

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonImport.clicked.connect(self.process)

    def selection_changed(self):
        self.labelReferenceSource.setEnabled(self.rbReferenceSource.isChecked())
        self.spinBoxReferenceCount.setEnabled(self.rbReferenceSource.isChecked())
        self.checkBoxNamespace.setEnabled(self.rbReferenceSource.isChecked())
        self.lineEditNamespace.setEnabled(self.rbReferenceSource.isChecked())

    #
    # checks if we can access the resource directly
    # also determine if that file is an archive that needs to be downloaded and uncompressed
    #
    def check_network(self):
        print("check_network: Resource {}".format(self.resource))
        try:
            resource_item = self.resource["file_path"]

            if not resource_item.endswith(self.resource["file_name"]):
                resource_item = os.path.join(self.resource["file_path"], self.resource["file_name"])

            download_path = os.path.normpath(resource_item.replace('/mnt/content/productions', SwingSettings.get_instance().swing_root()))
            self.lineEditTarget.setText(download_path)

            # we assume that we are 1) on Windows, and 2) have a Z: drive mapped to content/productions
            server_path = os.path.normpath(resource_item.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))

            # we also want to know what file type we are dealing with
            fn, ext = os.path.splitext(resource_item)

            print("check_network: Checking LAN for {}{} ".format(fn, ext))
            if not SwingSettings.get_instance().is_remote() and os.path.exists(server_path):
                self.lineEditNetworkStatus.setText("Found {}".format(server_path))

                self.set_download_only(False)
                self.resource_network_path = server_path
            else:
                self.lineEditNetworkStatus.setText("Resource will be downloaded from the server")
                self.resource_network_path = None

            print("check_network: Checking Archive Status {}{} ".format(fn, ext))
            if ext in self.handler.UNARCHIVE_TYPES:
                if ext in self.handler.UNARCHIVE_TYPES:
                    self.labelArchiveMessage.setText("This file is an archive and has to be uncompressed to a local workspace")
                    self.labelArchiveMessage.setStyleSheet(u"color: rgb(170, 0, 0)")#

                    self.set_download_only(True)
                else:
                    self.labelArchiveMessage.setText("")                
                    self.labelArchiveMessage.setStyleSheet(None)

            if not ext in self.handler.SUPPORTED_TYPES:
                self.labelNetworkMessage.setText("Importing / Referencing this file directly is not supported at this time")
                self.labelNetworkMessage.setStyleSheet(None)

                self.set_download_only(True)
        except:
            traceback.print_exc(file=sys.stdout)            
        return False

    #def check_working_folder(self):
    #    self.lineEditTarget.setText(self.handler.get_scene_path())

    def load_entity(self):
        print("load_entity entity: {}".format(self.entity))

        self.project = gazu.project.get_project(self.entity["project_id"])
        self.entity_type = gazu.entity.get_entity_type(self.entity["entity_type_id"])

        self.frame_in = None
        self.frame_out = None
        self.duration = None

        self.fps = None
        self.ratio = None
        self.resolution = None

        if self.project["fps"]:
            self.fps = self.project["fps"]

        if self.project["ratio"]:
            self.ratio = self.project["ratio"]

        if self.project["resolution"]:
            self.resolution = self.project["resolution"]

        # print("Check NameSpace Project {}".format(self.project))
        # print("Check NameSpace Entity Type {}".format(self.entity_type))
        self.lineEditSource.setText(self.resource["file_name"])

        self.sections = []

        if "code" in self.project:
            self.project_name = self.project["code"]
        else:
            self.project_name = self.project["name"]

        ## self.sections.append(self.project_name)                                
        if self.entity["type"] == "Asset":
            self.entity_type_name = self.entity_type["name"]

            # check if we have a shortened form of the name
            if self.entity_type_name in self.handler.ASSET_TYPE_LOOKUP:
                self.entity_type_name = self.handler.ASSET_TYPE_LOOKUP[self.entity_type_name]

            if not self.project_name in self.entity["name"]:
                self.sections.append(self.project_name) 

            if not self.entity_type_name in self.entity["name"]:
                self.sections.append(self.entity_type_name)
                
            self.sections.append(friendly_string(self.entity["name"]))

            self.lineEditNamespace.setText(friendly_string("_".join(self.sections).lower()))
        else:
            try:
                self.sequence = gazu.entity.get_entity(self.entity["parent_id"])
                print("Loaded Sequence {}".format(self.sequence))

                try:
                    self.episode = gazu.entity.get_entity(self.sequence["parent_id"])
                except:
                    # episode not found
                    self.episode = None
            except:
                self.sequence = None
            # parent sequence not found

            if self.episode:
                if not self.project_name in self.episode["name"]:
                    self.sections.append(self.project_name) 

                self.sections.append(self.episode["name"])

            if self.sequence:
                self.sections.append(self.sequence["name"])

            self.sections.append(self.entity["name"])

        if not self.namespace:
            self.namespace = friendly_string("_".join(self.sections).lower().strip())

        self.load_namespace()
        self.set_enabled(True)

    def load_namespace(self):
        self.lineEditNamespace.setText(self.namespace)            

    def set_download_only(self, only_download):
        if only_download:
            self.rbOpenSource.setEnabled(False)
            self.rbImportSource.setEnabled(False)
            self.rbReferenceSource.setEnabled(False)

            #self.spinBoxReferenceCount.setEnabled(False)
            #self.checkBoxNamespace.setEnabled(False)
            #self.lineEditNamespace.setEnabled(False)
        else:
            self.rbOpenSource.setEnabled(True)
            self.rbImportSource.setEnabled(True)
            self.rbReferenceSource.setEnabled(True)

            #self.spinBoxReferenceCount.setEnabled(True)
            #self.checkBoxNamespace.setEnabled(True)
            #self.lineEditNamespace.setEnabled(True)            

    def set_enabled(self, status):
        self.lineEditSource.setEnabled(status)

        self.textEditInfo.setEnabled(status)
        self.lineEditTarget.setEnabled(status)
        self.toolButtonTargetDir.setEnabled(status)
        
        self.rbOpenSource.setEnabled(status)
        self.rbImportSource.setEnabled(status)
        self.rbReferenceSource.setEnabled(status)

        #self.spinBoxReferenceCount.setEnabled(status)
        #self.checkBoxNamespace.setEnabled(status)
        #self.lineEditNamespace.setEnabled(status)

        self.checkBoxSkipExisting.setEnabled(status)
        self.checkBoxExtractZips.setEnabled(status)
        self.checkBoxForce.setEnabled(status)

        self.pushButtonImport.setEnabled(status)
        self.pushButtonCancel.setEnabled(status)        

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

        if self.rbOpenSource.isChecked():
            self.settings.setValue("load_type", "open")

        elif self.rbImportSource.isChecked():
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
                self.rbOpenSource.setChecked(True)
            elif "import" in load_type:
                self.rbImportSource.setChecked(True)
            else:
                self.rbReferenceSource.setChecked(True)
            self.selection_changed()

            self.settings.endGroup()              
        except:
            traceback.print_exc(file=sys.stdout)

    def open_url(self, url):
        link = QtCore.QUrl(self.url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')        

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
        self.textEditStatus.moveCursor(QTextCursor.End)
        cursor.insertHtml(text)

    #def process(self):
    #
    #    mutils.executeDeferred(lambda: self.background_process())

    #def background_process(self):
    def process(self):        
        print("background_process::start")
        self.set_enabled(False)
        try:
            try:
                target_path = self.handler.get_working_file()
                force_create = False
                if not target_path or len(target_path) == 0:
                    if self.resource and "target_path" in self.resource:
                        check = QtWidgets.QMessageBox.question(self, 'Task not Found', 'No scene found. Would you like to create a new scene?\n\nName: {}\nDir: {}'.format(os.path.basename(self.resource["target_path"]), os.path.dirname(self.resource["target_path"])))  

                        if check == QtWidgets.QMessageBox.Yes:
                            force_create = True
                            target_path = self.resource["target_path"]

                            self.copy_file(self.resource_network_path, target_path, force_create)
                            print("Copied to: {}".format(target_path))

                            #print("background_process::Didn't think so ")
                            #return False                       
                    else:      
                        # target_path = self.resource["target_path"]

                        QtWidgets.QMessageBox.warning(self, 'Scene Error', 'No scene found. Please save the current scene or task first')        
                        return False

                print("background_process::resource network path = {} target path = {}".format(self.resource_network_path, target_path))                

                #if not self.resource_network_path:
                if self.rbOpenSource.isChecked():
                    print("background_process::open source")

                    if os.path.exists(target_path) and not force_create:
                        print("background_process::Local file already exists, check with user ... ")
                        reply = QtWidgets.QMessageBox.question(self, 'Confirm Overwrite', 'This will overwrite the existing file {}\r\n\r\nAre you sure you wish to continue ?'.format(target_path))
                        if not reply == QtWidgets.QMessageBox.Yes:
                            print("background_process::Didn't think so ")
                            return False

                    if not self.resource_network_path:
                        print("background_process::Not on shared drive, have to download ... ")

                        self.download_file()
                        return False
                    else:
                        print("background_process::Just copy it from the shared drive ")
                        self.copy_file(self.resource_network_path, target_path)
                    # check if remote

                    # open from Z: 
                    
                elif self.rbImportSource.isChecked():
                    print("background_process::import resource")

                    if not self.resource_network_path:
                        print("Not on Z: drive, have to download ... ")

                        self.download_file()
                        return False

                    self.import_file()
                elif self.rbReferenceSource.isChecked():
                    print("background_process::reference resource")

                    if not self.resource_network_path:
                        print("Not on Z: drive, have to download ... ")

                        self.download_file()
                        return False
                    # check if remote

                    self.import_ref()
            except:
                traceback.print_exc(file=sys.stdout)          

        finally:
            self.set_enabled(True)
        # all done

    #copy file from server 
    def copy_file(self, source, target, force_create = False):
        print("copy_file file {} to {}".format(source, target))

        target_dir = os.path.dirname(target)
        if not os.path.exists(target_dir):
            self.append_status("creating dir {}".format(target_dir))
            os.makedirs(target_dir, mode=0o777)

        copy2(source, target, follow_symlinks=True)
        self.append_status("copy_file {}: load_file".format(source))

        if (self.handler.load_file(source = target, force = self.checkBoxForce.isChecked() or force_create)):
            self.append_status("copy_file loading done")
        else:
            self.append_status("copy_file loading error", True)

        self.set_enabled(True)

    def download_file(self):
        server = SwingSettings.get_instance().swing_server()
        edit_api = "{}/edit".format(server)
        target_path = self.lineEditTarget.text()

        print("download_file::target path = {}".format(target_path))
        print("download_file::resource {}".format(self.resource))

        if "library-file" in self.resource['file_type']:
            url = "{}/api/library_file/{}".format(edit_api, self.resource["entity_id"])
            ## set_target(item, self.working_dir)
            worker = FileDownloader(self, self.resource["file_id"], url, target_path, self.checkBoxSkipExisting.isChecked(), self.checkBoxExtractZips.isChecked(), { "fn": self.resource['file_name'] } )

        elif "working-file" in self.resource["file_type"]:
            #target_name = os.path.normpath(os.path.join(target_name_dir, item["name"]))
            url = "{}/api/working_file/{}".format(edit_api, self.resource["file_id"])
            ## set_target_name(item, target_name_dir)

            worker = FileDownloader(self, self.resource["file_id"], url, target_path, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())
        else:
            #target_name = os.path.normpath(os.path.join(target_name_dir, item["name"]))
            url = "{}/api/output_file/{}".format(edit_api, self.resource["file_id"])
            ## set_target_name(item, target_name_dir)

            worker = FileDownloader(self, self.resource["file_id"], url,  target_path, skip_existing = self.checkBoxSkipExisting.isChecked(), extract_zips = self.checkBoxExtractZips.isChecked())
            # file type

        self.append_status("{}: downloading to {}".format(self.resource["file_name"], target_path))

        worker.callback.progress.connect(self.file_loading)
        worker.callback.done.connect(self.file_loaded)
        
        self.resource["status"] = "Busy"    

        ##worker.run() # debug
        self.set_enabled(False)
        if self.resource["file_size"]:
            file_size = self.resource["file_size"]
        else:
            file_size = 1

        self.progressBar.setRange(0, file_size)
        self.threadpool.start(worker)  

    def file_loading(self, result):
        #message = result["message"]
        size = result["size"]
        # target = result["target"]

        print("File Loading {}".format(result))
        self.progressBar.setValue(size)
        #self.set_status_text("{}: {} {}".format(self.target_item["target_path"], message, human_size(size)))        

    #
    # we have a file or an archive now, let's see what needs to be done
    #
    def file_loaded(self, results):
        print("file_loaded:: {}".format(results))

        file_name = results["target"]
        self.resource_network_path = file_name
        print("file_loaded:: {}".format(file_name))
        try:
            if self.rbOpenSource.isChecked():
                print("file_loaded:: {}".format("open source file"))
                self.load_file()

            elif self.rbImportSource.isChecked():
                print("file_loaded:: {}".format("import source file"))

                self.import_file()

            else:
                print("file_loaded:: {}".format("reference source file"))

                self.import_ref()

        except:
            traceback.print_exc(file=sys.stdout)          

    def load_file(self):
        source = self.resource_network_path
        if not source:
            source = self.resource["target_path"]

        self.append_status("load_file {}: ".format(source))
        ## print("load_file:: {}".format(source))

        if (self.handler.load_file(source = source, force = self.checkBoxForce.isChecked())):
            self.append_status("load_file loaded file {}".format(source))
        else:
            self.append_status("load_file - Import error", True)

        self.set_enabled(True)

    def import_file(self):
        source = self.resource_network_path
        if not source:
            source = self.resource["target_path"]

        self.append_status("import_file {}:".format(source))
        ## print("load_file:: {}".format(source))

        if (self.handler.import_file(source = source)):
            self.append_status("import_file added file {}".format(source))
        else:
            self.append_status("import_file - Import error", True)

        self.set_enabled(True)

    def import_ref(self):
        self.append_status("import_ref {}: ".format(self.resource["file_name"]))
        ## print("load_file:: {}".format(self.resource["file_name"]))

        if self.checkBoxNamespace.checkState() == QtCore.Qt.Checked:
            namespace = self.lineEditNamespace.text()
        else:
            namespace = self.lineEditEntity.text()

        # loop through spinbox counter
        for ref in range(self.spinBoxReferenceCount.value()):
            ref_str = str(ref).zfill(4)
            ref_namespace = "{0}_{1}".format(namespace, ref_str)

            if (self.handler.import_reference(source = self.resource_network_path, namespace = ref_namespace)):
                self.append_status("import_ref {}: added ref {}".format(self.resource_network_path, ref_namespace))
            else:
                self.append_status("import_ref - Import error", True)

        self.set_enabled(True)
