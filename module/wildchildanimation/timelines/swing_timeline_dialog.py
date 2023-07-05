# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_timeline_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_SwingTimelineDialog(object):
    def setupUi(self, SwingTimelineDialog):
        if not SwingTimelineDialog.objectName():
            SwingTimelineDialog.setObjectName(u"SwingTimelineDialog")
        SwingTimelineDialog.resize(1010, 518)
        self.verticalLayout_2 = QVBoxLayout(SwingTimelineDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutProjectTitle = QHBoxLayout()
        self.horizontalLayoutProjectTitle.setObjectName(u"horizontalLayoutProjectTitle")
        self.labelProject = QLabel(SwingTimelineDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutProjectTitle.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(SwingTimelineDialog)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        self.comboBoxProject.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy)

        self.horizontalLayoutProjectTitle.addWidget(self.comboBoxProject)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutProjectTitle)

        self.horizontalLayoutEpisodeSequence = QHBoxLayout()
        self.horizontalLayoutEpisodeSequence.setObjectName(u"horizontalLayoutEpisodeSequence")
        self.labelShotEpisode = QLabel(SwingTimelineDialog)
        self.labelShotEpisode.setObjectName(u"labelShotEpisode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelShotEpisode.sizePolicy().hasHeightForWidth())
        self.labelShotEpisode.setSizePolicy(sizePolicy1)
        self.labelShotEpisode.setMinimumSize(QSize(100, 0))
        self.labelShotEpisode.setMaximumSize(QSize(60, 16777215))
        self.labelShotEpisode.setFont(font)
        self.labelShotEpisode.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotEpisode)

        self.comboBoxEpisode = QComboBox(SwingTimelineDialog)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        self.comboBoxEpisode.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxEpisode.sizePolicy().hasHeightForWidth())
        self.comboBoxEpisode.setSizePolicy(sizePolicy2)
        self.comboBoxEpisode.setMinimumSize(QSize(200, 0))
        self.comboBoxEpisode.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxEpisode)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProject)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEDLFile = QLabel(SwingTimelineDialog)
        self.labelEDLFile.setObjectName(u"labelEDLFile")
        self.labelEDLFile.setMinimumSize(QSize(100, 0))
        self.labelEDLFile.setFont(font)

        self.horizontalLayout_2.addWidget(self.labelEDLFile)

        self.lineEditEDLFile = QLineEdit(SwingTimelineDialog)
        self.lineEditEDLFile.setObjectName(u"lineEditEDLFile")

        self.horizontalLayout_2.addWidget(self.lineEditEDLFile)

        self.toolButtonSelectEDLFile = QToolButton(SwingTimelineDialog)
        self.toolButtonSelectEDLFile.setObjectName(u"toolButtonSelectEDLFile")

        self.horizontalLayout_2.addWidget(self.toolButtonSelectEDLFile)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelSource = QLabel(SwingTimelineDialog)
        self.labelSource.setObjectName(u"labelSource")
        self.labelSource.setMinimumSize(QSize(100, 0))
        self.labelSource.setFont(font)

        self.horizontalLayout_3.addWidget(self.labelSource)

        self.lineEditSource = QLineEdit(SwingTimelineDialog)
        self.lineEditSource.setObjectName(u"lineEditSource")

        self.horizontalLayout_3.addWidget(self.lineEditSource)

        self.toolButtonSelectSource = QToolButton(SwingTimelineDialog)
        self.toolButtonSelectSource.setObjectName(u"toolButtonSelectSource")

        self.horizontalLayout_3.addWidget(self.toolButtonSelectSource)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonScanXML = QPushButton(SwingTimelineDialog)
        self.pushButtonScanXML.setObjectName(u"pushButtonScanXML")

        self.horizontalLayout.addWidget(self.pushButtonScanXML)

        self.pushButtonUpdateKitsu = QPushButton(SwingTimelineDialog)
        self.pushButtonUpdateKitsu.setObjectName(u"pushButtonUpdateKitsu")

        self.horizontalLayout.addWidget(self.pushButtonUpdateKitsu)

        self.checkBoxForceUpload = QCheckBox(SwingTimelineDialog)
        self.checkBoxForceUpload.setObjectName(u"checkBoxForceUpload")

        self.horizontalLayout.addWidget(self.checkBoxForceUpload)

        self.checkBoxUploadVideo = QCheckBox(SwingTimelineDialog)
        self.checkBoxUploadVideo.setObjectName(u"checkBoxUploadVideo")

        self.horizontalLayout.addWidget(self.checkBoxUploadVideo)

        self.checkBoxUploadAudio = QCheckBox(SwingTimelineDialog)
        self.checkBoxUploadAudio.setObjectName(u"checkBoxUploadAudio")

        self.horizontalLayout.addWidget(self.checkBoxUploadAudio)

        self.checkBoxUploadImages = QCheckBox(SwingTimelineDialog)
        self.checkBoxUploadImages.setObjectName(u"checkBoxUploadImages")

        self.horizontalLayout.addWidget(self.checkBoxUploadImages)

        self.pushButtonUpdateTrackingSheet = QPushButton(SwingTimelineDialog)
        self.pushButtonUpdateTrackingSheet.setObjectName(u"pushButtonUpdateTrackingSheet")

        self.horizontalLayout.addWidget(self.pushButtonUpdateTrackingSheet)

        self.pushButtonExtractVideo = QPushButton(SwingTimelineDialog)
        self.pushButtonExtractVideo.setObjectName(u"pushButtonExtractVideo")

        self.horizontalLayout.addWidget(self.pushButtonExtractVideo)

        self.pushButtonExtractAudio = QPushButton(SwingTimelineDialog)
        self.pushButtonExtractAudio.setObjectName(u"pushButtonExtractAudio")

        self.horizontalLayout.addWidget(self.pushButtonExtractAudio)

        self.pushButtonExtractImages = QPushButton(SwingTimelineDialog)
        self.pushButtonExtractImages.setObjectName(u"pushButtonExtractImages")

        self.horizontalLayout.addWidget(self.pushButtonExtractImages)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.labelThreadCount = QLabel(SwingTimelineDialog)
        self.labelThreadCount.setObjectName(u"labelThreadCount")

        self.horizontalLayout.addWidget(self.labelThreadCount)

        self.spinBoxThreadCount = QSpinBox(SwingTimelineDialog)
        self.spinBoxThreadCount.setObjectName(u"spinBoxThreadCount")
        self.spinBoxThreadCount.setValue(3)

        self.horizontalLayout.addWidget(self.spinBoxThreadCount)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayoutShotTable = QVBoxLayout()
        self.verticalLayoutShotTable.setObjectName(u"verticalLayoutShotTable")
        self.tableView = QTableView(SwingTimelineDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setBaseSize(QSize(0, 0))

        self.verticalLayoutShotTable.addWidget(self.tableView)

        self.textEditLog = QTextEdit(SwingTimelineDialog)
        self.textEditLog.setObjectName(u"textEditLog")
        self.textEditLog.setMaximumSize(QSize(16777215, 100))

        self.verticalLayoutShotTable.addWidget(self.textEditLog)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pushButtonSelectAll = QPushButton(SwingTimelineDialog)
        self.pushButtonSelectAll.setObjectName(u"pushButtonSelectAll")

        self.horizontalLayoutButtons.addWidget(self.pushButtonSelectAll)

        self.pushButtonSelectNone = QPushButton(SwingTimelineDialog)
        self.pushButtonSelectNone.setObjectName(u"pushButtonSelectNone")

        self.horizontalLayoutButtons.addWidget(self.pushButtonSelectNone)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacer)

        self.pushButtonRunAll = QPushButton(SwingTimelineDialog)
        self.pushButtonRunAll.setObjectName(u"pushButtonRunAll")

        self.horizontalLayoutButtons.addWidget(self.pushButtonRunAll)

        self.pushButtonCancel = QPushButton(SwingTimelineDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)


        self.verticalLayoutShotTable.addLayout(self.horizontalLayoutButtons)


        self.verticalLayout_2.addLayout(self.verticalLayoutShotTable)


        self.retranslateUi(SwingTimelineDialog)

        QMetaObject.connectSlotsByName(SwingTimelineDialog)
    # setupUi

    def retranslateUi(self, SwingTimelineDialog):
        SwingTimelineDialog.setWindowTitle(fakestr(u"swing: timelines", None))
        self.labelProject.setText(fakestr(u"Project", None))
        self.labelShotEpisode.setText(fakestr(u"Episode", None))
        self.labelEDLFile.setText(fakestr(u"XML", None))
        self.toolButtonSelectEDLFile.setText(fakestr(u"...", None))
        self.labelSource.setText(fakestr(u"Source", None))
        self.toolButtonSelectSource.setText(fakestr(u"...", None))
        self.pushButtonScanXML.setText(fakestr(u"Scan XML", None))
        self.pushButtonUpdateKitsu.setText(fakestr(u"Update Kitsu", None))
        self.checkBoxForceUpload.setText(fakestr(u"Force", None))
        self.checkBoxUploadVideo.setText(fakestr(u"Upload Video", None))
        self.checkBoxUploadAudio.setText(fakestr(u"Upload Audio", None))
        self.checkBoxUploadImages.setText(fakestr(u"Upload Images", None))
        self.pushButtonUpdateTrackingSheet.setText(fakestr(u"Update Tracking Sheet", None))
        self.pushButtonExtractVideo.setText(fakestr(u"Extract Video", None))
        self.pushButtonExtractAudio.setText(fakestr(u"Extract Audio", None))
        self.pushButtonExtractImages.setText(fakestr(u"Extract Images", None))
        self.labelThreadCount.setText(fakestr(u"Thread Count:", None))
        self.pushButtonSelectAll.setText(fakestr(u"Select &All", None))
        self.pushButtonSelectNone.setText(fakestr(u"Select &None", None))
        self.pushButtonRunAll.setText(fakestr(u"Extract &All", None))
        self.pushButtonCancel.setText(fakestr(u"&Close", None))
    # retranslateUi

