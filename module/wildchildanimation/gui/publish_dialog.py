# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'publish_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PublishDialog(object):
    def setupUi(self, PublishDialog):
        if not PublishDialog.objectName():
            PublishDialog.setObjectName(u"PublishDialog")
        PublishDialog.resize(371, 420)
        self.verticalLayout = QVBoxLayout(PublishDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(PublishDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEditTask = QLineEdit(PublishDialog)
        self.lineEditTask.setObjectName(u"lineEditTask")
        self.lineEditTask.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEditTask)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayoutProjectFile = QHBoxLayout()
        self.horizontalLayoutProjectFile.setObjectName(u"horizontalLayoutProjectFile")
        self.projectFileLabel = QLabel(PublishDialog)
        self.projectFileLabel.setObjectName(u"projectFileLabel")
        self.projectFileLabel.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutProjectFile.addWidget(self.projectFileLabel)

        self.projectFileEdit = QLineEdit(PublishDialog)
        self.projectFileEdit.setObjectName(u"projectFileEdit")

        self.horizontalLayoutProjectFile.addWidget(self.projectFileEdit)

        self.projectFileToolButton = QToolButton(PublishDialog)
        self.projectFileToolButton.setObjectName(u"projectFileToolButton")
        self.projectFileToolButton.setMinimumSize(QSize(40, 0))
        self.projectFileToolButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile.addWidget(self.projectFileToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProjectFile)

        self.horizontalLayoutProjectFile_2 = QHBoxLayout()
        self.horizontalLayoutProjectFile_2.setObjectName(u"horizontalLayoutProjectFile_2")
        self.fbxFileLabel = QLabel(PublishDialog)
        self.fbxFileLabel.setObjectName(u"fbxFileLabel")
        self.fbxFileLabel.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutProjectFile_2.addWidget(self.fbxFileLabel)

        self.fbxFileEdit = QLineEdit(PublishDialog)
        self.fbxFileEdit.setObjectName(u"fbxFileEdit")

        self.horizontalLayoutProjectFile_2.addWidget(self.fbxFileEdit)

        self.fbxFileToolButton = QToolButton(PublishDialog)
        self.fbxFileToolButton.setObjectName(u"fbxFileToolButton")
        self.fbxFileToolButton.setMinimumSize(QSize(40, 0))
        self.fbxFileToolButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile_2.addWidget(self.fbxFileToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProjectFile_2)

        self.horizontalLayoutProjectFile_3 = QHBoxLayout()
        self.horizontalLayoutProjectFile_3.setObjectName(u"horizontalLayoutProjectFile_3")
        self.reviewFile = QLabel(PublishDialog)
        self.reviewFile.setObjectName(u"reviewFile")
        self.reviewFile.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutProjectFile_3.addWidget(self.reviewFile)

        self.reviewFileEdit = QLineEdit(PublishDialog)
        self.reviewFileEdit.setObjectName(u"reviewFileEdit")

        self.horizontalLayoutProjectFile_3.addWidget(self.reviewFileEdit)

        self.reviewFileToolButton = QToolButton(PublishDialog)
        self.reviewFileToolButton.setObjectName(u"reviewFileToolButton")
        self.reviewFileToolButton.setMinimumSize(QSize(40, 0))
        self.reviewFileToolButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile_3.addWidget(self.reviewFileToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProjectFile_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(PublishDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.label)

        self.reviewTitleLineEdit = QLineEdit(PublishDialog)
        self.reviewTitleLineEdit.setObjectName(u"reviewTitleLineEdit")

        self.horizontalLayout_4.addWidget(self.reviewTitleLineEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalLayoutReferences = QVBoxLayout()
        self.verticalLayoutReferences.setObjectName(u"verticalLayoutReferences")
        self.referencesLabel = QLabel(PublishDialog)
        self.referencesLabel.setObjectName(u"referencesLabel")
        self.referencesLabel.setMinimumSize(QSize(100, 0))

        self.verticalLayoutReferences.addWidget(self.referencesLabel)

        self.referencesTableWidget = QTableWidget(PublishDialog)
        self.referencesTableWidget.setObjectName(u"referencesTableWidget")

        self.verticalLayoutReferences.addWidget(self.referencesTableWidget)

        self.horizontalLayoutC4DReferences = QHBoxLayout()
        self.horizontalLayoutC4DReferences.setObjectName(u"horizontalLayoutC4DReferences")
        self.referencesAddPushButton = QPushButton(PublishDialog)
        self.referencesAddPushButton.setObjectName(u"referencesAddPushButton")

        self.horizontalLayoutC4DReferences.addWidget(self.referencesAddPushButton)

        self.referencesRemovePushButton = QPushButton(PublishDialog)
        self.referencesRemovePushButton.setObjectName(u"referencesRemovePushButton")

        self.horizontalLayoutC4DReferences.addWidget(self.referencesRemovePushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutC4DReferences.addItem(self.horizontalSpacer)


        self.verticalLayoutReferences.addLayout(self.horizontalLayoutC4DReferences)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.commentLabel = QLabel(PublishDialog)
        self.commentLabel.setObjectName(u"commentLabel")
        self.commentLabel.setMinimumSize(QSize(100, 0))
        self.commentLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_4.addWidget(self.commentLabel)

        self.commentEdit = QPlainTextEdit(PublishDialog)
        self.commentEdit.setObjectName(u"commentEdit")

        self.verticalLayout_4.addWidget(self.commentEdit)


        self.verticalLayoutReferences.addLayout(self.verticalLayout_4)


        self.verticalLayout_2.addLayout(self.verticalLayoutReferences)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pushButtonOK = QPushButton(PublishDialog)
        self.pushButtonOK.setObjectName(u"pushButtonOK")

        self.horizontalLayout.addWidget(self.pushButtonOK)

        self.pushButtonCancel = QPushButton(PublishDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(PublishDialog)

        self.pushButtonOK.setDefault(True)


        QMetaObject.connectSlotsByName(PublishDialog)
    # setupUi

    def retranslateUi(self, PublishDialog):
        PublishDialog.setWindowTitle(QCoreApplication.translate("PublishDialog", u"Publish Asset for Task", None))
        self.label_2.setText(QCoreApplication.translate("PublishDialog", u"Task", None))
        self.projectFileLabel.setText(QCoreApplication.translate("PublishDialog", u"Project File", None))
        self.projectFileToolButton.setText(QCoreApplication.translate("PublishDialog", u"...", None))
        self.fbxFileLabel.setText(QCoreApplication.translate("PublishDialog", u"FBX File", None))
        self.fbxFileToolButton.setText(QCoreApplication.translate("PublishDialog", u"...", None))
        self.reviewFile.setText(QCoreApplication.translate("PublishDialog", u"Preview File", None))
        self.reviewFileToolButton.setText(QCoreApplication.translate("PublishDialog", u"...", None))
        self.label.setText(QCoreApplication.translate("PublishDialog", u"Preview Title", None))
        self.referencesLabel.setText(QCoreApplication.translate("PublishDialog", u"References", None))
        self.referencesAddPushButton.setText(QCoreApplication.translate("PublishDialog", u"&Add", None))
        self.referencesRemovePushButton.setText(QCoreApplication.translate("PublishDialog", u"&Remove", None))
        self.commentLabel.setText(QCoreApplication.translate("PublishDialog", u"Comments", None))
        self.pushButtonOK.setText(QCoreApplication.translate("PublishDialog", u"OK", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("PublishDialog", u"Close", None))
    # retranslateUi

