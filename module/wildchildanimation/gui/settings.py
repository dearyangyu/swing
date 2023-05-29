# -*- coding: utf-8 -*-
import sys
import os

# ==== auto Qt load ====
try:
    from PySide2.QtWidgets import QApplication    
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5.QtWidgets import QApplication    
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False    

from wildchildanimation.gui.settings_dialog import Ui_SettingsDialog
from wildchildanimation.gui.swing_utils import save_password, load_keyring, set_button_icon, write_log

import json

'''
    Swing Settings
    ################################################################################
'''

class SwingSettings(QtCore.QObject):

    _APP_NAME = "treehouse: swing"
    _APP_SHORTNAME = "swing"
    _APP_VERSION = "0.0.0.33"
    _APP_DESCRIPTION = "treehouse: swing"    
    _CONNECTIONS_FILE = "Z:/env/wca/swing/swing-main/swing_connections.json" 

    #
    # Singleton
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = SwingSettings()
        return cls._instance
    
    # define if Swing is running remote or in studio
    _site = "remote"

    _swing_server = None
    _swing_user = None
    _swing_password = None
    _swing_root = None
    _shared_root = None
    _edit_root = None

    _ffmpeg_bin = None
    _ffprobe_bin = None
    _7z_bin = None
    _ue_editor_bin = None
    _ue_project_dir = None

    def __init__(self):
        super(SwingSettings, self).__init__()

        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName(SwingSettings._APP_NAME)   

        self.load_settings()     

    def load_settings(self):
        self._swing_password = load_keyring('swing', 'password', 'Not A Password')

        if not os.path.exists(SwingSettings._CONNECTIONS_FILE):
            SwingSettings._CONNECTIONS_FILE = os.path.abspath(os.path.join(sys.path[0], "../../../", "swing_connections.json")) 
        write_log("Loading connections {}".format(SwingSettings._CONNECTIONS_FILE))

        with open(SwingSettings._CONNECTIONS_FILE, 'r') as json_file:
            self._connections = json.load(json_file)  

        self.scan_site()      

        _settings = QtCore.QSettings()   
        self._swing_server = _settings.value('server', 'https://studio-api.example.com')
        self._swing_user = _settings.value('user', 'user@example.com')
        self._swing_root = _settings.value('projects_root', os.path.expanduser("~"))
        self._shared_root = _settings.value('shared_root', 'Z:/productions')
        self._ffmpeg_bin = _settings.value("ffmpeg_bin", "")
        self._ffprobe_bin = _settings.value("ffprobe_bin", "")
        self._7z_bin = _settings.value("7z_bin", "")
        self._edit_root = _settings.value("edit_root", os.path.expanduser("~"))
        self._ue_editor_bin = _settings.value("ue_editor", "")
        self._ue_project_dir = _settings.value("ue_project", "")

    def scan_site(self):
        for item in self._connections:
            if "site" in item:
                self._site = item["site"]
                break

    def save_settings(self):
        save_password('swing', 'password', self.swing_password())

        _settings = QtCore.QSettings()    
        _settings.setValue('server', self.swing_server())
        _settings.setValue('user', self.swing_user())
        _settings.setValue("projects_root", self.swing_root()) 
        _settings.setValue("shared_root", self.shared_root())                           
        _settings.setValue("ffmpeg_bin", self.bin_ffmpeg())    
        _settings.setValue("ffprobe_bin", self.bin_ffprobe())          
        _settings.setValue("7z_bin", self.bin_7z())          
        _settings.setValue("edit_root", self.edit_root())
        _settings.setValue("ue_editor", self.bin_ue_editor())
        _settings.setValue("ue_project", self.ue_project_root())
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

    def shared_root(self):
        return self._shared_root

    def bin_ffmpeg(self):
        return self._ffmpeg_bin

    def bin_ffprobe(self):
        return self._ffprobe_bin

    def bin_7z(self):
        return self._7z_bin

    def edit_root(self):
        return self._edit_root

    def bin_ue_editor(self):
        return self._ue_editor_bin

    def ue_project_root(self):
        return self._ue_project_dir

    def connections(self):
        return self._connections        
    
    def is_remote(self):
        return not self._site or self._site == "remote"


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

        self.comboBoxServer.blockSignals(True)
        index = -1
        found = -1

        for item in self.swing_settings.connections():
            self.comboBoxServer.addItem(item["url"], userData = item)
            index += 1

            if item["url"] == self.swing_settings.swing_server():
                found = index
        self.comboBoxServer.blockSignals(False)            

        self.comboBoxServer.currentIndexChanged.connect(self.server_changed)

        if found >= 0:
            self.comboBoxServer.setCurrentIndex(found)
            self.server_changed(found)

        self.lineEditEmail.setText(self.swing_settings.swing_user())
        self.lineEditPassword.setText(self.swing_settings.swing_password())
        self.lineEditWorkingFolder.setText(self.swing_settings.swing_root())
        self.lineEditSharedFolder.setText(self.swing_settings.shared_root())
        self.lineEditEditorialFolder.setText(self.swing_settings.edit_root())

        set_button_icon(self.toolButtonWorkingFolder, "../resources/fa-free/solid/folder.svg")
        self.toolButtonWorkingFolder.clicked.connect(self.select_working_dir)   

        set_button_icon(self.toolButtonSharedFolder, "../resources/fa-free/solid/folder.svg")
        self.toolButtonSharedFolder.clicked.connect(self.select_shared_dir)   

        self.lineEditFfmpegBin.setText(self.swing_settings.bin_ffmpeg())

        set_button_icon(self.toolButtonFfmpegBin, "../resources/fa-free/solid/folder.svg")
        self.toolButtonFfmpegBin.clicked.connect(self.select_ffmpeg_bin)    
        
        self.lineEditFfprobeBin.setText(self.swing_settings.bin_ffprobe())

        set_button_icon(self.toolButtonFfprobeBin, "../resources/fa-free/solid/folder.svg")
        self.toolButtonFfprobeBin.clicked.connect(self.select_ffprobe_bin)            

        self.lineEdit7zBinary.setText(self.swing_settings.bin_7z())
        self.toolButton7zSelect.clicked.connect(self.select_7z_bin)                    
        set_button_icon(self.toolButton7zSelect, "../resources/fa-free/solid/folder.svg")

        set_button_icon(self.toolButtonEditorialFolder, "../resources/fa-free/solid/folder.svg")
        self.toolButtonEditorialFolder.clicked.connect(self.select_editorial_dir)

        set_button_icon(self.toolButtonUESelect, "../resources/fa-free/solid/folder.svg")
        self.toolButtonUESelect.clicked.connect(self.select_ue_editor_bin)
        self.lineEditUEBin.setText(self.swing_settings.bin_ue_editor())        

        set_button_icon(self.toolButtonUESelectUEProject, "../resources/fa-free/solid/folder.svg")
        self.toolButtonUESelectUEProject.clicked.connect(self.select_ue_project)
        self.lineEditUEProject.setText(self.swing_settings.ue_project_root())      

        if self.swing_settings.is_remote():
            self.labelSharedFolder.setVisible(False)
            self.lineEditSharedFolder.setVisible(False)
            self.toolButtonSharedFolder.setVisible(False)

    def server_changed(self, index):
        connection = self.comboBoxServer.currentData()
        self.lineEditSharedFolder.setText(connection["shared_folder"])

    def select_working_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select working directory')
        if directory:
            self.lineEditWorkingFolder.setText(directory)

    def select_shared_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select shared project directory')
        if directory:
            self.lineEditSharedFolder.setText(directory)            

    def select_ue_project(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select UE Editor Project')
        if binary:
            self.lineEditUEProject.setText(binary[0])           

    def select_editorial_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select editorial directory')
        if directory:
            self.lineEditEditorialFolder.setText(directory)

    def select_ffmpeg_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select ffmpeg binary')
        if binary:
            self.lineEditFfmpegBin.setText(binary[0])    

    def select_ue_editor_bin(self):
        binary = QtWidgets.QFileDialog.getOpenFileName(self, 'Select UE Editor binary')
        if binary:
            self.lineEditUEBin.setText(binary[0])                     

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

        settings._swing_server = self.comboBoxServer.currentData()["url"]
        settings._swing_user = self.lineEditEmail.text()
        settings._swing_password = self.lineEditPassword.text()
        settings._swing_root = self.lineEditWorkingFolder.text()
        settings._shared_root = self.lineEditSharedFolder.text()
        settings._ffmpeg_bin = self.lineEditFfmpegBin.text()
        settings._ffprobe_bin = self.lineEditFfprobeBin.text()
        settings._edit_root = self.lineEditEditorialFolder.text()
        settings._7z_bin = self.lineEdit7zBinary.text()
        settings._ue_editor_bin = self.lineEditUEBin.text()
        settings._ue_project_dir = self.lineEditUEProject.text()

        settings.save_settings()

        self.buttonBox.accepted.connect(self.save_settings)
        return True

if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    
    app = QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # or in new API
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))        

    dialog = SettingsDialog()
    dialog.show()

    sys.exit(app.exec_())
