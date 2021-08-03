# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_update_task_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_SwingUpdateTask(object):
    def setupUi(self, SwingUpdateTask):
        if not SwingUpdateTask.objectName():
            SwingUpdateTask.setObjectName(u"SwingUpdateTask")
        SwingUpdateTask.resize(716, 227)
        self.verticalLayout_2 = QVBoxLayout(SwingUpdateTask)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableView = QTableView(SwingUpdateTask)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonOk = QPushButton(SwingUpdateTask)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)

        self.pushButtonCancel = QPushButton(SwingUpdateTask)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(SwingUpdateTask)

        QMetaObject.connectSlotsByName(SwingUpdateTask)
    # setupUi

    def retranslateUi(self, SwingUpdateTask):
        SwingUpdateTask.setWindowTitle(fakestr(u"Dialog", None))
        self.pushButtonOk.setText(fakestr(u"OK", None))
        self.pushButtonCancel.setText(fakestr(u"Cancel", None))
    # retranslateUi

