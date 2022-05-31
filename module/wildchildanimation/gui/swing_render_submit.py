# -*- coding: utf-8 -*-
import os
import sys
import traceback
import gazu

from wildchildanimation.gui.background_workers import WorkingFileUploader

from wildchildanimation.gui.upload_monitor import UploadMonitorDialog
from wildchildanimation.gui.settings import SwingSettings

from wildchildanimation.gui.swing_render_submit_dialog import Ui_RenderSubmitDialog
from wildchildanimation.gui.swing_utils import friendly_string, external_compress

try:
    from wildchildanimation.studio.openexr.swing_convert import SwingConvert
except:
    traceback.print_exc(file=sys.stdout)
    print("Error: OpenEXR not configured correctly, check env")

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1


class SwingRenderSubmitDialog(QtWidgets.QDialog, Ui_RenderSubmitDialog):

    def __init__(self, parent = None, task = None):
        super(SwingRenderSubmitDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setAcceptDrops(True)        
        self.read_settings()
        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.task = task
        self.prefix = "render_pub"

        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonGo.clicked.connect(self.process)

        self.toolButtonSelectPath.clicked.connect(self.select_render_directory)

        self.updateUI()
        ##self.textEditNotes.setEnabled(True)
        #self.progressBar.setRange(0, len(self.model.files))
        #self.progressBar.setValue("")

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()

        self.settings.beginGroup(self.__class__.__name__)
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("working_dir", self.lineEditRenderPath.text())
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.working_dir = self.settings.value("working_dir", "~")

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

            self.process_dropped_files(files)
        else:
            e.ignore()        

    def process_dropped_files(self, file_list):
        for selected_file in file_list:

            if os.path.isdir(selected_file):
                self.set_working_dir(selected_file)

                return True        

    def set_working_dir(self, selected_dir):
        self.working_dir = selected_dir

        self.lineEditRenderPath.setText(selected_dir)
        #self.lineEditH265Path.setText("{}/{}.mp4".format(q, self.prefix))
        #self.checkBoxEncodeH265.setChecked(True)

        self.lineEditArchiveName.setText("{}/{}.7z".format(selected_dir, self.prefix))        

        #self.radioButtonWorkingFile.setChecked(False)
        #self.radioButtonWorkingDir.setChecked(True)

        #self.scan_working_dir(selected_dir)
        #self.workingDirEdit.setText(selected_dir)
        #self.workingFileEdit.setText("")        

    def updateUI(self):
        self.lineEditProject.setText(self.task["project"]["name"])
        self.lineEditEpisode.setText(self.task["episode"]["name"])
        self.lineEditSequence.setText(self.task["sequence"]["name"])
        self.lineEditShot.setText(self.task["entity"]["name"])

        if "nb_frames" in self.task["entity"]:
            self.lineEditFrameCount.setText(str(self.task["entity"]["nb_frames"]))

        if "frame_in" in self.task["entity"]["data"]:
            self.lineEditFrameIn.setText(str(self.task["entity"]["data"]["frame_in"]))

        if "frame_out" in self.task["entity"]["data"]:
            self.lineEditFrameOut.setText(str(self.task["entity"]["data"]["frame_out"]))

        self.prefix = friendly_string("{}_{}_{}_{}".format(
            self.task["project"]["code"], 
            self.task["episode"]["name"],
            self.task["sequence"]["name"],
            self.task["entity"]["name"]
        ).lower())

        self.wfa = gazu.task.get_task_status_by_name("Waiting For Approval")

    def close_dialog(self):
        self.write_settings()
        self.hide()

    def select_render_directory(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, caption="Select Render Directory", directory=self.working_dir)
        if q:
            self.set_working_dir(q)        

    def is_done(self, status):
        self.labelStatus.setText("Completed")

    def process(self):
        self.write_settings()

        server = SwingSettings.get_instance().swing_server()
        edit_api = "{}/edit".format(server)   

        self.monitor = UploadMonitorDialog(self)
        self.monitor.set_task(self.task)
        self.output_mode = "render"


        if SwingSettings.get_instance().bin_7z():
            prog = SwingSettings.get_instance().bin_7z()
            arc_name = self.lineEditArchiveName.text()
            render_dir = self.lineEditRenderPath.text()
            task_comments = self.textEditNotes.toPlainText()

            self.labelStatus.setText("Creating archive")

            if external_compress(prog, arc_name, render_dir):
                self.labelStatus.setText("Uploading archive")

                print("Uploading archive: {}".format(self.lineEditArchiveName.text()))

                file_base = os.path.basename(arc_name)
                file_name, file_ext = os.path.splitext(file_base)

                worker = WorkingFileUploader(self, edit_api, self.task, arc_name, file_name, "Maya",  comment=task_comments, mode = self.output_mode, task_status = self.wfa["id"])

                worker.callback.progress.connect(self.monitor.file_loading)
                worker.callback.done.connect(self.monitor.file_loaded)
                worker.callback.done.connect(self.is_done)
                ## dialog.add_item(source, "Pending")    

                self.threadpool.start(worker)                   
                self.monitor.show()

        #convert = SwingConvert("{}/encode".format(self.working_dir), self.working_dir, "{}/png".format(self.working_dir))
        #convert.convert(self.progressBar)
