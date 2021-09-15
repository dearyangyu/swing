# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playlist_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr
class Ui_PlaylistDialog(object):
    def setupUi(self, PlaylistDialog):
        if not PlaylistDialog.objectName():
            PlaylistDialog.setObjectName(u"PlaylistDialog")
        PlaylistDialog.setEnabled(True)
        PlaylistDialog.resize(920, 414)
        self.verticalLayout = QVBoxLayout(PlaylistDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutEpisodeSequence = QHBoxLayout()
        self.horizontalLayoutEpisodeSequence.setObjectName(u"horizontalLayoutEpisodeSequence")
        self.labelPlayblastFolder = QLabel(PlaylistDialog)
        self.labelPlayblastFolder.setObjectName(u"labelPlayblastFolder")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelPlayblastFolder.sizePolicy().hasHeightForWidth())
        self.labelPlayblastFolder.setSizePolicy(sizePolicy)
        self.labelPlayblastFolder.setMinimumSize(QSize(100, 0))
        self.labelPlayblastFolder.setMaximumSize(QSize(60, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelPlayblastFolder.setFont(font)
        self.labelPlayblastFolder.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelPlayblastFolder)

        self.comboBoxEpisode = QComboBox(PlaylistDialog)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        self.comboBoxEpisode.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxEpisode.sizePolicy().hasHeightForWidth())
        self.comboBoxEpisode.setSizePolicy(sizePolicy1)
        self.comboBoxEpisode.setMinimumSize(QSize(200, 0))
        self.comboBoxEpisode.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxEpisode)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelProjectsFolder = QLabel(PlaylistDialog)
        self.labelProjectsFolder.setObjectName(u"labelProjectsFolder")
        sizePolicy.setHeightForWidth(self.labelProjectsFolder.sizePolicy().hasHeightForWidth())
        self.labelProjectsFolder.setSizePolicy(sizePolicy)
        self.labelProjectsFolder.setMinimumSize(QSize(100, 0))
        self.labelProjectsFolder.setMaximumSize(QSize(60, 16777215))
        self.labelProjectsFolder.setFont(font)
        self.labelProjectsFolder.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.labelProjectsFolder)

        self.comboBoxPlaylist = QComboBox(PlaylistDialog)
        self.comboBoxPlaylist.setObjectName(u"comboBoxPlaylist")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBoxPlaylist.sizePolicy().hasHeightForWidth())
        self.comboBoxPlaylist.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.comboBoxPlaylist)


        self.verticalLayoutProject.addLayout(self.horizontalLayout_7)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox = QCheckBox(PlaylistDialog)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_2.addWidget(self.checkBox, 1, 0, 1, 1)

        self.checkBox_2 = QCheckBox(PlaylistDialog)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.gridLayout_2.addWidget(self.checkBox_2, 2, 0, 1, 1)

        self.checkBoxZip = QCheckBox(PlaylistDialog)
        self.checkBoxZip.setObjectName(u"checkBoxZip")

        self.gridLayout_2.addWidget(self.checkBoxZip, 0, 0, 1, 1)


        self.verticalLayoutProject.addLayout(self.gridLayout_2)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableView = QTableView(PlaylistDialog)
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
        self.pushButtonCreate = QPushButton(PlaylistDialog)
        self.pushButtonCreate.setObjectName(u"pushButtonCreate")

        self.horizontalLayout_4.addWidget(self.pushButtonCreate)

        self.progressBar = QProgressBar(PlaylistDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButtonCancel = QPushButton(PlaylistDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.lineEdit = QLineEdit(PlaylistDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)


        self.retranslateUi(PlaylistDialog)

        QMetaObject.connectSlotsByName(PlaylistDialog)
    # setupUi

    def retranslateUi(self, PlaylistDialog):
        PlaylistDialog.setWindowTitle(fakestr(u"Shot Breakout", None))
#if QT_CONFIG(tooltip)
        PlaylistDialog.setToolTip(fakestr(u"Select playblast and project file directories to upload as Layout", None))
#endif // QT_CONFIG(tooltip)
        self.labelPlayblastFolder.setText(fakestr(u"Episode", None))
        self.labelProjectsFolder.setText(fakestr(u"Playlist", None))
        self.checkBox.setText(fakestr(u"CheckBox", None))
        self.checkBox_2.setText(fakestr(u"CheckBox", None))
        self.checkBoxZip.setText(fakestr(u"Zip projects folder", None))
        self.pushButtonCreate.setText(fakestr(u"Create Shots", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

