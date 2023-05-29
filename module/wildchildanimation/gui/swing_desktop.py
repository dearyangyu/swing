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
        SwingMain.resize(700, 491)
        SwingMain.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(SwingMain)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.connectionLayout = QHBoxLayout()
        self.connectionLayout.setObjectName(u"connectionLayout")
        self.toolButtonSettings = QToolButton(SwingMain)
        self.toolButtonSettings.setObjectName(u"toolButtonSettings")
        self.toolButtonSettings.setMinimumSize(QSize(80, 0))

        self.connectionLayout.addWidget(self.toolButtonSettings)

        self.toolButtonConnect = QToolButton(SwingMain)
        self.toolButtonConnect.setObjectName(u"toolButtonConnect")
        self.toolButtonConnect.setMinimumSize(QSize(80, 0))
        self.toolButtonConnect.setAutoFillBackground(False)
        self.toolButtonConnect.setStyleSheet(u"")

        self.connectionLayout.addWidget(self.toolButtonConnect)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.connectionLayout.addItem(self.horizontalSpacer_4)

        self.toolButtonPlayblast = QToolButton(SwingMain)
        self.toolButtonPlayblast.setObjectName(u"toolButtonPlayblast")
        self.toolButtonPlayblast.setMinimumSize(QSize(80, 0))

        self.connectionLayout.addWidget(self.toolButtonPlayblast)

        self.toolButtonEpisodes = QToolButton(SwingMain)
        self.toolButtonEpisodes.setObjectName(u"toolButtonEpisodes")

        self.connectionLayout.addWidget(self.toolButtonEpisodes)          

        self.toolButtonPlaylists = QToolButton(SwingMain)
        self.toolButtonPlaylists.setObjectName(u"toolButtonPlaylists")

        self.connectionLayout.addWidget(self.toolButtonPlaylists)

        self.toolButtonExport = QToolButton(SwingMain)
        self.toolButtonExport.setObjectName(u"toolButtonExport")
        self.toolButtonExport.setMinimumSize(QSize(80, 0))

        self.connectionLayout.addWidget(self.toolButtonExport)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.connectionLayout.addItem(self.horizontalSpacer_5)

        self.toolButtonLayout = QToolButton(SwingMain)
        self.toolButtonLayout.setObjectName(u"toolButtonLayout")
        self.toolButtonLayout.setMinimumSize(QSize(80, 0))

        self.connectionLayout.addWidget(self.toolButtonLayout)

        self.toolButtonUploads = QToolButton(SwingMain)
        self.toolButtonUploads.setObjectName(u"toolButtonUploads")

        self.connectionLayout.addWidget(self.toolButtonUploads)

        self.toolButtonSearchFiles = QToolButton(SwingMain)
        self.toolButtonSearchFiles.setObjectName(u"toolButtonSearchFiles")
        self.toolButtonSearchFiles.setMinimumSize(QSize(80, 0))

        self.connectionLayout.addWidget(self.toolButtonSearchFiles)


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
        self.toolButtonAssetInfo.setMinimumSize(QSize(80, 0))
        self.toolButtonAssetInfo.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayoutAsset.addWidget(self.toolButtonAssetInfo)


        self.verticalLayout.addLayout(self.horizontalLayoutAsset)

        self.horizontalLayoutShot = QHBoxLayout()
        self.horizontalLayoutShot.setObjectName(u"horizontalLayoutShot")
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
        self.toolButtonShotInfo.setMinimumSize(QSize(80, 0))
        self.toolButtonShotInfo.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

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
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelTaskTableSelection = QLabel(self.tabTasks)
        self.labelTaskTableSelection.setObjectName(u"labelTaskTableSelection")

        self.horizontalLayout_2.addWidget(self.labelTaskTableSelection)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)

        self.progressBarTaskTable = QProgressBar(self.tabTasks)
        self.progressBarTaskTable.setObjectName(u"progressBarTaskTable")
        self.progressBarTaskTable.setMaximumSize(QSize(50, 16777215))
        self.progressBarTaskTable.setMaximum(1)
        self.progressBarTaskTable.setValue(-1)
        self.progressBarTaskTable.setTextVisible(False)

        self.horizontalLayout_2.addWidget(self.progressBarTaskTable)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tableViewTasks = QTableView(self.tabTasks)
        self.tableViewTasks.setObjectName(u"tableViewTasks")

        self.verticalLayout_3.addWidget(self.tableViewTasks)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.toolButtonNew = QToolButton(self.tabTasks)
        self.toolButtonNew.setObjectName(u"toolButtonNew")
        self.toolButtonNew.setEnabled(False)
        self.toolButtonNew.setMinimumSize(QSize(80, 0))
        self.toolButtonNew.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_4.addWidget(self.toolButtonNew)

        self.toolButtonLoad = QToolButton(self.tabTasks)
        self.toolButtonLoad.setObjectName(u"toolButtonLoad")
        self.toolButtonLoad.setMinimumSize(QSize(80, 0))
        self.toolButtonLoad.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_4.addWidget(self.toolButtonLoad)

        self.toolButtonPublish = QToolButton(self.tabTasks)
        self.toolButtonPublish.setObjectName(u"toolButtonPublish")
        self.toolButtonPublish.setEnabled(False)
        self.toolButtonPublish.setMinimumSize(QSize(80, 0))
        self.toolButtonPublish.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_4.addWidget(self.toolButtonPublish)

        self.toolButtonRenderPub = QToolButton(self.tabTasks)
        self.toolButtonRenderPub.setObjectName(u"toolButtonRenderPub")
        self.toolButtonRenderPub.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.toolButtonRenderPub)

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
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFileTableSelection = QLabel(self.tabFiles)
        self.labelFileTableSelection.setObjectName(u"labelFileTableSelection")

        self.horizontalLayout_3.addWidget(self.labelFileTableSelection)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.progressBarFileTable = QProgressBar(self.tabFiles)
        self.progressBarFileTable.setObjectName(u"progressBarFileTable")
        self.progressBarFileTable.setMaximumSize(QSize(50, 16777215))
        self.progressBarFileTable.setMaximum(1)
        self.progressBarFileTable.setValue(-1)
        self.progressBarFileTable.setTextVisible(False)

        self.horizontalLayout_3.addWidget(self.progressBarFileTable)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.checkBoxProjectFiles = QCheckBox(self.tabFiles)
        self.checkBoxProjectFiles.setObjectName(u"checkBoxProjectFiles")
        self.checkBoxProjectFiles.setChecked(True)

        self.horizontalLayout_6.addWidget(self.checkBoxProjectFiles)

        self.checkBoxOutputFiles = QCheckBox(self.tabFiles)
        self.checkBoxOutputFiles.setObjectName(u"checkBoxOutputFiles")
        self.checkBoxOutputFiles.setChecked(True)

        self.horizontalLayout_6.addWidget(self.checkBoxOutputFiles)

        self.checkBoxAllVersions = QCheckBox(self.tabFiles)
        self.checkBoxAllVersions.setObjectName(u"checkBoxAllVersions")
        self.checkBoxAllVersions.setChecked(True)

        self.horizontalLayout_6.addWidget(self.checkBoxAllVersions)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.tableViewFiles = QTableView(self.tabFiles)
        self.tableViewFiles.setObjectName(u"tableViewFiles")

        self.verticalLayout_2.addWidget(self.tableViewFiles)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolButtonFileTableSelectAll = QToolButton(self.tabFiles)
        self.toolButtonFileTableSelectAll.setObjectName(u"toolButtonFileTableSelectAll")
        self.toolButtonFileTableSelectAll.setEnabled(False)
        self.toolButtonFileTableSelectAll.setMinimumSize(QSize(80, 0))
        self.toolButtonFileTableSelectAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_5.addWidget(self.toolButtonFileTableSelectAll)

        self.toolButtonFileSelectNone = QToolButton(self.tabFiles)
        self.toolButtonFileSelectNone.setObjectName(u"toolButtonFileSelectNone")
        self.toolButtonFileSelectNone.setEnabled(False)
        self.toolButtonFileSelectNone.setMinimumSize(QSize(80, 0))
        self.toolButtonFileSelectNone.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_5.addWidget(self.toolButtonFileSelectNone)

        self.toolButtonDownload = QToolButton(self.tabFiles)
        self.toolButtonDownload.setObjectName(u"toolButtonDownload")
        self.toolButtonDownload.setEnabled(False)
        self.toolButtonDownload.setMinimumSize(QSize(80, 0))
        self.toolButtonDownload.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_5.addWidget(self.toolButtonDownload)

        self.toolButtonImport = QToolButton(self.tabFiles)
        self.toolButtonImport.setObjectName(u"toolButtonImport")
        self.toolButtonImport.setEnabled(False)
        self.toolButtonImport.setMinimumSize(QSize(80, 0))
        self.toolButtonImport.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_5.addWidget(self.toolButtonImport)

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

        self.toolButtonClose = QToolButton(SwingMain)
        self.toolButtonClose.setObjectName(u"toolButtonClose")
        self.toolButtonClose.setMinimumSize(QSize(80, 0))

        self.horizontalLayoutStatus.addWidget(self.toolButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayoutStatus)


        self.retranslateUi(SwingMain)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SwingMain)
    # setupUi

    def retranslateUi(self, SwingMain):
        SwingMain.setWindowTitle(fakestr(u"treehouse: swing", None))
