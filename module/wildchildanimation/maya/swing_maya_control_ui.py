# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_maya_control.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_SwingControlWidget(object):
    def setupUi(self, SwingControlWidget):
        if not SwingControlWidget.objectName():
            SwingControlWidget.setObjectName(u"SwingControlWidget")
        SwingControlWidget.resize(1343, 44)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SwingControlWidget.sizePolicy().hasHeightForWidth())
        SwingControlWidget.setSizePolicy(sizePolicy)
        SwingControlWidget.setMaximumSize(QSize(16777215, 50))
        self.verticalLayout = QVBoxLayout(SwingControlWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.toolButtonRefresh = QToolButton(SwingControlWidget)
        self.toolButtonRefresh.setObjectName(u"toolButtonRefresh")

        self.horizontalLayout_3.addWidget(self.toolButtonRefresh)

        self.comboBoxProject = QComboBox(SwingControlWidget)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        self.comboBoxProject.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxProject)

        self.comboBoxEpisode = QComboBox(SwingControlWidget)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        self.comboBoxEpisode.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxEpisode)

        self.comboBoxTask = QComboBox(SwingControlWidget)
        self.comboBoxTask.setObjectName(u"comboBoxTask")
        self.comboBoxTask.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxTask)

        self.toolButtonSwing = QToolButton(SwingControlWidget)
        self.toolButtonSwing.setObjectName(u"toolButtonSwing")
        self.toolButtonSwing.setMinimumSize(QSize(50, 0))
        self.toolButtonSwing.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.toolButtonSwing)


        self.horizontalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButtonTask = QToolButton(SwingControlWidget)
        self.toolButtonTask.setObjectName(u"toolButtonTask")

        self.horizontalLayout_2.addWidget(self.toolButtonTask)

        self.toolButtonPlayblast = QToolButton(SwingControlWidget)
        self.toolButtonPlayblast.setObjectName(u"toolButtonPlayblast")

        self.horizontalLayout_2.addWidget(self.toolButtonPlayblast)

        self.toolButtonBreakOut = QToolButton(SwingControlWidget)
        self.toolButtonBreakOut.setObjectName(u"toolButtonBreakOut")

        self.horizontalLayout_2.addWidget(self.toolButtonBreakOut)

        self.toolButtonExport = QToolButton(SwingControlWidget)
        self.toolButtonExport.setObjectName(u"toolButtonExport")

        self.horizontalLayout_2.addWidget(self.toolButtonExport)

        self.toolButtonPublish = QToolButton(SwingControlWidget)
        self.toolButtonPublish.setObjectName(u"toolButtonPublish")

        self.horizontalLayout_2.addWidget(self.toolButtonPublish)


        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.lineEditSearch = QLineEdit(SwingControlWidget)
        self.lineEditSearch.setObjectName(u"lineEditSearch")
        self.lineEditSearch.setMinimumSize(QSize(100, 0))
        self.lineEditSearch.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.lineEditSearch)

        self.toolButtonSearch = QToolButton(SwingControlWidget)
        self.toolButtonSearch.setObjectName(u"toolButtonSearch")

        self.horizontalLayout.addWidget(self.toolButtonSearch)

        self.toolButtonEntityInfo = QToolButton(SwingControlWidget)
        self.toolButtonEntityInfo.setObjectName(u"toolButtonEntityInfo")

        self.horizontalLayout.addWidget(self.toolButtonEntityInfo)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(SwingControlWidget)

        QMetaObject.connectSlotsByName(SwingControlWidget)
    # setupUi

    def retranslateUi(self, SwingControlWidget):
        SwingControlWidget.setWindowTitle(fakestr(u"Form", None))
        self.toolButtonRefresh.setText(fakestr(u"Refresh", None))
        self.toolButtonSwing.setText(fakestr(u"Swing", None))
        self.toolButtonTask.setText(fakestr(u"Task", None))
        self.toolButtonPlayblast.setText(fakestr(u"Playblast", None))
        self.toolButtonBreakOut.setText(fakestr(u"Breakout", None))
        self.toolButtonExport.setText(fakestr(u"Export", None))
        self.toolButtonPublish.setText(fakestr(u"Publish", None))
        self.toolButtonSearch.setText(fakestr(u"Search", None))
        self.toolButtonEntityInfo.setText(fakestr(u"Info", None))
    # retranslateUi

