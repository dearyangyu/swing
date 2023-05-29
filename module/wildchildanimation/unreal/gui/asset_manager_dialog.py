# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_manager_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_AssetManagerDialog(object):
    def setupUi(self, AssetManagerDialog):
        if not AssetManagerDialog.objectName():
            AssetManagerDialog.setObjectName(u"AssetManagerDialog")
        AssetManagerDialog.resize(529, 114)
        self.verticalLayout_2 = QVBoxLayout(AssetManagerDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelFileName = QLabel(AssetManagerDialog)
        self.labelFileName.setObjectName(u"labelFileName")

        self.horizontalLayout.addWidget(self.labelFileName)

        self.lineEditFileName = QLineEdit(AssetManagerDialog)
        self.lineEditFileName.setObjectName(u"lineEditFileName")

        self.horizontalLayout.addWidget(self.lineEditFileName)

        self.toolButtonSelectFileName = QToolButton(AssetManagerDialog)
        self.toolButtonSelectFileName.setObjectName(u"toolButtonSelectFileName")

        self.horizontalLayout.addWidget(self.toolButtonSelectFileName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lineEditStatus = QLineEdit(AssetManagerDialog)
        self.lineEditStatus.setObjectName(u"lineEditStatus")
        self.lineEditStatus.setEnabled(False)

        self.verticalLayout.addWidget(self.lineEditStatus)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(AssetManagerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(AssetManagerDialog)
        self.buttonBox.accepted.connect(AssetManagerDialog.accept)
        self.buttonBox.rejected.connect(AssetManagerDialog.reject)

        QMetaObject.connectSlotsByName(AssetManagerDialog)
    # setupUi

    def retranslateUi(self, AssetManagerDialog):
        AssetManagerDialog.setWindowTitle(fakestr(u"Dialog", None))
        self.labelFileName.setText(fakestr(u"File:", None))
        self.toolButtonSelectFileName.setText(fakestr(u"...", None))
    # retranslateUi

