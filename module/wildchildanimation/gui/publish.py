# -*- coding: utf-8 -*-

import traceback
import sys
import os
import glob

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

from wildchildanimation.gui.image_loader import *
from wildchildanimation.gui.swing_utils import *

from wildchildanimation.gui.publish_dialog import Ui_PublishDialog
from wildchildanimation.gui.upload_monitor import UploadMonitorDialog

from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

class PublishDialogGUI(QtWidgets.QDialog, Ui_PublishDialog):

    projet_root = None
    last_work_dir = None
    last_output_dir = None

    def __init__(self, parent = None, project_nav = None, handler = None, task = None):
        super(PublishDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method    

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setAcceptDrops(True)
        self.read_settings()

        self.nav = project_nav
        self.handler = handler
        self.task = task

        project = self.nav.get_project()
        if project:
            self.lineEditProject.setText(project["name"])

        episode = self.nav.get_episode()
        if episode:
            self.lineEditFor.setText("Episode {}".format(episode["name"]))

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.references = []


        ##self.projectFileToolButton.clicked.connect(self.select_working_file)
        #self.fbxFileToolButton.clicked.connect(self.select_fbx_file)
        #self.reviewFileToolButton.clicked.connect(self.select_output_file)
        ##self.referencesAddPushButton.clicked.connect(self.select_references)

        model = QtGui.QStandardItemModel(self.referencesListView)
        self.referencesListView.setModel(model)        

        #self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        #self.toolButtonWeb.clicked.connect(self.open_url)
        #self.toolButtonWeb.setEnabled(False)

        self.pushButtonOK.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.close_dialog)
        
        self.request = self.handler.on_save()           

        task_loader = TaskFileInfoThread(self, self.task, self.project_root)
        task_loader.callback.loaded.connect(self.task_loaded)
        self.threadpool.start(task_loader)        


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

        self.workingFileSelectButton.clicked.connect(self.select_working_file)
        self.workingFileSelectButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))

        self.workingDirSelectButton.clicked.connect(self.select_working_dir)
        self.workingDirSelectButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))

        self.outputFileSelectButton.clicked.connect(self.select_output_file)
        self.outputFileSelectButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon))

        self.outputDirSelectButton.clicked.connect(self.select_output_dir)
        self.outputDirSelectButton.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon))


        # load artist allowed task status codes
        idx = 0
        sel = -1
        for item in self.nav.get_user_task_status():
            self.comboBoxTaskStatus.addItem(item["name"], userData = item) 

            # remember wfa as default
            if "Waiting for Approval" in item["name"]:
                sel = idx
            idx += 1

        if sel >= 0:
            self.comboBoxTaskStatus.setCurrentIndex(sel)

        idx = 0
        sel = -1
    
        for item in self.nav.get_software():
            self.comboBoxSoftware.addItem(item["name"], userData = item)

            if self.software in item["name"]:
                sel = idx
            
            idx += 1

        if sel >= 0:
            self.comboBoxSoftware.setCurrentIndex(sel)
        
        #self.lineEditTask.setText(name)
        if self.task["entity"]["preview_file_id"] and self.task["entity"]["preview_file_id"] != '':
            imageLoader = PreviewImageLoader(self, self.task["entity"]["preview_file_id"])
            imageLoader.callback.results.connect(self.load_preview_image)
            #imageLoader.run()
            self.threadpool.start(imageLoader)


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
        print(e.source())
        print(e.pos())

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

        self.labelZipMessage.setText("")

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

            self.reviewTitleLineEdit.setText(file_name)


    def set_output_dir(self, selected_dir):
        self.radioButtonOutputFile.setChecked(False)
        self.radioButtonOutputDir.setChecked(True)

        self.outputDirEdit.setText(selected_dir)
        self.outputFileEdit.setText("")

    def scan_working_dir(self, directory):
        media_files = []

        for file in glob.glob("{}/*.mp4".format(directory)):
            media_files.append(file)

        for file in glob.glob("{}/*.mov".format(directory)):
            media_files.append(file)

        if len(media_files) > 0:
            self.labelReviewFile.setText("Found review media to upload")
            self.set_output_file(media_files[0])

        self.labelZipMessage.setText("Compress and upload directory: {}".format(directory))


    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("Publish")

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("last_work_dir", self.last_work_dir)
        self.settings.setValue("last_output_dir", self.last_output_dir)
        self.settings.setValue("software", self.comboBoxSoftware.currentText())

        #self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        #self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()

        self.project_root = self.settings.value("projects_root", os.path.expanduser("~"))
        self.settings.beginGroup("Publish")

        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))

        self.last_work_dir = self.settings.value("last_work_dir", os.path.expanduser("~"))
        self.last_output_dir = self.settings.value("last_output_dir", os.path.expanduser("~"))
        self.software = self.settings.value("software", "")

        self.settings.endGroup()              

    def close_dialog(self):
        self.write_settings()
        self.close()

    def file_loaded(self, resuls):
        status = resuls["status"]
        if "ok" in status:
            self.process_count -= 1
            if self.process_count == 0:
                QtWidgets.QMessageBox.question(self, 'Publishing complete', 'All files uploaded, thank you', QtWidgets.QMessageBox.Ok)
                self.pushButtonCancel.setEnabled(True)

    def get_software(self):
        return self.comboBoxSoftware.currentData(QtCore.Qt.UserRole)        

    def process(self):
        self.pushButtonCancel.setEnabled(False)
        self.process_count = 0

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')        

        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)        

        #self, parent, task, source, software_name, comment, email, password
        dialog = UploadMonitorDialog(self, self.task)

        #
        # working files
        #
        if len(self.workingFileEdit.text()) > 0:
            source = self.workingFileEdit.text()

            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)                

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, self.get_software()["name"], self.commentEdit.toPlainText().strip(), email, password)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")

                self.process_count += 1                
                self.threadpool.start(worker)
                ##worker.run()
        #
        # working dir
        #
        elif len(self.workingDirEdit.text()) > 0:
            source = self.workingDirEdit.text()

            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)                

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, 
                    self.get_software()["name"], self.commentEdit.toPlainText().strip(), email, password, "working", [ os.path.basename(self.outputFileEdit.text()) ])
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)

                target = "{}/{}.zip".format(os.path.dirname(source), file_base)
                dialog.add_item(target, "Pending")

                self.process_count += 1                
                self.threadpool.start(worker)
                ##worker.run()             


        #if len(self.fbxFileEdit.text()) > 0:
        #    source = self.fbxFileEdit.text()
        #    if os.path.exists(source):
        #        file_base = os.path.basename(source)
        #        file_path = os.path.dirname(source)
        #        file_name, file_ext = os.path.splitext(file_base)

        #        worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, "fbx", self.commentEdit.toPlainText().strip(), email, password)
        #        worker.callback.progress.connect(dialog.file_loading)
        #        worker.callback.done.connect(dialog.file_loaded)
        #        dialog.add_item(source, "Pending")    

        #        self.process_count += 1
        #        self.threadpool.start(worker)            


        # def __init__(self, parent, edit_api, task, source, file_name, software_name, comment, email, password, mode = "working", filter = []):
        #
        # output files
        #
        if len(self.outputFileEdit.text()) > 0:
            source = self.outputFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_name, file_ext = os.path.splitext(file_base)

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, None, self.commentEdit.toPlainText().strip(), email, password, mode = self.output_mode)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")    

                self.process_count += 1
                self.threadpool.start(worker)   
            
        # output dir
        elif len(self.outputDirEdit.text()) > 0:
            source = self.outputDirEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_name, file_ext = os.path.splitext(file_base)

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, None, self.commentEdit.toPlainText().strip(), email, password, mode = self.output_mode)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")    

                self.process_count += 1
                self.threadpool.start(worker)    
                #worker.run()               

        row = 0
        model = self.referencesListView.model()
        while row < model.rowCount():
            item = model.item(row)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                source = model.data(item.index())

                if os.path.exists(source):
                    file_base = os.path.basename(source)
                    file_path = os.path.dirname(source)
                    file_name, file_ext = os.path.splitext(file_base)

                    worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, "working", self.commentEdit.toPlainText().strip(), email, password)
                    worker.callback.progress.connect(dialog.file_loading)
                    worker.callback.done.connect(dialog.file_loaded)
                    dialog.add_item(source, "Pending")   

                    self.process_count += 1
                    self.threadpool.start(worker)                  
            row += 1

        dialog.reset_progressbar()
        dialog.show()
        self.hide()

    def get_references(self):
        return self.references

    def select_references(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileNames(self, "Add secondary assets", self.last_dir, "All Files (*.*)")
        if not (q):
            return 

        for name in q[0]:
            self.references.append(name)

        model = QtGui.QStandardItemModel(self.referencesListView)
        for item in self.references:
            list_item = QtGui.QStandardItem(item)
            list_item.setCheckable(True)
            list_item.setCheckState(QtCore.Qt.CheckState.Checked)
            model.appendRow(list_item)

        self.referencesListView.setModel(model)

    def select_working_file(self):
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Select Working File for Task", self.last_work_dir, "Maya Ascii (*.ma), Maya Binary (*.mb), All Files (*.*)")
        if (q and q[0] != ''):        
            self.last_work_dir = q[0]
            self.set_working_file(q[0])

    def select_working_dir(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Working Directory for Task", self.last_work_dir)
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
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Media Directory", self.last_output_dir)
        if q:
            self.last_output_dir = q
            self.set_output_dir(q)

                