#if QT_CONFIG(tooltip)
        self.toolButtonSettings.setToolTip(fakestr(u"Open connection settings", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSettings.setText(fakestr(u"Settings", None))
#if QT_CONFIG(tooltip)
        self.toolButtonConnect.setToolTip(fakestr(u"Connect or reconnect to Treehouse", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonConnect.setText(fakestr(u"Connect", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPlayblast.setToolTip(fakestr(u"Open DCC Playblast", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPlayblast.setText(fakestr(u"Playblast", None))
        self.toolButtonPlaylists.setText(fakestr(u"Shot-Playlists", None))
        self.toolButtonEpisodes.setText(fakestr(u"Ep-Playlists", None))        
        
#if QT_CONFIG(tooltip)
        self.toolButtonExport.setToolTip(fakestr(u"Open DCC Export", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonExport.setText(fakestr(u"Export", None))
#if QT_CONFIG(shortcut)
        self.toolButtonExport.setShortcut(fakestr(u"F8", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.toolButtonLayout.setToolTip(fakestr(u"Open Shot Breakout", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonLayout.setText(fakestr(u"Layout", None))
        self.toolButtonUploads.setText(fakestr(u"Uploads", None))
#if QT_CONFIG(tooltip)
        self.toolButtonSearchFiles.setToolTip(fakestr(u"Search for files", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSearchFiles.setText(fakestr(u"Search", None))
#if QT_CONFIG(shortcut)
        self.toolButtonSearchFiles.setShortcut(fakestr(u"F3", None))
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
        self.toolButtonAssetInfo.setText(fakestr(u" Asset Info", None))
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
        self.toolButtonShotInfo.setText(fakestr(u" Shot Info", None))
        self.labelTaskTableSelection.setText(fakestr(u"Tasks for selection:", None))
#if QT_CONFIG(tooltip)
        self.toolButtonNew.setToolTip(fakestr(u"Create a new scene", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonNew.setText(fakestr(u" New", None))
        self.toolButtonLoad.setText(fakestr(u" Load", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPublish.setToolTip(fakestr(u"Publish current scene to Treehouse", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPublish.setText(fakestr(u" Publish", None))
#if QT_CONFIG(shortcut)
        self.toolButtonPublish.setShortcut(fakestr(u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
        self.toolButtonRenderPub.setText(fakestr(u"Render Pub", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTasks), fakestr(u"Tasks", None))
        self.labelFileTableSelection.setText(fakestr(u"Files for selection", None))
#if QT_CONFIG(tooltip)
        self.checkBoxProjectFiles.setToolTip(fakestr(u"Show or hide Project files", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxProjectFiles.setText(fakestr(u"Show Project Files", None))
#if QT_CONFIG(tooltip)
        self.checkBoxOutputFiles.setToolTip(fakestr(u"Show or hide Output files", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxOutputFiles.setText(fakestr(u"Show Output Files", None))
#if QT_CONFIG(tooltip)
        self.checkBoxAllVersions.setToolTip(fakestr(u"Show latest version or all versions", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxAllVersions.setText(fakestr(u"Show All Versions", None))
        self.toolButtonFileTableSelectAll.setText(fakestr(u" All", None))
        self.toolButtonFileSelectNone.setText(fakestr(u" None", None))
        self.toolButtonDownload.setText(fakestr(u" Download", None))
#if QT_CONFIG(shortcut)
        self.toolButtonDownload.setShortcut(fakestr(u"Alt+D", None))
#endif // QT_CONFIG(shortcut)
        self.toolButtonImport.setText(fakestr(u" Import", None))
#if QT_CONFIG(shortcut)
        self.toolButtonImport.setShortcut(fakestr(u"Alt+I", None))
#endif // QT_CONFIG(shortcut)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFiles), fakestr(u"Files", None))
        self.labelConnection.setText(fakestr(u"Offline", None))
        self.toolButtonClose.setText(fakestr(u" Close", None))
    # retranslateUi

