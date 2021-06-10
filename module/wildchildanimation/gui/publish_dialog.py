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

from wildchildanimation.gui.swing_utils import fakestr

class Ui_PublishDialog(object):
    def setupUi(self, PublishDialog):
        if not PublishDialog.objectName():
            PublishDialog.setObjectName(u"PublishDialog")
        PublishDialog.resize(577, 665)
        self.verticalLayout_6 = QVBoxLayout(PublishDialog)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(PublishDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit = QLineEdit(PublishDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_3.addWidget(self.lineEdit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_4 = QLabel(PublishDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_4)

        self.lineEdit_2 = QLineEdit(PublishDialog)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_5.addWidget(self.lineEdit_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(PublishDialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(100, 0))
        self.label_5.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_5)

        self.lineEdit_3 = QLineEdit(PublishDialog)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_6.addWidget(self.lineEdit_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.labelIcon = QLabel(PublishDialog)
        self.labelIcon.setObjectName(u"labelIcon")
        self.labelIcon.setMinimumSize(QSize(120, 0))
        self.labelIcon.setFrameShape(QFrame.Box)

        self.horizontalLayout_7.addWidget(self.labelIcon)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(PublishDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEditTask = QLineEdit(PublishDialog)
        self.lineEditTask.setObjectName(u"lineEditTask")
        self.lineEditTask.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEditTask)

        self.comboBoxTaskStatus = QComboBox(PublishDialog)
        self.comboBoxTaskStatus.setObjectName(u"comboBoxTaskStatus")

        self.horizontalLayout_2.addWidget(self.comboBoxTaskStatus)

        self.toolButtonWeb = QToolButton(PublishDialog)
        self.toolButtonWeb.setObjectName(u"toolButtonWeb")

        self.horizontalLayout_2.addWidget(self.toolButtonWeb)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.groupBox = QGroupBox(PublishDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayoutProjectFile = QHBoxLayout()
        self.horizontalLayoutProjectFile.setObjectName(u"horizontalLayoutProjectFile")
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setMinimumSize(QSize(100, 0))
        font1 = QFont()
        font1.setBold(False)
        font1.setWeight(50)
        self.radioButton.setFont(font1)

        self.horizontalLayoutProjectFile.addWidget(self.radioButton)

        self.projectFileEdit = QLineEdit(self.groupBox)
        self.projectFileEdit.setObjectName(u"projectFileEdit")

        self.horizontalLayoutProjectFile.addWidget(self.projectFileEdit)

        self.projectFileToolButton = QToolButton(self.groupBox)
        self.projectFileToolButton.setObjectName(u"projectFileToolButton")
        self.projectFileToolButton.setMinimumSize(QSize(40, 0))
        self.projectFileToolButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile.addWidget(self.projectFileToolButton)


        self.verticalLayout_5.addLayout(self.horizontalLayoutProjectFile)

        self.horizontalLayoutProjectFile_4 = QHBoxLayout()
        self.horizontalLayoutProjectFile_4.setObjectName(u"horizontalLayoutProjectFile_4")
        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setMinimumSize(QSize(100, 0))
        self.radioButton_2.setFont(font1)

        self.horizontalLayoutProjectFile_4.addWidget(self.radioButton_2)

        self.projectFileEdit_2 = QLineEdit(self.groupBox)
        self.projectFileEdit_2.setObjectName(u"projectFileEdit_2")

        self.horizontalLayoutProjectFile_4.addWidget(self.projectFileEdit_2)

        self.projectFileToolButton_2 = QToolButton(self.groupBox)
        self.projectFileToolButton_2.setObjectName(u"projectFileToolButton_2")
        self.projectFileToolButton_2.setMinimumSize(QSize(40, 0))
        self.projectFileToolButton_2.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile_4.addWidget(self.projectFileToolButton_2)


        self.verticalLayout_5.addLayout(self.horizontalLayoutProjectFile_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.referencesLabel = QLabel(self.groupBox)
        self.referencesLabel.setObjectName(u"referencesLabel")
        self.referencesLabel.setMinimumSize(QSize(100, 0))
        self.referencesLabel.setFont(font)

        self.verticalLayout_3.addWidget(self.referencesLabel)

        self.referencesListView = QListView(self.groupBox)
        self.referencesListView.setObjectName(u"referencesListView")

        self.verticalLayout_3.addWidget(self.referencesListView)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.referencesAddPushButton = QPushButton(self.groupBox)
        self.referencesAddPushButton.setObjectName(u"referencesAddPushButton")
        self.referencesAddPushButton.setEnabled(True)
        self.referencesAddPushButton.setFont(font1)

        self.horizontalLayout_8.addWidget(self.referencesAddPushButton)

        self.referencesRemovePushButton = QPushButton(self.groupBox)
        self.referencesRemovePushButton.setObjectName(u"referencesRemovePushButton")
        self.referencesRemovePushButton.setEnabled(True)
        self.referencesRemovePushButton.setFont(font1)

        self.horizontalLayout_8.addWidget(self.referencesRemovePushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(PublishDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.label)

        self.reviewTitleLineEdit = QLineEdit(self.groupBox_2)
        self.reviewTitleLineEdit.setObjectName(u"reviewTitleLineEdit")

        self.horizontalLayout_4.addWidget(self.reviewTitleLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayoutProjectFile_6 = QHBoxLayout()
        self.horizontalLayoutProjectFile_6.setObjectName(u"horizontalLayoutProjectFile_6")
        self.radioButton_4 = QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setMinimumSize(QSize(100, 0))
        self.radioButton_4.setFont(font1)

        self.horizontalLayoutProjectFile_6.addWidget(self.radioButton_4)

        self.projectFileEdit_4 = QLineEdit(self.groupBox_2)
        self.projectFileEdit_4.setObjectName(u"projectFileEdit_4")

        self.horizontalLayoutProjectFile_6.addWidget(self.projectFileEdit_4)

        self.projectFileToolButton_4 = QToolButton(self.groupBox_2)
        self.projectFileToolButton_4.setObjectName(u"projectFileToolButton_4")
        self.projectFileToolButton_4.setMinimumSize(QSize(40, 0))
        self.projectFileToolButton_4.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile_6.addWidget(self.projectFileToolButton_4)


        self.verticalLayout.addLayout(self.horizontalLayoutProjectFile_6)

        self.horizontalLayoutProjectFile_5 = QHBoxLayout()
        self.horizontalLayoutProjectFile_5.setObjectName(u"horizontalLayoutProjectFile_5")
        self.radioButton_3 = QRadioButton(self.groupBox_2)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setMinimumSize(QSize(100, 0))
        self.radioButton_3.setFont(font1)

        self.horizontalLayoutProjectFile_5.addWidget(self.radioButton_3)

        self.projectFileEdit_3 = QLineEdit(self.groupBox_2)
        self.projectFileEdit_3.setObjectName(u"projectFileEdit_3")

        self.horizontalLayoutProjectFile_5.addWidget(self.projectFileEdit_3)

        self.projectFileToolButton_3 = QToolButton(self.groupBox_2)
        self.projectFileToolButton_3.setObjectName(u"projectFileToolButton_3")
        self.projectFileToolButton_3.setMinimumSize(QSize(40, 0))
        self.projectFileToolButton_3.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile_5.addWidget(self.projectFileToolButton_3)


        self.verticalLayout.addLayout(self.horizontalLayoutProjectFile_5)


        self.verticalLayout_6.addWidget(self.groupBox_2)

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


        self.verticalLayout_6.addLayout(self.verticalLayout_4)

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


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.retranslateUi(PublishDialog)

        self.pushButtonOK.setDefault(True)


        QMetaObject.connectSlotsByName(PublishDialog)
    # setupUi

    def retranslateUi(self, PublishDialog):
        PublishDialog.setWindowTitle(fakestr(u"Publish Asset for Task", None))
        self.label_3.setText(fakestr(u"Project:", None))
        self.label_4.setText(fakestr(u"Episode", None))
        self.label_5.setText(fakestr(u"Selection", None))
        self.labelIcon.setText(fakestr(u"Preview", None))
        self.label_2.setText(fakestr(u"Task", None))
#if QT_CONFIG(tooltip)
        self.toolButtonWeb.setToolTip(fakestr(u"Open in Kitsu", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonWeb.setText(fakestr(u"...", None))
        self.groupBox.setTitle(fakestr(u"Working Files", None))
        self.radioButton.setText(fakestr(u"Working File", None))
        self.projectFileToolButton.setText(fakestr(u"...", None))
        self.radioButton_2.setText(fakestr(u"Working Dir", None))
        self.projectFileToolButton_2.setText(fakestr(u"...", None))
        self.referencesLabel.setText(fakestr(u"Secondary Assets", None))
        self.referencesAddPushButton.setText(fakestr(u"&Add", None))
        self.referencesRemovePushButton.setText(fakestr(u"&Remove", None))
        self.groupBox_2.setTitle(fakestr(u"Output Files", None))
        self.label.setText(fakestr(u"Review Title", None))
        self.radioButton_4.setText(fakestr(u"Output File", None))
        self.projectFileToolButton_4.setText(fakestr(u"...", None))
        self.radioButton_3.setText(fakestr(u"Output Dir", None))
        self.projectFileToolButton_3.setText(fakestr(u"...", None))
        self.commentLabel.setText(fakestr(u"Comments", None))
        self.pushButtonOK.setText(fakestr(u"OK", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

