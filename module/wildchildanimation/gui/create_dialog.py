# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_CreateDialog(object):
    def setupUi(self, CreateDialog):
        if not CreateDialog.objectName():
            CreateDialog.setObjectName(u"CreateDialog")
        CreateDialog.setEnabled(True)
        CreateDialog.resize(853, 416)
        self.verticalLayout = QVBoxLayout(CreateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEntity = QLabel(CreateDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(CreateDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")

        self.horizontalLayout_2.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(CreateDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")
        self.toolButtonWeb.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_2.addWidget(self.toolButtonWeb)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutProjectDir = QHBoxLayout()
        self.horizontalLayoutProjectDir.setObjectName(u"horizontalLayoutProjectDir")
        self.labelWorkingDir = QLabel(CreateDialog)
        self.labelWorkingDir.setObjectName(u"labelWorkingDir")
        self.labelWorkingDir.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutProjectDir.addWidget(self.labelWorkingDir)

        self.lineEditWorkingDir = QLineEdit(CreateDialog)
        self.lineEditWorkingDir.setObjectName(u"lineEditWorkingDir")

        self.horizontalLayoutProjectDir.addWidget(self.lineEditWorkingDir)

        self.toolButtonWorkingDir = QToolButton(CreateDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")
        self.toolButtonWorkingDir.setMinimumSize(QSize(40, 0))

        self.horizontalLayoutProjectDir.addWidget(self.toolButtonWorkingDir)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutProjectDir)

        self.horizontalLayoutSoftware = QHBoxLayout()
        self.horizontalLayoutSoftware.setObjectName(u"horizontalLayoutSoftware")
        self.labelSoftware = QLabel(CreateDialog)
        self.labelSoftware.setObjectName(u"labelSoftware")
        self.labelSoftware.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutSoftware.addWidget(self.labelSoftware)

        self.comboBoxSoftware = QComboBox(CreateDialog)
        self.comboBoxSoftware.setObjectName(u"comboBoxSoftware")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSoftware.sizePolicy().hasHeightForWidth())
        self.comboBoxSoftware.setSizePolicy(sizePolicy)

        self.horizontalLayoutSoftware.addWidget(self.comboBoxSoftware)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutSoftware)

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.horizontalLayoutFrameDetails = QHBoxLayout()
        self.horizontalLayoutFrameDetails.setObjectName(u"horizontalLayoutFrameDetails")
        self.labelFrames = QLabel(CreateDialog)
        self.labelFrames.setObjectName(u"labelFrames")
        self.labelFrames.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutFrameDetails.addWidget(self.labelFrames)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFrameIn = QLabel(CreateDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(50, 0))
        self.labelFrameIn.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(CreateDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")

        self.horizontalLayout_3.addWidget(self.lineEditFrameIn)

        self.labelFrameOut = QLabel(CreateDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(50, 0))
        self.labelFrameOut.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(CreateDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")

        self.horizontalLayout_3.addWidget(self.lineEditFrameOut)

        self.labelFrameCount = QLabel(CreateDialog)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(50, 0))
        self.labelFrameCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(CreateDialog)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")

        self.horizontalLayout_3.addWidget(self.lineEditFrameCount)


        self.horizontalLayoutFrameDetails.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFrameDetails.addItem(self.horizontalSpacer)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutFrameDetails)

        self.label = QLabel(CreateDialog)
        self.label.setObjectName(u"label")

        self.verticalLayoutEntityInfo.addWidget(self.label)

        self.textEditShotInfo = QTextEdit(CreateDialog)
        self.textEditShotInfo.setObjectName(u"textEditShotInfo")
        self.textEditShotInfo.setReadOnly(True)

        self.verticalLayoutEntityInfo.addWidget(self.textEditShotInfo)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.verticalLayoutOptions = QVBoxLayout()
        self.verticalLayoutOptions.setObjectName(u"verticalLayoutOptions")

        self.verticalLayout.addLayout(self.verticalLayoutOptions)

        self.verticalLayoutFiles = QVBoxLayout()
        self.verticalLayoutFiles.setObjectName(u"verticalLayoutFiles")
        self.labelFiles = QLabel(CreateDialog)
        self.labelFiles.setObjectName(u"labelFiles")

        self.verticalLayoutFiles.addWidget(self.labelFiles)

        self.textEditStatus = QTextEdit(CreateDialog)
        self.textEditStatus.setObjectName(u"textEditStatus")
        font = QFont()
        font.setFamily(u"MS Sans Serif")
        self.textEditStatus.setFont(font)

        self.verticalLayoutFiles.addWidget(self.textEditStatus)


        self.verticalLayout.addLayout(self.verticalLayoutFiles)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(CreateDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButtonImport = QPushButton(CreateDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.pushButtonCancel = QPushButton(CreateDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(CreateDialog)

        QMetaObject.connectSlotsByName(CreateDialog)
    # setupUi

    def retranslateUi(self, CreateDialog):
        CreateDialog.setWindowTitle(fakestr(u"swing: create new entity", None))
        self.labelEntity.setText(fakestr(u"File Name", None))
#if QT_CONFIG(tooltip)
        self.toolButtonWeb.setToolTip(fakestr(u"Opens link in Kitsu", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonWeb.setText(fakestr(u"Web", None))
        self.labelWorkingDir.setText(fakestr(u"Root Folder", None))
        self.toolButtonWorkingDir.setText(fakestr(u"...", None))
        self.labelSoftware.setText(fakestr(u"Software", None))
        self.labelFrames.setText(fakestr(u"Frame", None))
        self.labelFrameIn.setText(fakestr(u"In", None))
        self.labelFrameOut.setText(fakestr(u"Out", None))
        self.labelFrameCount.setText(fakestr(u"Count", None))
        self.label.setText(fakestr(u"Notes and Comments", None))
        self.labelFiles.setText(fakestr(u"Status", None))
        self.textEditStatus.setHtml(fakestr(u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Sans Serif'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.pushButtonImport.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

