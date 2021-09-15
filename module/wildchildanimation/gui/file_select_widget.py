# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_select_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from wildchildanimation.gui.swing_utils import fakestr


class Ui_FileSelectWidget(object):
    def setupUi(self, FileSelectWidget):
        if not FileSelectWidget.objectName():
            FileSelectWidget.setObjectName(u"FileSelectWidget")
        FileSelectWidget.resize(912, 336)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileSelectWidget.sizePolicy().hasHeightForWidth())
        FileSelectWidget.setSizePolicy(sizePolicy)
        FileSelectWidget.setModal(True)
        self.verticalLayout = QVBoxLayout(FileSelectWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(FileSelectWidget)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout.addWidget(self.treeView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonWorkingFiles = QPushButton(FileSelectWidget)
        self.pushButtonWorkingFiles.setObjectName(u"pushButtonWorkingFiles")

        self.horizontalLayout.addWidget(self.pushButtonWorkingFiles)

        self.pushButtonOutputFiles = QPushButton(FileSelectWidget)
        self.pushButtonOutputFiles.setObjectName(u"pushButtonOutputFiles")

        self.horizontalLayout.addWidget(self.pushButtonOutputFiles)

        self.pushButtonZip = QPushButton(FileSelectWidget)
        self.pushButtonZip.setObjectName(u"pushButtonZip")

        self.horizontalLayout.addWidget(self.pushButtonZip)

        self.labelMessage = QLabel(FileSelectWidget)
        self.labelMessage.setObjectName(u"labelMessage")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy1)
        self.labelMessage.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.labelMessage)

        self.pushButtonOK = QPushButton(FileSelectWidget)
        self.pushButtonOK.setObjectName(u"pushButtonOK")

        self.horizontalLayout.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QPushButton(FileSelectWidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(FileSelectWidget)

        QMetaObject.connectSlotsByName(FileSelectWidget)
    # setupUi

    def retranslateUi(self, FileSelectWidget):
        FileSelectWidget.setWindowTitle(fakestr(u"treehouse: swing", None))
        self.pushButtonWorkingFiles.setText(fakestr(u"Working Files", None))
        self.pushButtonOutputFiles.setText(fakestr(u"Output Files", None))
        self.pushButtonZip.setText(fakestr(u"Zip", None))
        self.labelMessage.setText("")
        self.pushButtonOK.setText(fakestr(u"OK", None))
        self.pushButtonCancel.setText(fakestr(u"Cancel", None))
    # retranslateUi

