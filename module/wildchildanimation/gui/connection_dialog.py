# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connection_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConnectionDialog(object):
    def setupUi(self, ConnectionDialog):
        if not ConnectionDialog.objectName():
            ConnectionDialog.setObjectName(u"ConnectionDialog")
        ConnectionDialog.resize(459, 130)
        self.verticalLayout = QVBoxLayout(ConnectionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelServer = QLabel(ConnectionDialog)
        self.labelServer.setObjectName(u"labelServer")
        self.labelServer.setMinimumSize(QSize(50, 0))

        self.horizontalLayout.addWidget(self.labelServer)

        self.lineEditServer = QLineEdit(ConnectionDialog)
        self.lineEditServer.setObjectName(u"lineEditServer")

        self.horizontalLayout.addWidget(self.lineEditServer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEmail = QLabel(ConnectionDialog)
        self.labelEmail.setObjectName(u"labelEmail")
        self.labelEmail.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_2.addWidget(self.labelEmail)

        self.lineEditEmail = QLineEdit(ConnectionDialog)
        self.lineEditEmail.setObjectName(u"lineEditEmail")

        self.horizontalLayout_2.addWidget(self.lineEditEmail)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(ConnectionDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(50, 0))

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEditPassword = QLineEdit(ConnectionDialog)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.lineEditPassword)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.buttonBox = QDialogButtonBox(ConnectionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConnectionDialog)
        self.buttonBox.accepted.connect(ConnectionDialog.accept)
        self.buttonBox.rejected.connect(ConnectionDialog.reject)

        QMetaObject.connectSlotsByName(ConnectionDialog)
    # setupUi

    def retranslateUi(self, ConnectionDialog):
        ConnectionDialog.setWindowTitle(QCoreApplication.translate("ConnectionDialog", u"Dialog", None))
        self.labelServer.setText(QCoreApplication.translate("ConnectionDialog", u"Server", None))
        self.labelEmail.setText(QCoreApplication.translate("ConnectionDialog", u"Email", None))
        self.label_3.setText(QCoreApplication.translate("ConnectionDialog", u"Password", None))
    # retranslateUi

