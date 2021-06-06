# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'project_nav_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr


class Ui_ProjectNavWidget(object):
    def setupUi(self, ProjectNavWidget):
        if not ProjectNavWidget.objectName():
            ProjectNavWidget.setObjectName(u"ProjectNavWidget")
        ProjectNavWidget.resize(831, 76)
        self.verticalLayout = QVBoxLayout(ProjectNavWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutProjectTitle = QHBoxLayout()
        self.horizontalLayoutProjectTitle.setObjectName(u"horizontalLayoutProjectTitle")
        self.labelProject = QLabel(ProjectNavWidget)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutProjectTitle.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(ProjectNavWidget)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        self.comboBoxProject.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy)

        self.horizontalLayoutProjectTitle.addWidget(self.comboBoxProject)

        self.toolButtonRefresh = QToolButton(ProjectNavWidget)
        self.toolButtonRefresh.setObjectName(u"toolButtonRefresh")

        self.horizontalLayoutProjectTitle.addWidget(self.toolButtonRefresh)

        self.progressBar = QProgressBar(ProjectNavWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setMaximumSize(QSize(50, 16777215))
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(True)

        self.horizontalLayoutProjectTitle.addWidget(self.progressBar)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutProjectTitle)

        self.horizontalLayoutEpisodeSequence = QHBoxLayout()
        self.horizontalLayoutEpisodeSequence.setObjectName(u"horizontalLayoutEpisodeSequence")
        self.labelShotEpisode = QLabel(ProjectNavWidget)
        self.labelShotEpisode.setObjectName(u"labelShotEpisode")
        sizePolicy1.setHeightForWidth(self.labelShotEpisode.sizePolicy().hasHeightForWidth())
        self.labelShotEpisode.setSizePolicy(sizePolicy1)
        self.labelShotEpisode.setMinimumSize(QSize(100, 0))
        self.labelShotEpisode.setMaximumSize(QSize(60, 16777215))
        self.labelShotEpisode.setFont(font)
        self.labelShotEpisode.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotEpisode)

        self.comboBoxEpisode = QComboBox(ProjectNavWidget)
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

        self.labelShotSequence = QLabel(ProjectNavWidget)
        self.labelShotSequence.setObjectName(u"labelShotSequence")
        sizePolicy1.setHeightForWidth(self.labelShotSequence.sizePolicy().hasHeightForWidth())
        self.labelShotSequence.setSizePolicy(sizePolicy1)
        self.labelShotSequence.setMinimumSize(QSize(100, 0))
        self.labelShotSequence.setMaximumSize(QSize(60, 16777215))
        self.labelShotSequence.setFont(font)
        self.labelShotSequence.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotSequence)

        self.comboBoxSequence = QComboBox(ProjectNavWidget)
        self.comboBoxSequence.setObjectName(u"comboBoxSequence")
        self.comboBoxSequence.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.comboBoxSequence.sizePolicy().hasHeightForWidth())
        self.comboBoxSequence.setSizePolicy(sizePolicy2)
        self.comboBoxSequence.setMinimumSize(QSize(200, 0))
        self.comboBoxSequence.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxSequence)

        self.toolButtonTaskTypes = QToolButton(ProjectNavWidget)
        self.toolButtonTaskTypes.setObjectName(u"toolButtonTaskTypes")
        self.toolButtonTaskTypes.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.toolButtonTaskTypes.sizePolicy().hasHeightForWidth())
        self.toolButtonTaskTypes.setSizePolicy(sizePolicy3)

        self.horizontalLayoutEpisodeSequence.addWidget(self.toolButtonTaskTypes)

        self.toolButtonStatusTypes = QToolButton(ProjectNavWidget)
        self.toolButtonStatusTypes.setObjectName(u"toolButtonStatusTypes")
        self.toolButtonStatusTypes.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.toolButtonStatusTypes.sizePolicy().hasHeightForWidth())
        self.toolButtonStatusTypes.setSizePolicy(sizePolicy3)

        self.horizontalLayoutEpisodeSequence.addWidget(self.toolButtonStatusTypes)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)


        self.retranslateUi(ProjectNavWidget)

        QMetaObject.connectSlotsByName(ProjectNavWidget)
    # setupUi

    def retranslateUi(self, ProjectNavWidget):
        ProjectNavWidget.setWindowTitle(fakestr(u"Form", None))
        self.labelProject.setText(fakestr(u"Project", None))
        self.toolButtonRefresh.setText(fakestr(u"...", None))
        self.labelShotEpisode.setText(fakestr(u"Episode", None))
        self.labelShotSequence.setText(fakestr(u"Sequence", None))
        self.toolButtonTaskTypes.setText("")
        self.toolButtonStatusTypes.setText("")
    # retranslateUi

