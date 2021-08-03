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
        SwingCreateDialog.resize(584, 263)
        SwingCreateDialog.setModal(False)
        self.verticalLayout = QVBoxLayout(SwingCreateDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
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

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.horizontalLayoutFrameDetails = QHBoxLayout()
        self.horizontalLayoutFrameDetails.setObjectName(u"horizontalLayoutFrameDetails")
        self.radioButtonShot = QRadioButton(SwingCreateDialog)
        self.radioButtonShot.setObjectName(u"radioButtonShot")
        self.radioButtonShot.setMinimumSize(QSize(100, 0))
        self.radioButtonShot.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayoutFrameDetails.addWidget(self.radioButtonShot)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelFrameIn = QLabel(SwingCreateDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(50, 0))
        self.labelFrameIn.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(SwingCreateDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")

        self.horizontalLayout_3.addWidget(self.lineEditFrameIn)

        self.labelFrameOut = QLabel(SwingCreateDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(50, 0))
        self.labelFrameOut.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(SwingCreateDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")

        self.horizontalLayout_3.addWidget(self.lineEditFrameOut)

        self.labelFrameCount = QLabel(SwingCreateDialog)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(50, 0))
        self.labelFrameCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(SwingCreateDialog)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")

        self.horizontalLayout_3.addWidget(self.lineEditFrameCount)


        self.horizontalLayoutFrameDetails.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFrameDetails.addItem(self.horizontalSpacer)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayoutFrameDetails)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButtonAsset = QRadioButton(SwingCreateDialog)
        self.radioButtonAsset.setObjectName(u"radioButtonAsset")
        self.radioButtonAsset.setMinimumSize(QSize(100, 0))
        self.radioButtonAsset.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.radioButtonAsset)

        self.lineEditAssetType = QLineEdit(SwingCreateDialog)
        self.lineEditAssetType.setObjectName(u"lineEditAssetType")

        self.horizontalLayout_4.addWidget(self.lineEditAssetType)


        self.verticalLayoutEntityInfo.addLayout(self.horizontalLayout_4)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.checkBoxLoadExisting = QCheckBox(SwingCreateDialog)
        self.checkBoxLoadExisting.setObjectName(u"checkBoxLoadExisting")

        self.verticalLayout_2.addWidget(self.checkBoxLoadExisting)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

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


        self.verticalLayout.addLayout(self.horizontalLayout)


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
        self.radioButtonShot.setText(fakestr(u"Shot", None))
        self.labelFrameIn.setText(fakestr(u"In", None))
        self.labelFrameOut.setText(fakestr(u"Out", None))
        self.labelFrameCount.setText(fakestr(u"Count", None))
        self.radioButtonAsset.setText(fakestr(u"Asset", None))
        self.checkBoxLoadExisting.setText(fakestr(u"Load existing file if found", None))
        self.pushButtonUpdate.setText(fakestr(u"Update", None))
        self.pushButtonImport.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

