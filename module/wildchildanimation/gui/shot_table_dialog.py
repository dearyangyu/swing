# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shot_table_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_ShotTableDialog(object):
    def setupUi(self, ShotTableDialog):
        if not ShotTableDialog.objectName():
            ShotTableDialog.setObjectName(u"ShotTableDialog")
        ShotTableDialog.resize(640, 400)
        self.verticalLayout_2 = QVBoxLayout(ShotTableDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableView = QTableView(ShotTableDialog)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonAll = QPushButton(ShotTableDialog)
        self.buttonAll.setObjectName(u"buttonAll")

        self.horizontalLayout.addWidget(self.buttonAll)

        self.buttonClear = QPushButton(ShotTableDialog)
        self.buttonClear.setObjectName(u"buttonClear")

        self.horizontalLayout.addWidget(self.buttonClear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonCancel = QPushButton(ShotTableDialog)
        self.buttonCancel.setObjectName(u"buttonCancel")

        self.horizontalLayout.addWidget(self.buttonCancel)

        self.buttonOk = QPushButton(ShotTableDialog)
        self.buttonOk.setObjectName(u"buttonOk")

        self.horizontalLayout.addWidget(self.buttonOk)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(ShotTableDialog)

        self.buttonOk.setDefault(True)


        QMetaObject.connectSlotsByName(ShotTableDialog)
    # setupUi

    def retranslateUi(self, ShotTableDialog):
        ShotTableDialog.setWindowTitle(fakestr(u"Dialog", None))
        self.buttonAll.setText(fakestr(u"All", None))
        self.buttonClear.setText(fakestr(u"None", None))
        self.buttonCancel.setText(fakestr(u"Cancel", None))
        self.buttonOk.setText(fakestr(u"OK", None))
    # retranslateUi

