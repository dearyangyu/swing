# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_list_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_fileListDialog(object):
    def setupUi(self, fileListDialog):
        if not fileListDialog.objectName():
            fileListDialog.setObjectName(u"fileListDialog")
        fileListDialog.resize(452, 255)
        self.verticalLayout_2 = QVBoxLayout(fileListDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listView = QListView(fileListDialog)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_2.addWidget(self.listView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonClear = QPushButton(fileListDialog)
        self.buttonClear.setObjectName(u"buttonClear")

        self.horizontalLayout.addWidget(self.buttonClear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonCancel = QPushButton(fileListDialog)
        self.buttonCancel.setObjectName(u"buttonCancel")

        self.horizontalLayout.addWidget(self.buttonCancel)

        self.buttonOk = QPushButton(fileListDialog)
        self.buttonOk.setObjectName(u"buttonOk")

        self.horizontalLayout.addWidget(self.buttonOk)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(fileListDialog)

        self.buttonOk.setDefault(True)


        QMetaObject.connectSlotsByName(fileListDialog)
    # setupUi

    def retranslateUi(self, fileListDialog):
        fileListDialog.setWindowTitle(fakestr(u"Dialog", None))
        self.buttonClear.setText(fakestr(u"Clear", None))
        self.buttonCancel.setText(fakestr(u"Cancel", None))
        self.buttonOk.setText(fakestr(u"OK", None))
    # retranslateUi

