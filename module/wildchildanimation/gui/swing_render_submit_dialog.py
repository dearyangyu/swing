# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_render_submit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_RenderSubmitDialog(object):
    def setupUi(self, RenderSubmitDialog):
        if not RenderSubmitDialog.objectName():
            RenderSubmitDialog.setObjectName(u"RenderSubmitDialog")
        RenderSubmitDialog.setWindowModality(Qt.ApplicationModal)
        RenderSubmitDialog.setEnabled(True)
        RenderSubmitDialog.resize(711, 461)
        RenderSubmitDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(RenderSubmitDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.labelProject = QLabel(RenderSubmitDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_1.addWidget(self.labelProject)

        self.lineEditProject = QLineEdit(RenderSubmitDialog)
        self.lineEditProject.setObjectName(u"lineEditProject")
        self.lineEditProject.setEnabled(False)

        self.horizontalLayout_1.addWidget(self.lineEditProject)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelEp = QLabel(RenderSubmitDialog)
        self.labelEp.setObjectName(u"labelEp")
        self.labelEp.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.labelEp)

        self.lineEditEpisode = QLineEdit(RenderSubmitDialog)
        self.lineEditEpisode.setObjectName(u"lineEditEpisode")
        self.lineEditEpisode.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEditEpisode)

        self.labelSeq = QLabel(RenderSubmitDialog)
        self.labelSeq.setObjectName(u"labelSeq")

        self.horizontalLayout_4.addWidget(self.labelSeq)

        self.lineEditSequence = QLineEdit(RenderSubmitDialog)
        self.lineEditSequence.setObjectName(u"lineEditSequence")
        self.lineEditSequence.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEditSequence)

        self.labelShot = QLabel(RenderSubmitDialog)
        self.labelShot.setObjectName(u"labelShot")

        self.horizontalLayout_4.addWidget(self.labelShot)

        self.lineEditShot = QLineEdit(RenderSubmitDialog)
        self.lineEditShot.setObjectName(u"lineEditShot")
        self.lineEditShot.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEditShot)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelFrameIn = QLabel(RenderSubmitDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(100, 0))
        self.labelFrameIn.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(RenderSubmitDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")
        self.lineEditFrameIn.setEnabled(False)
        self.lineEditFrameIn.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEditFrameIn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelFrameOut = QLabel(RenderSubmitDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(100, 0))
        self.labelFrameOut.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(RenderSubmitDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")
        self.lineEditFrameOut.setEnabled(False)
        self.lineEditFrameOut.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_6.addWidget(self.lineEditFrameOut)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelFrameCount = QLabel(RenderSubmitDialog)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(100, 0))
        self.labelFrameCount.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(RenderSubmitDialog)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")
        self.lineEditFrameCount.setEnabled(False)
        self.lineEditFrameCount.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEditFrameCount)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelRenderPath = QLabel(RenderSubmitDialog)
        self.labelRenderPath.setObjectName(u"labelRenderPath")
        self.labelRenderPath.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.labelRenderPath)

        self.lineEditRenderPath = QLineEdit(RenderSubmitDialog)
        self.lineEditRenderPath.setObjectName(u"lineEditRenderPath")

        self.horizontalLayout_2.addWidget(self.lineEditRenderPath)

        self.toolButtonSelectPath = QToolButton(RenderSubmitDialog)
        self.toolButtonSelectPath.setObjectName(u"toolButtonSelectPath")

        self.horizontalLayout_2.addWidget(self.toolButtonSelectPath)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelArchiveName = QLabel(RenderSubmitDialog)
        self.labelArchiveName.setObjectName(u"labelArchiveName")
        self.labelArchiveName.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.labelArchiveName)

        self.lineEditArchiveName = QLineEdit(RenderSubmitDialog)
        self.lineEditArchiveName.setObjectName(u"lineEditArchiveName")

        self.horizontalLayout_3.addWidget(self.lineEditArchiveName)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label = QLabel(RenderSubmitDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_10.addWidget(self.label)

        self.radioButtonExr = QRadioButton(RenderSubmitDialog)
        self.radioButtonExr.setObjectName(u"radioButtonExr")

        self.horizontalLayout_10.addWidget(self.radioButtonExr)

        self.radioButtonPng = QRadioButton(RenderSubmitDialog)
        self.radioButtonPng.setObjectName(u"radioButtonPng")

        self.horizontalLayout_10.addWidget(self.radioButtonPng)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.labelHandles = QLabel(RenderSubmitDialog)
        self.labelHandles.setObjectName(u"labelHandles")
        self.labelHandles.setMinimumSize(QSize(100, 0))
        self.labelHandles.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_11.addWidget(self.labelHandles)

        self.labelHandlesIn = QLabel(RenderSubmitDialog)
        self.labelHandlesIn.setObjectName(u"labelHandlesIn")

        self.horizontalLayout_11.addWidget(self.labelHandlesIn)

        self.spinBoxHandlesIn = QSpinBox(RenderSubmitDialog)
        self.spinBoxHandlesIn.setObjectName(u"spinBoxHandlesIn")

        self.horizontalLayout_11.addWidget(self.spinBoxHandlesIn)

        self.labelHandlesOut = QLabel(RenderSubmitDialog)
        self.labelHandlesOut.setObjectName(u"labelHandlesOut")

        self.horizontalLayout_11.addWidget(self.labelHandlesOut)

        self.spinBoxHandlesOut = QSpinBox(RenderSubmitDialog)
        self.spinBoxHandlesOut.setObjectName(u"spinBoxHandlesOut")

        self.horizontalLayout_11.addWidget(self.spinBoxHandlesOut)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.labelNamingConvention = QLabel(RenderSubmitDialog)
        self.labelNamingConvention.setObjectName(u"labelNamingConvention")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelNamingConvention.setFont(font)

        self.horizontalLayout_9.addWidget(self.labelNamingConvention)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelWarningMessage = QLabel(RenderSubmitDialog)
        self.labelWarningMessage.setObjectName(u"labelWarningMessage")
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        font1.setWeight(75)
        self.labelWarningMessage.setFont(font1)
        self.labelWarningMessage.setStyleSheet(u"color: red")

        self.horizontalLayout_8.addWidget(self.labelWarningMessage)

        self.checkBoxOverride = QCheckBox(RenderSubmitDialog)
        self.checkBoxOverride.setObjectName(u"checkBoxOverride")

        self.horizontalLayout_8.addWidget(self.checkBoxOverride)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_8)

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.labelNotes = QLabel(RenderSubmitDialog)
        self.labelNotes.setObjectName(u"labelNotes")

        self.verticalLayoutEntityInfo.addWidget(self.labelNotes)

        self.textEditNotes = QTextEdit(RenderSubmitDialog)
        self.textEditNotes.setObjectName(u"textEditNotes")
        self.textEditNotes.setReadOnly(False)

        self.verticalLayoutEntityInfo.addWidget(self.textEditNotes)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelStatus = QLabel(RenderSubmitDialog)
        self.labelStatus.setObjectName(u"labelStatus")

        self.horizontalLayout.addWidget(self.labelStatus)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonGo = QPushButton(RenderSubmitDialog)
        self.pushButtonGo.setObjectName(u"pushButtonGo")

        self.horizontalLayout.addWidget(self.pushButtonGo)

        self.pushButtonCancel = QPushButton(RenderSubmitDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(RenderSubmitDialog)

        QMetaObject.connectSlotsByName(RenderSubmitDialog)
    # setupUi

    def retranslateUi(self, RenderSubmitDialog):
        RenderSubmitDialog.setWindowTitle(fakestr(u"swing: render submit", None))
        self.labelProject.setText(fakestr(u"Project:", None))
        self.labelEp.setText(fakestr(u"Episode:", None))
        self.labelSeq.setText(fakestr(u"Sequence:", None))
        self.labelShot.setText(fakestr(u"Shot:", None))
        self.labelFrameIn.setText(fakestr(u"Frame In", None))
        self.labelFrameOut.setText(fakestr(u"Frame Out", None))
        self.labelFrameCount.setText(fakestr(u"Frame Count", None))
        self.labelRenderPath.setText(fakestr(u"Render Path", None))
        self.toolButtonSelectPath.setText(fakestr(u"...", None))
        self.labelArchiveName.setText(fakestr(u"Archive Name", None))
        self.label.setText(fakestr(u"Image Type:", None))
        self.radioButtonExr.setText(fakestr(u"exr", None))
        self.radioButtonPng.setText(fakestr(u"png", None))
        self.labelHandles.setText(fakestr(u"Handles", None))
        self.labelHandlesIn.setText(fakestr(u"In", None))
        self.labelHandlesOut.setText(fakestr(u"Out", None))
        self.labelNamingConvention.setText(fakestr(u"Naming: {xxx}_sc{xxx}_sh{xxx}.{xxxx} i.e: 104_sc110_sh010.0073", None))
        self.labelWarningMessage.setText(fakestr(u"Warning: Shot name error - Frame count error", None))
        self.checkBoxOverride.setText(fakestr(u"Override and Upload", None))
        self.labelNotes.setText(fakestr(u"Notes and Comments", None))
        self.labelStatus.setText("")
        self.pushButtonGo.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

