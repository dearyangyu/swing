# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loader_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_LoaderDialog(object):
    def setupUi(self, LoaderDialog):
        if not LoaderDialog.objectName():
            LoaderDialog.setObjectName(u"LoaderDialog")
        LoaderDialog.setEnabled(True)
        LoaderDialog.resize(651, 598)
        self.verticalLayout = QVBoxLayout(LoaderDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEntity = QLabel(LoaderDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(LoaderDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")

        self.horizontalLayout_2.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(LoaderDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")

        self.horizontalLayout_2.addWidget(self.toolButtonWeb)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutWorkingFile = QHBoxLayout()
        self.horizontalLayoutWorkingFile.setObjectName(u"horizontalLayoutWorkingFile")
        self.labelWorkingFile = QLabel(LoaderDialog)
        self.labelWorkingFile.setObjectName(u"labelWorkingFile")
        self.labelWorkingFile.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutWorkingFile.addWidget(self.labelWorkingFile)

        self.comboBoxWorkingFile = QComboBox(LoaderDialog)
        self.comboBoxWorkingFile.setObjectName(u"comboBoxWorkingFile")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxWorkingFile.sizePolicy().hasHeightForWidth())
        self.comboBoxWorkingFile.setSizePolicy(sizePolicy)

        self.horizontalLayoutWorkingFile.addWidget(self.comboBoxWorkingFile)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutWorkingFile)

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.horizontalLayoutFrameDetails = QHBoxLayout()
        self.horizontalLayoutFrameDetails.setObjectName(u"horizontalLayoutFrameDetails")
        self.labelFrames = QLabel(LoaderDialog)
        self.labelFrames.setObjectName(u"labelFrames")
        self.labelFrames.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutFrameDetails.addWidget(self.labelFrames)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFrameIn = QLabel(LoaderDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(50, 0))
        self.labelFrameIn.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(LoaderDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")

        self.horizontalLayout_3.addWidget(self.lineEditFrameIn)

        self.labelFrameOut = QLabel(LoaderDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(50, 0))
        self.labelFrameOut.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(LoaderDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")

        self.horizontalLayout_3.addWidget(self.lineEditFrameOut)

        self.labelFrameCount = QLabel(LoaderDialog)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(50, 0))
        self.labelFrameCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(LoaderDialog)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")

        self.horizontalLayout_3.addWidget(self.lineEditFrameCount)


        self.horizontalLayoutFrameDetails.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFrameDetails.addItem(self.horizontalSpacer)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutFrameDetails)

        self.label = QLabel(LoaderDialog)
        self.label.setObjectName(u"label")

        self.verticalLayoutEntityInfo.addWidget(self.label)

        self.textEditShotInfo = QTextEdit(LoaderDialog)
        self.textEditShotInfo.setObjectName(u"textEditShotInfo")
        self.textEditShotInfo.setReadOnly(True)

        self.verticalLayoutEntityInfo.addWidget(self.textEditShotInfo)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)

        self.horizontalLayoutProjectDir = QHBoxLayout()
        self.horizontalLayoutProjectDir.setObjectName(u"horizontalLayoutProjectDir")
        self.cbDownloadTarget = QCheckBox(LoaderDialog)
        self.cbDownloadTarget.setObjectName(u"cbDownloadTarget")
        self.cbDownloadTarget.setMinimumSize(QSize(120, 0))
        self.cbDownloadTarget.setAutoExclusive(False)

        self.horizontalLayoutProjectDir.addWidget(self.cbDownloadTarget)

        self.lineEditTarget = QLineEdit(LoaderDialog)
        self.lineEditTarget.setObjectName(u"lineEditTarget")

        self.horizontalLayoutProjectDir.addWidget(self.lineEditTarget)

        self.toolButtonTargetDir = QToolButton(LoaderDialog)
        self.toolButtonTargetDir.setObjectName(u"toolButtonTargetDir")

        self.horizontalLayoutProjectDir.addWidget(self.toolButtonTargetDir)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutProjectDir)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cbNetworkSource = QCheckBox(LoaderDialog)
        self.cbNetworkSource.setObjectName(u"cbNetworkSource")
        self.cbNetworkSource.setMinimumSize(QSize(120, 0))
        self.cbNetworkSource.setAutoExclusive(False)

        self.horizontalLayout_5.addWidget(self.cbNetworkSource)

        self.lineEditNetworkSource = QLineEdit(LoaderDialog)
        self.lineEditNetworkSource.setObjectName(u"lineEditNetworkSource")

        self.horizontalLayout_5.addWidget(self.lineEditNetworkSource)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelNetworkMessage = QLabel(LoaderDialog)
        self.labelNetworkMessage.setObjectName(u"labelNetworkMessage")
        self.labelNetworkMessage.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.labelNetworkMessage)

        self.labelArchiveMessage = QLabel(LoaderDialog)
        self.labelArchiveMessage.setObjectName(u"labelArchiveMessage")

        self.verticalLayout_2.addWidget(self.labelArchiveMessage)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayoutOptions = QVBoxLayout()
        self.verticalLayoutOptions.setObjectName(u"verticalLayoutOptions")
        self.checkBoxSkipExisting = QCheckBox(LoaderDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setMinimumSize(QSize(100, 0))
        self.checkBoxSkipExisting.setStyleSheet(u"")
        self.checkBoxSkipExisting.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxSkipExisting)

        self.checkBoxExtractZips = QCheckBox(LoaderDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setMinimumSize(QSize(100, 0))
        self.checkBoxExtractZips.setChecked(True)

        self.verticalLayoutOptions.addWidget(self.checkBoxExtractZips)

        self.checkBoxForce = QCheckBox(LoaderDialog)
        self.checkBoxForce.setObjectName(u"checkBoxForce")

        self.verticalLayoutOptions.addWidget(self.checkBoxForce)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.openRb = QRadioButton(LoaderDialog)
        self.openRb.setObjectName(u"openRb")
        self.openRb.setChecked(True)

        self.horizontalLayout_4.addWidget(self.openRb)

        self.importRb = QRadioButton(LoaderDialog)
        self.importRb.setObjectName(u"importRb")

        self.horizontalLayout_4.addWidget(self.importRb)

        self.referenceRb = QRadioButton(LoaderDialog)
        self.referenceRb.setObjectName(u"referenceRb")

        self.horizontalLayout_4.addWidget(self.referenceRb)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.spinBoxReferenceCount = QSpinBox(LoaderDialog)
        self.spinBoxReferenceCount.setObjectName(u"spinBoxReferenceCount")
        self.spinBoxReferenceCount.setMinimum(1)
        self.spinBoxReferenceCount.setMaximum(999999)

        self.horizontalLayout_4.addWidget(self.spinBoxReferenceCount)

        self.checkBoxNamespace = QCheckBox(LoaderDialog)
        self.checkBoxNamespace.setObjectName(u"checkBoxNamespace")
        self.checkBoxNamespace.setChecked(True)

        self.horizontalLayout_4.addWidget(self.checkBoxNamespace)

        self.lineEditNamespace = QLineEdit(LoaderDialog)
        self.lineEditNamespace.setObjectName(u"lineEditNamespace")

        self.horizontalLayout_4.addWidget(self.lineEditNamespace)


        self.verticalLayoutOptions.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.verticalLayoutOptions)

        self.verticalLayoutFiles = QVBoxLayout()
        self.verticalLayoutFiles.setObjectName(u"verticalLayoutFiles")
        self.labelFiles = QLabel(LoaderDialog)
        self.labelFiles.setObjectName(u"labelFiles")

        self.verticalLayoutFiles.addWidget(self.labelFiles)

        self.textEditStatus = QTextEdit(LoaderDialog)
        self.textEditStatus.setObjectName(u"textEditStatus")

        self.verticalLayoutFiles.addWidget(self.textEditStatus)


        self.verticalLayout.addLayout(self.verticalLayoutFiles)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(LoaderDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButtonImport = QPushButton(LoaderDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")
        self.pushButtonImport.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.pushButtonCancel = QPushButton(LoaderDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setMinimumSize(QSize(80, 0))

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LoaderDialog)

        QMetaObject.connectSlotsByName(LoaderDialog)
    # setupUi

    def retranslateUi(self, LoaderDialog):
        LoaderDialog.setWindowTitle(fakestr(u"swing: downloader", None))
        self.labelEntity.setText(fakestr(u"Entity", None))
#if QT_CONFIG(tooltip)
        self.toolButtonWeb.setToolTip(fakestr(u"Opens link in Kitsu", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonWeb.setText(fakestr(u"Web", None))
        self.labelWorkingFile.setText(fakestr(u"Project File", None))
        self.labelFrames.setText(fakestr(u"Frame", None))
        self.labelFrameIn.setText(fakestr(u"In", None))
        self.labelFrameOut.setText(fakestr(u"Out", None))
        self.labelFrameCount.setText(fakestr(u"Count", None))
        self.label.setText(fakestr(u"Notes and Comments", None))
        self.cbDownloadTarget.setText(fakestr(u"Download Target:", None))
        self.toolButtonTargetDir.setText(fakestr(u"...", None))
        self.cbNetworkSource.setText(fakestr(u"Network Source:", None))
        self.labelNetworkMessage.setText("")
        self.labelArchiveMessage.setText("")
        self.checkBoxSkipExisting.setText(fakestr(u"Skip existing files", None))
        self.checkBoxExtractZips.setText(fakestr(u"Extract zip files automatically", None))
        self.checkBoxForce.setText(fakestr(u"Force load (Ignore unsaved changed)", None))
        self.openRb.setText(fakestr(u"Open File", None))
#if QT_CONFIG(shortcut)
        self.openRb.setShortcut(fakestr(u"Alt+O", None))
#endif // QT_CONFIG(shortcut)
        self.importRb.setText(fakestr(u"Import File", None))
#if QT_CONFIG(shortcut)
        self.importRb.setShortcut(fakestr(u"Alt+I", None))
#endif // QT_CONFIG(shortcut)
        self.referenceRb.setText(fakestr(u"Reference File", None))
#if QT_CONFIG(shortcut)
        self.referenceRb.setShortcut(fakestr(u"Alt+F", None))
#endif // QT_CONFIG(shortcut)
        self.checkBoxNamespace.setText(fakestr(u"Set Namespace", None))
#if QT_CONFIG(shortcut)
        self.checkBoxNamespace.setShortcut(fakestr(u"Alt+N", None))
#endif // QT_CONFIG(shortcut)
        self.labelFiles.setText(fakestr(u"Status", None))
        self.pushButtonImport.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

