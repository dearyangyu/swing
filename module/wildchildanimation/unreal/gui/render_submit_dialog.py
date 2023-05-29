# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'render_submit_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_RenderSubmit(object):
    def setupUi(self, RenderSubmit):
        if not RenderSubmit.objectName():
            RenderSubmit.setObjectName(u"RenderSubmit")
        RenderSubmit.resize(461, 521)
        self.verticalLayout_6 = QVBoxLayout(RenderSubmit)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBoxTask = QGroupBox(RenderSubmit)
        self.groupBoxTask.setObjectName(u"groupBoxTask")
        self.verticalLayout_7 = QVBoxLayout(self.groupBoxTask)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.labelKitsuProject = QLabel(self.groupBoxTask)
        self.labelKitsuProject.setObjectName(u"labelKitsuProject")
        self.labelKitsuProject.setMinimumSize(QSize(75, 0))
        self.labelKitsuProject.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_10.addWidget(self.labelKitsuProject)

        self.comboBoxKitsuProject = QComboBox(self.groupBoxTask)
        self.comboBoxKitsuProject.setObjectName(u"comboBoxKitsuProject")

        self.horizontalLayout_10.addWidget(self.comboBoxKitsuProject)

        self.toolButtonRefreshKitsuProject = QToolButton(self.groupBoxTask)
        self.toolButtonRefreshKitsuProject.setObjectName(u"toolButtonRefreshKitsuProject")

        self.horizontalLayout_10.addWidget(self.toolButtonRefreshKitsuProject)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelKitsuTask = QLabel(self.groupBoxTask)
        self.labelKitsuTask.setObjectName(u"labelKitsuTask")
        self.labelKitsuTask.setMinimumSize(QSize(75, 0))
        self.labelKitsuTask.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_8.addWidget(self.labelKitsuTask)

        self.comboBoxKitsuTask = QComboBox(self.groupBoxTask)
        self.comboBoxKitsuTask.setObjectName(u"comboBoxKitsuTask")

        self.horizontalLayout_8.addWidget(self.comboBoxKitsuTask)

        self.toolButtonRefreshKitsuTask = QToolButton(self.groupBoxTask)
        self.toolButtonRefreshKitsuTask.setObjectName(u"toolButtonRefreshKitsuTask")

        self.horizontalLayout_8.addWidget(self.toolButtonRefreshKitsuTask)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)


        self.verticalLayout_6.addWidget(self.groupBoxTask)

        self.groupBoxUnreal = QGroupBox(RenderSubmit)
        self.groupBoxUnreal.setObjectName(u"groupBoxUnreal")
        self.verticalLayout = QVBoxLayout(self.groupBoxUnreal)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelUEProject = QLabel(self.groupBoxUnreal)
        self.labelUEProject.setObjectName(u"labelUEProject")
        self.labelUEProject.setMinimumSize(QSize(75, 0))
        self.labelUEProject.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout.addWidget(self.labelUEProject)

        self.lineEditUEProject = QLineEdit(self.groupBoxUnreal)
        self.lineEditUEProject.setObjectName(u"lineEditUEProject")
        self.lineEditUEProject.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEditUEProject)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.verticalLayout_6.addWidget(self.groupBoxUnreal)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.groupBoxMap = QGroupBox(RenderSubmit)
        self.groupBoxMap.setObjectName(u"groupBoxMap")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxMap)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelMapDir = QLabel(self.groupBoxMap)
        self.labelMapDir.setObjectName(u"labelMapDir")
        self.labelMapDir.setMinimumSize(QSize(75, 0))
        self.labelMapDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_2.addWidget(self.labelMapDir)

        self.lineEditMapDir = QLineEdit(self.groupBoxMap)
        self.lineEditMapDir.setObjectName(u"lineEditMapDir")

        self.horizontalLayout_2.addWidget(self.lineEditMapDir)

        self.toolButtonMap = QToolButton(self.groupBoxMap)
        self.toolButtonMap.setObjectName(u"toolButtonMap")

        self.horizontalLayout_2.addWidget(self.toolButtonMap)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelMapAsset = QLabel(self.groupBoxMap)
        self.labelMapAsset.setObjectName(u"labelMapAsset")
        self.labelMapAsset.setMinimumSize(QSize(75, 0))
        self.labelMapAsset.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_4.addWidget(self.labelMapAsset)

        self.comboBoxMapAsset = QComboBox(self.groupBoxMap)
        self.comboBoxMapAsset.setObjectName(u"comboBoxMapAsset")

        self.horizontalLayout_4.addWidget(self.comboBoxMapAsset)

        self.toolButtonRefreshMapAsset = QToolButton(self.groupBoxMap)
        self.toolButtonRefreshMapAsset.setObjectName(u"toolButtonRefreshMapAsset")

        self.horizontalLayout_4.addWidget(self.toolButtonRefreshMapAsset)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.verticalLayout_6.addWidget(self.groupBoxMap)

        self.groupBoxSequence = QGroupBox(RenderSubmit)
        self.groupBoxSequence.setObjectName(u"groupBoxSequence")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxSequence)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelLevelDir = QLabel(self.groupBoxSequence)
        self.labelLevelDir.setObjectName(u"labelLevelDir")
        self.labelLevelDir.setMinimumSize(QSize(75, 0))
        self.labelLevelDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_3.addWidget(self.labelLevelDir)

        self.lineEditSequenceDir = QLineEdit(self.groupBoxSequence)
        self.lineEditSequenceDir.setObjectName(u"lineEditSequenceDir")

        self.horizontalLayout_3.addWidget(self.lineEditSequenceDir)

        self.toolButtonSequence = QToolButton(self.groupBoxSequence)
        self.toolButtonSequence.setObjectName(u"toolButtonSequence")

        self.horizontalLayout_3.addWidget(self.toolButtonSequence)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelLevelAsset = QLabel(self.groupBoxSequence)
        self.labelLevelAsset.setObjectName(u"labelLevelAsset")
        self.labelLevelAsset.setMinimumSize(QSize(75, 0))
        self.labelLevelAsset.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_5.addWidget(self.labelLevelAsset)

        self.comboBoxSequenceAsset = QComboBox(self.groupBoxSequence)
        self.comboBoxSequenceAsset.setObjectName(u"comboBoxSequenceAsset")

        self.horizontalLayout_5.addWidget(self.comboBoxSequenceAsset)

        self.toolButtonRefreshSequenceAsset = QToolButton(self.groupBoxSequence)
        self.toolButtonRefreshSequenceAsset.setObjectName(u"toolButtonRefreshSequenceAsset")

        self.horizontalLayout_5.addWidget(self.toolButtonRefreshSequenceAsset)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)


        self.verticalLayout_6.addWidget(self.groupBoxSequence)

        self.groupBoxPreset = QGroupBox(RenderSubmit)
        self.groupBoxPreset.setObjectName(u"groupBoxPreset")
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxPreset)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelPreset = QLabel(self.groupBoxPreset)
        self.labelPreset.setObjectName(u"labelPreset")
        self.labelPreset.setMinimumSize(QSize(75, 0))
        self.labelPreset.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_6.addWidget(self.labelPreset)

        self.comboBoxPreset = QComboBox(self.groupBoxPreset)
        self.comboBoxPreset.setObjectName(u"comboBoxPreset")

        self.horizontalLayout_6.addWidget(self.comboBoxPreset)

        self.toolButtonRefreshPresets = QToolButton(self.groupBoxPreset)
        self.toolButtonRefreshPresets.setObjectName(u"toolButtonRefreshPresets")

        self.horizontalLayout_6.addWidget(self.toolButtonRefreshPresets)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelOutputDir = QLabel(self.groupBoxPreset)
        self.labelOutputDir.setObjectName(u"labelOutputDir")
        self.labelOutputDir.setMinimumSize(QSize(75, 0))
        self.labelOutputDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_7.addWidget(self.labelOutputDir)

        self.lineEditOutputDir = QLineEdit(self.groupBoxPreset)
        self.lineEditOutputDir.setObjectName(u"lineEditOutputDir")

        self.horizontalLayout_7.addWidget(self.lineEditOutputDir)

        self.toolButtonOutput = QToolButton(self.groupBoxPreset)
        self.toolButtonOutput.setObjectName(u"toolButtonOutput")

        self.horizontalLayout_7.addWidget(self.toolButtonOutput)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)


        self.verticalLayout_6.addWidget(self.groupBoxPreset)

        self.groupBox_6 = QGroupBox(RenderSubmit)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.pushButtonSubmit = QPushButton(self.groupBox_6)
        self.pushButtonSubmit.setObjectName(u"pushButtonSubmit")

        self.horizontalLayout_9.addWidget(self.pushButtonSubmit)

        self.pushButtonCancel = QPushButton(self.groupBox_6)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout_9.addWidget(self.pushButtonCancel)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.verticalLayout_6.addWidget(self.groupBox_6)


        self.retranslateUi(RenderSubmit)

        self.pushButtonSubmit.setDefault(True)


        QMetaObject.connectSlotsByName(RenderSubmit)
    # setupUi

    def retranslateUi(self, RenderSubmit):
        RenderSubmit.setWindowTitle(fakestr(u"Dialog", None))
        self.groupBoxTask.setTitle(fakestr(u"Kitsu", None))
        self.labelKitsuProject.setText(fakestr(u"Project:", None))
        self.toolButtonRefreshKitsuProject.setText(fakestr(u"...", None))
        self.labelKitsuTask.setText(fakestr(u"Task:", None))
        self.toolButtonRefreshKitsuTask.setText(fakestr(u"...", None))
        self.groupBoxUnreal.setTitle(fakestr(u"Unreal:", None))
        self.labelUEProject.setText(fakestr(u"Project:", None))
        self.groupBoxMap.setTitle(fakestr(u"Map Selection:", None))
        self.labelMapDir.setText(fakestr(u"Folder:", None))
        self.toolButtonMap.setText(fakestr(u"...", None))
        self.labelMapAsset.setText(fakestr(u"Map:", None))
        self.toolButtonRefreshMapAsset.setText(fakestr(u"...", None))
        self.groupBoxSequence.setTitle(fakestr(u"Level Sequence:", None))
        self.labelLevelDir.setText(fakestr(u"Folder:", None))
        self.toolButtonSequence.setText(fakestr(u"...", None))
        self.labelLevelAsset.setText(fakestr(u"Sequence", None))
        self.toolButtonRefreshSequenceAsset.setText(fakestr(u"...", None))
        self.groupBoxPreset.setTitle(fakestr(u"Render Preset:", None))
        self.labelPreset.setText(fakestr(u"Preset:", None))
        self.toolButtonRefreshPresets.setText(fakestr(u"...", None))
        self.labelOutputDir.setText(fakestr(u"Output Folder:", None))
        self.toolButtonOutput.setText(fakestr(u"...", None))
        self.groupBox_6.setTitle("")
        self.pushButtonSubmit.setText(fakestr(u"Submit", None))
        self.pushButtonCancel.setText(fakestr(u"Cancel", None))
    # retranslateUi

