# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr
class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        if not DownloadDialog.objectName():
            DownloadDialog.setObjectName(u"DownloadDialog")
        DownloadDialog.setEnabled(True)
        DownloadDialog.resize(900, 480)
        DownloadDialog.setMinimumSize(QSize(640, 480))
        self.verticalLayout = QVBoxLayout(DownloadDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelEntity = QLabel(DownloadDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(DownloadDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")

        self.horizontalLayout_6.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(DownloadDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")

        self.horizontalLayout_6.addWidget(self.toolButtonWeb)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelWorkingDirectory = QLabel(DownloadDialog)
        self.labelWorkingDirectory.setObjectName(u"labelWorkingDirectory")
        self.labelWorkingDirectory.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.labelWorkingDirectory)

        self.lineEditWorkingDirectory = QLineEdit(DownloadDialog)
        self.lineEditWorkingDirectory.setObjectName(u"lineEditWorkingDirectory")

        self.horizontalLayout.addWidget(self.lineEditWorkingDirectory)

        self.toolButtonWorkingDir = QToolButton(DownloadDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")

        self.horizontalLayout.addWidget(self.toolButtonWorkingDir)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.checkBoxSkipExisting = QCheckBox(DownloadDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setMinimumSize(QSize(100, 0))
        self.checkBoxSkipExisting.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBoxSkipExisting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.checkBoxExtractZips = QCheckBox(DownloadDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBoxExtractZips)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolButtonAll = QToolButton(DownloadDialog)
        self.toolButtonAll.setObjectName(u"toolButtonAll")

        self.horizontalLayout_5.addWidget(self.toolButtonAll)

        self.toolButtonNone = QToolButton(DownloadDialog)
        self.toolButtonNone.setObjectName(u"toolButtonNone")

        self.horizontalLayout_5.addWidget(self.toolButtonNone)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.tableView = QTableView(DownloadDialog)
        self.tableView.setObjectName(u"tableView")
        font = QFont()
        font.setPointSize(8)
        self.tableView.setFont(font)
        self.tableView.setProperty("showDropIndicator", False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.verticalHeader().setCascadingSectionResizes(True)

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonDownload = QPushButton(DownloadDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout_4.addWidget(self.pushButtonDownload)

        self.progressBar = QProgressBar(DownloadDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButtonCancel = QPushButton(DownloadDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(DownloadDialog)

        self.pushButtonDownload.setDefault(True)


        QMetaObject.connectSlotsByName(DownloadDialog)
    # setupUi

    def retranslateUi(self, DownloadDialog):
        DownloadDialog.setWindowTitle(fakestr(u"Download Files", None))
        self.labelEntity.setText(fakestr(u"Entity", None))
        self.toolButtonWeb.setText(fakestr(u"...", None))
        self.labelWorkingDirectory.setText(fakestr(u"Root Folder", None))
        self.toolButtonWorkingDir.setText(fakestr(u"...", None))
        self.checkBoxSkipExisting.setText(fakestr(u"Skip Existing Files", None))
        self.checkBoxExtractZips.setText(fakestr(u"Extract Zip Files", None))
        self.toolButtonAll.setText(fakestr(u"+", None))
        self.toolButtonNone.setText(fakestr(u"-", None))
        self.pushButtonDownload.setText(fakestr(u"Download", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

