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


class Ui_DownloadDialog(object):
    def setupUi(self, DownloadDialog):
        if not DownloadDialog.objectName():
            DownloadDialog.setObjectName(u"DownloadDialog")
        DownloadDialog.resize(1002, 439)
        self.verticalLayout_2 = QVBoxLayout(DownloadDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelWorkingDirectory = QLabel(DownloadDialog)
        self.labelWorkingDirectory.setObjectName(u"labelWorkingDirectory")

        self.horizontalLayout.addWidget(self.labelWorkingDirectory)

        self.lineEditWorkingDirectory = QLineEdit(DownloadDialog)
        self.lineEditWorkingDirectory.setObjectName(u"lineEditWorkingDirectory")

        self.horizontalLayout.addWidget(self.lineEditWorkingDirectory)

        self.pushButtonSelectWorkingDir = QPushButton(DownloadDialog)
        self.pushButtonSelectWorkingDir.setObjectName(u"pushButtonSelectWorkingDir")

        self.horizontalLayout.addWidget(self.pushButtonSelectWorkingDir)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBoxSkipExisting = QCheckBox(DownloadDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBoxSkipExisting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBoxExtractZip = QCheckBox(DownloadDialog)
        self.checkBoxExtractZip.setObjectName(u"checkBoxExtractZip")
        self.checkBoxExtractZip.setChecked(False)

        self.horizontalLayout_3.addWidget(self.checkBoxExtractZip)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.tableView = QTableView(DownloadDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_2.addWidget(self.tableView)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.pushButtonDownload = QPushButton(DownloadDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout_4.addWidget(self.pushButtonDownload)

        self.pushButtonCancel = QPushButton(DownloadDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.retranslateUi(DownloadDialog)

        self.pushButtonDownload.setDefault(True)


        QMetaObject.connectSlotsByName(DownloadDialog)
    # setupUi

    def retranslateUi(self, DownloadDialog):
        DownloadDialog.setWindowTitle(QCoreApplication.translate("DownloadDialog", u"Download Files", None))
        self.labelWorkingDirectory.setText(QCoreApplication.translate("DownloadDialog", u"Working Directory:", None))
        self.pushButtonSelectWorkingDir.setText(QCoreApplication.translate("DownloadDialog", u"Select", None))
        self.checkBoxSkipExisting.setText(QCoreApplication.translate("DownloadDialog", u"Skip Existing Files", None))
        self.checkBoxExtractZip.setText(QCoreApplication.translate("DownloadDialog", u"Extract Zip Files", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("DownloadDialog", u"Download", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DownloadDialog", u"Cancel", None))
    # retranslateUi

