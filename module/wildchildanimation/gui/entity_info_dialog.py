# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entity_info_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr
class Ui_EntityInfoDialog(object):
    def setupUi(self, EntityInfoDialog):
        if not EntityInfoDialog.objectName():
            EntityInfoDialog.setObjectName(u"EntityInfoDialog")
        EntityInfoDialog.resize(958, 809)
        EntityInfoDialog.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(EntityInfoDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayoutProject = QHBoxLayout()
        self.horizontalLayoutProject.setObjectName(u"horizontalLayoutProject")
        self.labelProject = QLabel(EntityInfoDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))
        self.labelProject.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayoutProject.addWidget(self.labelProject)

        self.lineEditProject = QLineEdit(EntityInfoDialog)
        self.lineEditProject.setObjectName(u"lineEditProject")
        self.lineEditProject.setEnabled(False)

        self.horizontalLayoutProject.addWidget(self.lineEditProject)


        self.verticalLayout.addLayout(self.horizontalLayoutProject)

        self.horizontalLayoutEntity = QHBoxLayout()
        self.horizontalLayoutEntity.setObjectName(u"horizontalLayoutEntity")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayoutName = QHBoxLayout()
        self.horizontalLayoutName.setObjectName(u"horizontalLayoutName")
        self.labelEntity = QLabel(EntityInfoDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))
        self.labelEntity.setMaximumSize(QSize(100, 22))

        self.horizontalLayoutName.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(EntityInfoDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")
        self.lineEditEntity.setEnabled(False)
        self.lineEditEntity.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayoutName.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(EntityInfoDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")
        self.toolButtonWeb.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayoutName.addWidget(self.toolButtonWeb)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutName)

        self.textEdit = QTextEdit(EntityInfoDialog)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayoutEntity.addWidget(self.textEdit)


        self.horizontalLayoutEntity.addLayout(self.verticalLayoutEntity)

        self.labelPreview = QLabel(EntityInfoDialog)
        self.labelPreview.setObjectName(u"labelPreview")
        self.labelPreview.setMinimumSize(QSize(160, 160))
        self.labelPreview.setAutoFillBackground(True)
        self.labelPreview.setStyleSheet(u"")
        self.labelPreview.setFrameShape(QFrame.Box)
        self.labelPreview.setFrameShadow(QFrame.Raised)
        self.labelPreview.setAlignment(Qt.AlignCenter)

        self.horizontalLayoutEntity.addWidget(self.labelPreview)


        self.verticalLayout.addLayout(self.horizontalLayoutEntity)

        self.lineTable = QFrame(EntityInfoDialog)
        self.lineTable.setObjectName(u"lineTable")
        self.lineTable.setFrameShape(QFrame.HLine)
        self.lineTable.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.lineTable)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.toolButtonAll = QToolButton(EntityInfoDialog)
        self.toolButtonAll.setObjectName(u"toolButtonAll")

        self.horizontalLayout.addWidget(self.toolButtonAll)

        self.toolButtonNone = QToolButton(EntityInfoDialog)
        self.toolButtonNone.setObjectName(u"toolButtonNone")

        self.horizontalLayout.addWidget(self.toolButtonNone)

        self.labelWorkingDirectory = QLabel(EntityInfoDialog)
        self.labelWorkingDirectory.setObjectName(u"labelWorkingDirectory")
        self.labelWorkingDirectory.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.labelWorkingDirectory)

        self.lineEditWorkingDirectory = QLineEdit(EntityInfoDialog)
        self.lineEditWorkingDirectory.setObjectName(u"lineEditWorkingDirectory")

        self.horizontalLayout.addWidget(self.lineEditWorkingDirectory)

        self.toolButtonWorkingDir = QToolButton(EntityInfoDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")

        self.horizontalLayout.addWidget(self.toolButtonWorkingDir)

        self.checkBoxSkipExisting = QCheckBox(EntityInfoDialog)
        self.checkBoxSkipExisting.setObjectName(u"checkBoxSkipExisting")
        self.checkBoxSkipExisting.setMinimumSize(QSize(100, 0))
        self.checkBoxSkipExisting.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBoxSkipExisting)

        self.checkBoxExtractZips = QCheckBox(EntityInfoDialog)
        self.checkBoxExtractZips.setObjectName(u"checkBoxExtractZips")
        self.checkBoxExtractZips.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBoxExtractZips)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayoutFiles = QHBoxLayout()
        self.horizontalLayoutFiles.setObjectName(u"horizontalLayoutFiles")
        self.tableView = QTableView(EntityInfoDialog)
        self.tableView.setObjectName(u"tableView")
        font = QFont()
        font.setPointSize(8)
        self.tableView.setFont(font)
        self.tableView.setProperty("showDropIndicator", False)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.verticalHeader().setCascadingSectionResizes(True)

        self.horizontalLayoutFiles.addWidget(self.tableView)


        self.verticalLayout.addLayout(self.horizontalLayoutFiles)

        self.lineButtons = QFrame(EntityInfoDialog)
        self.lineButtons.setObjectName(u"lineButtons")
        self.lineButtons.setFrameShape(QFrame.HLine)
        self.lineButtons.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.lineButtons)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.pushButtonDownload = QPushButton(EntityInfoDialog)
        self.pushButtonDownload.setObjectName(u"pushButtonDownload")

        self.horizontalLayoutButtons.addWidget(self.pushButtonDownload)

        self.pushButtonPublish = QPushButton(EntityInfoDialog)
        self.pushButtonPublish.setObjectName(u"pushButtonPublish")
        self.pushButtonPublish.setEnabled(False)

        self.horizontalLayoutButtons.addWidget(self.pushButtonPublish)

        self.comboBoxTasks = QComboBox(EntityInfoDialog)
        self.comboBoxTasks.setObjectName(u"comboBoxTasks")
        self.comboBoxTasks.setEnabled(False)
        self.comboBoxTasks.setMinimumSize(QSize(200, 0))

        self.horizontalLayoutButtons.addWidget(self.comboBoxTasks)

        self.progressBar = QProgressBar(EntityInfoDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(-1)

        self.horizontalLayoutButtons.addWidget(self.progressBar)

        self.pushButtonClose = QPushButton(EntityInfoDialog)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayoutButtons.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayoutButtons)


        self.retranslateUi(EntityInfoDialog)

        QMetaObject.connectSlotsByName(EntityInfoDialog)
    # setupUi

    def retranslateUi(self, EntityInfoDialog):
        EntityInfoDialog.setWindowTitle(fakestr(u"Entity Information", None))
        self.labelProject.setText(fakestr(u"Project", None))
        self.labelEntity.setText(fakestr(u"Entity", None))
#if QT_CONFIG(tooltip)
        self.toolButtonWeb.setToolTip(fakestr(u"Open in Kitsu", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonWeb.setText(fakestr(u"...", None))
        self.labelPreview.setText("")
        self.toolButtonAll.setText(fakestr(u"+", None))
        self.toolButtonNone.setText(fakestr(u"-", None))
        self.labelWorkingDirectory.setText(fakestr(u"Root Folder", None))
        self.toolButtonWorkingDir.setText(fakestr(u"...", None))
        self.checkBoxSkipExisting.setText(fakestr(u"Skip Existing Files", None))
        self.checkBoxExtractZips.setText(fakestr(u"Extract Zip Files", None))
        self.pushButtonDownload.setText(fakestr(u"Download", None))
        self.pushButtonPublish.setText(fakestr(u"Publish", None))
        self.pushButtonClose.setText(fakestr(u"Close", None))
    # retranslateUi

