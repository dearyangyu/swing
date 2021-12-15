# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'layout_control_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_LayoutDialog(object):
    def setupUi(self, LayoutDialog):
        if not LayoutDialog.objectName():
            LayoutDialog.setObjectName(u"LayoutDialog")
        LayoutDialog.resize(550, 175)
        LayoutDialog.setMinimumSize(QSize(550, 175))
        LayoutDialog.setMaximumSize(QSize(550, 175))
        LayoutDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(LayoutDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonImagePlane = QPushButton(LayoutDialog)
        self.pushButtonImagePlane.setObjectName(u"pushButtonImagePlane")

        self.horizontalLayout_5.addWidget(self.pushButtonImagePlane)

        self.labelImagePlane = QLabel(LayoutDialog)
        self.labelImagePlane.setObjectName(u"labelImagePlane")

        self.horizontalLayout_5.addWidget(self.labelImagePlane)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButtonChainsaw = QPushButton(LayoutDialog)
        self.pushButtonChainsaw.setObjectName(u"pushButtonChainsaw")

        self.horizontalLayout_2.addWidget(self.pushButtonChainsaw)

        self.labelChainsaw = QLabel(LayoutDialog)
        self.labelChainsaw.setObjectName(u"labelChainsaw")

        self.horizontalLayout_2.addWidget(self.labelChainsaw)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonAnimPrep = QPushButton(LayoutDialog)
        self.pushButtonAnimPrep.setObjectName(u"pushButtonAnimPrep")

        self.horizontalLayout_3.addWidget(self.pushButtonAnimPrep)

        self.labelAnimPrep = QLabel(LayoutDialog)
        self.labelAnimPrep.setObjectName(u"labelAnimPrep")

        self.horizontalLayout_3.addWidget(self.labelAnimPrep)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonTurnover = QPushButton(LayoutDialog)
        self.pushButtonTurnover.setObjectName(u"pushButtonTurnover")

        self.horizontalLayout_4.addWidget(self.pushButtonTurnover)

        self.labelTurnover = QLabel(LayoutDialog)
        self.labelTurnover.setObjectName(u"labelTurnover")

        self.horizontalLayout_4.addWidget(self.labelTurnover)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonClose = QPushButton(LayoutDialog)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(LayoutDialog)

        QMetaObject.connectSlotsByName(LayoutDialog)
    # setupUi

    def retranslateUi(self, LayoutDialog):
        LayoutDialog.setWindowTitle(fakestr(u"Swing: Break Out", None))
        self.pushButtonImagePlane.setText(fakestr(u"Image Plane", None))
        self.labelImagePlane.setText(fakestr(u"Add an image plane to the camera sequencer", None))
        self.pushButtonChainsaw.setText(fakestr(u"Chainsaw", None))
        self.labelChainsaw.setText(fakestr(u"Breakout a layout scene into scenes per shot ", None))
        self.pushButtonAnimPrep.setText(fakestr(u"Anim Prep", None))
        self.labelAnimPrep.setText(fakestr(u"Clean up animation chainsaw scene files", None))
        self.pushButtonTurnover.setText(fakestr(u"Turnover", None))
        self.labelTurnover.setText(fakestr(u"Create shots for selected scene files and playblasts", None))
        self.pushButtonClose.setText(fakestr(u"Close", None))
    # retranslateUi

