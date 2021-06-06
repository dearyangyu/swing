# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entity_select_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_EntitySelectWidget(object):
    def setupUi(self, EntitySelectWidget):
        if not EntitySelectWidget.objectName():
            EntitySelectWidget.setObjectName(u"EntitySelectWidget")
        EntitySelectWidget.resize(465, 352)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EntitySelectWidget.sizePolicy().hasHeightForWidth())
        EntitySelectWidget.setSizePolicy(sizePolicy)
        EntitySelectWidget.setModal(True)
        self.verticalLayout = QVBoxLayout(EntitySelectWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listWidget = QListWidget(EntitySelectWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setAutoFillBackground(True)
        self.listWidget.setProperty("showDropIndicator", False)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButtonSelectAll = QToolButton(EntitySelectWidget)
        self.toolButtonSelectAll.setObjectName(u"toolButtonSelectAll")

        self.horizontalLayout.addWidget(self.toolButtonSelectAll)

        self.toolButtonSelectNone = QToolButton(EntitySelectWidget)
        self.toolButtonSelectNone.setObjectName(u"toolButtonSelectNone")

        self.horizontalLayout.addWidget(self.toolButtonSelectNone)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOK = QPushButton(EntitySelectWidget)
        self.pushButtonOK.setObjectName(u"pushButtonOK")

        self.horizontalLayout.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QPushButton(EntitySelectWidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(EntitySelectWidget)

        QMetaObject.connectSlotsByName(EntitySelectWidget)
    # setupUi

    def retranslateUi(self, EntitySelectWidget):
        EntitySelectWidget.setWindowTitle(fakestr(u"treehouse: swing", None))
        self.toolButtonSelectAll.setText(fakestr(u"All", None))
        self.toolButtonSelectNone.setText(fakestr(u"None", None))
        self.pushButtonOK.setText(fakestr(u"OK", None))
        self.pushButtonCancel.setText(fakestr(u"Cancel", None))
    # retranslateUi

