# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'upload_monitor_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr


class Ui_UploadMonitorDialog(object):
    def setupUi(self, UploadMonitorDialog):
        if not UploadMonitorDialog.objectName():
            UploadMonitorDialog.setObjectName(u"UploadMonitorDialog")
        UploadMonitorDialog.setEnabled(True)
        UploadMonitorDialog.resize(600, 240)
        self.verticalLayout = QVBoxLayout(UploadMonitorDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listView = QListView(UploadMonitorDialog)
        self.listView.setObjectName(u"listView")
        self.listView.setProperty("isWrapping", True)

        self.horizontalLayout_3.addWidget(self.listView)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.progressBar = QProgressBar(UploadMonitorDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButtonCancel = QPushButton(UploadMonitorDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(UploadMonitorDialog)

        QMetaObject.connectSlotsByName(UploadMonitorDialog)
    # setupUi

    def retranslateUi(self, UploadMonitorDialog):
        UploadMonitorDialog.setWindowTitle(fakestr(u"File Monitor", None))
        self.pushButtonCancel.setText(fakestr(u"Hide", None))
    # retranslateUi

