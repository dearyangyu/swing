# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'references_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr
class Ui_ReferencesDialog(object):
    def setupUi(self, ReferencesDialog):
        if not ReferencesDialog.objectName():
            ReferencesDialog.setObjectName(u"ReferencesDialog")
        ReferencesDialog.setEnabled(True)
        ReferencesDialog.resize(800, 600)
        self.verticalLayout = QVBoxLayout(ReferencesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(ReferencesDialog)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolButtonAll = QToolButton(ReferencesDialog)
        self.toolButtonAll.setObjectName(u"toolButtonAll")

        self.horizontalLayout_5.addWidget(self.toolButtonAll)

        self.toolButtonNone = QToolButton(ReferencesDialog)
        self.toolButtonNone.setObjectName(u"toolButtonNone")

        self.horizontalLayout_5.addWidget(self.toolButtonNone)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.tableWidget = QTableWidget(ReferencesDialog)
        if (self.tableWidget.columnCount() < 1):
            self.tableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.tableWidget.setObjectName(u"tableWidget")
        font = QFont()
        font.setPointSize(8)
        self.tableWidget.setFont(font)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonDownload = QPushButton(ReferencesDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayout_4.addWidget(self.pushButtonDownload)

        self.progressBar = QProgressBar(ReferencesDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)

        self.horizontalLayout_4.addWidget(self.progressBar)

        self.pushButtonCancel = QPushButton(ReferencesDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(ReferencesDialog)

        self.pushButtonDownload.setDefault(True)


        QMetaObject.connectSlotsByName(ReferencesDialog)
    # setupUi

    def retranslateUi(self, ReferencesDialog):
        ReferencesDialog.setWindowTitle(fakestr(u"Find references", None))
        self.label.setText(fakestr(u"Select files to find ... ", None))
        self.toolButtonAll.setText(fakestr(u"+", None))
        self.toolButtonNone.setText(fakestr(u"-", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(fakestr(u"Name", None));
        self.pushButtonDownload.setText(fakestr(u"Search", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

