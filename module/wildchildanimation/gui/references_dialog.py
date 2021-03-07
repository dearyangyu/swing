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


class Ui_ReferencesDialog(object):
    def setupUi(self, ReferencesDialog):
        if not ReferencesDialog.objectName():
            ReferencesDialog.setObjectName(u"ReferencesDialog")
        ReferencesDialog.setEnabled(True)
        ReferencesDialog.resize(629, 301)
        self.verticalLayout = QVBoxLayout(ReferencesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelEntity = QLabel(ReferencesDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(ReferencesDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")

        self.horizontalLayout_6.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(ReferencesDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")

        self.horizontalLayout_6.addWidget(self.toolButtonWeb)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelWorkingDirectory = QLabel(ReferencesDialog)
        self.labelWorkingDirectory.setObjectName(u"labelWorkingDirectory")
        self.labelWorkingDirectory.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.labelWorkingDirectory)

        self.lineEditWorkingDirectory = QLineEdit(ReferencesDialog)
        self.lineEditWorkingDirectory.setObjectName(u"lineEditWorkingDirectory")

        self.horizontalLayout.addWidget(self.lineEditWorkingDirectory)

        self.toolButtonWorkingDir = QToolButton(ReferencesDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")

        self.horizontalLayout.addWidget(self.toolButtonWorkingDir)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.checkBoxSkipExisting = QCheckBox(ReferencesDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setMinimumSize(QSize(100, 0))
        self.checkBoxSkipExisting.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBoxSkipExisting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.checkBoxExtractZips = QCheckBox(ReferencesDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBoxExtractZips)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

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
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
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

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

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
        ReferencesDialog.setWindowTitle(QCoreApplication.translate("ReferencesDialog", u"Find references", None))
        self.labelEntity.setText(QCoreApplication.translate("ReferencesDialog", u"Entity", None))
        self.toolButtonWeb.setText(QCoreApplication.translate("ReferencesDialog", u"...", None))
        self.labelWorkingDirectory.setText(QCoreApplication.translate("ReferencesDialog", u"Projects Folder", None))
        self.toolButtonWorkingDir.setText(QCoreApplication.translate("ReferencesDialog", u"...", None))
        self.checkBoxSkipExisting.setText(QCoreApplication.translate("ReferencesDialog", u"Skip Existing Files", None))
        self.checkBoxExtractZips.setText(QCoreApplication.translate("ReferencesDialog", u"Extract Zip Files", None))
        self.toolButtonAll.setText(QCoreApplication.translate("ReferencesDialog", u"+", None))
        self.toolButtonNone.setText(QCoreApplication.translate("ReferencesDialog", u"-", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ReferencesDialog", u"File", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ReferencesDialog", u"Size", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ReferencesDialog", u"v", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("ReferencesDialog", u"Task", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("ReferencesDialog", u"Updated", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("ReferencesDialog", u"Status", None));
        self.pushButtonDownload.setText(QCoreApplication.translate("ReferencesDialog", u"Search", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("ReferencesDialog", u"Close", None))
    # retranslateUi

