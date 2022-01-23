# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'desktop_layout_control_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_DesktopLayoutDialog(object):
    def setupUi(self, DesktopLayoutDialog):
        if not DesktopLayoutDialog.objectName():
            DesktopLayoutDialog.setObjectName(u"DesktopLayoutDialog")
        DesktopLayoutDialog.resize(550, 175)
        DesktopLayoutDialog.setMinimumSize(QSize(550, 175))
        DesktopLayoutDialog.setMaximumSize(QSize(550, 175))
        DesktopLayoutDialog.setModal(False)
        self.verticalLayout = QVBoxLayout(DesktopLayoutDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonImportXML = QPushButton(DesktopLayoutDialog)
        self.pushButtonImportXML.setObjectName(u"pushButtonImportXML")

        self.horizontalLayout_5.addWidget(self.pushButtonImportXML)

        self.labelImagePlane = QLabel(DesktopLayoutDialog)
        self.labelImagePlane.setObjectName(u"labelImagePlane")

        self.horizontalLayout_5.addWidget(self.labelImagePlane)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonBreakout = QPushButton(DesktopLayoutDialog)
        self.pushButtonBreakout.setObjectName(u"pushButtonBreakout")

        self.horizontalLayout_2.addWidget(self.pushButtonBreakout)

        self.labelChainsaw = QLabel(DesktopLayoutDialog)
        self.labelChainsaw.setObjectName(u"labelChainsaw")

        self.horizontalLayout_2.addWidget(self.labelChainsaw)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonClose = QPushButton(DesktopLayoutDialog)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(DesktopLayoutDialog)

        QMetaObject.connectSlotsByName(DesktopLayoutDialog)
    # setupUi

    def retranslateUi(self, DesktopLayoutDialog):
        DesktopLayoutDialog.setWindowTitle(fakestr(u"Swing: Layout", None))
        self.pushButtonImportXML.setText(fakestr(u"Import XML", None))
        self.labelImagePlane.setText(fakestr(u"Select FCPXML to create shots in the selected sequence", None))
        self.pushButtonBreakout.setText(fakestr(u"Break Out", None))
        self.labelChainsaw.setText(fakestr(u"Import Scenes and Playblasts into the selected episode", None))
        self.pushButtonClose.setText(fakestr(u"Close", None))
    # retranslateUi

