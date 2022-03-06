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
        SwingControlWidget.resize(1650, 27)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SwingControlWidget.sizePolicy().hasHeightForWidth())
        SwingControlWidget.setSizePolicy(sizePolicy)
        SwingControlWidget.setMinimumSize(QSize(640, 24))
        SwingControlWidget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(SwingControlWidget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.toolButtonRefresh = QToolButton(SwingControlWidget)
        self.toolButtonRefresh.setObjectName(u"toolButtonRefresh")

        self.horizontalLayout_3.addWidget(self.toolButtonRefresh)

        self.horizontalSpacer_7 = QSpacerItem(3, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.comboBoxProject = QComboBox(SwingControlWidget)
        self.comboBoxProject.setObjectName(u"comboBoxProject")
        self.comboBoxProject.setEnabled(False)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBoxProject.sizePolicy().hasHeightForWidth())
        self.comboBoxProject.setSizePolicy(sizePolicy1)
        self.comboBoxProject.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxProject)

        self.horizontalSpacer = QSpacerItem(3, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.comboBoxEpisode = QComboBox(SwingControlWidget)
        self.comboBoxEpisode.setObjectName(u"comboBoxEpisode")
        self.comboBoxEpisode.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxEpisode.sizePolicy().hasHeightForWidth())
        self.comboBoxEpisode.setSizePolicy(sizePolicy1)
        self.comboBoxEpisode.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxEpisode)

        self.horizontalSpacer_4 = QSpacerItem(3, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.comboBoxTaskType = QComboBox(SwingControlWidget)
        self.comboBoxTaskType.setObjectName(u"comboBoxTaskType")
        self.comboBoxTaskType.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxTaskType.sizePolicy().hasHeightForWidth())
        self.comboBoxTaskType.setSizePolicy(sizePolicy1)
        self.comboBoxTaskType.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxTaskType)

        self.horizontalSpacer_6 = QSpacerItem(3, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.comboBoxTask = QComboBox(SwingControlWidget)
        self.comboBoxTask.setObjectName(u"comboBoxTask")
        self.comboBoxTask.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.comboBoxTask.sizePolicy().hasHeightForWidth())
        self.comboBoxTask.setSizePolicy(sizePolicy1)
        self.comboBoxTask.setMinimumSize(QSize(225, 0))

        self.horizontalLayout_3.addWidget(self.comboBoxTask)

        self.checkBoxDoneTasks = QCheckBox(SwingControlWidget)
        self.checkBoxDoneTasks.setObjectName(u"checkBoxDoneTasks")

        self.horizontalLayout_3.addWidget(self.checkBoxDoneTasks)

        self.horizontalSpacer_5 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.toolButtonSwing = QToolButton(SwingControlWidget)
        self.toolButtonSwing.setObjectName(u"toolButtonSwing")
        self.toolButtonSwing.setMinimumSize(QSize(50, 0))
        self.toolButtonSwing.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.toolButtonSwing)


        self.horizontalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_3 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolButtonTask = QToolButton(SwingControlWidget)
        self.toolButtonTask.setObjectName(u"toolButtonTask")
        self.toolButtonTask.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.toolButtonTask)

        self.toolButtonPlayblast = QToolButton(SwingControlWidget)
        self.toolButtonPlayblast.setObjectName(u"toolButtonPlayblast")
        self.toolButtonPlayblast.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.toolButtonPlayblast)

        self.toolButtonBreakOut = QToolButton(SwingControlWidget)
        self.toolButtonBreakOut.setObjectName(u"toolButtonBreakOut")
        self.toolButtonBreakOut.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.toolButtonBreakOut)

        self.toolButtonExport = QToolButton(SwingControlWidget)
        self.toolButtonExport.setObjectName(u"toolButtonExport")
        self.toolButtonExport.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.toolButtonExport)

        self.toolButtonPublish = QToolButton(SwingControlWidget)
        self.toolButtonPublish.setObjectName(u"toolButtonPublish")
        self.toolButtonPublish.setEnabled(False)

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
        SwingControlWidget.setWindowTitle(fakestr(u"Swing Maya", None))
        self.toolButtonRefresh.setText(fakestr(u"Refresh", None))
#if QT_CONFIG(tooltip)
        self.checkBoxDoneTasks.setToolTip(fakestr(u"Show tasks marked Done or Completed", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxDoneTasks.setText(fakestr(u"Done", None))
#if QT_CONFIG(tooltip)
        self.toolButtonSwing.setToolTip(fakestr(u"Show Swing Manager GUI", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSwing.setText(fakestr(u"Swing", None))
#if QT_CONFIG(tooltip)
        self.toolButtonTask.setToolTip(fakestr(u"Creates or Loads a Task", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonTask.setText(fakestr(u"Task", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPlayblast.setToolTip(fakestr(u"Playblast selected Task", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPlayblast.setText(fakestr(u"Playblast", None))
#if QT_CONFIG(tooltip)
        self.toolButtonBreakOut.setToolTip(fakestr(u"Layout Utilities", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonBreakOut.setText(fakestr(u"Layout", None))
#if QT_CONFIG(tooltip)
        self.toolButtonExport.setToolTip(fakestr(u"Export Utilities", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonExport.setText(fakestr(u"Export", None))
#if QT_CONFIG(tooltip)
        self.toolButtonPublish.setToolTip(fakestr(u"Publish existing Task", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonPublish.setText(fakestr(u"Publish", None))
#if QT_CONFIG(tooltip)
        self.toolButtonSearch.setToolTip(fakestr(u"Search for files", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonSearch.setText(fakestr(u"Search", None))
#if QT_CONFIG(tooltip)
        self.toolButtonEntityInfo.setToolTip(fakestr(u"Show Entity Info GUI for selected Task Entity", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonEntityInfo.setText(fakestr(u"Info", None))
    # retranslateUi

