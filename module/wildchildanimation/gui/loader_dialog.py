# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loader_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LoaderDialog(object):
    def setupUi(self, LoaderDialog):
        if not LoaderDialog.objectName():
            LoaderDialog.setObjectName(u"LoaderDialog")
        LoaderDialog.resize(670, 572)
        self.verticalLayout = QVBoxLayout(LoaderDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayoutWorkingFile = QHBoxLayout()
        self.horizontalLayoutWorkingFile.setObjectName(u"horizontalLayoutWorkingFile")
        self.labelWorkingFile = QLabel(LoaderDialog)
        self.labelWorkingFile.setObjectName(u"labelWorkingFile")
        self.labelWorkingFile.setMinimumSize(QSize(75, 0))

        self.horizontalLayoutWorkingFile.addWidget(self.labelWorkingFile)

        self.comboBoxWorkingFile = QComboBox(LoaderDialog)
        self.comboBoxWorkingFile.setObjectName(u"comboBoxWorkingFile")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxWorkingFile.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkingFile.setSizePolicy(sizePolicy)

        self.horizontalLayoutWorkingFile.addWidget(self.comboBoxWorkingFile)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutWorkingFile)

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.horizontalLayoutEntityDescription = QHBoxLayout()
        self.horizontalLayoutEntityDescription.setObjectName(u"horizontalLayoutEntityDescription")
        self.labelEntity = QLabel(LoaderDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(75, 0))

        self.horizontalLayoutEntityDescription.addWidget(self.labelEntity)

        self.lineEditAsset = QLineEdit(LoaderDialog)
        self.lineEditAsset.setObjectName(u"lineEditAsset")

        self.horizontalLayoutEntityDescription.addWidget(self.lineEditAsset)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutEntityDescription)

        self.horizontalLayoutFrameDetails = QHBoxLayout()
        self.horizontalLayoutFrameDetails.setObjectName(u"horizontalLayoutFrameDetails")
        self.labelFrameIn = QLabel(LoaderDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(75, 0))

        self.horizontalLayoutFrameDetails.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(LoaderDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")

        self.horizontalLayoutFrameDetails.addWidget(self.lineEditFrameIn)

        self.labelFrameOut = QLabel(LoaderDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")

        self.horizontalLayoutFrameDetails.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(LoaderDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")

        self.horizontalLayoutFrameDetails.addWidget(self.lineEditFrameOut)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutFrameDetails)

        self.textEditShotInfo = QTextEdit(LoaderDialog)
        self.textEditShotInfo.setObjectName(u"textEditShotInfo")

        self.verticalLayoutEntityInfo.addWidget(self.textEditShotInfo)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)

        self.horizontalLayoutProjectDir = QHBoxLayout()
        self.horizontalLayoutProjectDir.setObjectName(u"horizontalLayoutProjectDir")
        self.labelWorkingDir = QLabel(LoaderDialog)
        self.labelWorkingDir.setObjectName(u"labelWorkingDir")
        self.labelWorkingDir.setMinimumSize(QSize(75, 0))

        self.horizontalLayoutProjectDir.addWidget(self.labelWorkingDir)

        self.lineEditWorkingDir = QLineEdit(LoaderDialog)
        self.lineEditWorkingDir.setObjectName(u"lineEditWorkingDir")

        self.horizontalLayoutProjectDir.addWidget(self.lineEditWorkingDir)

        self.toolButtonWorkingDir = QToolButton(LoaderDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")

        self.horizontalLayoutProjectDir.addWidget(self.toolButtonWorkingDir)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutProjectDir)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.verticalLayoutLinkedAssets = QVBoxLayout()
        self.verticalLayoutLinkedAssets.setObjectName(u"verticalLayoutLinkedAssets")
        self.textEditNotes = QTextEdit(LoaderDialog)
        self.textEditNotes.setObjectName(u"textEditNotes")
        self.textEditNotes.setAutoFillBackground(True)
        self.textEditNotes.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEditNotes.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEditNotes.setReadOnly(True)

        self.verticalLayoutLinkedAssets.addWidget(self.textEditNotes)

        self.checkBoxLinkedAssets = QCheckBox(LoaderDialog)
        self.checkBoxLinkedAssets.setObjectName(u"checkBoxLinkedAssets")
        self.checkBoxLinkedAssets.setChecked(True)

        self.verticalLayoutLinkedAssets.addWidget(self.checkBoxLinkedAssets)

        self.treeViewLinkedAssets = QTreeView(LoaderDialog)
        self.treeViewLinkedAssets.setObjectName(u"treeViewLinkedAssets")

        self.verticalLayoutLinkedAssets.addWidget(self.treeViewLinkedAssets)


        self.verticalLayout.addLayout(self.verticalLayoutLinkedAssets)

        self.verticalLayoutOptions = QVBoxLayout()
        self.verticalLayoutOptions.setObjectName(u"verticalLayoutOptions")
        self.checkBoxSkipExisting = QCheckBox(LoaderDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setStyleSheet(u"")
        self.checkBoxSkipExisting.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxSkipExisting)

        self.checkBoxExtractZips = QCheckBox(LoaderDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxExtractZips)


        self.verticalLayout.addLayout(self.verticalLayoutOptions)

        self.verticalLayoutFiles = QVBoxLayout()
        self.verticalLayoutFiles.setObjectName(u"verticalLayoutFiles")
        self.labelFiles = QLabel(LoaderDialog)
        self.labelFiles.setObjectName(u"labelFiles")

        self.verticalLayoutFiles.addWidget(self.labelFiles)

        self.tableViewFiles = QTableView(LoaderDialog)
        self.tableViewFiles.setObjectName(u"tableViewFiles")

        self.verticalLayoutFiles.addWidget(self.tableViewFiles)


        self.verticalLayout.addLayout(self.verticalLayoutFiles)

        self.buttonBox = QDialogButtonBox(LoaderDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(LoaderDialog)
        self.buttonBox.accepted.connect(LoaderDialog.accept)
        self.buttonBox.rejected.connect(LoaderDialog.reject)

        QMetaObject.connectSlotsByName(LoaderDialog)
    # setupUi

    def retranslateUi(self, LoaderDialog):
        LoaderDialog.setWindowTitle(QCoreApplication.translate("LoaderDialog", u"swing: load files", None))
        self.labelWorkingFile.setText(QCoreApplication.translate("LoaderDialog", u"Working File", None))
        self.labelEntity.setText(QCoreApplication.translate("LoaderDialog", u"Asset / Shot", None))
        self.labelFrameIn.setText(QCoreApplication.translate("LoaderDialog", u"Frame In", None))
        self.labelFrameOut.setText(QCoreApplication.translate("LoaderDialog", u"Frame Out", None))
        self.labelWorkingDir.setText(QCoreApplication.translate("LoaderDialog", u"Project Folder", None))
        self.toolButtonWorkingDir.setText(QCoreApplication.translate("LoaderDialog", u"...", None))
        self.textEditNotes.setHtml(QCoreApplication.translate("LoaderDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Select the root project folder and working file</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- This will create a new scene in Maya, open the working file and scan for relatives <br /></p></body></html>", None))
        self.checkBoxLinkedAssets.setText(QCoreApplication.translate("LoaderDialog", u"Import linked assets", None))
        self.checkBoxSkipExisting.setText(QCoreApplication.translate("LoaderDialog", u"Skip existing files", None))
        self.checkBoxExtractZips.setText(QCoreApplication.translate("LoaderDialog", u"Extract zip files automatically", None))
        self.labelFiles.setText(QCoreApplication.translate("LoaderDialog", u"Files", None))
    # retranslateUi

