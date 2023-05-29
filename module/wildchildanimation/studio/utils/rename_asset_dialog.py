# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rename_asset_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_RenameAssetWidget(object):
    def setupUi(self, RenameAssetWidget):
        if not RenameAssetWidget.objectName():
            RenameAssetWidget.setObjectName(u"RenameAssetWidget")
        RenameAssetWidget.resize(601, 391)
        self.verticalLayout = QVBoxLayout(RenameAssetWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutProjectTitle = QHBoxLayout()
        self.horizontalLayoutProjectTitle.setObjectName(u"horizontalLayoutProjectTitle")
        self.labelProject = QLabel(RenameAssetWidget)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutProjectTitle.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(RenameAssetWidget)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        self.comboBoxProject.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy)

        self.horizontalLayoutProjectTitle.addWidget(self.comboBoxProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProjectTitle)

        self.horizontalLayoutAssetType = QHBoxLayout()
        self.horizontalLayoutAssetType.setObjectName(u"horizontalLayoutAssetType")
        self.labelAssetType = QLabel(RenameAssetWidget)
        self.labelAssetType.setObjectName(u"labelAssetType")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelAssetType.sizePolicy().hasHeightForWidth())
        self.labelAssetType.setSizePolicy(sizePolicy1)
        self.labelAssetType.setMinimumSize(QSize(100, 0))
        self.labelAssetType.setMaximumSize(QSize(60, 16777215))
        self.labelAssetType.setFont(font)
        self.labelAssetType.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutAssetType.addWidget(self.labelAssetType)

        self.comboBoxAssetType = QComboBox(RenameAssetWidget)
        self.comboBoxAssetType.setObjectName(u"comboBoxAssetType")
        self.comboBoxAssetType.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxAssetType.sizePolicy().hasHeightForWidth())
        self.comboBoxAssetType.setSizePolicy(sizePolicy2)
        self.comboBoxAssetType.setMinimumSize(QSize(200, 0))
        self.comboBoxAssetType.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutAssetType.addWidget(self.comboBoxAssetType)


        self.verticalLayout.addLayout(self.horizontalLayoutAssetType)

        self.horizontalLayoutAssetName = QHBoxLayout()
        self.horizontalLayoutAssetName.setObjectName(u"horizontalLayoutAssetName")
        self.labelAssetName = QLabel(RenameAssetWidget)
        self.labelAssetName.setObjectName(u"labelAssetName")
        sizePolicy1.setHeightForWidth(self.labelAssetName.sizePolicy().hasHeightForWidth())
        self.labelAssetName.setSizePolicy(sizePolicy1)
        self.labelAssetName.setMinimumSize(QSize(100, 0))
        self.labelAssetName.setMaximumSize(QSize(60, 16777215))
        self.labelAssetName.setFont(font)
        self.labelAssetName.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutAssetName.addWidget(self.labelAssetName)

        self.comboBoxAssetName = QComboBox(RenameAssetWidget)
        self.comboBoxAssetName.setObjectName(u"comboBoxAssetName")
        self.comboBoxAssetName.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.comboBoxAssetName.sizePolicy().hasHeightForWidth())
        self.comboBoxAssetName.setSizePolicy(sizePolicy2)
        self.comboBoxAssetName.setMinimumSize(QSize(200, 0))
        self.comboBoxAssetName.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutAssetName.addWidget(self.comboBoxAssetName)


        self.verticalLayout.addLayout(self.horizontalLayoutAssetName)

        self.horizontalLayoutFBX = QHBoxLayout()
        self.horizontalLayoutFBX.setObjectName(u"horizontalLayoutFBX")
        self.labelFBX = QLabel(RenameAssetWidget)
        self.labelFBX.setObjectName(u"labelFBX")
        sizePolicy1.setHeightForWidth(self.labelFBX.sizePolicy().hasHeightForWidth())
        self.labelFBX.setSizePolicy(sizePolicy1)
        self.labelFBX.setMinimumSize(QSize(100, 0))
        self.labelFBX.setMaximumSize(QSize(60, 16777215))
        self.labelFBX.setFont(font)
        self.labelFBX.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutFBX.addWidget(self.labelFBX)

        self.lineEdit = QLineEdit(RenameAssetWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayoutFBX.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayoutFBX)

        self.horizontalLayoutTextures = QHBoxLayout()
        self.horizontalLayoutTextures.setObjectName(u"horizontalLayoutTextures")
        self.labelTextures = QLabel(RenameAssetWidget)
        self.labelTextures.setObjectName(u"labelTextures")
        sizePolicy1.setHeightForWidth(self.labelTextures.sizePolicy().hasHeightForWidth())
        self.labelTextures.setSizePolicy(sizePolicy1)
        self.labelTextures.setMinimumSize(QSize(100, 0))
        self.labelTextures.setMaximumSize(QSize(60, 16777215))
        self.labelTextures.setFont(font)
        self.labelTextures.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.horizontalLayoutTextures.addWidget(self.labelTextures)

        self.tableViewDir = QTableView(RenameAssetWidget)
        self.tableViewDir.setObjectName(u"tableViewDir")

        self.horizontalLayoutTextures.addWidget(self.tableViewDir)


        self.verticalLayout.addLayout(self.horizontalLayoutTextures)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(RenameAssetWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label)

        self.tableViewFile = QTableView(RenameAssetWidget)
        self.tableViewFile.setObjectName(u"tableViewFile")

        self.horizontalLayout.addWidget(self.tableViewFile)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(RenameAssetWidget)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayoutButtons.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(RenameAssetWidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayoutButtons)


        self.retranslateUi(RenameAssetWidget)

        QMetaObject.connectSlotsByName(RenameAssetWidget)
    # setupUi

    def retranslateUi(self, RenameAssetWidget):
        RenameAssetWidget.setWindowTitle(fakestr(u"Form", None))
        self.labelProject.setText(fakestr(u"Project", None))
        self.labelAssetType.setText(fakestr(u"Asset Type", None))
        self.labelAssetName.setText(fakestr(u"Asset Name", None))
        self.labelFBX.setText(fakestr(u"New Name", None))
        self.labelTextures.setText(fakestr(u"Directories", None))
        self.label.setText(fakestr(u"Files", None))
        self.pushButtonOk.setText(fakestr(u"&Rename", None))
        self.pushButtonCancel.setText(fakestr(u"&Close", None))
    # retranslateUi

