# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_library_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_AssetLibraryDialog(object):
    def setupUi(self, AssetLibraryDialog):
        if not AssetLibraryDialog.objectName():
            AssetLibraryDialog.setObjectName(u"AssetLibraryDialog")
        AssetLibraryDialog.resize(821, 461)
        self.verticalLayout_2 = QVBoxLayout(AssetLibraryDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutProjectTitle = QHBoxLayout()
        self.horizontalLayoutProjectTitle.setObjectName(u"horizontalLayoutProjectTitle")
        self.labelProject = QLabel(AssetLibraryDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutProjectTitle.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(AssetLibraryDialog)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        self.comboBoxProject.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy)

        self.horizontalLayoutProjectTitle.addWidget(self.comboBoxProject)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutProjectTitle)

        self.horizontalLayoutEpisodeSequence = QHBoxLayout()
        self.horizontalLayoutEpisodeSequence.setObjectName(u"horizontalLayoutEpisodeSequence")
        self.labelShotEpisode = QLabel(AssetLibraryDialog)
        self.labelShotEpisode.setObjectName(u"labelShotEpisode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelShotEpisode.sizePolicy().hasHeightForWidth())
        self.labelShotEpisode.setSizePolicy(sizePolicy1)
        self.labelShotEpisode.setMinimumSize(QSize(100, 0))
        self.labelShotEpisode.setMaximumSize(QSize(60, 16777215))
        self.labelShotEpisode.setFont(font)
        self.labelShotEpisode.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotEpisode)

        self.comboBoxEpisode = QComboBox(AssetLibraryDialog)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        self.comboBoxEpisode.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxEpisode.sizePolicy().hasHeightForWidth())
        self.comboBoxEpisode.setSizePolicy(sizePolicy2)
        self.comboBoxEpisode.setMinimumSize(QSize(200, 0))
        self.comboBoxEpisode.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxEpisode)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)


        self.verticalLayout_2.addLayout(self.verticalLayoutProject)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditLibraryFolder = QLineEdit(AssetLibraryDialog)
        self.lineEditLibraryFolder.setObjectName(u"lineEditLibraryFolder")

        self.horizontalLayout.addWidget(self.lineEditLibraryFolder)

        self.toolButtonLibraryFolder = QToolButton(AssetLibraryDialog)
        self.toolButtonLibraryFolder.setObjectName(u"toolButtonLibraryFolder")

        self.horizontalLayout.addWidget(self.toolButtonLibraryFolder)

        self.checkBoxFlattenPath = QCheckBox(AssetLibraryDialog)
        self.checkBoxFlattenPath.setObjectName(u"checkBoxFlattenPath")

        self.horizontalLayout.addWidget(self.checkBoxFlattenPath)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeWidget = QTreeWidget(AssetLibraryDialog)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pushButtonSelectAll = QPushButton(AssetLibraryDialog)
        self.pushButtonSelectAll.setObjectName(u"pushButtonSelectAll")

        self.horizontalLayoutButtons.addWidget(self.pushButtonSelectAll)

        self.pushButtonSelectNone = QPushButton(AssetLibraryDialog)
        self.pushButtonSelectNone.setObjectName(u"pushButtonSelectNone")

        self.horizontalLayoutButtons.addWidget(self.pushButtonSelectNone)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacer)

        self.pushButtonRunAll = QPushButton(AssetLibraryDialog)
        self.pushButtonRunAll.setObjectName(u"pushButtonRunAll")

        self.horizontalLayoutButtons.addWidget(self.pushButtonRunAll)

        self.pushButtonCancel = QPushButton(AssetLibraryDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)


        self.verticalLayout_2.addLayout(self.horizontalLayoutButtons)


        self.retranslateUi(AssetLibraryDialog)

        QMetaObject.connectSlotsByName(AssetLibraryDialog)
    # setupUi

    def retranslateUi(self, AssetLibraryDialog):
        AssetLibraryDialog.setWindowTitle(fakestr(u"swing: asset library", None))
        self.labelProject.setText(fakestr(u"Project", None))
        self.labelShotEpisode.setText(fakestr(u"Episode", None))
        self.toolButtonLibraryFolder.setText(fakestr(u"...", None))
        self.checkBoxFlattenPath.setText(fakestr(u"Flatten Path", None))
        self.pushButtonSelectAll.setText(fakestr(u"Select &All", None))
        self.pushButtonSelectNone.setText(fakestr(u"Select &None", None))
        self.pushButtonRunAll.setText(fakestr(u"&Sync", None))
        self.pushButtonCancel.setText(fakestr(u"&Close", None))
    # retranslateUi

