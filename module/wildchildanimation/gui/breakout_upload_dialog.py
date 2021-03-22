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


class Ui_BreakoutUploadDialog(object):
    def setupUi(self, BreakoutUploadDialog):
        if not BreakoutUploadDialog.objectName():
            BreakoutUploadDialog.setObjectName(u"BreakoutUploadDialog")
        BreakoutUploadDialog.setEnabled(True)
        BreakoutUploadDialog.resize(924, 714)
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
        self.label.setAlignment(Qt.AlignCenter)

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
        self.labelPlayblastFolder = QLabel(BreakoutUploadDialog)
        self.labelPlayblastFolder.setObjectName(u"labelPlayblastFolder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelPlayblastFolder.sizePolicy().hasHeightForWidth())
        self.labelPlayblastFolder.setSizePolicy(sizePolicy2)
        self.labelPlayblastFolder.setMinimumSize(QSize(100, 0))
        self.labelPlayblastFolder.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelPlayblastFolder.setFont(font)
        self.labelPlayblastFolder.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelPlayblastFolder)

        self.lineEditPlayblastFolder = QLineEdit(BreakoutUploadDialog)
        self.lineEditPlayblastFolder.setObjectName(u"lineEditPlayblastFolder")

        self.horizontalLayout.addWidget(self.lineEditPlayblastFolder)

        self.toolButtonSelectPlayblasts = QToolButton(BreakoutUploadDialog)
        self.toolButtonSelectPlayblasts.setObjectName(u"toolButtonSelectPlayblasts")

        self.horizontalLayout.addWidget(self.toolButtonSelectPlayblasts)


        self.verticalLayoutProject.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelProjectsFolder = QLabel(BreakoutUploadDialog)
        self.labelProjectsFolder.setObjectName(u"labelProjectsFolder")
        sizePolicy2.setHeightForWidth(self.labelProjectsFolder.sizePolicy().hasHeightForWidth())
        self.labelProjectsFolder.setSizePolicy(sizePolicy2)
        self.labelProjectsFolder.setMinimumSize(QSize(100, 0))
        self.labelProjectsFolder.setMaximumSize(QSize(60, 16777215))
        self.labelProjectsFolder.setFont(font)
        self.labelProjectsFolder.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.labelProjectsFolder)

        self.lineEditProjectsFolder = QLineEdit(BreakoutUploadDialog)
        self.lineEditProjectsFolder.setObjectName(u"lineEditProjectsFolder")

        self.horizontalLayout_6.addWidget(self.lineEditProjectsFolder)

        self.toolButtonSelectProjects = QToolButton(BreakoutUploadDialog)
        self.toolButtonSelectProjects.setObjectName(u"toolButtonSelectProjects")

        self.horizontalLayout_6.addWidget(self.toolButtonSelectProjects)


        self.verticalLayoutProject.addLayout(self.horizontalLayout_6)

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

        self.horizontalLayout_9.addWidget(self.spinBoxStartingFrame)

        self.checkBoxHandles = QCheckBox(BreakoutUploadDialog)
        self.checkBoxHandles.setObjectName(u"checkBoxHandles")

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
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(10)
        sizePolicy3.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy3)
        self.tableView.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(9)
        self.tableView.setFont(font1)
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
        BreakoutUploadDialog.setWindowTitle(QCoreApplication.translate("BreakoutUploadDialog", u"Shot Breakout", None))
#if QT_CONFIG(tooltip)
        BreakoutUploadDialog.setToolTip(QCoreApplication.translate("BreakoutUploadDialog", u"Select playblast and project file directories to upload as Layout", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxSequence.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Sequence", None))
        self.label.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Naming", None))
        self.comboBoxNaming.setItemText(0, QCoreApplication.translate("BreakoutUploadDialog", u"{203}bun_{010}.{ext}", None))
        self.comboBoxNaming.setItemText(1, QCoreApplication.translate("BreakoutUploadDialog", u"{tg118wha}_{030}fun_{010}_v01", None))

        self.labelPlayblastFolder.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Playblasts", None))
#if QT_CONFIG(tooltip)
        self.lineEditPlayblastFolder.setToolTip(QCoreApplication.translate("BreakoutUploadDialog", u"Select a directory containing media files ###ABC_###", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSelectPlayblasts.setText(QCoreApplication.translate("BreakoutUploadDialog", u"...", None))
        self.labelProjectsFolder.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Projects", None))
#if QT_CONFIG(tooltip)
        self.lineEditProjectsFolder.setToolTip(QCoreApplication.translate("BreakoutUploadDialog", u"Select a directory containing project files ###ABC_###", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSelectProjects.setText(QCoreApplication.translate("BreakoutUploadDialog", u"...", None))
        self.pushButtonLoad.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Load", None))
        self.pushButtonSave.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Save", None))
        self.pushButtonScan.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Scan Folders", None))
        self.pushButtonFfprobe.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Count Frames", None))
        self.pushButtonSetRange.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Set Range", None))
        self.labelStartingAt.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Starting at", None))
        self.checkBoxHandles.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Add handles", None))
        self.checkBoxZip.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Zip projects folder", None))
        self.pushButtonCreate.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Create Shots", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("BreakoutUploadDialog", u"Close", None))
    # retranslateUi

