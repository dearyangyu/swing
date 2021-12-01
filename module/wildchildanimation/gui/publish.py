# -*- coding: utf-8 -*-

import traceback
import sys
import os
import glob

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_tables import SecondaryAssetsFileTableModel

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

from wildchildanimation.gui.background_workers import SoftwareLoader, StatusTypeLoader, TaskFileInfoThread, TaskTypeLoader, WorkingFileUploader
from wildchildanimation.gui.swing_utils import set_button_icon
from wildchildanimation.gui.image_loader import PreviewImageLoader
from wildchildanimation.gui.publish_dialog import Ui_PublishDialog
from wildchildanimation.gui.file_selector import FileSelectDialog
from wildchildanimation.gui.upload_monitor import UploadMonitorDialog

class PublishDialogGUI(QtWidgets.QDialog, Ui_PublishDialog):

    project_root = None
    last_work_dir = None
    last_output_dir = None
    default_software = None

    working_filter = None
    output_filter = None

    wf_excluded = []
    of_included = []

    def __init__(self, parent = None, task = None, task_types = None, status_types = None, upload_monitor = None):
        super(PublishDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method    

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setAcceptDrops(True)
        self.read_settings()

        if not upload_monitor:
            self.monitor = UploadMonitorDialog(self)
        else:
            self.monitor = upload_monitor

        self.task = task
        if not task_types:
            self.task_types = TaskTypeLoader(self).run()["results"]
        else:
            self.task_types = task_types

        if not status_types:
            self.status_types = StatusTypeLoader(self).run()["results"]
        else:
            self.status_types = task_types

        self.software = SoftwareLoader(self).run()["software"]

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.references = []

        self.working_filter = FileSelectDialog(self)

        self.workingFileSelectButton.clicked.connect(self.select_working_file)
        set_button_icon(self.workingFileSelectButton, "../resources/fa-free/solid/folder.svg")

        self.workingDirSelectButton.clicked.connect(self.select_working_dir)
        set_button_icon(self.workingDirSelectButton, "../resources/fa-free/solid/folder.svg")

        self.toolButtonWorkingDirFilter.clicked.connect(self.show_working_filter)
        set_button_icon(self.toolButtonWorkingDirFilter, "../resources/fa-free/solid/list.svg")

        self.output_filter = FileSelectDialog(self)

        self.outputFileSelectButton.clicked.connect(self.select_output_file)
        set_button_icon(self.outputFileSelectButton, "../resources/fa-free/solid/folder.svg")

        self.outputDirSelectButton.clicked.connect(self.select_output_dir)
        set_button_icon(self.outputDirSelectButton, "../resources/fa-free/solid/folder.svg")   

        self.toolButtonReviewFilter.clicked.connect(self.show_output_filter)
        set_button_icon(self.toolButtonReviewFilter, "../resources/fa-free/solid/list.svg")


        self.comboBoxSoftware.currentIndexChanged.connect(self.software_changed)  
        ##self.projectFileToolButton.clicked.connect(self.select_working_file)
        #self.fbxFileToolButton.clicked.connect(self.select_fbx_file)
        #self.reviewFileToolButton.clicked.connect(self.select_output_file)
        self.referencesAddPushButton.clicked.connect(self.select_references)
        self.referencesRemovePushButton.clicked.connect(self.remove_references)

        self.load_reference_table()

        self.pushButtonOK.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.set_enabled(False)       
        self.labelOutputFilesMessage.setText("")
        self.labelWorkingFilesMessage.setText("") 

        task_loader = TaskFileInfoThread(self, self.task, self.project_root)
        task_loader.callback.loaded.connect(self.task_loaded)
        self.threadpool.start(task_loader)  

        # QtCore.QTimer.singleShot(0, lambda: self.treeView.expandRecursively(model.index(root_dir.path()), 10))      

    def set_wf_exclude(self, excluded):
        self.wf_excluded = excluded
    
    def set_of_include(self, included):
        self.of_included = included

    def set_enabled(self, enabled):
        self.lineEditProject.setEnabled(enabled)
        self.lineEditFor.setEnabled(enabled)        
        self.tabWidget.setEnabled(enabled)        
        self.comboBoxSoftware.setEnabled(enabled)       

        self.radioButtonWorkingFile.setEnabled(enabled)       
        self.workingFileEdit.setEnabled(enabled)        
        self.workingFileSelectButton.setEnabled(enabled)        

        self.radioButtonWorkingDir.setEnabled(enabled)        
        self.workingDirEdit.setEnabled(enabled)        
        self.workingDirSelectButton.setEnabled(enabled)        

        self.groupBoxOutputFiles.setEnabled(enabled)        

        self.reviewTitleLineEdit.setEnabled(enabled)        
        self.comboBoxTaskStatus.setEnabled(enabled)        

        self.radioButtonOutputFile.setEnabled(enabled)        
        self.outputFileEdit.setEnabled(enabled)        
        self.outputFileSelectButton.setEnabled(enabled)        

        self.radioButtonOutputDir.setEnabled(enabled)        
        self.outputDirEdit.setEnabled(enabled)        
        self.outputDirSelectButton.setEnabled(enabled)        

        self.commentEdit.setEnabled(enabled)        
        self.pushButtonOK.setEnabled(enabled)        

    
    def software_changed(self, index):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        self.settings.setValue("software", self.comboBoxSoftware.currentText())
        self.settings.endGroup()
    
    def load_preview_image(self, pixmap):
        """
        Set the image to the pixmap
        :return:
        """
        self.labelIcon.setPixmap(pixmap)   

    def task_loaded(self, results):
        self.task = results["task"]

        name = ""
        if "entity_type" in self.task:
            name = '{} {}'.format(name, self.task["entity_type"]["name"])
        else:
            name = '{} {}'.format(name, self.task["entity_type_name"])

        if "entity" in self.task:
            name = '{} {}'.format(name, self.task["entity"]["name"])
        else:
            name = '{} {}'.format(name, self.task["entity_name"])

        if "task_type" in self.task:
            task_type = self.task["task_type"]["name"]
            name = '{} {}'.format(name, self.task["task_type"]["name"])   
        else:
            task_type = self.task["task_type_name"]

        name = '{} {}'.format(name, task_type)   
        if "final" in task_type.lower():
            self.output_mode = "render"
            self.groupBoxOutputFiles.setTitle("Final Output")
        else:
            self.output_mode = "wip"
            self.groupBoxOutputFiles.setTitle("Media for Review")

        self.lineEditSelection.setText(name)
        self.lineEditFor.setText("{}: {}".format(self.task["entity_type"]["name"], self.task["entity"]["name"]))        
        self.lineEditProject.setText(self.task["project"]["name"])

        self.reviewTitleLineEdit.setText("Review: {}: {}".format(self.task["entity_type"]["name"], self.task["entity"]["name"]))

        # load artist allowed task status codes
        for item in self.status_types:
            self.comboBoxTaskStatus.addItem(item["name"], userData = item) 
        
        status_index = self.comboBoxTaskStatus.findText("Waiting for Approval")
        if status_index >= 0:
            self.comboBoxTaskStatus.setCurrentIndex(status_index)        
        else:
            self.comboBoxTaskStatus.setCurrentIndex(0)                    

        idx = 0
        sel = -1
        for item in self.software:
            self.comboBoxSoftware.addItem(item["name"], userData = item)
            if self.default_software in item["name"]:
                sel = idx
            idx += 1
        if sel >= 0:
            self.comboBoxSoftware.setCurrentIndex(sel)
        
        #self.lineEditTask.setText(name)
        if self.task["entity"]["preview_file_id"] and self.task["entity"]["preview_file_id"] != '':
            imageLoader = PreviewImageLoader(self, self.task["entity"]["preview_file_id"])
            imageLoader.callback.results.connect(self.load_preview_image)
            self.threadpool.start(imageLoader)

        self.setWindowTitle("swing: publisher - {}".format(name))
        self.set_enabled(True)


    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Drop files directly onto the widget
        File locations are stored in fname
        :param e:
        :return:
        """

        if e.mimeData().hasUrls:        
            files = []
            for url in e.mimeData().urls():
                fname = str(url.toLocalFile())
                files.append(fname)

            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()

            if self.tabWidget.geometry().contains(e.pos()):
                file_type = "working"
            elif self.groupBoxOutputFiles.geometry().contains(e.pos()):
                file_type = "output"

            self.process_dropped_files(files, file_type)
        else:
            e.ignore()

    def process_dropped_files(self, file_list, file_type):
        for selected_file in file_list:

            # if directory set rb
            if os.path.isfile(selected_file):
                if "working" in file_type:
                    self.set_working_file(selected_file)
                else:
                    self.set_output_file(selected_file)

                return True

            if os.path.isdir(selected_file):
                if "working" in file_type:
                    self.set_working_dir(selected_file)
                else:
                    self.set_output_dir(selected_file)

                return True

    def set_working_file(self, selected_file):
        self.radioButtonWorkingFile.setChecked(True)
        self.radioButtonWorkingDir.setChecked(False)

        self.workingDirEdit.setText("")
        self.workingFileEdit.setText(selected_file)

        self.labelWorkingFilesMessage.setText("")

    def set_working_dir(self, selected_dir):
        self.radioButtonWorkingFile.setChecked(False)
        self.radioButtonWorkingDir.setChecked(True)

        self.scan_working_dir(selected_dir)
        self.workingDirEdit.setText(selected_dir)
        self.workingFileEdit.setText("")

    def set_output_file(self, selected_file):
        self.radioButtonOutputFile.setChecked(True)
        self.radioButtonOutputDir.setChecked(False)

        self.outputDirEdit.setText("")
        self.outputFileEdit.setText(selected_file)

        if os.path.exists(selected_file):
            file_base = os.path.basename(selected_file)
            file_name, file_ext = os.path.splitext(file_base)

            self.reviewTitleLineEdit.setText("Review: {}".format(file_name))

    def set_output_dir(self, selected_dir):
        self.radioButtonOutputFile.setChecked(False)
        self.radioButtonOutputDir.setChecked(True)

        self.scan_output_dir(selected_dir, self.of_included)
        self.outputDirEdit.setText(selected_dir)
        self.outputFileEdit.setText("")

    def scan_working_dir(self, directory):
        self.working_filter.set_root(directory)
        self.working_filter.scan_working_files()

        #self.media_files = []

        #self.media_files += filter(os.path.isfile, glob.glob(directory + '/*.mp4'))
        #self.media_files += filter(os.path.isfile, glob.glob(directory + '/*.mov'))

        #self.media_files = sorted(self.media_files, key = os.path.getmtime)

        #if len(self.media_files) > 0:
        #    self.labelReviewFile.setText("Found review media to upload")
        #    self.set_output_file(self.media_files[len(self.media_files)-1])

        self.labelWorkingFilesMessage.setText("Compress and upload directory: {}".format(directory))

    def scan_output_dir(self, directory, excluded):
        self.output_filter.set_root(directory)
        self.output_filter.scan_output_files()

        #self.media_files = []

        #self.media_files += filter(os.path.isfile, glob.glob(directory + '/*.mp4'))
        #self.media_files += filter(os.path.isfile, glob.glob(directory + '/*.mov'))

        #self.media_files = sorted(self.media_files, key = os.path.getmtime)

        #if len(self.media_files) > 0:
        #    self.labelReviewFile.setText("Found review media to upload")
        #    self.set_output_file(self.media_files[len(self.media_files)-1])

        self.labelOutputFilesMessage.setText("Compress and upload directory: {}".format(directory))

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("last_work_dir", self.last_work_dir)
        self.settings.setValue("last_output_dir", self.last_output_dir)
        #self.settings.setValue("software", self.comboBoxSoftware.currentText())

        #self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        #self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.project_root = self.settings.value("projects_root", os.path.expanduser("~"))
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        ##self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))

        self.last_work_dir = self.settings.value("last_work_dir", os.path.expanduser("~"))
        self.last_output_dir = self.settings.value("last_output_dir", os.path.expanduser("~"))
        self.default_software = self.settings.value("software", "")

        self.settings.endGroup()              

    def close_dialog(self):
        self.write_settings()
        self.close()

    def file_loaded(self, resuls):
        status = resuls["status"]
        if "ok" in status:
            self.process_count -= 1

        if self.process_count == 0:
            self.threadpool.waitForDone()
            QtWidgets.QMessageBox.question(self, 'Swing: Publisher', 'Task {} succesfully published\r\nAll files uploaded, thank you'.format(self.lineEditSelection.text()), QtWidgets.QMessageBox.Ok)
            self.pushButtonCancel.setEnabled(True)

    def get_software(self):
        return self.comboBoxSoftware.currentData(QtCore.Qt.UserRole)        

    def show_working_filter(self):
        self.working_filter.pushButtonWorkingFiles.setVisible(True)
        self.working_filter.pushButtonOutputFiles.setVisible(False)
        self.working_filter.pushButtonZip.setVisible(True)

        if self.working_filter.show():
            for item in self.working_filter.treeView.model().checkStates:
                print(item)

    def show_output_filter(self):
        self.working_filter.pushButtonWorkingFiles.setVisible(False)
        self.working_filter.pushButtonOutputFiles.setVisible(True)
        self.working_filter.pushButtonZip.setVisible(True)

        if self.output_filter.show():
            for item in self.output_filter.treeView.model().checkStates:
                print(item)                
        

    # ToDo: Desktop Only, Move to Swing Studio Handler
    def process(self):
        self.pushButtonCancel.setEnabled(False)

        self.process_count = 0
        self.queue = []

        server = SwingSettings.get_instance().swing_server()
        edit_api = "{}/edit".format(server)        


        task_comments = self.commentEdit.toPlainText().strip()

        if self.groupBoxWorkingFiles.isChecked():        

            #
            # working files
            #
            if len(self.workingFileEdit.text()) > 0:
                source = self.workingFileEdit.text()

                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_name, file_ext = os.path.splitext(file_base)                

                    worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, self.get_software()["name"], 
                        comment = task_comments, mode = "working", task_status = self.comboBoxTaskStatus.currentData(QtCore.Qt.UserRole)["id"])
                    worker.callback.progress.connect(self.monitor.file_loading)
                    worker.callback.done.connect(self.monitor.file_loaded)

                    ## dialog.add_item(source, "Pending")

                    self.process_count += 1       
                    self.queue.append(worker)         
                    #self.threadpool.start(worker)
            #
            # working dir
            #
            elif len(self.workingDirEdit.text()) > 0:
                source = self.workingDirEdit.text()

                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_path = os.path.dirname(source)
                    file_name, file_ext = os.path.splitext(file_base)                

                    worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, software_name = self.get_software()["name"], 
                        comment = task_comments, mode = "working", file_model = self.working_filter.treeView.model(), task_status = self.comboBoxTaskStatus.currentData(QtCore.Qt.UserRole)["id"])

                    worker.callback.progress.connect(self.monitor.file_loading)
                    worker.callback.done.connect(self.monitor.file_loaded)

                    target = "{}/{}.zip".format(os.path.dirname(source), file_base)
                    ## dialog.add_item(target, "Pending")

                    self.process_count += 1                
                    self.queue.append(worker)
                    #self.threadpool.start(worker)
                    ## worker.run()     
        ### Working files        

        if self.groupBoxOutputFiles.isChecked():
            #
            # output files
            #

            if len(self.outputFileEdit.text()) > 0:
                source = self.outputFileEdit.text()
                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_name, file_ext = os.path.splitext(file_base)

                    worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, self.get_software()["name"],  
                        comment=task_comments, mode = self.output_mode, task_status = self.comboBoxTaskStatus.currentData(QtCore.Qt.UserRole)["id"])

                    worker.callback.progress.connect(self.monitor.file_loading)
                    worker.callback.done.connect(self.monitor.file_loaded)
                    ## dialog.add_item(source, "Pending")    

                    self.process_count += 1
                    self.queue.append(worker)         
                    #self.threadpool.start(worker)   
                
            # output dir
            elif len(self.outputDirEdit.text()) > 0:
                source = self.outputDirEdit.text()
                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_name, file_ext = os.path.splitext(file_base)

                    worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, software_name = self.get_software()["name"], 
                        comment=task_comments, mode = self.output_mode, file_model = self.output_filter.treeView.model(), task_status = self.comboBoxTaskStatus.currentData(QtCore.Qt.UserRole)["id"])

                    worker.callback.progress.connect(self.monitor.file_loading)
                    worker.callback.done.connect(self.monitor.file_loaded)
                    ## dialog.add_item(source, "Pending")    

                    self.process_count += 1
                    #self.threadpool.start(worker)    
                    self.queue.append(worker)         
                    # worker.run()               

        model = self.tableViewReferences.model().items
        for item in model:
                source = item["item"]
                mode = item["type"]

                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_name, file_ext = os.path.splitext(file_base)

                    worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, self.get_software()["name"], comment=task_comments, 
                        mode = mode, task_status = self.comboBoxTaskStatus.currentData(QtCore.Qt.UserRole)["id"])                    
                        
                    worker.callback.progress.connect(self.monitor.file_loading)
                    worker.callback.done.connect(self.monitor.file_loaded)
                    ## dialog.add_item(source, "Pending")   

                    self.process_count += 1
                    #self.threadpool.start(worker)      
                    self.queue.append(worker)                     

        if len(self.queue) > 0:
            self.monitor.set_queue(self.queue)
            self.monitor.reset_progressbar()            
            self.monitor.show()

            self.hide()            

            for item in self.queue:
                self.threadpool.start(item)
                #self.threadpool.waitForDone()


    def get_references(self):
        return self.references

    def select_references(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_work_dir:
            self.last_work_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileNames(self, "Add secondary assets", self.last_work_dir, "Alembic file (*.abc);;FBX files (*.fbx);;Images (*.png *.jpg);;Zip files (*.zip);;All Files (*.*)")
        if not (q):
            return 

        references = []
        for item in q[0]:
            references.append(item)

        if len(references) > 0:
            self.add_references(references)

    def add_reference_file(self, file_name, file_type):
        item = { "item": file_name, "type": file_type }
        if not item in self.references:
            self.references.append(item)

    def load_reference_table(self):
        if not self.task or not  "entity" in self.task:
            return 

        self.tableViewReferences.setModel(SecondaryAssetsFileTableModel(self, self.references, self.task["entity"]))

        self.tableViewReferences.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableViewReferences.setSortingEnabled(True)
        self.tableViewReferences.sortByColumn(SecondaryAssetsFileTableModel.COL_FILE_NAME, QtCore.Qt.DescendingOrder)
        self.tableViewReferences.setColumnWidth(SecondaryAssetsFileTableModel.COL_FILE_NAME, 100)

        self.tableViewReferences.resizeRowsToContents()
        self.tableViewReferences.verticalHeader().setDefaultSectionSize(self.tableViewReferences.verticalHeader().minimumSectionSize())        
        self.tableViewReferences.horizontalHeader().setSectionResizeMode(SecondaryAssetsFileTableModel.COL_FILE_NAME, QtWidgets.QHeaderView.Stretch)

        self.tableViewReferences.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableViewReferences.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)             


    def add_references(self, items):
        for item in items:
            fn, fext = os.path.splitext(item)
            fext = fext.lower()

            if ".abc" == fext:
                self.add_reference_file(item, "Alembic")

            elif ".fbx" == fext:
                self.add_reference_file(item, "FBX")

            elif fext in [".png", ".jpg", ".bmp" ]:
                self.add_reference_file(item, "Image")

            elif ".zip" == fext:
                self.add_reference_file(item, "Zip")

            else:
                print("Reference type {}.{} not supported yet".format(fn, fext))

        self.load_reference_table()

    def remove_references(self):
        for item in self.tableViewReferences.model().items:
            if item["selected"]:
                self.references.remove(item)
        self.load_reference_table()

    def select_working_file(self):
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Select Working File for Task", self.last_work_dir, "Maya Ascii (*.ma), Maya Binary (*.mb), All Files (*.*)")
        if (q and q[0] != ''):        
            self.last_work_dir = q[0]
            self.set_working_file(q[0])

    def select_working_dir(self):
        working_dir = self.workingDirEdit.text()
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Working Directory for Task", working_dir)
        if q:
            self.last_work_dir = q
            self.set_working_dir(q)


    def select_fbx_file(self):
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Output File", self.last_work_dir, "FBX (*.fbx), All Files (*.*)")
        if (q and q[0] != ''):     
            self.fbxFileEdit.setText(q[0])
            self.last_work_dir = q[0]

    def select_output_file(self):
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Review File", self.last_output_dir, "Images (*.bmp, *.jpg, *.png), Videos (*.mp4), All Files (*.*)")
        if (q and q[0] != ''):     
            self.last_output_dir = q[0]
            self.set_output_file(q[0])

    def select_output_dir(self):
        working_dir = self.outputDirEdit.text()
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Media Directory", working_dir)
        if q:
            self.last_output_dir = q
            self.set_output_dir(q)

                