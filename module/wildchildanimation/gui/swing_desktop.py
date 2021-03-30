# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_desktop.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr


class Ui_SwingMain(object):
    def setupUi(self, SwingMain):
        if not SwingMain.objectName():
            SwingMain.setObjectName(u"SwingMain")
        SwingMain.resize(650, 491)
        self.verticalLayout = QVBoxLayout(SwingMain)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.connectionLayout = QHBoxLayout()
        self.connectionLayout.setObjectName(u"connectionLayout")
        self.pushButtonSettings = QPushButton(SwingMain)
        self.pushButtonSettings.setObjectName(u"pushButtonSettings")

        self.connectionLayout.addWidget(self.pushButtonSettings)

        self.pushButtonConnect = QPushButton(SwingMain)
        self.pushButtonConnect.setObjectName(u"pushButtonConnect")
        self.pushButtonConnect.setAutoFillBackground(False)
        self.pushButtonConnect.setStyleSheet(u"")

        self.connectionLayout.addWidget(self.pushButtonConnect)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.connectionLayout.addItem(self.horizontalSpacer_4)

        self.pushButtonPlayblast = QPushButton(SwingMain)
        self.pushButtonPlayblast.setObjectName(u"pushButtonPlayblast")

        self.connectionLayout.addWidget(self.pushButtonPlayblast)

        self.pushButtonExport = QPushButton(SwingMain)
        self.pushButtonExport.setObjectName(u"pushButtonExport")

        self.connectionLayout.addWidget(self.pushButtonExport)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.connectionLayout.addItem(self.horizontalSpacer_5)

        self.pushButtonBreakout = QPushButton(SwingMain)
        self.pushButtonBreakout.setObjectName(u"pushButtonBreakout")

        self.connectionLayout.addWidget(self.pushButtonBreakout)

        self.pushButtonSearchFiles = QPushButton(SwingMain)
        self.pushButtonSearchFiles.setObjectName(u"pushButtonSearchFiles")

        self.connectionLayout.addWidget(self.pushButtonSearchFiles)


        self.verticalLayout.addLayout(self.connectionLayout)

        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.horizontalLayoutProject.setSizeConstraint(QLayout.SetMinimumSize)

        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.line = QFrame(SwingMain)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayoutAsset = QHBoxLayout()
        self.horizontalLayoutAsset.setObjectName(u"horizontalLayoutAsset")
        self.horizontalSpacerAsset = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayoutAsset.addItem(self.horizontalSpacerAsset)

        self.radioButtonAsset = QRadioButton(SwingMain)
        self.radioButtonAsset.setObjectName(u"radioButtonAsset")
        self.radioButtonAsset.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonAsset.setFont(font)
        self.radioButtonAsset.setChecked(True)

        self.horizontalLayoutAsset.addWidget(self.radioButtonAsset)

        self.comboBoxAssetType = QComboBox(SwingMain)
        self.comboBoxAssetType.setObjectName(u"comboBoxAssetType")
        self.comboBoxAssetType.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxAssetType.sizePolicy().hasHeightForWidth())
        self.comboBoxAssetType.setSizePolicy(sizePolicy)
        self.comboBoxAssetType.setMinimumSize(QSize(200, 0))
        self.comboBoxAssetType.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutAsset.addWidget(self.comboBoxAssetType)

        self.comboBoxAsset = QComboBox(SwingMain)
        self.comboBoxAsset.setObjectName(u"comboBoxAsset")
        self.comboBoxAsset.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxAsset.sizePolicy().hasHeightForWidth())
        self.comboBoxAsset.setSizePolicy(sizePolicy1)
        self.comboBoxAsset.setMinimumSize(QSize(200, 0))

        self.horizontalLayoutAsset.addWidget(self.comboBoxAsset)

        self.toolButtonAssetInfo = QToolButton(SwingMain)
        self.toolButtonAssetInfo.setObjectName(u"toolButtonAssetInfo")
        self.toolButtonAssetInfo.setEnabled(True)

        self.horizontalLayoutAsset.addWidget(self.toolButtonAssetInfo)


        self.verticalLayout.addLayout(self.horizontalLayoutAsset)

        self.horizontalLayoutShot = QHBoxLayout()
        self.horizontalLayoutShot.setObjectName(u"horizontalLayoutShot")
        self.horizontalSpacerShot = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayoutShot.addItem(self.horizontalSpacerShot)

        self.radioButtonShot = QRadioButton(SwingMain)
        self.radioButtonShot.setObjectName(u"radioButtonShot")
        self.radioButtonShot.setMinimumSize(QSize(100, 0))
        self.radioButtonShot.setFont(font)
        self.radioButtonShot.setChecked(False)

        self.horizontalLayoutShot.addWidget(self.radioButtonShot)

        self.comboBoxShot = QComboBox(SwingMain)
        self.comboBoxShot.setObjectName(u"comboBoxShot")
        self.comboBoxShot.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxShot.sizePolicy().hasHeightForWidth())
        self.comboBoxShot.setSizePolicy(sizePolicy2)
        self.comboBoxShot.setMinimumSize(QSize(200, 0))
        self.comboBoxShot.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutShot.addWidget(self.comboBoxShot)

        self.toolButtonShotInfo = QToolButton(SwingMain)
        self.toolButtonShotInfo.setObjectName(u"toolButtonShotInfo")
        self.toolButtonShotInfo.setEnabled(True)

        self.horizontalLayoutShot.addWidget(self.toolButtonShotInfo)


        self.verticalLayout.addLayout(self.horizontalLayoutShot)

        self.horizontalLayoutFiles = QHBoxLayout()
        self.horizontalLayoutFiles.setObjectName(u"horizontalLayoutFiles")
        self.tabWidget = QTabWidget(SwingMain)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabTasks = QWidget()
        self.tabTasks.setObjectName(u"tabTasks")
        self.verticalLayout_5 = QVBoxLayout(self.tabTasks)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableViewTasks = QTableView(self.tabTasks)
        self.tableViewTasks.setObjectName(u"tableViewTasks")

        self.verticalLayout_3.addWidget(self.tableViewTasks)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonNew = QPushButton(self.tabTasks)
        self.pushButtonNew.setObjectName(u"pushButtonNew")
        self.pushButtonNew.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.pushButtonNew)

        self.pushButtonPublish = QPushButton(self.tabTasks)
        self.pushButtonPublish.setObjectName(u"pushButtonPublish")
        self.pushButtonPublish.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.pushButtonPublish)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tabTasks, "")
        self.tabFiles = QWidget()
        self.tabFiles.setObjectName(u"tabFiles")
        self.horizontalLayout = QHBoxLayout(self.tabFiles)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableViewFiles = QTableView(self.tabFiles)
        self.tableViewFiles.setObjectName(u"tableViewFiles")

        self.verticalLayout_2.addWidget(self.tableViewFiles)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonImport = QPushButton(self.tabFiles)
        self.pushButtonImport.setObjectName(u"pushButtonImport")
        self.pushButtonImport.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.pushButtonImport)

        self.pushButtonDownload = QPushButton(self.tabFiles)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")
        self.pushButtonDownload.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.pushButtonDownload)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.tabWidget.addTab(self.tabFiles, "")

        self.horizontalLayoutFiles.addWidget(self.tabWidget)


        self.verticalLayout.addLayout(self.horizontalLayoutFiles)

        self.horizontalLayoutStatus = QHBoxLayout()
        self.horizontalLayoutStatus.setObjectName(u"horizontalLayoutStatus")
        self.labelConnection = QLabel(SwingMain)
        self.labelConnection.setObjectName(u"labelConnection")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelConnection.sizePolicy().hasHeightForWidth())
        self.labelConnection.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setPointSize(7)
        font1.setBold(True)
        font1.setWeight(75)
        self.labelConnection.setFont(font1)
        self.labelConnection.setFrameShape(QFrame.NoFrame)
        self.labelConnection.setLineWidth(0)
        self.labelConnection.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelConnection.setIndent(5)

        self.horizontalLayoutStatus.addWidget(self.labelConnection)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutStatus.addItem(self.horizontalSpacer)

        self.pushButtonClose = QPushButton(SwingMain)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayoutStatus.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayoutStatus)


        self.retranslateUi(SwingMain)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SwingMain)
    # setupUi

    def retranslateUi(self, SwingMain):
        SwingMain.setWindowTitle(fakestr(u"treehouse: swing", None))
