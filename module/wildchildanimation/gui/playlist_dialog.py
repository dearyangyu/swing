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
        PlaylistDialog.resize(973, 338)
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

        self.toolButtonRefresh = QToolButton(PlaylistDialog)
        self.toolButtonRefresh.setObjectName(u"toolButtonRefresh")

        self.horizontalLayoutEpisodeSequence.addWidget(self.toolButtonRefresh)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
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


        self.verticalLayoutProject.addLayout(self.horizontalLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButtonSelectAll = QToolButton(PlaylistDialog)
        self.toolButtonSelectAll.setObjectName(u"toolButtonSelectAll")

        self.horizontalLayout_2.addWidget(self.toolButtonSelectAll)

        self.toolButtonSelectNone = QToolButton(PlaylistDialog)
        self.toolButtonSelectNone.setObjectName(u"toolButtonSelectNone")

        self.horizontalLayout_2.addWidget(self.toolButtonSelectNone)

        self.radioButtonLatestVersion = QRadioButton(PlaylistDialog)
        self.radioButtonLatestVersion.setObjectName(u"radioButtonLatestVersion")

        self.horizontalLayout_2.addWidget(self.radioButtonLatestVersion)

        self.radioButtonLastDay = QRadioButton(PlaylistDialog)
        self.radioButtonLastDay.setObjectName(u"radioButtonLastDay")

        self.horizontalLayout_2.addWidget(self.radioButtonLastDay)

        self.radioButtonShowAll = QRadioButton(PlaylistDialog)
        self.radioButtonShowAll.setObjectName(u"radioButtonShowAll")

        self.horizontalLayout_2.addWidget(self.radioButtonShowAll)

        self.checkBoxExtractZip = QCheckBox(PlaylistDialog)
        self.checkBoxExtractZip.setObjectName(u"checkBoxExtractZip")
        self.checkBoxExtractZip.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBoxExtractZip)

        self.checkBoxSequences = QCheckBox(PlaylistDialog)
        self.checkBoxSequences.setObjectName(u"checkBoxSequences")
        self.checkBoxSequences.setChecked(False)

        self.horizontalLayout_2.addWidget(self.checkBoxSequences)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(PlaylistDialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEditSearch = QLineEdit(PlaylistDialog)
        self.lineEditSearch.setObjectName(u"lineEditSearch")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEditSearch.sizePolicy().hasHeightForWidth())
        self.lineEditSearch.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.lineEditSearch)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.verticalLayoutProject.addLayout(self.gridLayout_2)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableView = QTableView(PlaylistDialog)
        self.tableView.setObjectName(u"tableView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(10)
        sizePolicy2.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy2)
        self.tableView.setSizeIncrement(QSize(0, 0))
        font1 = QFont()
        font1.setPointSize(8)
        self.tableView.setFont(font1)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)

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
        self.toolButtonRefresh.setText(fakestr(u"Refresh", None))
        self.label.setText(fakestr(u"Folder", None))
        self.toolButtonSelectFolder.setText(fakestr(u"...", None))
        self.toolButtonSelectAll.setText(fakestr(u"+", None))
        self.toolButtonSelectNone.setText(fakestr(u"-", None))
        self.radioButtonLatestVersion.setText(fakestr(u"Latest", None))
        self.radioButtonLastDay.setText(fakestr(u"24H", None))
        self.radioButtonShowAll.setText(fakestr(u"All", None))
        self.checkBoxExtractZip.setText(fakestr(u"Extract Zip Files", None))
        self.checkBoxSequences.setText(fakestr(u"Sequences (Sh 00's)", None))
        self.label_2.setText(fakestr(u"Search:", None))
        self.pushButtonProcess.setText(fakestr(u"Sync", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

