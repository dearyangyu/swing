# -*- coding: utf-8 -*-
import traceback
import sys
import os
import platform

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

from pyshortcuts import make_shortcut

from wildchildanimation.gui.settings_dialog import Ui_SettingsDialog
from wildchildanimation.gui.swing_utils import save_password, load_keyring, set_button_icon

'''
    Swing Settings
    ################################################################################
'''

class SwingSettings(QtCore.QObject):

    _APP_NAME = "treehouse: swing"
    _APP_SHORTNAME = "swing"
    _APP_VERSION = "0.0.0.27"
    _APP_DESCRIPTION = "treehouse: swing"    

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
    _edit_root = None

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
        self._edit_root = _settings.value("edit_root", os.path.expanduser("~"))

    def save_settings(self):
        save_password('swing', 'password', self.swing_password())

        _settings = QtCore.QSettings()    
        _settings.setValue('server', self.swing_server())
        _settings.setValue('user', self.swing_user())
        _settings.setValue("projects_root", self.swing_root())                            
        _settings.setValue("ffmpeg_bin", self.bin_ffmpeg())    
        _settings.setValue("ffprobe_bin", self.bin_ffprobe())          
        _settings.setValue("7z_bin", self.bin_7z())          
        _settings.setValue("edit_root", self.edit_root())
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

    def edit_root(self):
        return self._edit_root

    def create_shortcut(self, install_dir = None):
        root = sys.path[0]
        # drive, tail = os.path.splitdrive(root)        

        if "Darwin" in platform.system():
            cmd = "swing/swing-main/bin/swing_desktop.sh"            
            if not install_dir:
                install_dir = os.path.expanduser("~/WCA")
            
            #cmd = 'cd {}/swing/swing-main && source {}/env/bin/activate && python3 {}/swing/swing-main/module/wildchildanimation/plugin/swing_desktop.py'.format(dir, dir, dir)
            #C:\WCA\swing\swing-main\bin
        else:
            cmd = "swing/swing-main/bin/swing_desktop.bat"
            if not install_dir:
                install_dir = os.path.expanduser("C:/WCA")

        command_line = "{}/{}".format(install_dir, cmd)
        if not os.path.exists(command_line):
            print("Error: not foud {}".format(command_line))
            return False

        resource_icon = "{}/swing/swing-main/module/wildchildanimation/resources/wca.ico".format(install_dir)        
        if not os.path.exists(resource_icon):
            print("Resource Icon not found: {}".format(resource_icon))
            return False        

        make_shortcut(command_line, name = SwingSettings._APP_SHORTNAME, description = SwingSettings._APP_DESCRIPTION, icon = resource_icon)
        return True
        #, folder = working_dir, terminal=True, desktop=True, executable=python_line)


'''
    Settings Dialog
    ################################################################################
'''

class SettingsDialog(QtWidgets.QDialog, Ui_SettingsDialog):

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

        self.pushButtonShortcut.clicked.connect(self.create_shortcut)

        set_button_icon(self.toolButtonEditorialFolder, "../resources/fa-free/solid/folder.svg")
        self.toolButtonEditorialFolder.clicked.connect(self.select_editorial_dir)


    def create_shortcut(self):
        if SwingSettings.get_instance().create_shortcut():
            QtWidgets.QMessageBox.information(self, SwingSettings._APP_NAME, 'Created desktop shortcut')               


    def select_projects_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if directory:
            self.lineEditProjectsFolder.setText(directory)

    def select_editorial_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select editorial directory')
        if directory:
            self.lineEditEditorialFolder.setText(directory)

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

        settings = SwingSettings.get_instance()

        settings._swing_server = self.lineEditServer.text()
        settings._swing_user = self.lineEditEmail.text()
        settings._swing_password = self.lineEditPassword.text()
        settings._swing_root = self.lineEditProjectsFolder.text()
        settings._ffmpeg_bin = self.lineEditFfmpegBin.text()
        settings._ffprobe_bin = self.lineEditFfprobeBin.text()
        settings._7z_bin = self.lineEdit7zBinary.text()

        settings.save_settings()

        self.buttonBox.accepted.connect(self.save_settings)
        return True










