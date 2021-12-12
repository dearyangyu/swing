# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shot_list_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr


class Ui_ShotListDialog(object):
    def setupUi(self, ShotListDialog):
        if not ShotListDialog.objectName():
            ShotListDialog.setObjectName(u"ShotListDialog")
        ShotListDialog.resize(609, 255)
        self.verticalLayout_2 = QVBoxLayout(ShotListDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listView = QListView(ShotListDialog)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_2.addWidget(self.listView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonAll = QPushButton(ShotListDialog)
        self.buttonAll.setObjectName(u"buttonAll")

        self.horizontalLayout.addWidget(self.buttonAll)

        self.buttonClear = QPushButton(ShotListDialog)
        self.buttonClear.setObjectName(u"buttonClear")

        self.horizontalLayout.addWidget(self.buttonClear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonCancel = QPushButton(ShotListDialog)
        self.buttonCancel.setObjectName(u"buttonCancel")

        self.horizontalLayout.addWidget(self.buttonCancel)

        self.buttonOk = QPushButton(ShotListDialog)
        self.buttonOk.setObjectName(u"buttonOk")

        self.horizontalLayout.addWidget(self.buttonOk)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ShotListDialog)

        self.buttonOk.setDefault(True)


        QMetaObject.connectSlotsByName(ShotListDialog)
    # setupUi

    def retranslateUi(self, ShotListDialog):
        ShotListDialog.setWindowTitle(fakestr(u"Dialog", None))
        self.buttonAll.setText(fakestr(u"All", None))
        self.buttonClear.setText(fakestr(u"None", None))
        self.buttonCancel.setText(fakestr(u"Cancel", None))
        self.buttonOk.setText(fakestr(u"OK", None))
    # retranslateUi

