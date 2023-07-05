# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_create_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_SwingCreateDialog(object):
    def setupUi(self, SwingCreateDialog):
        if not SwingCreateDialog.objectName():
            SwingCreateDialog.setObjectName(u"SwingCreateDialog")
        SwingCreateDialog.setEnabled(True)
        SwingCreateDialog.resize(641, 458)
        SwingCreateDialog.setModal(False)
        self.verticalLayout_6 = QVBoxLayout(SwingCreateDialog)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEntity = QLabel(SwingCreateDialog)
        self.labelEntity.setObjectName(u"labelEntity")
        self.labelEntity.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.labelEntity)

        self.lineEditEntity = QLineEdit(SwingCreateDialog)
        self.lineEditEntity.setObjectName(u"lineEditEntity")

        self.horizontalLayout_2.addWidget(self.lineEditEntity)

        self.toolButtonWeb = QToolButton(SwingCreateDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")
        self.toolButtonWeb.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_2.addWidget(self.toolButtonWeb)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_2)

        self.horizontalLayoutProjectDir = QHBoxLayout()
        self.horizontalLayoutProjectDir.setObjectName(u"horizontalLayoutProjectDir")
        self.labelWorkingDir = QLabel(SwingCreateDialog)
        self.labelWorkingDir.setObjectName(u"labelWorkingDir")
        self.labelWorkingDir.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutProjectDir.addWidget(self.labelWorkingDir)

        self.lineEditWorkingDir = QLineEdit(SwingCreateDialog)
        self.lineEditWorkingDir.setObjectName(u"lineEditWorkingDir")

        self.horizontalLayoutProjectDir.addWidget(self.lineEditWorkingDir)

        self.toolButtonWorkingDir = QToolButton(SwingCreateDialog)
        self.toolButtonWorkingDir.setObjectName(u"toolButtonWorkingDir")
        self.toolButtonWorkingDir.setMinimumSize(QSize(40, 0))

        self.horizontalLayoutProjectDir.addWidget(self.toolButtonWorkingDir)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutProjectDir)

        self.horizontalLayoutSoftware = QHBoxLayout()
        self.horizontalLayoutSoftware.setObjectName(u"horizontalLayoutSoftware")
        self.labelSoftware = QLabel(SwingCreateDialog)
        self.labelSoftware.setObjectName(u"labelSoftware")
        self.labelSoftware.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutSoftware.addWidget(self.labelSoftware)

        self.comboBoxSoftware = QComboBox(SwingCreateDialog)
        self.comboBoxSoftware.setObjectName(u"comboBoxSoftware")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSoftware.sizePolicy().hasHeightForWidth())
        self.comboBoxSoftware.setSizePolicy(sizePolicy)

        self.horizontalLayoutSoftware.addWidget(self.comboBoxSoftware)


        self.verticalLayoutEntity.addLayout(self.horizontalLayoutSoftware)


        self.verticalLayout_6.addLayout(self.verticalLayoutEntity)

        self.groupBoxTaskInfo = QGroupBox(SwingCreateDialog)
        self.groupBoxTaskInfo.setObjectName(u"groupBoxTaskInfo")
        self.groupBoxTaskInfo.setFlat(True)
        self.verticalLayout_4 = QVBoxLayout(self.groupBoxTaskInfo)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 9, 0, 0)
        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.horizontalLayoutFrameDetails = QHBoxLayout()
        self.horizontalLayoutFrameDetails.setObjectName(u"horizontalLayoutFrameDetails")
        self.radioButtonShot = QRadioButton(self.groupBoxTaskInfo)
        self.radioButtonShot.setObjectName(u"radioButtonShot")
        self.radioButtonShot.setMinimumSize(QSize(100, 0))
        self.radioButtonShot.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayoutFrameDetails.addWidget(self.radioButtonShot)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFrameIn = QLabel(self.groupBoxTaskInfo)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(60, 0))
        self.labelFrameIn.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(self.groupBoxTaskInfo)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")

        self.horizontalLayout_3.addWidget(self.lineEditFrameIn)

        self.labelFrameOut = QLabel(self.groupBoxTaskInfo)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(60, 0))
        self.labelFrameOut.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(self.groupBoxTaskInfo)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")

        self.horizontalLayout_3.addWidget(self.lineEditFrameOut)

        self.labelFrameCount = QLabel(self.groupBoxTaskInfo)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(70, 0))
        self.labelFrameCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(self.groupBoxTaskInfo)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")

        self.horizontalLayout_3.addWidget(self.lineEditFrameCount)


        self.horizontalLayoutFrameDetails.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFrameDetails.addItem(self.horizontalSpacer)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutFrameDetails)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButtonAsset = QRadioButton(self.groupBoxTaskInfo)
        self.radioButtonAsset.setObjectName(u"radioButtonAsset")
        self.radioButtonAsset.setMinimumSize(QSize(100, 0))
        self.radioButtonAsset.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.radioButtonAsset)

        self.lineEditAssetType = QLineEdit(self.groupBoxTaskInfo)
        self.lineEditAssetType.setObjectName(u"lineEditAssetType")

        self.horizontalLayout_4.addWidget(self.lineEditAssetType)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addLayout(self.verticalLayoutEntityInfo)


        self.verticalLayout_6.addWidget(self.groupBoxTaskInfo)

        self.groupBoxFileInfo = QGroupBox(SwingCreateDialog)
        self.groupBoxFileInfo.setObjectName(u"groupBoxFileInfo")
        self.groupBoxFileInfo.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxFileInfo)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.rbCreateNew = QRadioButton(self.groupBoxFileInfo)
        self.rbCreateNew.setObjectName(u"rbCreateNew")

        self.horizontalLayout_5.addWidget(self.rbCreateNew)

        self.rbOpenExisting = QRadioButton(self.groupBoxFileInfo)
        self.rbOpenExisting.setObjectName(u"rbOpenExisting")

        self.horizontalLayout_5.addWidget(self.rbOpenExisting)

        self.rbLoad = QRadioButton(self.groupBoxFileInfo)
        self.rbLoad.setObjectName(u"rbLoad")

        self.horizontalLayout_5.addWidget(self.rbLoad)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.tableView = QTableView(self.groupBoxFileInfo)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.verticalLayout_6.addWidget(self.groupBoxFileInfo)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labelFileDetails = QLabel(SwingCreateDialog)
        self.labelFileDetails.setObjectName(u"labelFileDetails")
        self.labelFileDetails.setMinimumSize(QSize(0, 20))
        self.labelFileDetails.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.labelFileDetails)


        self.verticalLayout_6.addLayout(self.verticalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(SwingCreateDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.pushButtonUpdate = QPushButton(SwingCreateDialog)
        self.pushButtonUpdate.setObjectName(u"pushButtonUpdate")

        self.horizontalLayout.addWidget(self.pushButtonUpdate)

        self.pushButtonImport = QPushButton(SwingCreateDialog)
        self.pushButtonImport.setObjectName(u"pushButtonImport")

        self.horizontalLayout.addWidget(self.pushButtonImport)

        self.pushButtonCancel = QPushButton(SwingCreateDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.retranslateUi(SwingCreateDialog)

        QMetaObject.connectSlotsByName(SwingCreateDialog)
    # setupUi

    def retranslateUi(self, SwingCreateDialog):
        SwingCreateDialog.setWindowTitle(fakestr(u"swing: create new entity", None))
        self.labelEntity.setText(fakestr(u"Entity", None))
#if QT_CONFIG(tooltip)
        self.toolButtonWeb.setToolTip(fakestr(u"Opens link in Kitsu", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonWeb.setText(fakestr(u"Web", None))
        self.labelWorkingDir.setText(fakestr(u"Working Dir", None))
        self.toolButtonWorkingDir.setText(fakestr(u"...", None))
        self.labelSoftware.setText(fakestr(u"Software", None))
        self.groupBoxTaskInfo.setTitle(fakestr(u"Task Type", None))
        self.radioButtonShot.setText(fakestr(u"Shot", None))
        self.labelFrameIn.setText(fakestr(u"Frame In", None))
        self.labelFrameOut.setText(fakestr(u" Frame Out", None))
        self.labelFrameCount.setText(fakestr(u"Frame Count", None))
        self.radioButtonAsset.setText(fakestr(u"Asset", None))
        self.groupBoxFileInfo.setTitle(fakestr(u"File Action", None))
        self.rbCreateNew.setText(fakestr(u"&New", None))
#if QT_CONFIG(shortcut)
        self.rbCreateNew.setShortcut(fakestr(u"N", None))
#endif // QT_CONFIG(shortcut)
        self.rbOpenExisting.setText(fakestr(u"&Open", None))
#if QT_CONFIG(shortcut)
        self.rbOpenExisting.setShortcut(fakestr(u"O", None))
#endif // QT_CONFIG(shortcut)
        self.rbLoad.setText(fakestr(u"&Load", None))
#if QT_CONFIG(shortcut)
        self.rbLoad.setShortcut(fakestr(u"L", None))
#endif // QT_CONFIG(shortcut)
        self.labelFileDetails.setText("")
        self.pushButtonUpdate.setText(fakestr(u"Update", None))
        self.pushButtonImport.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

