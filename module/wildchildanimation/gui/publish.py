# -*- coding: utf-8 -*-

import traceback
import sys
import os
import re

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

from wildchildanimation.gui.publish_dialog import Ui_PublishDialog
from wildchildanimation.gui.upload_monitor import UploadMonitorDialog

from wildchildanimation.gui.swing_tables import human_size, load_file_table_widget

class PublishDialogGUI(QtWidgets.QDialog, Ui_PublishDialog):

    def __init__(self, parent = None, handler = None, task = None):
        super(PublishDialogGUI, self).__init__(parent) # Call the inherited classes __init__ method    

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.read_settings()

        self.handler = handler
        self.task = task
        self.last_dir = None
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.references = []

        if "project" in self.task:
            name = '{}'.format(self.task["project"]["name"])
        else:
            name = '{}'.format(self.task["project_name"])

        if "entity_type" in self.task:
            name = '{} {}'.format(name, self.task["entity_type"]["name"])
        else:
            name = '{} {}'.format(name, self.task["entity_type_name"])

        if "entity" in self.task:
            name = '{} {}'.format(name, self.task["entity"]["name"])
        else:
            name = '{} {}'.format(name, self.task["entity_name"])

        if "task_type" in self.task:
            name = '{} {}'.format(name, self.task["task_type"]["name"])   
        else:
            name = '{} {}'.format(name, self.task["task_type_name"])   

        self.lineEditTask.setText(name)

        self.projectFileToolButton.clicked.connect(self.select_project_file)
        #self.fbxFileToolButton.clicked.connect(self.select_fbx_file)
        #self.reviewFileToolButton.clicked.connect(self.select_review_file)
        self.referencesAddPushButton.clicked.connect(self.select_references)

        model = QtGui.QStandardItemModel(self.referencesListView)
        self.referencesListView.setModel(model)        

        #self.toolButtonWeb.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_CommandLink))
        #self.toolButtonWeb.clicked.connect(self.open_url)
        #self.toolButtonWeb.setEnabled(False)

        self.pushButtonOK.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.close_dialog)

        self.request = self.handler.on_save() 
        if self.request:
            self.projectFileEdit.setText(self.request["file_path"])

        self.groupBox.setAcceptDrops(True)

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
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            # Workaround for OSx dragging and dropping
            #for url in e.mimeData().urls():
            #    if op_sys == 'Darwin':
            #        fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
            #    else:
            #        fname = str(url.toLocalFile())
            #self.fname = fname
            #self.load_image()
        else:
            e.ignore()


    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("Publish")

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        #self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        #self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("Publish")

        self.resize(self.settings.value("size", QtCore.QSize(600, 800)))
        self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))
        self.settings.endGroup()              

    def close_dialog(self):
        self.write_settings()
        self.close()

    def file_loaded(self, status):
        self.process_count -= 1
        if self.process_count == 0:
            QtWidgets.QMessageBox.question(self, 'Publishing complete', 'All files uploaded, thank you', QtWidgets.QMessageBox.Ok)
            self.pushButtonCancel.setEnabled(True)

    def process(self):
        self.pushButtonCancel.setEnabled(False)
        self.process_count = 0

        email = load_settings('user', 'user@example.com')
        password = load_keyring('swing', 'password', 'Not A Password')        

        server = load_settings('server', 'https://example.wildchildanimation.com')
        edit_api = "{}/edit".format(server)        

        #self, parent, task, source, software_name, comment, email, password
        dialog = UploadMonitorDialog(self, self.task)

        # project file
        if len(self.projectFileEdit.text()) > 0:
            source = self.projectFileEdit.text()

            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)                

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, "Maya 2020", self.commentEdit.toPlainText().strip(), email, password)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")

                self.process_count += 1                
                self.threadpool.start(worker)


        if len(self.fbxFileEdit.text()) > 0:
            source = self.fbxFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, "fbx", self.commentEdit.toPlainText().strip(), email, password)
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")    

                self.process_count += 1
                self.threadpool.start(worker)            

        if len(self.reviewFileEdit.text()) > 0:
            source = self.reviewFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)

                worker = WorkingFileUploader(self, edit_api, self.task, source, file_name, "wip", self.commentEdit.toPlainText().strip(), email, password, mode = "preview")
                worker.callback.progress.connect(dialog.file_loading)
                worker.callback.done.connect(dialog.file_loaded)
                dialog.add_item(source, "Pending")    

                self.process_count += 1
                self.threadpool.start(worker)   

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

    def select_project_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Project File", self.last_dir, "Maya Ascii (*.ma), Maya Binary (*.mb), All Files (*.*)")
        if (q and q[0] != ''):        
            self.projectFileEdit.setText(q[0])
            self.last_dir = q[0]

    def select_fbx_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."
        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Output File", self.last_dir, "FBX (*.fbx), All Files (*.*)")
        if (q and q[0] != ''):     
            self.fbxFileEdit.setText(q[0])
            self.last_dir = q[0]

    def select_review_file(self):
        """
        Open a File dialog when the button is pressed
        :return:
        """
        if not self.last_dir:
            self.last_dir = "."

        
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Review File", self.last_dir, "Images (*.bmp, *.jpg, *.png), Videos (*.mp4), All Files (*.*)")
        if (q and q[0] != ''):     
            self.reviewFileEdit.setText(q[0])

            source = self.reviewFileEdit.text()
            if os.path.exists(source):
                file_base = os.path.basename(source)
                file_path = os.path.dirname(source)
                file_name, file_ext = os.path.splitext(file_base)

                self.reviewTitleLineEdit.setText(file_name)
                self.last_dir = q[0]