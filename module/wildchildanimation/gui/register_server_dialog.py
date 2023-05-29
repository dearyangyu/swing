# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_server_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_register_server_dialog(object):
    def setupUi(self, register_server_dialog):
        if not register_server_dialog.objectName():
            register_server_dialog.setObjectName(u"register_server_dialog")
        register_server_dialog.resize(506, 152)
        register_server_dialog.setSizeGripEnabled(True)
        register_server_dialog.setModal(True)
        self.verticalLayout = QVBoxLayout(register_server_dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTreeHouse = QLabel(register_server_dialog)
        self.labelTreeHouse.setObjectName(u"labelTreeHouse")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTreeHouse.setFont(font)

        self.verticalLayout.addWidget(self.labelTreeHouse)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelServer = QLabel(register_server_dialog)
        self.labelServer.setObjectName(u"labelServer")
        self.labelServer.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.labelServer)

        self.comboBoxServer = QComboBox(register_server_dialog)
        self.comboBoxServer.setObjectName(u"comboBoxServer")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxServer.sizePolicy().hasHeightForWidth())
        self.comboBoxServer.setSizePolicy(sizePolicy)
        self.comboBoxServer.setEditable(True)

        self.horizontalLayout.addWidget(self.comboBoxServer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEmail = QLabel(register_server_dialog)
        self.labelEmail.setObjectName(u"labelEmail")
        self.labelEmail.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_2.addWidget(self.labelEmail)

        self.lineEditEmail = QLineEdit(register_server_dialog)
        self.lineEditEmail.setObjectName(u"lineEditEmail")

        self.horizontalLayout_2.addWidget(self.lineEditEmail)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelPassword = QLabel(register_server_dialog)
        self.labelPassword.setObjectName(u"labelPassword")
        self.labelPassword.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_3.addWidget(self.labelPassword)

        self.lineEditPassword = QLineEdit(register_server_dialog)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.lineEditPassword)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonTest = QPushButton(register_server_dialog)
        self.pushButtonTest.setObjectName(u"pushButtonTest")

        self.horizontalLayout_4.addWidget(self.pushButtonTest)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(register_server_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_4.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(register_server_dialog)
        self.buttonBox.accepted.connect(register_server_dialog.accept)
        self.buttonBox.rejected.connect(register_server_dialog.reject)

        QMetaObject.connectSlotsByName(register_server_dialog)
    # setupUi

    def retranslateUi(self, register_server_dialog):
        register_server_dialog.setWindowTitle(fakestr(u"Treehouse: Register Server", None))
        self.labelTreeHouse.setText(fakestr(u"Treehouse: Server Registration", None))
        self.labelServer.setText(fakestr(u"Server URL", None))
        self.comboBoxServer.setPlaceholderText(fakestr(u"Server Address", None))
        self.labelEmail.setText(fakestr(u"Email address", None))
#if QT_CONFIG(tooltip)
        self.lineEditEmail.setToolTip(fakestr(u"Logon email address", None))
#endif // QT_CONFIG(tooltip)
        self.labelPassword.setText(fakestr(u"Password", None))
#if QT_CONFIG(tooltip)
        self.lineEditPassword.setToolTip(fakestr(u"Logon password", None))
#endif // QT_CONFIG(tooltip)
        self.pushButtonTest.setText(fakestr(u"Test", None))
    # retranslateUi

