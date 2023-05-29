# -*- coding: utf-8 -*-
import traceback
import sys
import os

from glob import glob

from wildchildanimation.gui.settings import SwingSettings

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1


from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.utils.video_to_image_convert_dialog import Ui_VideoToImageDialog


'''
    VideoToImageDialog class
    ################################################################################

    Converts a video file to a pnga image sequence using ffmpeg
    For use as Maya image planes
'''

class VideoToImageDialog(QtWidgets.QDialog, Ui_VideoToImageDialog):

    working_dir = None
    
    def __init__(self, parent = None):
        super(VideoToImageDialog, self).__init__(None) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)

        self.swing_settings = SwingSettings.get_instance()

        self.toolButtonSelectFile.clicked.connect(self.select_file)
        self.toolButtonSelectDirectory.clicked.connect(self.select_folder)
        self.pushButtonConvert.clicked.connect(self.process)

    def select_file(self):
        last = load_settings("vid_to_png_file", "")
        selection = QtWidgets.QFileDialog.getOpenFileName(self, 'Select video file', last, "Video files (*.mov *.mp4 *)")
        if (selection):
            self.lineEditFile.setText(selection[0])
            save_settings("vid_to_png_file", self.lineEditFile.text())    


    def select_folder(self):
        last = load_settings("vid_to_png_dir", "")        
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory', last)
        if (dir):
            self.lineEditDirectory.setText(dir)
            save_settings("vid_to_png_dir", self.lineEditDirectory.text())                

    def process(self):   
        if self.radioButtonFile.isChecked():
            ffmpeg_cmd = SwingSettings.get_instance().bin_ffmpeg()
            fps = self.lineEditFPS.text()

            source = self.lineEditFile.text()

            self.process_file(ffmpeg_cmd, source, fps)
            QtWidgets.QMessageBox.information(self, "Info", "Converted media files")
        elif self.radioButtonDirectory.isChecked():
            ffmpeg_cmd = SwingSettings.get_instance().bin_ffmpeg()
            fps = self.lineEditFPS.text()

            source_dir = self.lineEditDirectory.text()

            count = 0

            for source in glob("{}/**".format(source_dir)):
                if os.path.isfile(source):
                    _, ext = os.path.splitext(source)

                    if ext.lower() in [".mov", ".mp4"]:
                        self.process_file(ffmpeg_cmd, source, fps)
                        count += 1

            if count == 0:
                QtWidgets.QMessageBox.information(self, "Info", "No media files found to convert")
            else:
                QtWidgets.QMessageBox.information(self, "Info", "Converted {} media files".format(count))

                

    def process_file(self, ffmpeg, source, fps):
        image_dir = os.path.dirname(source)
        fn, ext = os.path.splitext(source)

        video_output = "{}/{}/{}.%04d.png".format(image_dir, os.path.basename(fn), os.path.basename(fn))
        
        command = ffmpeg + " -i " + '"{}"'.format(source) + " -start_number 0" + " -pix_fmt yuva420p " + '"{}"'.format(video_output) 
        try:
            output_dir = os.path.dirname(video_output)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            print(command)
            os.system(command)
        except:
            traceback.print_exc()
        #pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = VideoToImageDialog(app)
    dialog.show()
    sys.exit(app.exec_())