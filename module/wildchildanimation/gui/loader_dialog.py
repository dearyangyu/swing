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
        LoaderDialog.setEnabled(True)
        LoaderDialog.resize(874, 443)
        self.verticalLayout = QVBoxLayout(LoaderDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEntity = QLabel(LoaderDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(LoaderDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")

        self.horizontalLayout_2.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(LoaderDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")

        self.horizontalLayout_2.addWidget(self.toolButtonWeb)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutWorkingFile = QHBoxLayout()
        self.horizontalLayoutWorkingFile.setObjectName(u"horizontalLayoutWorkingFile")
        self.labelWorkingFile = QLabel(LoaderDialog)
        self.labelWorkingFile.setObjectName(u"labelWorkingFile")
        self.labelWorkingFile.setMinimumSize(QSize(100, 0))

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
        self.horizontalLayoutFrameDetails = QHBoxLayout()
        self.horizontalLayoutFrameDetails.setObjectName(u"horizontalLayoutFrameDetails")
        self.labelFrames = QLabel(LoaderDialog)
        self.labelFrames.setObjectName(u"labelFrames")
        self.labelFrames.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutFrameDetails.addWidget(self.labelFrames)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFrameIn = QLabel(LoaderDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(50, 0))
        self.labelFrameIn.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(LoaderDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")

        self.horizontalLayout_3.addWidget(self.lineEditFrameIn)

        self.labelFrameOut = QLabel(LoaderDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(50, 0))
        self.labelFrameOut.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(LoaderDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")

        self.horizontalLayout_3.addWidget(self.lineEditFrameOut)

        self.labelFrameCount = QLabel(LoaderDialog)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(50, 0))
        self.labelFrameCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(LoaderDialog)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")

        self.horizontalLayout_3.addWidget(self.lineEditFrameCount)


        self.horizontalLayoutFrameDetails.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFrameDetails.addItem(self.horizontalSpacer)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutFrameDetails)

        self.label = QLabel(LoaderDialog)
        self.label.setObjectName(u"label")

        self.verticalLayoutEntityInfo.addWidget(self.label)

        self.textEditShotInfo = QTextEdit(LoaderDialog)
        self.textEditShotInfo.setObjectName(u"textEditShotInfo")
        self.textEditShotInfo.setReadOnly(True)

        self.verticalLayoutEntityInfo.addWidget(self.textEditShotInfo)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)

        self.horizontalLayoutProjectDir = QHBoxLayout()
        self.horizontalLayoutProjectDir.setObjectName(u"horizontalLayoutProjectDir")
        self.labelWorkingDir = QLabel(LoaderDialog)
        self.labelWorkingDir.setObjectName(u"labelWorkingDir")
        self.labelWorkingDir.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutProjectDir.addWidget(self.labelWorkingDir)

        self.lineEditWorkingDir = QLineEdit(LoaderDialog)
        self.lineEditWorkingDir.setObjectName(u"lineEditWorkingDir")

        self.horizontalLayoutProjectDir.addWidget(self.lineEditWorkingDir)

        self.toolButtonWorkingDir = QToolButton(LoaderDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")

        self.horizontalLayoutProjectDir.addWidget(self.toolButtonWorkingDir)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutProjectDir)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.verticalLayoutOptions = QVBoxLayout()
        self.verticalLayoutOptions.setObjectName(u"verticalLayoutOptions")
        self.checkBoxSkipExisting = QCheckBox(LoaderDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setMinimumSize(QSize(100, 0))
        self.checkBoxSkipExisting.setStyleSheet(u"")
        self.checkBoxSkipExisting.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxSkipExisting)

        self.checkBoxExtractZips = QCheckBox(LoaderDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setMinimumSize(QSize(100, 0))
        self.checkBoxExtractZips.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxExtractZips)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.checkBoxReferences = QCheckBox(LoaderDialog)
        self.checkBoxReferences.setObjectName(u"checkBoxReferences")
        self.checkBoxReferences.setChecked(True)

        self.horizontalLayout_4.addWidget(self.checkBoxReferences)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.checkBoxNamespace = QCheckBox(LoaderDialog)
        self.checkBoxNamespace.setObjectName(u"checkBoxNamespace")
        self.checkBoxNamespace.setChecked(True)

        self.horizontalLayout_4.addWidget(self.checkBoxNamespace)

        self.lineEditNamespace = QLineEdit(LoaderDialog)
        self.lineEditNamespace.setObjectName(u"lineEditNamespace")

        self.horizontalLayout_4.addWidget(self.lineEditNamespace)


        self.verticalLayoutOptions.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.verticalLayoutOptions)

        self.verticalLayoutFiles = QVBoxLayout()
        self.verticalLayoutFiles.setObjectName(u"verticalLayoutFiles")
        self.labelFiles = QLabel(LoaderDialog)
        self.labelFiles.setObjectName(u"labelFiles")

        self.verticalLayoutFiles.addWidget(self.labelFiles)

        self.textEditStatus = QTextEdit(LoaderDialog)
        self.textEditStatus.setObjectName(u"textEditStatus")
        font = QFont()
        font.setFamily(u"MS Sans Serif")
        self.textEditStatus.setFont(font)

        self.verticalLayoutFiles.addWidget(self.textEditStatus)


        self.verticalLayout.addLayout(self.verticalLayoutFiles)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(LoaderDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButtonImport = QPushButton(LoaderDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.pushButtonCancel = QPushButton(LoaderDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LoaderDialog)

        QMetaObject.connectSlotsByName(LoaderDialog)
    # setupUi

    def retranslateUi(self, LoaderDialog):
        LoaderDialog.setWindowTitle(QCoreApplication.translate("LoaderDialog", u"swing: load files", None))
        self.labelEntity.setText(QCoreApplication.translate("LoaderDialog", u"Entity", None))
#if QT_CONFIG(tooltip)
        self.toolButtonWeb.setToolTip(QCoreApplication.translate("LoaderDialog", u"Opens link in Kitsu", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonWeb.setText(QCoreApplication.translate("LoaderDialog", u"Web", None))
        self.labelWorkingFile.setText(QCoreApplication.translate("LoaderDialog", u"Project File", None))
        self.labelFrames.setText(QCoreApplication.translate("LoaderDialog", u"Frame", None))
        self.labelFrameIn.setText(QCoreApplication.translate("LoaderDialog", u"In", None))
        self.labelFrameOut.setText(QCoreApplication.translate("LoaderDialog", u"Out", None))
        self.labelFrameCount.setText(QCoreApplication.translate("LoaderDialog", u"Count", None))
        self.label.setText(QCoreApplication.translate("LoaderDialog", u"Notes and Comments", None))
        self.labelWorkingDir.setText(QCoreApplication.translate("LoaderDialog", u"Work Folder", None))
        self.toolButtonWorkingDir.setText(QCoreApplication.translate("LoaderDialog", u"...", None))
        self.checkBoxSkipExisting.setText(QCoreApplication.translate("LoaderDialog", u"Skip existing files", None))
        self.checkBoxExtractZips.setText(QCoreApplication.translate("LoaderDialog", u"Extract zip files automatically", None))
#if QT_CONFIG(tooltip)
        self.checkBoxReferences.setToolTip(QCoreApplication.translate("LoaderDialog", u"Unselect to load file", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxReferences.setText(QCoreApplication.translate("LoaderDialog", u"Import as Reference", None))
        self.checkBoxNamespace.setText(QCoreApplication.translate("LoaderDialog", u"Set Namespace", None))
        self.labelFiles.setText(QCoreApplication.translate("LoaderDialog", u"Status", None))
        self.textEditStatus.setHtml(QCoreApplication.translate("LoaderDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButtonImport.setText(QCoreApplication.translate("LoaderDialog", u"Go", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("LoaderDialog", u"Close", None))
    # retranslateUi

