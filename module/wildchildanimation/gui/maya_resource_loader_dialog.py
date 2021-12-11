# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maya_resource_loader_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_MayaResourceLoaderDialog(object):
    def setupUi(self, MayaResourceLoaderDialog):
        if not MayaResourceLoaderDialog.objectName():
            MayaResourceLoaderDialog.setObjectName(u"MayaResourceLoaderDialog")
        MayaResourceLoaderDialog.setEnabled(True)
        MayaResourceLoaderDialog.resize(455, 541)
        self.verticalLayout = QVBoxLayout(MayaResourceLoaderDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayoutWorkingFile = QHBoxLayout()
        self.horizontalLayoutWorkingFile.setObjectName(u"horizontalLayoutWorkingFile")
        self.labelSource = QLabel(MayaResourceLoaderDialog)
        self.labelSource.setObjectName(u"labelSource")
        self.labelSource.setMinimumSize(QSize(125, 0))

        self.horizontalLayoutWorkingFile.addWidget(self.labelSource)

        self.lineEditSource = QLineEdit(MayaResourceLoaderDialog)
        self.lineEditSource.setObjectName(u"lineEditSource")

        self.horizontalLayoutWorkingFile.addWidget(self.lineEditSource)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutWorkingFile)

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.textEditInfo = QTextEdit(MayaResourceLoaderDialog)
        self.textEditInfo.setObjectName(u"textEditInfo")
        self.textEditInfo.setReadOnly(True)

        self.verticalLayoutEntityInfo.addWidget(self.textEditInfo)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelNetworkStatus = QLabel(MayaResourceLoaderDialog)
        self.labelNetworkStatus.setObjectName(u"labelNetworkStatus")
        self.labelNetworkStatus.setMinimumSize(QSize(125, 0))

        self.horizontalLayout_2.addWidget(self.labelNetworkStatus)

        self.lineEditNetworkStatus = QLineEdit(MayaResourceLoaderDialog)
        self.lineEditNetworkStatus.setObjectName(u"lineEditNetworkStatus")

        self.horizontalLayout_2.addWidget(self.lineEditNetworkStatus)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutProjectDir = QHBoxLayout()
        self.horizontalLayoutProjectDir.setObjectName(u"horizontalLayoutProjectDir")
        self.labelDownloadTarget = QLabel(MayaResourceLoaderDialog)
        self.labelDownloadTarget.setObjectName(u"labelDownloadTarget")
        self.labelDownloadTarget.setMinimumSize(QSize(125, 0))

        self.horizontalLayoutProjectDir.addWidget(self.labelDownloadTarget)

        self.lineEditTarget = QLineEdit(MayaResourceLoaderDialog)
        self.lineEditTarget.setObjectName(u"lineEditTarget")

        self.horizontalLayoutProjectDir.addWidget(self.lineEditTarget)

        self.toolButtonTargetDir = QToolButton(MayaResourceLoaderDialog)
        self.toolButtonTargetDir.setObjectName(u"toolButtonTargetDir")

        self.horizontalLayoutProjectDir.addWidget(self.toolButtonTargetDir)


        self.verticalLayout_3.addLayout(self.horizontalLayoutProjectDir)

        self.rbOpenSource = QRadioButton(MayaResourceLoaderDialog)
        self.rbOpenSource.setObjectName(u"rbOpenSource")

        self.verticalLayout_3.addWidget(self.rbOpenSource)

        self.rbImportSource = QRadioButton(MayaResourceLoaderDialog)
        self.rbImportSource.setObjectName(u"rbImportSource")

        self.verticalLayout_3.addWidget(self.rbImportSource)

        self.rbReferenceSource = QRadioButton(MayaResourceLoaderDialog)
        self.rbReferenceSource.setObjectName(u"rbReferenceSource")

        self.verticalLayout_3.addWidget(self.rbReferenceSource)


        self.verticalLayoutEntity.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelReferenceSource = QLabel(MayaResourceLoaderDialog)
        self.labelReferenceSource.setObjectName(u"labelReferenceSource")
        self.labelReferenceSource.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.labelReferenceSource)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.spinBoxReferenceCount = QSpinBox(MayaResourceLoaderDialog)
        self.spinBoxReferenceCount.setObjectName(u"spinBoxReferenceCount")
        self.spinBoxReferenceCount.setMinimum(1)
        self.spinBoxReferenceCount.setMaximum(999999)

        self.horizontalLayout_4.addWidget(self.spinBoxReferenceCount)

        self.checkBoxNamespace = QCheckBox(MayaResourceLoaderDialog)
        self.checkBoxNamespace.setObjectName(u"checkBoxNamespace")
        self.checkBoxNamespace.setChecked(True)

        self.horizontalLayout_4.addWidget(self.checkBoxNamespace)

        self.lineEditNamespace = QLineEdit(MayaResourceLoaderDialog)
        self.lineEditNamespace.setObjectName(u"lineEditNamespace")

        self.horizontalLayout_4.addWidget(self.lineEditNamespace)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelNetworkMessage = QLabel(MayaResourceLoaderDialog)
        self.labelNetworkMessage.setObjectName(u"labelNetworkMessage")
        self.labelNetworkMessage.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.labelNetworkMessage)

        self.labelArchiveMessage = QLabel(MayaResourceLoaderDialog)
        self.labelArchiveMessage.setObjectName(u"labelArchiveMessage")

        self.verticalLayout_2.addWidget(self.labelArchiveMessage)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayoutOptions = QVBoxLayout()
        self.verticalLayoutOptions.setObjectName(u"verticalLayoutOptions")
        self.checkBoxSkipExisting = QCheckBox(MayaResourceLoaderDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setMinimumSize(QSize(100, 0))
        self.checkBoxSkipExisting.setStyleSheet(u"")
        self.checkBoxSkipExisting.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxSkipExisting)

        self.checkBoxExtractZips = QCheckBox(MayaResourceLoaderDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setMinimumSize(QSize(100, 0))
        self.checkBoxExtractZips.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxExtractZips)

        self.checkBoxForce = QCheckBox(MayaResourceLoaderDialog)
        self.checkBoxForce.setObjectName(u"checkBoxForce")

        self.verticalLayoutOptions.addWidget(self.checkBoxForce)


        self.verticalLayout.addLayout(self.verticalLayoutOptions)

        self.verticalLayoutFiles = QVBoxLayout()
        self.verticalLayoutFiles.setObjectName(u"verticalLayoutFiles")
        self.labelFiles = QLabel(MayaResourceLoaderDialog)
        self.labelFiles.setObjectName(u"labelFiles")

        self.verticalLayoutFiles.addWidget(self.labelFiles)

        self.textEditStatus = QTextEdit(MayaResourceLoaderDialog)
        self.textEditStatus.setObjectName(u"textEditStatus")

        self.verticalLayoutFiles.addWidget(self.textEditStatus)


        self.verticalLayout.addLayout(self.verticalLayoutFiles)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(MayaResourceLoaderDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButtonImport = QPushButton(MayaResourceLoaderDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")
        self.pushButtonImport.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.pushButtonCancel = QPushButton(MayaResourceLoaderDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(MayaResourceLoaderDialog)

        QMetaObject.connectSlotsByName(MayaResourceLoaderDialog)
    # setupUi

    def retranslateUi(self, MayaResourceLoaderDialog):
        MayaResourceLoaderDialog.setWindowTitle(fakestr(u"swing: downloader", None))
        self.labelSource.setText(fakestr(u"Resource Source:", None))
        self.labelNetworkStatus.setText(fakestr(u"Network Status: ", None))
        self.labelDownloadTarget.setText(fakestr(u"Download Target:", None))
#if QT_CONFIG(statustip)
        self.lineEditTarget.setStatusTip(fakestr(u"Where to download and extract if file is an archive or not available on the local network", None))
#endif // QT_CONFIG(statustip)
        self.toolButtonTargetDir.setText(fakestr(u"...", None))
#if QT_CONFIG(statustip)
        self.rbOpenSource.setStatusTip(fakestr(u"Open resource from location", None))
#endif // QT_CONFIG(statustip)
        self.rbOpenSource.setText(fakestr(u"Open Resource", None))
#if QT_CONFIG(shortcut)
        self.rbOpenSource.setShortcut(fakestr(u"Alt+O", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(statustip)
        self.rbImportSource.setStatusTip(fakestr(u"Import resource into scene", None))
#endif // QT_CONFIG(statustip)
        self.rbImportSource.setText(fakestr(u"Import Resource", None))
#if QT_CONFIG(shortcut)
        self.rbImportSource.setShortcut(fakestr(u"Alt+I", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(statustip)
        self.rbReferenceSource.setStatusTip(fakestr(u"Reference reference into scene", None))
#endif // QT_CONFIG(statustip)
        self.rbReferenceSource.setText(fakestr(u"Reference Resource", None))
#if QT_CONFIG(shortcut)
        self.rbReferenceSource.setShortcut(fakestr(u"Alt+R", None))
#endif // QT_CONFIG(shortcut)
        self.labelReferenceSource.setText(fakestr(u"Referencing", None))
        self.checkBoxNamespace.setText(fakestr(u"Set Namespace", None))
#if QT_CONFIG(shortcut)
        self.checkBoxNamespace.setShortcut(fakestr(u"Alt+N", None))
#endif // QT_CONFIG(shortcut)
        self.labelNetworkMessage.setText("")
        self.labelArchiveMessage.setText("")
#if QT_CONFIG(statustip)
        self.checkBoxSkipExisting.setStatusTip(fakestr(u"Will not overwrite file if it already exists", None))
#endif // QT_CONFIG(statustip)
        self.checkBoxSkipExisting.setText(fakestr(u"Skip existing files", None))
        self.checkBoxExtractZips.setText(fakestr(u"Extract zip files automatically", None))
        self.checkBoxForce.setText(fakestr(u"Force load (Ignore unsaved changed)", None))
        self.labelFiles.setText(fakestr(u"Status", None))
        self.pushButtonImport.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

