# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'breakout_upload_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_BreakoutUploadDialog(object):
    def setupUi(self, BreakoutUploadDialog):
        if not BreakoutUploadDialog.objectName():
            BreakoutUploadDialog.setObjectName(u"BreakoutUploadDialog")
        BreakoutUploadDialog.setEnabled(True)
        BreakoutUploadDialog.resize(567, 513)
        self.verticalLayout = QVBoxLayout(BreakoutUploadDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutEpisodeSequence = QHBoxLayout()
        self.horizontalLayoutEpisodeSequence.setObjectName(u"horizontalLayoutEpisodeSequence")
        self.checkBoxSequence = QCheckBox(BreakoutUploadDialog)
        self.checkBoxSequence.setObjectName(u"checkBoxSequence")
        self.checkBoxSequence.setMinimumSize(QSize(100, 0))
        self.checkBoxSequence.setChecked(True)

        self.horizontalLayoutEpisodeSequence.addWidget(self.checkBoxSequence)

        self.comboBoxSequence = QComboBox(BreakoutUploadDialog)
        self.comboBoxSequence.setObjectName(u"comboBoxSequence")
        self.comboBoxSequence.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSequence.sizePolicy().hasHeightForWidth())
        self.comboBoxSequence.setSizePolicy(sizePolicy)
        self.comboBoxSequence.setMinimumSize(QSize(200, 0))
        self.comboBoxSequence.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxSequence)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(BreakoutUploadDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label)

        self.comboBoxNaming = QComboBox(BreakoutUploadDialog)
        self.comboBoxNaming.addItem("")
        self.comboBoxNaming.addItem("")
        self.comboBoxNaming.setObjectName(u"comboBoxNaming")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxNaming.sizePolicy().hasHeightForWidth())
        self.comboBoxNaming.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.comboBoxNaming)


        self.verticalLayoutProject.addLayout(self.horizontalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cbPlayblast = QCheckBox(BreakoutUploadDialog)
        self.cbPlayblast.setObjectName(u"cbPlayblast")
        self.cbPlayblast.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.cbPlayblast)

        self.lineEditPlayblastFolder = QLineEdit(BreakoutUploadDialog)
        self.lineEditPlayblastFolder.setObjectName(u"lineEditPlayblastFolder")

        self.horizontalLayout.addWidget(self.lineEditPlayblastFolder)

        self.toolButtonSelectPlayblasts = QToolButton(BreakoutUploadDialog)
        self.toolButtonSelectPlayblasts.setObjectName(u"toolButtonSelectPlayblasts")

        self.horizontalLayout.addWidget(self.toolButtonSelectPlayblasts)


        self.verticalLayoutProject.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.cbProjects = QCheckBox(BreakoutUploadDialog)
        self.cbProjects.setObjectName(u"cbProjects")
        self.cbProjects.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.cbProjects)

        self.lineEditProjectsFolder = QLineEdit(BreakoutUploadDialog)
        self.lineEditProjectsFolder.setObjectName(u"lineEditProjectsFolder")

        self.horizontalLayout_6.addWidget(self.lineEditProjectsFolder)

        self.toolButtonSelectProjects = QToolButton(BreakoutUploadDialog)
        self.toolButtonSelectProjects.setObjectName(u"toolButtonSelectProjects")

        self.horizontalLayout_6.addWidget(self.toolButtonSelectProjects)


        self.verticalLayoutProject.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cbAudio = QCheckBox(BreakoutUploadDialog)
        self.cbAudio.setObjectName(u"cbAudio")
        self.cbAudio.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.cbAudio)

        self.lineEdit_2 = QLineEdit(BreakoutUploadDialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)


        self.verticalLayoutProject.addLayout(self.horizontalLayout_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButtonLoad = QPushButton(BreakoutUploadDialog)
        self.pushButtonLoad.setObjectName(u"pushButtonLoad")

        self.horizontalLayout_8.addWidget(self.pushButtonLoad)

        self.pushButtonSave = QPushButton(BreakoutUploadDialog)
        self.pushButtonSave.setObjectName(u"pushButtonSave")

        self.horizontalLayout_8.addWidget(self.pushButtonSave)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout_8, 4, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButtonScan = QPushButton(BreakoutUploadDialog)
        self.pushButtonScan.setObjectName(u"pushButtonScan")

        self.horizontalLayout_9.addWidget(self.pushButtonScan)

        self.pushButtonFfprobe = QPushButton(BreakoutUploadDialog)
        self.pushButtonFfprobe.setObjectName(u"pushButtonFfprobe")

        self.horizontalLayout_9.addWidget(self.pushButtonFfprobe)

        self.pushButtonSetRange = QPushButton(BreakoutUploadDialog)
        self.pushButtonSetRange.setObjectName(u"pushButtonSetRange")

        self.horizontalLayout_9.addWidget(self.pushButtonSetRange)

        self.labelStartingAt = QLabel(BreakoutUploadDialog)
        self.labelStartingAt.setObjectName(u"labelStartingAt")

        self.horizontalLayout_9.addWidget(self.labelStartingAt)

        self.spinBoxStartingFrame = QSpinBox(BreakoutUploadDialog)
        self.spinBoxStartingFrame.setObjectName(u"spinBoxStartingFrame")
        self.spinBoxStartingFrame.setAccelerated(True)
        self.spinBoxStartingFrame.setMaximum(9999999)
        self.spinBoxStartingFrame.setValue(1)

        self.horizontalLayout_9.addWidget(self.spinBoxStartingFrame)

        self.checkBoxHandles = QCheckBox(BreakoutUploadDialog)
        self.checkBoxHandles.setObjectName(u"checkBoxHandles")
        self.checkBoxHandles.setChecked(True)

        self.horizontalLayout_9.addWidget(self.checkBoxHandles)

        self.spinBoxHandles = QSpinBox(BreakoutUploadDialog)
        self.spinBoxHandles.setObjectName(u"spinBoxHandles")

        self.horizontalLayout_9.addWidget(self.spinBoxHandles)


        self.gridLayout_2.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)

        self.checkBoxZip = QCheckBox(BreakoutUploadDialog)
        self.checkBoxZip.setObjectName(u"checkBoxZip")

        self.gridLayout_2.addWidget(self.checkBoxZip, 0, 0, 1, 1)


        self.verticalLayoutProject.addLayout(self.gridLayout_2)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableView = QTableView(BreakoutUploadDialog)
        self.tableView.setObjectName(u"tableView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(10)
        sizePolicy2.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy2)
        self.tableView.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setPointSize(9)
        self.tableView.setFont(font)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setWordWrap(False)

        self.horizontalLayout_3.addWidget(self.tableView)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonCreate = QPushButton(BreakoutUploadDialog)
        self.pushButtonCreate.setObjectName(u"pushButtonCreate")

        self.horizontalLayout_4.addWidget(self.pushButtonCreate)

        self.progressBar = QProgressBar(BreakoutUploadDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButtonCancel = QPushButton(BreakoutUploadDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.lineEdit = QLineEdit(BreakoutUploadDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)


        self.retranslateUi(BreakoutUploadDialog)

        QMetaObject.connectSlotsByName(BreakoutUploadDialog)
    # setupUi

    def retranslateUi(self, BreakoutUploadDialog):
        BreakoutUploadDialog.setWindowTitle(fakestr(u"Shot Breakout", None))
#if QT_CONFIG(tooltip)
        BreakoutUploadDialog.setToolTip(fakestr(u"Select playblast and project file directories to upload as Layout", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxSequence.setText(fakestr(u"Sequence", None))
        self.label.setText(fakestr(u"Naming", None))
        self.comboBoxNaming.setItemText(0, fakestr(u"{203}bun_{010}.{ext}", None))
        self.comboBoxNaming.setItemText(1, fakestr(u"{tg118wha}_{030}fun_{010}_v01", None))

        self.cbPlayblast.setText(fakestr(u"Playblasts", None))
#if QT_CONFIG(tooltip)
        self.lineEditPlayblastFolder.setToolTip(fakestr(u"Select a directory containing media files ###ABC_###", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSelectPlayblasts.setText(fakestr(u"...", None))
        self.cbProjects.setText(fakestr(u"Projects", None))
#if QT_CONFIG(tooltip)
        self.lineEditProjectsFolder.setToolTip(fakestr(u"Select a directory containing project files ###ABC_###", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSelectProjects.setText(fakestr(u"...", None))
        self.cbAudio.setText(fakestr(u"Audio", None))
        self.pushButtonLoad.setText(fakestr(u"Load", None))
        self.pushButtonSave.setText(fakestr(u"Save", None))
        self.pushButtonScan.setText(fakestr(u"Scan Folders", None))
        self.pushButtonFfprobe.setText(fakestr(u"Count Frames", None))
        self.pushButtonSetRange.setText(fakestr(u"Set Range", None))
        self.labelStartingAt.setText(fakestr(u"Starting at", None))
        self.checkBoxHandles.setText(fakestr(u"Add handles", None))
        self.checkBoxZip.setText(fakestr(u"Zip projects folder", None))
        self.pushButtonCreate.setText(fakestr(u"Create Shots", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

