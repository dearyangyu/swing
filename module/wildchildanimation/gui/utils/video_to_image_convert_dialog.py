# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_to_image_convert_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_VideoToImageDialog(object):
    def setupUi(self, VideoToImageDialog):
        if not VideoToImageDialog.objectName():
            VideoToImageDialog.setObjectName(u"VideoToImageDialog")
        VideoToImageDialog.resize(507, 154)
        self.verticalLayout_2 = QVBoxLayout(VideoToImageDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutFile = QHBoxLayout()
        self.horizontalLayoutFile.setObjectName(u"horizontalLayoutFile")
        self.radioButtonFile = QRadioButton(VideoToImageDialog)
        self.radioButtonFile.setObjectName(u"radioButtonFile")
        self.radioButtonFile.setMinimumSize(QSize(100, 0))
        self.radioButtonFile.setChecked(True)
        self.radioButtonFile.setAutoExclusive(True)

        self.horizontalLayoutFile.addWidget(self.radioButtonFile)

        self.lineEditFile = QLineEdit(VideoToImageDialog)
        self.lineEditFile.setObjectName(u"lineEditFile")

        self.horizontalLayoutFile.addWidget(self.lineEditFile)

        self.toolButtonSelectFile = QToolButton(VideoToImageDialog)
        self.toolButtonSelectFile.setObjectName(u"toolButtonSelectFile")

        self.horizontalLayoutFile.addWidget(self.toolButtonSelectFile)


        self.verticalLayout.addLayout(self.horizontalLayoutFile)

        self.horizontalLayoutDirectory = QHBoxLayout()
        self.horizontalLayoutDirectory.setObjectName(u"horizontalLayoutDirectory")
        self.radioButtonDirectory = QRadioButton(VideoToImageDialog)
        self.radioButtonDirectory.setObjectName(u"radioButtonDirectory")
        self.radioButtonDirectory.setMinimumSize(QSize(100, 0))
        self.radioButtonDirectory.setAutoExclusive(True)

        self.horizontalLayoutDirectory.addWidget(self.radioButtonDirectory)

        self.lineEditDirectory = QLineEdit(VideoToImageDialog)
        self.lineEditDirectory.setObjectName(u"lineEditDirectory")

        self.horizontalLayoutDirectory.addWidget(self.lineEditDirectory)

        self.toolButtonSelectDirectory = QToolButton(VideoToImageDialog)
        self.toolButtonSelectDirectory.setObjectName(u"toolButtonSelectDirectory")

        self.horizontalLayoutDirectory.addWidget(self.toolButtonSelectDirectory)


        self.verticalLayout.addLayout(self.horizontalLayoutDirectory)

        self.horizontalLayoutFPS = QHBoxLayout()
        self.horizontalLayoutFPS.setObjectName(u"horizontalLayoutFPS")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFPS.addItem(self.horizontalSpacer_2)

        self.labelFPS = QLabel(VideoToImageDialog)
        self.labelFPS.setObjectName(u"labelFPS")

        self.horizontalLayoutFPS.addWidget(self.labelFPS)

        self.lineEditFPS = QLineEdit(VideoToImageDialog)
        self.lineEditFPS.setObjectName(u"lineEditFPS")
        self.lineEditFPS.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayoutFPS.addWidget(self.lineEditFPS)


        self.verticalLayout.addLayout(self.horizontalLayoutFPS)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButtonConvert = QPushButton(VideoToImageDialog)
        self.pushButtonConvert.setObjectName(u"pushButtonConvert")

        self.horizontalLayout_3.addWidget(self.pushButtonConvert)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(VideoToImageDialog)

        QMetaObject.connectSlotsByName(VideoToImageDialog)
    # setupUi

    def retranslateUi(self, VideoToImageDialog):
        VideoToImageDialog.setWindowTitle(fakestr(u"Video to Image Converter", None))
        self.radioButtonFile.setText(fakestr(u"Select File:", None))
        self.toolButtonSelectFile.setText(fakestr(u"...", None))
        self.radioButtonDirectory.setText(fakestr(u"Select Directory:", None))
        self.toolButtonSelectDirectory.setText(fakestr(u"...", None))
        self.labelFPS.setText(fakestr(u"FPS", None))
        self.lineEditFPS.setText(fakestr(u"24", None))
        self.pushButtonConvert.setText(fakestr(u"Convert", None))
    # retranslateUi