#if QT_CONFIG(tooltip)
        self.pushButtonSettings.setToolTip(fakestr(u"Open connection settings", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonSettings.setText(fakestr(u"Settings", None))
#if QT_CONFIG(tooltip)
        self.pushButtonConnect.setToolTip(fakestr(u"Connect or reconnect to Treehouse", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonConnect.setText(fakestr(u"Connect", None))
#if QT_CONFIG(tooltip)
        self.pushButtonPlayblast.setToolTip(fakestr(u"Open DCC Playblast", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonPlayblast.setText(fakestr(u"Playblast", None))
#if QT_CONFIG(tooltip)
        self.pushButtonExport.setToolTip(fakestr(u"Open DCC Export", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonExport.setText(fakestr(u"Export", None))
#if QT_CONFIG(shortcut)
        self.pushButtonExport.setShortcut(fakestr(u"F8", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pushButtonBreakout.setToolTip(fakestr(u"Open Shot Breakout", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonBreakout.setText(fakestr(u"Breakout", None))
#if QT_CONFIG(tooltip)
        self.pushButtonSearchFiles.setToolTip(fakestr(u"Search for files", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonSearchFiles.setText(fakestr(u"Search", None))
#if QT_CONFIG(shortcut)
        self.pushButtonSearchFiles.setShortcut(fakestr(u"F3", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.radioButtonAsset.setToolTip(fakestr(u"Filter files by selected asset", None))
#endif // QT_CONFIG(tooltip)
        self.radioButtonAsset.setText(fakestr(u"Asset", None))
#if QT_CONFIG(shortcut)
        self.radioButtonAsset.setShortcut(fakestr(u"Alt+A", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.toolButtonAssetInfo.setToolTip(fakestr(u"Open Asset Information", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonAssetInfo.setText(fakestr(u"...", None))
#if QT_CONFIG(tooltip)
        self.radioButtonShot.setToolTip(fakestr(u"Filter files by selected shot", None))
#endif // QT_CONFIG(tooltip)
        self.radioButtonShot.setText(fakestr(u"Shot", None))
#if QT_CONFIG(shortcut)
        self.radioButtonShot.setShortcut(fakestr(u"Alt+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.toolButtonShotInfo.setToolTip(fakestr(u"Open Shot Information", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonShotInfo.setText(fakestr(u"...", None))
#if QT_CONFIG(tooltip)
        self.pushButtonNew.setToolTip(fakestr(u"Create a new scene", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonNew.setText(fakestr(u"New", None))
#if QT_CONFIG(tooltip)
        self.pushButtonPublish.setToolTip(fakestr(u"Publish current scene to Treehouse", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonPublish.setText(fakestr(u"Publish", None))
#if QT_CONFIG(shortcut)
        self.pushButtonPublish.setShortcut(fakestr(u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTasks), fakestr(u"Tasks", None))
        self.pushButtonImport.setText(fakestr(u"Import", None))
#if QT_CONFIG(shortcut)
        self.pushButtonImport.setShortcut(fakestr(u"Alt+I", None))
#endif // QT_CONFIG(shortcut)
        self.pushButtonDownload.setText(fakestr(u"Download", None))
#if QT_CONFIG(shortcut)
        self.pushButtonDownload.setShortcut(fakestr(u"Alt+D", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFiles), fakestr(u"Files", None))
        self.labelConnection.setText(fakestr(u"Offline", None))
        self.pushButtonClose.setText(fakestr(u"Close", None))
    # retranslateUi

