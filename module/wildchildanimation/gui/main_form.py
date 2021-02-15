# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WcaMayaDialog(object):
    def setupUi(self, WcaMayaDialog):
        if not WcaMayaDialog.objectName():
            WcaMayaDialog.setObjectName(u"WcaMayaDialog")
        WcaMayaDialog.resize(650, 491)
        self.verticalLayout = QVBoxLayout(WcaMayaDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.connectionLayout = QHBoxLayout()
        self.connectionLayout.setObjectName(u"connectionLayout")
        self.pushButtonSettings = QPushButton(WcaMayaDialog)
        self.pushButtonSettings.setObjectName(u"pushButtonSettings")

        self.connectionLayout.addWidget(self.pushButtonSettings)

        self.pushButtonConnect = QPushButton(WcaMayaDialog)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")
        self.pushButtonConnect.setAutoFillBackground(False)
        self.pushButtonConnect.setStyleSheet(u"color: rgb(0, 255, 122)")

        self.connectionLayout.addWidget(self.pushButtonConnect)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.connectionLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.connectionLayout)

        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutProjectTitle = QHBoxLayout()
        self.horizontalLayoutProjectTitle.setObjectName(u"horizontalLayoutProjectTitle")
        self.labelProject = QLabel(WcaMayaDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutProjectTitle.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(WcaMayaDialog)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy)

        self.horizontalLayoutProjectTitle.addWidget(self.comboBoxProject)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutProjectTitle)

        self.horizontalLayoutEpisodeSequence = QHBoxLayout()
        self.horizontalLayoutEpisodeSequence.setObjectName(u"horizontalLayoutEpisodeSequence")
        self.labelShotEpisode = QLabel(WcaMayaDialog)
        self.labelShotEpisode.setObjectName(u"labelShotEpisode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelShotEpisode.sizePolicy().hasHeightForWidth())
        self.labelShotEpisode.setSizePolicy(sizePolicy1)
        self.labelShotEpisode.setMinimumSize(QSize(100, 0))
        self.labelShotEpisode.setMaximumSize(QSize(60, 16777215))
        self.labelShotEpisode.setFont(font)
        self.labelShotEpisode.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotEpisode)

        self.comboBoxEpisode = QComboBox(WcaMayaDialog)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        self.comboBoxEpisode.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxEpisode.sizePolicy().hasHeightForWidth())
        self.comboBoxEpisode.setSizePolicy(sizePolicy2)
        self.comboBoxEpisode.setMinimumSize(QSize(200, 0))
        self.comboBoxEpisode.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxEpisode)

        self.labelShotSequence = QLabel(WcaMayaDialog)
        self.labelShotSequence.setObjectName(u"labelShotSequence")
        sizePolicy1.setHeightForWidth(self.labelShotSequence.sizePolicy().hasHeightForWidth())
        self.labelShotSequence.setSizePolicy(sizePolicy1)
        self.labelShotSequence.setMinimumSize(QSize(100, 0))
        self.labelShotSequence.setMaximumSize(QSize(60, 16777215))
        self.labelShotSequence.setFont(font)
        self.labelShotSequence.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotSequence)

        self.comboBoxSequence = QComboBox(WcaMayaDialog)
        self.comboBoxSequence.setObjectName(u"comboBoxSequence")
        self.comboBoxSequence.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.comboBoxSequence.sizePolicy().hasHeightForWidth())
        self.comboBoxSequence.setSizePolicy(sizePolicy2)
        self.comboBoxSequence.setMinimumSize(QSize(200, 0))
        self.comboBoxSequence.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxSequence)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.line = QFrame(WcaMayaDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayoutAsset = QHBoxLayout()
        self.horizontalLayoutAsset.setObjectName(u"horizontalLayoutAsset")
        self.horizontalSpacerAsset = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayoutAsset.addItem(self.horizontalSpacerAsset)

        self.radioButtonAsset = QRadioButton(WcaMayaDialog)
        self.radioButtonAsset.setObjectName(u"radioButtonAsset")
        self.radioButtonAsset.setMinimumSize(QSize(100, 0))
        self.radioButtonAsset.setFont(font)
        self.radioButtonAsset.setChecked(True)

        self.horizontalLayoutAsset.addWidget(self.radioButtonAsset)

        self.comboBoxAssetType = QComboBox(WcaMayaDialog)
        self.comboBoxAssetType.setObjectName(u"comboBoxAssetType")
        self.comboBoxAssetType.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboBoxAssetType.sizePolicy().hasHeightForWidth())
        self.comboBoxAssetType.setSizePolicy(sizePolicy3)
        self.comboBoxAssetType.setMinimumSize(QSize(200, 0))
        self.comboBoxAssetType.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutAsset.addWidget(self.comboBoxAssetType)

        self.comboBoxAsset = QComboBox(WcaMayaDialog)
        self.comboBoxAsset.setObjectName(u"comboBoxAsset")
        self.comboBoxAsset.setEnabled(False)
        sizePolicy.setHeightForWidth(self.comboBoxAsset.sizePolicy().hasHeightForWidth())
        self.comboBoxAsset.setSizePolicy(sizePolicy)
        self.comboBoxAsset.setMinimumSize(QSize(200, 0))

        self.horizontalLayoutAsset.addWidget(self.comboBoxAsset)


        self.verticalLayout.addLayout(self.horizontalLayoutAsset)

        self.horizontalLayoutShot = QHBoxLayout()
        self.horizontalLayoutShot.setObjectName(u"horizontalLayoutShot")
        self.horizontalSpacerShot = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayoutShot.addItem(self.horizontalSpacerShot)

        self.radioButtonShot = QRadioButton(WcaMayaDialog)
        self.radioButtonShot.setObjectName(u"radioButtonShot")
        self.radioButtonShot.setMinimumSize(QSize(100, 0))
        self.radioButtonShot.setFont(font)
        self.radioButtonShot.setChecked(False)

        self.horizontalLayoutShot.addWidget(self.radioButtonShot)

        self.comboBoxShot = QComboBox(WcaMayaDialog)
        self.comboBoxShot.setObjectName(u"comboBoxShot")
        self.comboBoxShot.setEnabled(False)
        sizePolicy2.setHeightForWidth(self.comboBoxShot.sizePolicy().hasHeightForWidth())
        self.comboBoxShot.setSizePolicy(sizePolicy2)
        self.comboBoxShot.setMinimumSize(QSize(200, 0))
        self.comboBoxShot.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutShot.addWidget(self.comboBoxShot)


        self.verticalLayout.addLayout(self.horizontalLayoutShot)

        self.horizontalLayoutFiles = QHBoxLayout()
        self.horizontalLayoutFiles.setObjectName(u"horizontalLayoutFiles")
        self.tabWidget = QTabWidget(WcaMayaDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabFiles = QWidget()
        self.tabFiles.setObjectName(u"tabFiles")
        self.horizontalLayout = QHBoxLayout(self.tabFiles)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableViewFiles = QTableView(self.tabFiles)
        self.tableViewFiles.setObjectName(u"tableViewFiles")

        self.horizontalLayout.addWidget(self.tableViewFiles)

        self.tabWidget.addTab(self.tabFiles, "")
        self.tabTasks = QWidget()
        self.tabTasks.setObjectName(u"tabTasks")
        self.verticalLayout_5 = QVBoxLayout(self.tabTasks)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableViewTasks = QTableView(self.tabTasks)
        self.tableViewTasks.setObjectName(u"tableViewTasks")

        self.verticalLayout_5.addWidget(self.tableViewTasks)

        self.tabWidget.addTab(self.tabTasks, "")

        self.horizontalLayoutFiles.addWidget(self.tabWidget)


        self.verticalLayout.addLayout(self.horizontalLayoutFiles)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pushButtonLoad = QPushButton(WcaMayaDialog)
        self.pushButtonLoad.setObjectName(u"pushButtonLoad")

        self.horizontalLayoutButtons.addWidget(self.pushButtonLoad)

        self.pushButtonImport = QPushButton(WcaMayaDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayoutButtons.addWidget(self.pushButtonImport)

        self.pushButtonDownload = QPushButton(WcaMayaDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayoutButtons.addWidget(self.pushButtonDownload)

        self.pushButtonPublish = QPushButton(WcaMayaDialog)
        self.pushButtonPublish.setObjectName(u"pushButtonPublish")
        self.pushButtonPublish.setEnabled(False)

        self.horizontalLayoutButtons.addWidget(self.pushButtonPublish)

        self.horizontalSpacerButton = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacerButton)


        self.verticalLayout.addLayout(self.horizontalLayoutButtons)

        self.horizontalLayoutStatus = QHBoxLayout()
        self.horizontalLayoutStatus.setObjectName(u"horizontalLayoutStatus")
        self.labelConnection = QLabel(WcaMayaDialog)
        self.labelConnection.setObjectName(u"labelConnection")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.labelConnection.sizePolicy().hasHeightForWidth())
        self.labelConnection.setSizePolicy(sizePolicy4)
        font1 = QFont()
        font1.setPointSize(7)
        self.labelConnection.setFont(font1)
        self.labelConnection.setFrameShape(QFrame.NoFrame)
        self.labelConnection.setLineWidth(0)
        self.labelConnection.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelConnection.setIndent(5)

        self.horizontalLayoutStatus.addWidget(self.labelConnection)

        self.line_2 = QFrame(WcaMayaDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayoutStatus.addWidget(self.line_2)

        self.horizontalSpacerStatus = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutStatus.addItem(self.horizontalSpacerStatus)

        self.labelMessage = QLabel(WcaMayaDialog)
        self.labelMessage.setObjectName(u"labelMessage")
        sizePolicy4.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy4)
        self.labelMessage.setFont(font1)
        self.labelMessage.setFrameShape(QFrame.NoFrame)
        self.labelMessage.setLineWidth(0)
        self.labelMessage.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.labelMessage.setMargin(1)
        self.labelMessage.setIndent(5)

        self.horizontalLayoutStatus.addWidget(self.labelMessage)


        self.verticalLayout.addLayout(self.horizontalLayoutStatus)


        self.retranslateUi(WcaMayaDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(WcaMayaDialog)
    # setupUi

    def retranslateUi(self, WcaMayaDialog):
        WcaMayaDialog.setWindowTitle(QCoreApplication.translate("WcaMayaDialog", u"swing", None))
        self.pushButtonSettings.setText(QCoreApplication.translate("WcaMayaDialog", u"Settings", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("WcaMayaDialog", u"Connect", None))
        self.labelProject.setText(QCoreApplication.translate("WcaMayaDialog", u"Project", None))
        self.labelShotEpisode.setText(QCoreApplication.translate("WcaMayaDialog", u"Episode", None))
        self.labelShotSequence.setText(QCoreApplication.translate("WcaMayaDialog", u"Sequence", None))
        self.radioButtonAsset.setText(QCoreApplication.translate("WcaMayaDialog", u"Asset", None))
#if QT_CONFIG(shortcut)
        self.radioButtonAsset.setShortcut(QCoreApplication.translate("WcaMayaDialog", u"Alt+A", None))
#endif // QT_CONFIG(shortcut)
        self.radioButtonShot.setText(QCoreApplication.translate("WcaMayaDialog", u"Shot", None))
#if QT_CONFIG(shortcut)
        self.radioButtonShot.setShortcut(QCoreApplication.translate("WcaMayaDialog", u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFiles), QCoreApplication.translate("WcaMayaDialog", u"Files", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTasks), QCoreApplication.translate("WcaMayaDialog", u"Tasks", None))
        self.pushButtonLoad.setText(QCoreApplication.translate("WcaMayaDialog", u"Load", None))
#if QT_CONFIG(shortcut)
        self.pushButtonLoad.setShortcut(QCoreApplication.translate("WcaMayaDialog", u"Alt+L", None))
#endif // QT_CONFIG(shortcut)
        self.pushButtonImport.setText(QCoreApplication.translate("WcaMayaDialog", u"Import", None))
#if QT_CONFIG(shortcut)
        self.pushButtonImport.setShortcut(QCoreApplication.translate("WcaMayaDialog", u"Alt+I", None))
#endif // QT_CONFIG(shortcut)
        self.pushButtonDownload.setText(QCoreApplication.translate("WcaMayaDialog", u"Download", None))
#if QT_CONFIG(shortcut)
        self.pushButtonDownload.setShortcut(QCoreApplication.translate("WcaMayaDialog", u"Alt+D", None))
#endif // QT_CONFIG(shortcut)
        self.pushButtonPublish.setText(QCoreApplication.translate("WcaMayaDialog", u"Publish", None))
#if QT_CONFIG(shortcut)
        self.pushButtonPublish.setShortcut(QCoreApplication.translate("WcaMayaDialog", u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
        self.labelConnection.setText(QCoreApplication.translate("WcaMayaDialog", u"Offline", None))
        self.labelMessage.setText(QCoreApplication.translate("WcaMayaDialog", u"OK", None))
    # retranslateUi

