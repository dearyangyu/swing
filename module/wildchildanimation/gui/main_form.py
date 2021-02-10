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
        WcaMayaDialog.resize(579, 470)
        self.verticalLayout_4 = QVBoxLayout(WcaMayaDialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
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


        self.verticalLayout_4.addLayout(self.connectionLayout)

        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.labelProject = QLabel(WcaMayaDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(WcaMayaDialog)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.comboBoxProject)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
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

        self.horizontalLayout_9.addWidget(self.labelShotEpisode)

        self.comboBoxEpisode = QComboBox(WcaMayaDialog)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxEpisode.sizePolicy().hasHeightForWidth())
        self.comboBoxEpisode.setSizePolicy(sizePolicy2)
        self.comboBoxEpisode.setMinimumSize(QSize(200, 0))
        self.comboBoxEpisode.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_9.addWidget(self.comboBoxEpisode)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.labelShotSequence = QLabel(WcaMayaDialog)
        self.labelShotSequence.setObjectName(u"labelShotSequence")
        sizePolicy1.setHeightForWidth(self.labelShotSequence.sizePolicy().hasHeightForWidth())
        self.labelShotSequence.setSizePolicy(sizePolicy1)
        self.labelShotSequence.setMinimumSize(QSize(100, 0))
        self.labelShotSequence.setMaximumSize(QSize(60, 16777215))
        self.labelShotSequence.setFont(font)
        self.labelShotSequence.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.labelShotSequence)

        self.comboBoxSequence = QComboBox(WcaMayaDialog)
        self.comboBoxSequence.setObjectName(u"comboBoxSequence")
        sizePolicy2.setHeightForWidth(self.comboBoxSequence.sizePolicy().hasHeightForWidth())
        self.comboBoxSequence.setSizePolicy(sizePolicy2)
        self.comboBoxSequence.setMinimumSize(QSize(200, 0))
        self.comboBoxSequence.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_10.addWidget(self.comboBoxSequence)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)


        self.horizontalLayoutProject.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayoutProject)

        self.shotLayout = QVBoxLayout()
        self.shotLayout.setObjectName(u"shotLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelShotName = QLabel(WcaMayaDialog)
        self.labelShotName.setObjectName(u"labelShotName")
        sizePolicy1.setHeightForWidth(self.labelShotName.sizePolicy().hasHeightForWidth())
        self.labelShotName.setSizePolicy(sizePolicy1)
        self.labelShotName.setMinimumSize(QSize(100, 0))
        self.labelShotName.setMaximumSize(QSize(60, 16777215))
        self.labelShotName.setFont(font)
        self.labelShotName.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.labelShotName)

        self.comboBoxShot = QComboBox(WcaMayaDialog)
        self.comboBoxShot.setObjectName(u"comboBoxShot")
        sizePolicy2.setHeightForWidth(self.comboBoxShot.sizePolicy().hasHeightForWidth())
        self.comboBoxShot.setSizePolicy(sizePolicy2)
        self.comboBoxShot.setMinimumSize(QSize(200, 0))
        self.comboBoxShot.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_7.addWidget(self.comboBoxShot)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.shotLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.shotLayout)

        self.assetLayout = QVBoxLayout()
        self.assetLayout.setObjectName(u"assetLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelAssetType = QLabel(WcaMayaDialog)
        self.labelAssetType.setObjectName(u"labelAssetType")
        sizePolicy1.setHeightForWidth(self.labelAssetType.sizePolicy().hasHeightForWidth())
        self.labelAssetType.setSizePolicy(sizePolicy1)
        self.labelAssetType.setMinimumSize(QSize(100, 0))
        self.labelAssetType.setMaximumSize(QSize(60, 16777215))
        self.labelAssetType.setFont(font)
        self.labelAssetType.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.labelAssetType)

        self.comboBoxAssetType = QComboBox(WcaMayaDialog)
        self.comboBoxAssetType.setObjectName(u"comboBoxAssetType")
        sizePolicy2.setHeightForWidth(self.comboBoxAssetType.sizePolicy().hasHeightForWidth())
        self.comboBoxAssetType.setSizePolicy(sizePolicy2)
        self.comboBoxAssetType.setMinimumSize(QSize(200, 0))
        self.comboBoxAssetType.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayout_5.addWidget(self.comboBoxAssetType)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelAsset = QLabel(WcaMayaDialog)
        self.labelAsset.setObjectName(u"labelAsset")
        sizePolicy1.setHeightForWidth(self.labelAsset.sizePolicy().hasHeightForWidth())
        self.labelAsset.setSizePolicy(sizePolicy1)
        self.labelAsset.setMinimumSize(QSize(100, 0))
        self.labelAsset.setMaximumSize(QSize(60, 16777215))
        self.labelAsset.setFont(font)
        self.labelAsset.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.labelAsset)

        self.comboBoxAsset = QComboBox(WcaMayaDialog)
        self.comboBoxAsset.setObjectName(u"comboBoxAsset")
        sizePolicy2.setHeightForWidth(self.comboBoxAsset.sizePolicy().hasHeightForWidth())
        self.comboBoxAsset.setSizePolicy(sizePolicy2)
        self.comboBoxAsset.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.comboBoxAsset)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.assetLayout.addLayout(self.verticalLayout)


        self.verticalLayout_4.addLayout(self.assetLayout)

        self.horizontalLayoutFiles = QHBoxLayout()
        self.horizontalLayoutFiles.setObjectName(u"horizontalLayoutFiles")
        self.tabWidget = QTabWidget(WcaMayaDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabFiles = QWidget()
        self.tabFiles.setObjectName(u"tabFiles")
        self.horizontalLayout = QHBoxLayout(self.tabFiles)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.treeWidgetFiles = QTreeWidget(self.tabFiles)
        font1 = QFont()
        font1.setBold(False)
        font1.setWeight(50)
        font2 = QFont()
        font2.setPointSize(8)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(3, font2);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setText(0, u"name");
        __qtreewidgetitem.setFont(0, font1);
        self.treeWidgetFiles.setHeaderItem(__qtreewidgetitem)
        self.treeWidgetFiles.setObjectName(u"treeWidgetFiles")
        self.treeWidgetFiles.setAutoFillBackground(True)
        self.treeWidgetFiles.setHeaderHidden(False)
        self.treeWidgetFiles.setColumnCount(4)
        self.treeWidgetFiles.header().setVisible(True)
        self.treeWidgetFiles.header().setCascadingSectionResizes(True)
        self.treeWidgetFiles.header().setMinimumSectionSize(50)
        self.treeWidgetFiles.header().setDefaultSectionSize(200)
        self.treeWidgetFiles.header().setHighlightSections(True)
        self.treeWidgetFiles.header().setProperty("showSortIndicator", True)
        self.treeWidgetFiles.header().setStretchLastSection(True)

        self.horizontalLayout.addWidget(self.treeWidgetFiles)

        self.tabWidget.addTab(self.tabFiles, "")
        self.tabTasks = QWidget()
        self.tabTasks.setObjectName(u"tabTasks")
        self.verticalLayout_5 = QVBoxLayout(self.tabTasks)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listWidgetTasks = QListWidget(self.tabTasks)
        self.listWidgetTasks.setObjectName(u"listWidgetTasks")

        self.verticalLayout_5.addWidget(self.listWidgetTasks)

        self.tabWidget.addTab(self.tabTasks, "")

        self.horizontalLayoutFiles.addWidget(self.tabWidget)


        self.verticalLayout_4.addLayout(self.horizontalLayoutFiles)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pushButtonDownload = QPushButton(WcaMayaDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayoutButtons.addWidget(self.pushButtonDownload)

        self.pushButtonPublish = QPushButton(WcaMayaDialog)
        self.pushButtonPublish.setObjectName(u"pushButtonPublish")
        self.pushButtonPublish.setEnabled(False)

        self.horizontalLayoutButtons.addWidget(self.pushButtonPublish)

        self.horizontalSpacerButton = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacerButton)


        self.verticalLayout_4.addLayout(self.horizontalLayoutButtons)


        self.retranslateUi(WcaMayaDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(WcaMayaDialog)
    # setupUi

    def retranslateUi(self, WcaMayaDialog):
        WcaMayaDialog.setWindowTitle(QCoreApplication.translate("WcaMayaDialog", u"treehouse: Swing", None))
        self.pushButtonSettings.setText(QCoreApplication.translate("WcaMayaDialog", u"Settings", None))
        self.pushButtonConnect.setText(QCoreApplication.translate("WcaMayaDialog", u"Connect", None))
        self.labelProject.setText(QCoreApplication.translate("WcaMayaDialog", u"Project", None))
        self.labelShotEpisode.setText(QCoreApplication.translate("WcaMayaDialog", u"Episode", None))
        self.labelShotSequence.setText(QCoreApplication.translate("WcaMayaDialog", u"Seq", None))
        self.labelShotName.setText(QCoreApplication.translate("WcaMayaDialog", u"Shot", None))
        self.labelAssetType.setText(QCoreApplication.translate("WcaMayaDialog", u"Asset Type", None))
        self.labelAsset.setText(QCoreApplication.translate("WcaMayaDialog", u"Asset", None))
        ___qtreewidgetitem = self.treeWidgetFiles.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("WcaMayaDialog", u"comments", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("WcaMayaDialog", u"updated", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("WcaMayaDialog", u"version", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFiles), QCoreApplication.translate("WcaMayaDialog", u"Files", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTasks), QCoreApplication.translate("WcaMayaDialog", u"Tasks", None))
        self.pushButtonDownload.setText(QCoreApplication.translate("WcaMayaDialog", u"Download", None))
        self.pushButtonPublish.setText(QCoreApplication.translate("WcaMayaDialog", u"Publish", None))
    # retranslateUi

