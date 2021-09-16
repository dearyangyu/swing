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
        self.labelEpisode = QLabel(PlaylistDialog)
        self.labelEpisode.setObjectName(u"labelEpisode")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelEpisode.sizePolicy().hasHeightForWidth())
        self.labelEpisode.setSizePolicy(sizePolicy)
        self.labelEpisode.setMinimumSize(QSize(100, 0))
        self.labelEpisode.setMaximumSize(QSize(100, 16777215))
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.labelEpisode.setFont(font)
        self.labelEpisode.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelEpisode)

        self.lineEditEpisode = QLineEdit(PlaylistDialog)
        self.lineEditEpisode.setObjectName(u"lineEditEpisode")

        self.horizontalLayoutEpisodeSequence.addWidget(self.lineEditEpisode)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(PlaylistDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.lineEditFolder = QLineEdit(PlaylistDialog)
        self.lineEditFolder.setObjectName(u"lineEditFolder")

        self.horizontalLayout.addWidget(self.lineEditFolder)

        self.toolButtonSelectFolder = QToolButton(PlaylistDialog)
        self.toolButtonSelectFolder.setObjectName(u"toolButtonSelectFolder")

        self.horizontalLayout.addWidget(self.toolButtonSelectFolder)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.verticalLayoutProject.addLayout(self.gridLayout_2)

        self.checkboxShowAll = QCheckBox(PlaylistDialog)
        self.checkboxShowAll.setObjectName(u"checkboxShowAll")

        self.verticalLayoutProject.addWidget(self.checkboxShowAll)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableView = QTableView(PlaylistDialog)
        self.tableView.setObjectName(u"tableView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(10)
        sizePolicy1.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy1)
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
        self.pushButtonProcess = QPushButton(PlaylistDialog)
        self.pushButtonProcess.setObjectName(u"pushButtonProcess")

        self.horizontalLayout_4.addWidget(self.pushButtonProcess)

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


        self.retranslateUi(PlaylistDialog)

        QMetaObject.connectSlotsByName(PlaylistDialog)
    # setupUi

    def retranslateUi(self, PlaylistDialog):
        PlaylistDialog.setWindowTitle(fakestr(u"swing: playlists", None))
#if QT_CONFIG(tooltip)
        PlaylistDialog.setToolTip(fakestr(u"Episode Playlist", None))
#endif // QT_CONFIG(tooltip)
        self.labelEpisode.setText(fakestr(u"Episode", None))
        self.label.setText(fakestr(u"Folder", None))
        self.toolButtonSelectFolder.setText(fakestr(u"...", None))
        self.checkboxShowAll.setText(fakestr(u"Show all versions", None))
        self.pushButtonProcess.setText(fakestr(u"Sync", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

