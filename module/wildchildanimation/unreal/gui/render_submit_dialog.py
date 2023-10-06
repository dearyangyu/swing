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
        RenderSubmit.resize(444, 586)
        self.verticalLayout_7 = QVBoxLayout(RenderSubmit)
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(3, 3, 3, 3)
        self.groupBoxTask = QGroupBox(RenderSubmit)
        self.groupBoxTask.setObjectName(u"groupBoxTask")
        self.verticalLayout_6 = QVBoxLayout(self.groupBoxTask)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayoutKitsuProject = QHBoxLayout()
        self.horizontalLayoutKitsuProject.setObjectName(u"horizontalLayoutKitsuProject")
        self.labelKitsuProject = QLabel(self.groupBoxTask)
        self.labelKitsuProject.setObjectName(u"labelKitsuProject")
        self.labelKitsuProject.setMinimumSize(QSize(100, 0))
        self.labelKitsuProject.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutKitsuProject.addWidget(self.labelKitsuProject)

        self.comboBoxKitsuProject = QComboBox(self.groupBoxTask)
        self.comboBoxKitsuProject.setObjectName(u"comboBoxKitsuProject")

        self.horizontalLayoutKitsuProject.addWidget(self.comboBoxKitsuProject)

        self.toolButtonRefreshKitsuProject = QToolButton(self.groupBoxTask)
        self.toolButtonRefreshKitsuProject.setObjectName(u"toolButtonRefreshKitsuProject")

        self.horizontalLayoutKitsuProject.addWidget(self.toolButtonRefreshKitsuProject)


        self.verticalLayout_6.addLayout(self.horizontalLayoutKitsuProject)

        self.horizontalLayoutKitsuTask = QHBoxLayout()
        self.horizontalLayoutKitsuTask.setObjectName(u"horizontalLayoutKitsuTask")
        self.labelKitsuTask = QLabel(self.groupBoxTask)
        self.labelKitsuTask.setObjectName(u"labelKitsuTask")
        self.labelKitsuTask.setMinimumSize(QSize(100, 0))
        self.labelKitsuTask.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutKitsuTask.addWidget(self.labelKitsuTask)

        self.comboBoxKitsuTask = QComboBox(self.groupBoxTask)
        self.comboBoxKitsuTask.setObjectName(u"comboBoxKitsuTask")

        self.horizontalLayoutKitsuTask.addWidget(self.comboBoxKitsuTask)

        self.toolButtonRefreshKitsuTask = QToolButton(self.groupBoxTask)
        self.toolButtonRefreshKitsuTask.setObjectName(u"toolButtonRefreshKitsuTask")

        self.horizontalLayoutKitsuTask.addWidget(self.toolButtonRefreshKitsuTask)


        self.verticalLayout_6.addLayout(self.horizontalLayoutKitsuTask)

        self.horizontalLayoutTaskFrameRange = QHBoxLayout()
        self.horizontalLayoutTaskFrameRange.setObjectName(u"horizontalLayoutTaskFrameRange")
        self.labelTaskFrameRange = QLabel(self.groupBoxTask)
        self.labelTaskFrameRange.setObjectName(u"labelTaskFrameRange")
        self.labelTaskFrameRange.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutTaskFrameRange.addWidget(self.labelTaskFrameRange)

        self.lineEditTaskFrameRange = QLineEdit(self.groupBoxTask)
        self.lineEditTaskFrameRange.setObjectName(u"lineEditTaskFrameRange")
        self.lineEditTaskFrameRange.setReadOnly(True)

        self.horizontalLayoutTaskFrameRange.addWidget(self.lineEditTaskFrameRange)


        self.verticalLayout_6.addLayout(self.horizontalLayoutTaskFrameRange)

        self.textEditTaskData = QTextEdit(self.groupBoxTask)
        self.textEditTaskData.setObjectName(u"textEditTaskData")
        self.textEditTaskData.setMinimumSize(QSize(0, 0))

        self.verticalLayout_6.addWidget(self.textEditTaskData)


        self.verticalLayout_7.addWidget(self.groupBoxTask)

        self.groupBoxUnreal = QGroupBox(RenderSubmit)
        self.groupBoxUnreal.setObjectName(u"groupBoxUnreal")
        self.verticalLayout = QVBoxLayout(self.groupBoxUnreal)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayoutUEProject = QHBoxLayout()
        self.horizontalLayoutUEProject.setObjectName(u"horizontalLayoutUEProject")
        self.labelUEProject = QLabel(self.groupBoxUnreal)
        self.labelUEProject.setObjectName(u"labelUEProject")
        self.labelUEProject.setMinimumSize(QSize(100, 0))
        self.labelUEProject.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutUEProject.addWidget(self.labelUEProject)

        self.lineEditUEProject = QLineEdit(self.groupBoxUnreal)
        self.lineEditUEProject.setObjectName(u"lineEditUEProject")
        self.lineEditUEProject.setEnabled(True)

        self.horizontalLayoutUEProject.addWidget(self.lineEditUEProject)

        self.toolButtonUnrealProject = QToolButton(self.groupBoxUnreal)
        self.toolButtonUnrealProject.setObjectName(u"toolButtonUnrealProject")

        self.horizontalLayoutUEProject.addWidget(self.toolButtonUnrealProject)


        self.verticalLayout.addLayout(self.horizontalLayoutUEProject)


        self.verticalLayout_7.addWidget(self.groupBoxUnreal)

        self.groupBoxSequence = QGroupBox(RenderSubmit)
        self.groupBoxSequence.setObjectName(u"groupBoxSequence")
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxSequence)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayoutLevelDir = QHBoxLayout()
        self.horizontalLayoutLevelDir.setObjectName(u"horizontalLayoutLevelDir")
        self.labelLevelDir = QLabel(self.groupBoxSequence)
        self.labelLevelDir.setObjectName(u"labelLevelDir")
        self.labelLevelDir.setMinimumSize(QSize(100, 0))
        self.labelLevelDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutLevelDir.addWidget(self.labelLevelDir)

        self.lineEditSequenceDir = QLineEdit(self.groupBoxSequence)
        self.lineEditSequenceDir.setObjectName(u"lineEditSequenceDir")

        self.horizontalLayoutLevelDir.addWidget(self.lineEditSequenceDir)

        self.toolButtonSequence = QToolButton(self.groupBoxSequence)
        self.toolButtonSequence.setObjectName(u"toolButtonSequence")

        self.horizontalLayoutLevelDir.addWidget(self.toolButtonSequence)


        self.verticalLayout_3.addLayout(self.horizontalLayoutLevelDir)

        self.horizontalLayoutSequenceAsset = QHBoxLayout()
        self.horizontalLayoutSequenceAsset.setObjectName(u"horizontalLayoutSequenceAsset")
        self.labelLevelAsset = QLabel(self.groupBoxSequence)
        self.labelLevelAsset.setObjectName(u"labelLevelAsset")
        self.labelLevelAsset.setMinimumSize(QSize(100, 0))
        self.labelLevelAsset.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutSequenceAsset.addWidget(self.labelLevelAsset)

        self.comboBoxSequenceAsset = QComboBox(self.groupBoxSequence)
        self.comboBoxSequenceAsset.setObjectName(u"comboBoxSequenceAsset")

        self.horizontalLayoutSequenceAsset.addWidget(self.comboBoxSequenceAsset)

        self.toolButtonRefreshSequenceAsset = QToolButton(self.groupBoxSequence)
        self.toolButtonRefreshSequenceAsset.setObjectName(u"toolButtonRefreshSequenceAsset")

        self.horizontalLayoutSequenceAsset.addWidget(self.toolButtonRefreshSequenceAsset)


        self.verticalLayout_3.addLayout(self.horizontalLayoutSequenceAsset)


        self.verticalLayout_7.addWidget(self.groupBoxSequence)

        self.groupBoxMap = QGroupBox(RenderSubmit)
        self.groupBoxMap.setObjectName(u"groupBoxMap")
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxMap)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayoutMapFolder = QHBoxLayout()
        self.horizontalLayoutMapFolder.setObjectName(u"horizontalLayoutMapFolder")
        self.labelMapDir = QLabel(self.groupBoxMap)
        self.labelMapDir.setObjectName(u"labelMapDir")
        self.labelMapDir.setMinimumSize(QSize(100, 0))
        self.labelMapDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutMapFolder.addWidget(self.labelMapDir)

        self.lineEditMapDir = QLineEdit(self.groupBoxMap)
        self.lineEditMapDir.setObjectName(u"lineEditMapDir")

        self.horizontalLayoutMapFolder.addWidget(self.lineEditMapDir)

        self.toolButtonMap = QToolButton(self.groupBoxMap)
        self.toolButtonMap.setObjectName(u"toolButtonMap")

        self.horizontalLayoutMapFolder.addWidget(self.toolButtonMap)


        self.verticalLayout_2.addLayout(self.horizontalLayoutMapFolder)

        self.horizontalLayoutMapAsset = QHBoxLayout()
        self.horizontalLayoutMapAsset.setObjectName(u"horizontalLayoutMapAsset")
        self.labelMapAsset = QLabel(self.groupBoxMap)
        self.labelMapAsset.setObjectName(u"labelMapAsset")
        self.labelMapAsset.setMinimumSize(QSize(100, 0))
        self.labelMapAsset.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutMapAsset.addWidget(self.labelMapAsset)

        self.comboBoxMapAsset = QComboBox(self.groupBoxMap)
        self.comboBoxMapAsset.setObjectName(u"comboBoxMapAsset")

        self.horizontalLayoutMapAsset.addWidget(self.comboBoxMapAsset)

        self.toolButtonRefreshMapAsset = QToolButton(self.groupBoxMap)
        self.toolButtonRefreshMapAsset.setObjectName(u"toolButtonRefreshMapAsset")

        self.horizontalLayoutMapAsset.addWidget(self.toolButtonRefreshMapAsset)


        self.verticalLayout_2.addLayout(self.horizontalLayoutMapAsset)


        self.verticalLayout_7.addWidget(self.groupBoxMap)

        self.groupBoxPreset = QGroupBox(RenderSubmit)
        self.groupBoxPreset.setObjectName(u"groupBoxPreset")
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxPreset)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayoutPresetDir = QHBoxLayout()
        self.horizontalLayoutPresetDir.setObjectName(u"horizontalLayoutPresetDir")
        self.labelPresetDir = QLabel(self.groupBoxPreset)
        self.labelPresetDir.setObjectName(u"labelPresetDir")
        self.labelPresetDir.setMinimumSize(QSize(100, 0))
        self.labelPresetDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutPresetDir.addWidget(self.labelPresetDir)

        self.lineEditPresetDir = QLineEdit(self.groupBoxPreset)
        self.lineEditPresetDir.setObjectName(u"lineEditPresetDir")

        self.horizontalLayoutPresetDir.addWidget(self.lineEditPresetDir)

        self.toolButtonPreset = QToolButton(self.groupBoxPreset)
        self.toolButtonPreset.setObjectName(u"toolButtonPreset")

        self.horizontalLayoutPresetDir.addWidget(self.toolButtonPreset)


        self.verticalLayout_4.addLayout(self.horizontalLayoutPresetDir)

        self.horizontalLayoutPresetAsset = QHBoxLayout()
        self.horizontalLayoutPresetAsset.setObjectName(u"horizontalLayoutPresetAsset")
        self.labelPreset = QLabel(self.groupBoxPreset)
        self.labelPreset.setObjectName(u"labelPreset")
        self.labelPreset.setMinimumSize(QSize(100, 0))
        self.labelPreset.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutPresetAsset.addWidget(self.labelPreset)

        self.comboBoxPreset = QComboBox(self.groupBoxPreset)
        self.comboBoxPreset.setObjectName(u"comboBoxPreset")

        self.horizontalLayoutPresetAsset.addWidget(self.comboBoxPreset)

        self.toolButtonRefreshPresets = QToolButton(self.groupBoxPreset)
        self.toolButtonRefreshPresets.setObjectName(u"toolButtonRefreshPresets")

        self.horizontalLayoutPresetAsset.addWidget(self.toolButtonRefreshPresets)


        self.verticalLayout_4.addLayout(self.horizontalLayoutPresetAsset)

        self.horizontalLayoutOutputDir = QHBoxLayout()
        self.horizontalLayoutOutputDir.setObjectName(u"horizontalLayoutOutputDir")
        self.labelOutputDir = QLabel(self.groupBoxPreset)
        self.labelOutputDir.setObjectName(u"labelOutputDir")
        self.labelOutputDir.setMinimumSize(QSize(100, 0))
        self.labelOutputDir.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayoutOutputDir.addWidget(self.labelOutputDir)

        self.lineEditOutputDir = QLineEdit(self.groupBoxPreset)
        self.lineEditOutputDir.setObjectName(u"lineEditOutputDir")

        self.horizontalLayoutOutputDir.addWidget(self.lineEditOutputDir)

        self.toolButtonOutput = QToolButton(self.groupBoxPreset)
        self.toolButtonOutput.setObjectName(u"toolButtonOutput")

        self.horizontalLayoutOutputDir.addWidget(self.toolButtonOutput)


        self.verticalLayout_4.addLayout(self.horizontalLayoutOutputDir)

        self.horizontalLayoutFrameInfo = QHBoxLayout()
        self.horizontalLayoutFrameInfo.setObjectName(u"horizontalLayoutFrameInfo")
        self.checkBoxFrameIn = QCheckBox(self.groupBoxPreset)
        self.checkBoxFrameIn.setObjectName(u"checkBoxFrameIn")
        self.checkBoxFrameIn.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutFrameInfo.addWidget(self.checkBoxFrameIn)

        self.spinBoxFrameIn = QSpinBox(self.groupBoxPreset)
        self.spinBoxFrameIn.setObjectName(u"spinBoxFrameIn")
        self.spinBoxFrameIn.setMinimumSize(QSize(50, 0))
        self.spinBoxFrameIn.setMaximum(999999)

        self.horizontalLayoutFrameInfo.addWidget(self.spinBoxFrameIn)

        self.labelFrameOut = QLabel(self.groupBoxPreset)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(0, 0))

        self.horizontalLayoutFrameInfo.addWidget(self.labelFrameOut)

        self.spinBoxFrameOut = QSpinBox(self.groupBoxPreset)
        self.spinBoxFrameOut.setObjectName(u"spinBoxFrameOut")
        self.spinBoxFrameOut.setMinimumSize(QSize(50, 0))
        self.spinBoxFrameOut.setMaximum(999999)
        self.spinBoxFrameOut.setValue(0)

        self.horizontalLayoutFrameInfo.addWidget(self.spinBoxFrameOut)

        self.labelFrameCount = QLabel(self.groupBoxPreset)
        self.labelFrameCount.setObjectName(u"labelFrameCount")

        self.horizontalLayoutFrameInfo.addWidget(self.labelFrameCount)

        self.spinBoxFrameCount = QSpinBox(self.groupBoxPreset)
        self.spinBoxFrameCount.setObjectName(u"spinBoxFrameCount")
        self.spinBoxFrameCount.setEnabled(True)
        self.spinBoxFrameCount.setMinimumSize(QSize(50, 0))
        self.spinBoxFrameCount.setReadOnly(True)
        self.spinBoxFrameCount.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxFrameCount.setProperty("showGroupSeparator", True)
        self.spinBoxFrameCount.setMaximum(999999)
        self.spinBoxFrameCount.setValue(1)

        self.horizontalLayoutFrameInfo.addWidget(self.spinBoxFrameCount)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFrameInfo.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayoutFrameInfo)


        self.verticalLayout_7.addWidget(self.groupBoxPreset)

        self.groupBoxDialogControl = QGroupBox(RenderSubmit)
        self.groupBoxDialogControl.setObjectName(u"groupBoxDialogControl")
        self.verticalLayout_5 = QVBoxLayout(self.groupBoxDialogControl)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.horizontalLayoutDialogControl = QHBoxLayout()
        self.horizontalLayoutDialogControl.setObjectName(u"horizontalLayoutDialogControl")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutDialogControl.addItem(self.horizontalSpacer)

        self.pushButtonSubmit = QPushButton(self.groupBoxDialogControl)
        self.pushButtonSubmit.setObjectName(u"pushButtonSubmit")

        self.horizontalLayoutDialogControl.addWidget(self.pushButtonSubmit)

        self.pushButtonClose = QPushButton(self.groupBoxDialogControl)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayoutDialogControl.addWidget(self.pushButtonClose)


        self.verticalLayout_5.addLayout(self.horizontalLayoutDialogControl)


        self.verticalLayout_7.addWidget(self.groupBoxDialogControl)


        self.retranslateUi(RenderSubmit)

        self.pushButtonSubmit.setDefault(True)


        QMetaObject.connectSlotsByName(RenderSubmit)
    # setupUi

    def retranslateUi(self, RenderSubmit):
        RenderSubmit.setWindowTitle(fakestr(u"Submit Remote Render", None))
        self.groupBoxTask.setTitle(fakestr(u"Kitsu", None))
        self.labelKitsuProject.setText(fakestr(u"Project:", None))
        self.toolButtonRefreshKitsuProject.setText(fakestr(u"...", None))
        self.labelKitsuTask.setText(fakestr(u"Task:", None))
        self.toolButtonRefreshKitsuTask.setText(fakestr(u"...", None))
        self.labelTaskFrameRange.setText(fakestr(u"Frame Range:", None))
        self.groupBoxUnreal.setTitle(fakestr(u"Unreal:", None))
        self.labelUEProject.setText(fakestr(u"Project:", None))
        self.toolButtonUnrealProject.setText(fakestr(u"...", None))
        self.groupBoxSequence.setTitle(fakestr(u"Level Sequence:", None))
        self.labelLevelDir.setText(fakestr(u"Folder:", None))
        self.toolButtonSequence.setText(fakestr(u"...", None))
        self.labelLevelAsset.setText(fakestr(u"Sequence", None))
        self.toolButtonRefreshSequenceAsset.setText(fakestr(u"...", None))
        self.groupBoxMap.setTitle(fakestr(u"Map Selection:", None))
        self.labelMapDir.setText(fakestr(u"Folder:", None))
        self.toolButtonMap.setText(fakestr(u"...", None))
        self.labelMapAsset.setText(fakestr(u"Map:", None))
        self.toolButtonRefreshMapAsset.setText(fakestr(u"...", None))
        self.groupBoxPreset.setTitle(fakestr(u"Render Preset:", None))
        self.labelPresetDir.setText(fakestr(u"Folder:", None))
        self.toolButtonPreset.setText(fakestr(u"...", None))
        self.labelPreset.setText(fakestr(u"Preset:", None))
        self.toolButtonRefreshPresets.setText(fakestr(u"...", None))
        self.labelOutputDir.setText(fakestr(u"Output Folder:", None))
        self.toolButtonOutput.setText(fakestr(u"...", None))
        self.checkBoxFrameIn.setText(fakestr(u"Frame In", None))
        self.labelFrameOut.setText(fakestr(u"Frame Out", None))
        self.labelFrameCount.setText(fakestr(u"Frame Count", None))
        self.groupBoxDialogControl.setTitle("")
        self.pushButtonSubmit.setText(fakestr(u"Submit", None))
        self.pushButtonClose.setText(fakestr(u"Close", None))
    # retranslateUi

