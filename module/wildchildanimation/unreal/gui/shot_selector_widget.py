# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shot_selector_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_ShotSelectorWidget(object):
    def setupUi(self, ShotSelectorWidget):
        if not ShotSelectorWidget.objectName():
            ShotSelectorWidget.setObjectName(u"ShotSelectorWidget")
        ShotSelectorWidget.resize(642, 329)
        self.verticalLayout_2 = QVBoxLayout(ShotSelectorWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.verticalLayoutProject = QVBoxLayout()
        self.verticalLayoutProject.setObjectName(u"verticalLayoutProject")
        self.horizontalLayoutProjectTitle = QHBoxLayout()
        self.horizontalLayoutProjectTitle.setObjectName(u"horizontalLayoutProjectTitle")
        self.labelProject = QLabel(ShotSelectorWidget)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelProject.setFont(font)
        self.labelProject.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutProjectTitle.addWidget(self.labelProject)

        self.comboBoxProject = QComboBox(ShotSelectorWidget)
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
        self.labelShotEpisode = QLabel(ShotSelectorWidget)
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

        self.comboBoxEpisode = QComboBox(ShotSelectorWidget)
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

        self.labelShotSequence = QLabel(ShotSelectorWidget)
        self.labelShotSequence.setObjectName(u"labelShotSequence")
        sizePolicy1.setHeightForWidth(self.labelShotSequence.sizePolicy().hasHeightForWidth())
        self.labelShotSequence.setSizePolicy(sizePolicy1)
        self.labelShotSequence.setMinimumSize(QSize(100, 0))
        self.labelShotSequence.setMaximumSize(QSize(60, 16777215))
        self.labelShotSequence.setFont(font)
        self.labelShotSequence.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayoutEpisodeSequence.addWidget(self.labelShotSequence)

        self.comboBoxSequence = QComboBox(ShotSelectorWidget)
        self.comboBoxSequence.setObjectName(u"comboBoxSequence")
        self.comboBoxSequence.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.comboBoxSequence.sizePolicy().hasHeightForWidth())
        self.comboBoxSequence.setSizePolicy(sizePolicy2)
        self.comboBoxSequence.setMinimumSize(QSize(200, 0))
        self.comboBoxSequence.setMaximumSize(QSize(16777215, 25))

        self.horizontalLayoutEpisodeSequence.addWidget(self.comboBoxSequence)


        self.verticalLayoutProject.addLayout(self.horizontalLayoutEpisodeSequence)


        self.horizontalLayoutProject.addLayout(self.verticalLayoutProject)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProject)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelHandles = QLabel(ShotSelectorWidget)
        self.labelHandles.setObjectName(u"labelHandles")
        self.labelHandles.setMinimumSize(QSize(100, 0))
        self.labelHandles.setFont(font)

        self.horizontalLayout.addWidget(self.labelHandles)

        self.spinBoxHandles = QSpinBox(ShotSelectorWidget)
        self.spinBoxHandles.setObjectName(u"spinBoxHandles")
        self.spinBoxHandles.setValue(2)

        self.horizontalLayout.addWidget(self.spinBoxHandles)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayoutShotTable = QVBoxLayout()
        self.verticalLayoutShotTable.setObjectName(u"verticalLayoutShotTable")
        self.tableViewShots = QTableView(ShotSelectorWidget)
        self.tableViewShots.setObjectName(u"tableViewShots")

        self.verticalLayoutShotTable.addWidget(self.tableViewShots)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pushButtonSelectAll = QPushButton(ShotSelectorWidget)
        self.pushButtonSelectAll.setObjectName(u"pushButtonSelectAll")

        self.horizontalLayoutButtons.addWidget(self.pushButtonSelectAll)

        self.pushButtonSelectNone = QPushButton(ShotSelectorWidget)
        self.pushButtonSelectNone.setObjectName(u"pushButtonSelectNone")

        self.horizontalLayoutButtons.addWidget(self.pushButtonSelectNone)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutButtons.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(ShotSelectorWidget)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayoutButtons.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(ShotSelectorWidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)


        self.verticalLayoutShotTable.addLayout(self.horizontalLayoutButtons)


        self.verticalLayout_2.addLayout(self.verticalLayoutShotTable)


        self.retranslateUi(ShotSelectorWidget)

        QMetaObject.connectSlotsByName(ShotSelectorWidget)
    # setupUi

    def retranslateUi(self, ShotSelectorWidget):
        ShotSelectorWidget.setWindowTitle(fakestr(u"Form", None))
        self.labelProject.setText(fakestr(u"Project", None))
        self.labelShotEpisode.setText(fakestr(u"Episode", None))
        self.labelShotSequence.setText(fakestr(u"Sequence", None))
        self.labelHandles.setText(fakestr(u"Handles", None))
        self.pushButtonSelectAll.setText(fakestr(u"Select &All", None))
        self.pushButtonSelectNone.setText(fakestr(u"Select &None", None))
        self.pushButtonOk.setText(fakestr(u"&Ok", None))
        self.pushButtonCancel.setText(fakestr(u"&Cancel", None))
    # retranslateUi

