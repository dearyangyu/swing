# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_render_submit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from wildchildanimation.gui.swing_utils import fakestr

class Ui_RenderSubmitDialog(object):
    def setupUi(self, RenderSubmitDialog):
        if not RenderSubmitDialog.objectName():
            RenderSubmitDialog.setObjectName(u"RenderSubmitDialog")
        RenderSubmitDialog.setWindowModality(Qt.ApplicationModal)
        RenderSubmitDialog.setEnabled(True)
        RenderSubmitDialog.resize(449, 489)
        RenderSubmitDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(RenderSubmitDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayoutEntity = QVBoxLayout()
        self.verticalLayoutEntity.setObjectName(u"verticalLayoutEntity")
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.labelProject = QLabel(RenderSubmitDialog)
        self.labelProject.setObjectName(u"labelProject")
        self.labelProject.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_1.addWidget(self.labelProject)

        self.lineEditProject = QLineEdit(RenderSubmitDialog)
        self.lineEditProject.setObjectName(u"lineEditProject")
        self.lineEditProject.setEnabled(False)

        self.horizontalLayout_1.addWidget(self.lineEditProject)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelEp = QLabel(RenderSubmitDialog)
        self.labelEp.setObjectName(u"labelEp")
        self.labelEp.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.labelEp)

        self.lineEditEpisode = QLineEdit(RenderSubmitDialog)
        self.lineEditEpisode.setObjectName(u"lineEditEpisode")
        self.lineEditEpisode.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEditEpisode)

        self.labelSeq = QLabel(RenderSubmitDialog)
        self.labelSeq.setObjectName(u"labelSeq")

        self.horizontalLayout_4.addWidget(self.labelSeq)

        self.lineEditSequence = QLineEdit(RenderSubmitDialog)
        self.lineEditSequence.setObjectName(u"lineEditSequence")
        self.lineEditSequence.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEditSequence)

        self.labelShot = QLabel(RenderSubmitDialog)
        self.labelShot.setObjectName(u"labelShot")

        self.horizontalLayout_4.addWidget(self.labelShot)

        self.lineEditShot = QLineEdit(RenderSubmitDialog)
        self.lineEditShot.setObjectName(u"lineEditShot")
        self.lineEditShot.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.lineEditShot)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.labelFrameIn = QLabel(RenderSubmitDialog)
        self.labelFrameIn.setObjectName(u"labelFrameIn")
        self.labelFrameIn.setMinimumSize(QSize(100, 0))
        self.labelFrameIn.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.labelFrameIn)

        self.lineEditFrameIn = QLineEdit(RenderSubmitDialog)
        self.lineEditFrameIn.setObjectName(u"lineEditFrameIn")
        self.lineEditFrameIn.setEnabled(False)
        self.lineEditFrameIn.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEditFrameIn)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelFrameOut = QLabel(RenderSubmitDialog)
        self.labelFrameOut.setObjectName(u"labelFrameOut")
        self.labelFrameOut.setMinimumSize(QSize(100, 0))
        self.labelFrameOut.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.labelFrameOut)

        self.lineEditFrameOut = QLineEdit(RenderSubmitDialog)
        self.lineEditFrameOut.setObjectName(u"lineEditFrameOut")
        self.lineEditFrameOut.setEnabled(False)
        self.lineEditFrameOut.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_6.addWidget(self.lineEditFrameOut)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelFrameCount = QLabel(RenderSubmitDialog)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setMinimumSize(QSize(100, 0))
        self.labelFrameCount.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.labelFrameCount)

        self.lineEditFrameCount = QLineEdit(RenderSubmitDialog)
        self.lineEditFrameCount.setObjectName(u"lineEditFrameCount")
        self.lineEditFrameCount.setEnabled(False)
        self.lineEditFrameCount.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_5.addWidget(self.lineEditFrameCount)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelRenderPath = QLabel(RenderSubmitDialog)
        self.labelRenderPath.setObjectName(u"labelRenderPath")
        self.labelRenderPath.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.labelRenderPath)

        self.lineEditRenderPath = QLineEdit(RenderSubmitDialog)
        self.lineEditRenderPath.setObjectName(u"lineEditRenderPath")

        self.horizontalLayout_2.addWidget(self.lineEditRenderPath)

        self.toolButtonSelectPath = QToolButton(RenderSubmitDialog)
        self.toolButtonSelectPath.setObjectName(u"toolButtonSelectPath")

        self.horizontalLayout_2.addWidget(self.toolButtonSelectPath)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelArchiveName = QLabel(RenderSubmitDialog)
        self.labelArchiveName.setObjectName(u"labelArchiveName")
        self.labelArchiveName.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.labelArchiveName)

        self.lineEditArchiveName = QLineEdit(RenderSubmitDialog)
        self.lineEditArchiveName.setObjectName(u"lineEditArchiveName")

        self.horizontalLayout_3.addWidget(self.lineEditArchiveName)


        self.verticalLayoutEntity.addLayout(self.horizontalLayout_3)

        self.verticalLayoutEntityInfo = QVBoxLayout()
        self.verticalLayoutEntityInfo.setObjectName(u"verticalLayoutEntityInfo")
        self.labelNotes = QLabel(RenderSubmitDialog)
        self.labelNotes.setObjectName(u"labelNotes")

        self.verticalLayoutEntityInfo.addWidget(self.labelNotes)

        self.textEditNotes = QTextEdit(RenderSubmitDialog)
        self.textEditNotes.setObjectName(u"textEditNotes")
        self.textEditNotes.setReadOnly(False)

        self.verticalLayoutEntityInfo.addWidget(self.textEditNotes)


        self.verticalLayoutEntity.addLayout(self.verticalLayoutEntityInfo)


        self.verticalLayout.addLayout(self.verticalLayoutEntity)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelStatus = QLabel(RenderSubmitDialog)
        self.labelStatus.setObjectName(u"labelStatus")

        self.horizontalLayout.addWidget(self.labelStatus)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonGo = QPushButton(RenderSubmitDialog)
        self.pushButtonGo.setObjectName(u"pushButtonGo")

        self.horizontalLayout.addWidget(self.pushButtonGo)

        self.pushButtonCancel = QPushButton(RenderSubmitDialog)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(RenderSubmitDialog)

        QMetaObject.connectSlotsByName(RenderSubmitDialog)
    # setupUi

    def retranslateUi(self, RenderSubmitDialog):
        RenderSubmitDialog.setWindowTitle(fakestr(u"swing: render submit", None))
        self.labelProject.setText(fakestr(u"Project:", None))
        self.labelEp.setText(fakestr(u"Episode:", None))
        self.labelSeq.setText(fakestr(u"Sequence:", None))
        self.labelShot.setText(fakestr(u"Shot:", None))
        self.labelFrameIn.setText(fakestr(u"Frame In", None))
        self.labelFrameOut.setText(fakestr(u"Frame Out", None))
        self.labelFrameCount.setText(fakestr(u"Frame Count", None))
        self.labelRenderPath.setText(fakestr(u"Render Path", None))
        self.toolButtonSelectPath.setText(fakestr(u"...", None))
        self.labelArchiveName.setText(fakestr(u"Archive Name", None))
        self.labelNotes.setText(fakestr(u"Notes and Comments", None))
        self.labelStatus.setText("")
        self.pushButtonGo.setText(fakestr(u"Go", None))
        self.pushButtonCancel.setText(fakestr(u"Close", None))
    # retranslateUi

