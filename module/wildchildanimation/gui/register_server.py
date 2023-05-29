# -*- coding: utf-8 -*-
import sys
from wildchildanimation.gui.settings import SwingSettings

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import QApplication
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets 
    from PyQt5.QtWidgets import QApplication
    qtMode = 1

# === theme it dark
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False    

from wildchildanimation.gui.register_server_dialog import Ui_register_server_dialog
from wildchildanimation.gui.swing_utils import connect_to_server, load_keyring, set_button_icon

class SwingConnection(QtCore.QObject):

    connnection_name = None
    user_name = None
    password = None

    def __init__(self, connection_name, user_name, password):
        self.connnection_name = connection_name
        self.user_name = user_name
        self.password = password

    def __str__(self):
        return "{}@{}".format(self.user_name, self.connnection_name)

'''
    RegisterServerDialog
    ################################################################################
'''

class RegisterServerDialog(QtWidgets.QDialog, Ui_register_server_dialog):

    def __init__(self):
        super(RegisterServerDialog, self).__init__() # Call the inherited classes __init__ method
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("treehouse: register server")

        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName(SwingSettings._APP_NAME)   

        self.load_settings()   
        self.comboBoxServer.currentIndexChanged.connect(self.server_changed)        

        self.status = 'OK'

    def close_dialog(self):
        self.status = 'OK'
        self.close()

    def cancel_dialog(self):
        self.status = 'Cancel'
        self.close()                    

    def server_changed(self, index):
        connection = self.comboBoxServer.itemData(index)
        print(connection)

    
    def load_settings(self):
        _settings = QtCore.QSettings()   

        self.num_servers = _settings.value('connection_count', 0)

        if self.num_servers == 0:
            server_name = _settings.value('server', 'https://studio-api.example.com')
            user_name = _settings.value('user', 'user@example.com')            
            user_password = load_keyring('swing', 'password', 'Not A Password')

            connection = SwingConnection(server_name, user_name, user_password)
            self.comboBoxServer.addItem(server_name, connection)


if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    connect_to_server("user@example.com", password)
    
    app = QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # or in new API
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))        

    nav = RegisterServerDialog()
    nav.show()

    sys.exit(app.exec_())        

        





