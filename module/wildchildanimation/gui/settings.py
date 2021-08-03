# -*- coding: utf-8 -*-
import traceback
import sys
import os
import re
import json

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtCore, QtWidgets
    import sip
    qtMode = 1

from wildchildanimation.gui.settings_dialog import Ui_SettingsDialog
from wildchildanimation.gui.swing_utils import save_password, load_keyring, set_button_icon

'''
    Swing Settings
    ################################################################################
'''

class SwingSettings(QtCore.QObject):

    _APP_NAME = "treehouse: swing"
    _APP_VERSION = "0.0.0.25"

    #
    # Singleton
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = SwingSettings()
        return cls._instance

    _swing_server = None
    _swing_user = None
    _swing_password = None
    _swing_root = None

    _ffmpeg_bin = None
    _ffprobe_bin = None
    _7z_bin = None

    def __init__(self):
        super(SwingSettings, self).__init__()

        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName(SwingSettings._APP_NAME)   

        self.load_settings()     

    def load_settings(self):
        self._swing_password = load_keyring('swing', 'password', 'Not A Password')

        _settings = QtCore.QSettings()   
        self._swing_server = _settings.value('server', 'https://studio-api.example.com')
        self._swing_user = _settings.value('user', 'user@example.com')
        self._swing_root = _settings.value('projects_root', os.path.expanduser("~"))
        self._ffmpeg_bin = _settings.value("ffmpeg_bin", "")
        self._ffprobe_bin = _settings.value("ffprobe_bin", "")
        self._7z_bin = _settings.value("7z_bin", "")

    def save_settings(self):
        save_password('swing', 'password', self.swing_password())

        _settings = QtCore.QSettings()    
        _settings.setValue('server', self.swing_server())
        _settings.setValue('user', self.swing_user())
        _settings.setValue("projects_root", self.swing_root())                            
        _settings.setValue("ffmpeg_bin", self.bin_ffmpeg())    
        _settings.setValue("ffprobe_bin", self.bin_ffprobe())          
        _settings.setValue("7z_bin", self.bin_7z())          
        _settings.sync()        

        self.load_settings()

    def swing_server(self):
        return self._swing_server

    def swing_user(self):
        return self._swing_user

    def swing_password(self):
        return self._swing_password

    def swing_root(self):
        return self._swing_root

    def bin_ffmpeg(self):
        return self._ffmpeg_bin

    def bin_ffprobe(self):
        return self._ffprobe_bin

    def bin_7z(self):
        return self._7z_bin

'''
    Settings Dialog
    ################################################################################
'''

class SettingsDialog(QtWidgets.QDialog, Ui_SettingsDialog):

    working_dir = None
    swing_settings = None
    
    def __init__(self, parent = None):
        super(SettingsDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.swing_settings = SwingSettings.get_instance()

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setModal(True)
        self.buttonBox.accepted.connect(self.save_settings)

        self.lineEditServer.setText(self.swing_settings.swing_server())
        self.lineEditEmail.setText(self.swing_settings.swing_user())
        self.lineEditPassword.setText(self.swing_settings.swing_password())
        self.lineEditProjectsFolder.setText(self.swing_settings.swing_root())

        set_button_icon(self.toolButtonProjectsFolder, "../resources/fa-free/solid/folder.svg")
        self.toolButtonProjectsFolder.clicked.connect(self.select_projects_dir)    

        self.lineEditFfmpegBin.setText(self.swing_settings.bin_ffmpeg())

        set_button_icon(self.toolButtonFfmpegBin, "../resources/fa-free/solid/folder.svg")
        self.toolButtonFfmpegBin.clicked.connect(self.select_ffmpeg_bin)    
        
        self.lineEditFfprobeBin.setText(self.swing_settings.bin_ffprobe())

        set_button_icon(self.toolButtonFfprobeBin, "../resources/fa-free/solid/folder.svg")
        self.toolButtonFfprobeBin.clicked.connect(self.select_ffprobe_bin)            

        self.lineEdit7zBinary.setText(self.swing_settings.bin_7z())
        self.toolButton7zSelect.clicked.connect(self.select_7z_bin)                    
        set_button_icon(self.toolButton7zSelect, "../resources/fa-free/solid/folder.svg")


    def select_projects_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if directory:
            self.lineEditProjectsFolder.setText(directory)

    def select_ffmpeg_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select ffmpeg binary')
        if binary:
            self.lineEditFfmpegBin.setText(binary[0])            

    def select_ffprobe_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select ffprobe binary')
        if binary:
            self.lineEditFfprobeBin.setText(binary[0])            

    def select_7z_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select 7z binary')
        if binary:
            self.lineEdit7zBinary.setText(binary[0])                  

    def save_settings(self):
        self.buttonBox.accepted.disconnect()

        self.swing_settings._swing_server = self.lineEditServer.text()
        self.swing_settings._swing_user = self.lineEditEmail.text()
        self.swing_settings._swing_password = self.lineEditPassword.text()
        self.swing_settings._swing_root = self.lineEditProjectsFolder.text()
        self.swing_settings._ffmpeg_bin = self.lineEditFfmpegBin.text()
        self.swing_settings._ffprobe_bin = self.lineEditFfprobeBin.text()
        self.swing_settings._7z_bin = self.lineEdit7zBinary.text()

        self.swing_settings.save_settings()
        self.buttonBox.accepted.connect(self.save_settings)

        return True










