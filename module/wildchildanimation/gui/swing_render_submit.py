# -*- coding: utf-8 -*-
import os
import sys
import traceback
import gazu
import zipfile

from wildchildanimation.gui.background_workers import WorkingFileUploader

from wildchildanimation.gui.upload_monitor import UploadMonitorDialog
from wildchildanimation.gui.settings import SwingSettings

from wildchildanimation.gui.swing_render_submit_dialog import Ui_RenderSubmitDialog
from wildchildanimation.gui.swing_utils import friendly_string, external_compress

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
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
        self.checkBoxOverride.setChecked(False)

        self.updateUI()
        self.clear_warnings()

        if not self.radioButtonExr.isChecked() or self.radioButtonPng.isChecked():
            self.radioButtonPng.setChecked(True)

    def clear_warnings(self):
        self.warningMessage = ""
        self.labelWarningMessage.setVisible(False)
        self.checkBoxOverride.setVisible(False)
        

    def show_warning(self):
        self.labelWarningMessage.setText(self.warningMessage)

        self.labelWarningMessage.setVisible(True)
        self.checkBoxOverride.setVisible(True)

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings("WCA", self.__class__.__name__)
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("pos", self.pos())
        self.settings.setValue("working_dir", self.lineEditRenderPath.text())

        self.settings.setValue("handles_in", self.spinBoxHandlesIn.value())
        self.settings.setValue("handles_out", self.spinBoxHandlesOut.value())

        if self.radioButtonExr.isChecked():
            self.settings.setValue("image_type", "exr")
        elif self.radioButtonPng.isChecked():
            self.settings.setValue("image_type", "png")            
        
        self.settings.endGroup()
        self.settings.sync()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings("WCA", self.__class__.__name__)
        self.settings.beginGroup(self.__class__.__name__)

        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        self.working_dir = self.settings.value("working_dir", "~")

        self.spinBoxHandlesIn.setValue(self.settings.value("handles_in", 0))
        self.spinBoxHandlesOut.setValue(self.settings.value("handles_out", 0))
        
        image_type = self.settings.value("image_type", "exr") 

        if "exr" in image_type:
            self.radioButtonExr.setChecked(True)
            self.radioButtonPng.setChecked(False)
        elif "png" in image_type:
            self.radioButtonExr.setChecked(False)
            self.radioButtonPng.setChecked(True)


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

        prog = SwingSettings.get_instance().bin_7z()
        if prog and len(prog) > 0:
            extension = ".7z"
        else:
            extension = ".zip"

        version = 1
        version_string = "{}".format(version).zfill(3)
        arc_name = os.path.normpath("{}/../{}_v{}{}".format(selected_dir, self.prefix, version_string, extension))

        while os.path.exists(arc_name):
            version += 1
            version_string = "{}".format(version).zfill(3)
            arc_name = os.path.normpath("{}/../{}_v{}{}".format(selected_dir, self.prefix, version_string, extension))
                                    
        self.lineEditArchiveName.setText(arc_name)
        self.scan_working_dir()

    def updateUI(self):
        self.lineEditProject.setText(self.task["project"]["name"])
        self.lineEditEpisode.setText(self.task["episode"]["name"])
        self.lineEditSequence.setText(self.task["sequence"]["name"])
        self.lineEditShot.setText(self.task["entity"]["name"])

        if "nb_frames" in self.task["entity"]:
            self.lineEditFrameCount.setText(str(self.task["entity"]["nb_frames"]))

        if "data" in self.task["entity"] and self.task["entity"]["data"]:
            if "frame_in" in self.task["entity"]["data"]:
                self.lineEditFrameIn.setText(str(self.task["entity"]["data"]["frame_in"]))

            if "frame_out" in self.task["entity"]["data"]:
                self.lineEditFrameOut.setText(str(self.task["entity"]["data"]["frame_out"]))

        if not self.task["project"]["code"] in self.task["episode"]["name"]:
            self.prefix = friendly_string("{}_{}_{}_{}".format(
                self.task["project"]["code"],
                self.task["episode"]["name"],
                self.task["sequence"]["name"],
                self.task["entity"]["name"]
            ).lower())
        else:
            self.prefix = friendly_string("{}_{}_{}".format(
                self.task["episode"]["name"],
                self.task["sequence"]["name"],
                self.task["entity"]["name"]
            ).lower())

        self.wfa = gazu.task.get_task_status_by_name("Waiting For Approval")
        self.render = gazu.task.get_task_status_by_name("Render")

    def close_dialog(self):
        self.write_settings()
        self.hide()

    def select_render_directory(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, caption="Select Render Directory", dir=self.lineEditRenderPath.text())
        if q:
            self.set_working_dir(q)        

    def is_done(self, status):
        #shot = gazu.shot.get_shot(self.task["entity"]["id"])        
        #data = shot["data"]
        # gazu.shot.update_shot_data(shot, data)
        # update shot render quality
        self.labelStatus.setText("Completed")

    def zip_dir(self, path, zipfile):
        for root, dirs, files in os.walk(path):
            for file in files:
                zipfile.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))               

    def process(self):
        if not self.scan_working_dir():
            if not self.checkBoxOverride.isChecked():
                QtWidgets.QMessageBox.warning(self, 'Render Pub Error:', 'Please check render folder for naming and frame range')
                return False

        self.write_settings()

        server = SwingSettings.get_instance().swing_server()
        edit_api = "{}/edit".format(server)   

        self.monitor = UploadMonitorDialog(self)
        self.monitor.set_task(self.task)
        self.output_mode = "render"

        prog = SwingSettings.get_instance().bin_7z()
        arc_name = self.lineEditArchiveName.text()
        render_dir = self.lineEditRenderPath.text()
        task_comments = self.textEditNotes.toPlainText()

        self.labelStatus.setText("Creating archive")

        file_filter = "*.*"
        if self.radioButtonExr.isChecked():
            file_filter = "*.exr"
        elif self.radioButtonPng.isChecked():
            file_filter = "*.png"

        if "tg" == self.task["project"]["code"].lower():
            task_status = self.wfa
        else:
            task_status = self.render

        self.labelStatus.setText(F"Compressing {render_dir}")            
        if not prog or prog == '':
            ## if we don't have 7zip available, try Python Zipfile
            file_count = self.compress_folder(arc_name, render_dir)

            if file_count == 0:
                print(F"swing::render pub - no .png or .exr found in {render_dir}")

                QtWidgets.QMessageBox.warning(self, 'Render Pub Error:', 'No images found, please check directory')
                return False
        else: 
            external_compress(prog, arc_name, render_dir, file_filter=file_filter)

        if not os.path.exists(arc_name):
            print(F"swing::render pub - error creating archive {arc_name}")

            QtWidgets.QMessageBox.warning(self, 'Render Pub Error:', 'Error creating archive, please check directory and settings')
            return False
    
        self.labelStatus.setText(F"Uploading {self.lineEditArchiveName.text()}")
        print("Uploading archive: {}".format(self.lineEditArchiveName.text()))

        file_base = os.path.basename(arc_name)
        file_name, file_ext = os.path.splitext(file_base)

        worker = WorkingFileUploader(self, edit_api, self.task, arc_name, file_name, "Maya",  comment=task_comments, mode = self.output_mode, task_status = task_status["id"])

        worker.callback.progress.connect(self.monitor.file_loading)
        worker.callback.progress.connect(self.file_loading)
        
        worker.callback.done.connect(self.monitor.file_loaded)
        worker.callback.done.connect(self.is_done)
        ## dialog.add_item(source, "Pending")    

        self.threadpool.start(worker)                   
        self.monitor.show()

    def file_loading(self, results):
        ## print("file loading: {}".format(results))

        message = results["message"]
        source = results["source"]     

        self.labelStatus.setText(F"Uploading {message} {source}")            

    def compress_folder(self, arc_name, render_dir):
        file_count = 0
        with zipfile.ZipFile(arc_name, 'w', zipfile.ZIP_DEFLATED) as archive:  
            for item in os.listdir(render_dir):
                item_path = os.path.join(render_dir, item)
                    
                fn, ext = os.path.splitext(item)
                if ext.lower() in [ ".png", ".exr" ]:
                    archive.write(item_path, item)                                  
                    file_count += 1
        return file_count

        #convert = SwingConvert("{}/encode".format(self.working_dir), self.working_dir, "{}/png".format(self.working_dir))
        #convert.convert(self.progressBar)

    def scan_working_dir(self):
        # Warning: Shot name error - Frame count error
        handles = (int)(self.spinBoxHandlesIn.value() + self.spinBoxHandlesOut.value())
        try:
            render_dir = self.lineEditRenderPath.text()    

            if not os.path.exists(render_dir):
                return False 
            
            nb_frames = 0
            if self.task["entity"] and self.task["entity"]["nb_frames"]:
                nb_frames = int(self.task["entity"]["nb_frames"])
            
            frame_count = 0

            # 104_sc110_sh010.0073
            for filename in os.scandir(render_dir):
                if os.path.isfile(filename):

                    shot_name, extension = os.path.splitext(filename.name)
                    shot_parts = shot_name.split("_")

                    if extension.lower() in [ ".exr", ".png", ".jpg" ]:
                        if len(shot_parts) == 5:
                            validEp = shot_parts[1] in self.task["episode"]["name"]
                            validSeq  = shot_parts[2] in self.task["sequence"]["name"]
                            validShot = shot_parts[3] in self.task["entity"]["name"]
                        elif len(shot_parts) >= 3:
                            validEp = shot_parts[0] in self.task["episode"]["name"]
                            validSeq  = self.task["sequence"]["name"] in shot_parts[1]
                            validShot = self.task["entity"]["name"] in shot_parts[2]
                        else:
                            self.warningMessage = "Error: Unexpected name format. Expecting epXXX_scXXX_shXXX.xxxx, found: {}".format(filename.name)
                            self.show_warning()
                            return False                                                        

                        #if validEp and validSeq and validShot:
                        #    frame_count += 1
                        #else:
                        #    self.warningMessage = "Error: Found invalid shots in directory"
                        #    print("Naming error: {}".format(shot_name))
                        #    self.show_warning()
                        #    return False                            
                        
                        frame_count += 1

            if nb_frames > 0 and not (frame_count == nb_frames + handles):
                self.warningMessage = "Error: Expected {} frames, found {}".format(nb_frames, frame_count)
                self.show_warning()
                return False
            else:
                self.labelNamingConvention.setText(F"Found {frame_count} frames to upload")

            return True

        except:
            print(traceback.format_exc())              
            return False

        return False  

