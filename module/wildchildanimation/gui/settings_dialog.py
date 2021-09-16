# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr
class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.setWindowModality(Qt.ApplicationModal)
        SettingsDialog.resize(361, 478)
        SettingsDialog.setFocusPolicy(Qt.StrongFocus)
        SettingsDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTreeHouse = QLabel(SettingsDialog)
        self.labelTreeHouse.setObjectName(u"labelTreeHouse")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTreeHouse.setFont(font)

        self.verticalLayout.addWidget(self.labelTreeHouse)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelServer = QLabel(SettingsDialog)
        self.labelServer.setObjectName(u"labelServer")
        self.labelServer.setMinimumSize(QSize(120, 0))

        self.horizontalLayout.addWidget(self.labelServer)

        self.lineEditServer = QLineEdit(SettingsDialog)
        self.lineEditServer.setObjectName(u"lineEditServer")

        self.horizontalLayout.addWidget(self.lineEditServer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelEmail = QLabel(SettingsDialog)
        self.labelEmail.setObjectName(u"labelEmail")
        self.labelEmail.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_2.addWidget(self.labelEmail)

        self.lineEditEmail = QLineEdit(SettingsDialog)
        self.lineEditEmail.setObjectName(u"lineEditEmail")

        self.horizontalLayout_2.addWidget(self.lineEditEmail)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelPassword = QLabel(SettingsDialog)
        self.labelPassword.setObjectName(u"labelPassword")
        self.labelPassword.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_3.addWidget(self.labelPassword)

        self.lineEditPassword = QLineEdit(SettingsDialog)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.lineEditPassword)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_10 = QLabel(SettingsDialog)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.verticalLayout.addWidget(self.label_10)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labelProjectsFolder = QLabel(SettingsDialog)
        self.labelProjectsFolder.setObjectName(u"labelProjectsFolder")
        self.labelProjectsFolder.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_4.addWidget(self.labelProjectsFolder)

        self.lineEditProjectsFolder = QLineEdit(SettingsDialog)
        self.lineEditProjectsFolder.setObjectName(u"lineEditProjectsFolder")

        self.horizontalLayout_4.addWidget(self.lineEditProjectsFolder)

        self.toolButtonProjectsFolder = QToolButton(SettingsDialog)
        self.toolButtonProjectsFolder.setObjectName(u"toolButtonProjectsFolder")

        self.horizontalLayout_4.addWidget(self.toolButtonProjectsFolder)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_14 = QLabel(SettingsDialog)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.verticalLayout.addWidget(self.label_14)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.labelEditorialFolder = QLabel(SettingsDialog)
        self.labelEditorialFolder.setObjectName(u"labelEditorialFolder")
        self.labelEditorialFolder.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_9.addWidget(self.labelEditorialFolder)

        self.lineEditEditorialFolder = QLineEdit(SettingsDialog)
        self.lineEditEditorialFolder.setObjectName(u"lineEditEditorialFolder")

        self.horizontalLayout_9.addWidget(self.lineEditEditorialFolder)

        self.toolButtonEditorialFolder = QToolButton(SettingsDialog)
        self.toolButtonEditorialFolder.setObjectName(u"toolButtonEditorialFolder")

        self.horizontalLayout_9.addWidget(self.toolButtonEditorialFolder)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_3 = QSpacerItem(20, 6, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_6 = QLabel(SettingsDialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.verticalLayout.addWidget(self.label_6)

        self.labelFfmpeg = QLabel(SettingsDialog)
        self.labelFfmpeg.setObjectName(u"labelFfmpeg")

        self.verticalLayout.addWidget(self.labelFfmpeg)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelFfmpegBin = QLabel(SettingsDialog)
        self.labelFfmpegBin.setObjectName(u"labelFfmpegBin")
        self.labelFfmpegBin.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_5.addWidget(self.labelFfmpegBin)

        self.lineEditFfmpegBin = QLineEdit(SettingsDialog)
        self.lineEditFfmpegBin.setObjectName(u"lineEditFfmpegBin")

        self.horizontalLayout_5.addWidget(self.lineEditFfmpegBin)

        self.toolButtonFfmpegBin = QToolButton(SettingsDialog)
        self.toolButtonFfmpegBin.setObjectName(u"toolButtonFfmpegBin")

        self.horizontalLayout_5.addWidget(self.toolButtonFfmpegBin)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelFfprobeBin = QLabel(SettingsDialog)
        self.labelFfprobeBin.setObjectName(u"labelFfprobeBin")
        self.labelFfprobeBin.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_6.addWidget(self.labelFfprobeBin)

        self.lineEditFfprobeBin = QLineEdit(SettingsDialog)
        self.lineEditFfprobeBin.setObjectName(u"lineEditFfprobeBin")

        self.horizontalLayout_6.addWidget(self.lineEditFfprobeBin)

        self.toolButtonFfprobeBin = QToolButton(SettingsDialog)
        self.toolButtonFfprobeBin.setObjectName(u"toolButtonFfprobeBin")

        self.horizontalLayout_6.addWidget(self.toolButtonFfprobeBin)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.label7Zip = QLabel(SettingsDialog)
        self.label7Zip.setObjectName(u"label7Zip")

        self.verticalLayout.addWidget(self.label7Zip)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label7ZipBin = QLabel(SettingsDialog)
        self.label7ZipBin.setObjectName(u"label7ZipBin")
        self.label7ZipBin.setMinimumSize(QSize(120, 0))

        self.horizontalLayout_7.addWidget(self.label7ZipBin)

        self.lineEdit7zBinary = QLineEdit(SettingsDialog)
        self.lineEdit7zBinary.setObjectName(u"lineEdit7zBinary")

        self.horizontalLayout_7.addWidget(self.lineEdit7zBinary)

        self.toolButton7zSelect = QToolButton(SettingsDialog)
        self.toolButton7zSelect.setObjectName(u"toolButton7zSelect")

        self.horizontalLayout_7.addWidget(self.toolButton7zSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.labelIntegrations = QLabel(SettingsDialog)
        self.labelIntegrations.setObjectName(u"labelIntegrations")
        self.labelIntegrations.setFont(font)

        self.verticalLayout.addWidget(self.labelIntegrations)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButtonShortcut = QPushButton(SettingsDialog)
        self.pushButtonShortcut.setObjectName(u"pushButtonShortcut")

        self.horizontalLayout_8.addWidget(self.pushButtonShortcut)

        self.labelDesktopShortCut = QLabel(SettingsDialog)
        self.labelDesktopShortCut.setObjectName(u"labelDesktopShortCut")

        self.horizontalLayout_8.addWidget(self.labelDesktopShortCut)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(fakestr(u"Swing: Application Settings", None))
        self.labelTreeHouse.setText(fakestr(u"Treehouse:", None))
        self.labelServer.setText(fakestr(u"Server", None))
#if QT_CONFIG(tooltip)
        self.lineEditServer.setToolTip(fakestr(u"Server URL - https://example.wildchildanimation.com", None))
#endif // QT_CONFIG(tooltip)
        self.labelEmail.setText(fakestr(u"Email", None))
#if QT_CONFIG(tooltip)
        self.lineEditEmail.setToolTip(fakestr(u"Logon email address", None))
#endif // QT_CONFIG(tooltip)
        self.labelPassword.setText(fakestr(u"Password", None))
#if QT_CONFIG(tooltip)
        self.lineEditPassword.setToolTip(fakestr(u"Logon password", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(fakestr(u"Storage:", None))
        self.labelProjectsFolder.setText(fakestr(u"Projects Folder", None))
#if QT_CONFIG(tooltip)
        self.lineEditProjectsFolder.setToolTip(fakestr(u"<html><head/><body><p>Root directory for projects</p><p><br/></p><p>Shots will be downloaded to:</p><p><span style=\" font-weight:600;\">root/project/assets</span></p><p><br/></p><p>Assets will be downloaded to: </p><p><span style=\" font-weight:600;\">root/project/assets</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonProjectsFolder.setText(fakestr(u"...", None))
        self.label_14.setText(fakestr(u"Playlist", None))
        self.labelEditorialFolder.setText(fakestr(u"Editorial Folder", None))
#if QT_CONFIG(tooltip)
        self.lineEditEditorialFolder.setToolTip(fakestr(u"<html><head/><body><p>Root directory for projects</p><p><br/></p><p>Shots will be downloaded to:</p><p><span style=\" font-weight:600;\">root/project/assets</span></p><p><br/></p><p>Assets will be downloaded to: </p><p><span style=\" font-weight:600;\">root/project/assets</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonEditorialFolder.setText(fakestr(u"...", None))
        self.label_6.setText(fakestr(u"Applications:", None))
        self.labelFfmpeg.setText(fakestr(u"ffmpeg - video encoding", None))
        self.labelFfmpegBin.setText(fakestr(u"ffmpeg binary", None))
#if QT_CONFIG(tooltip)
        self.lineEditFfmpegBin.setToolTip(fakestr(u"<html><head/><body><p>Location of ffmpeg executable, usually something like </p><p><br/></p><p>C:\\ffmpeg\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg.exe</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonFfmpegBin.setText(fakestr(u"...", None))
        self.labelFfprobeBin.setText(fakestr(u"ffprobe binary", None))
#if QT_CONFIG(tooltip)
        self.lineEditFfprobeBin.setToolTip(fakestr(u"<html><head/><body><p>Location of ffmpeg executable, usually something like </p><p><br/></p><p>C:\\ffmpeg\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg.exe</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonFfprobeBin.setText(fakestr(u"...", None))
        self.label7Zip.setText(fakestr(u"7zip - compress and extract archive", None))
        self.label7ZipBin.setText(fakestr(u"7zip binary", None))
#if QT_CONFIG(tooltip)
        self.lineEdit7zBinary.setToolTip(fakestr(u"<html><head/><body><p>Location of ffmpeg executable, usually something like </p><p><br/></p><p>C:\\ffmpeg\\ffmpeg-20200831-4a11a6f-win64-static\\bin\\ffmpeg.exe</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton7zSelect.setText(fakestr(u"...", None))
        self.labelIntegrations.setText(fakestr(u"Integrations:", None))
        self.pushButtonShortcut.setText(fakestr(u"Desktop Shortcut", None))
        self.labelDesktopShortCut.setText(fakestr(u"Creates a new desktop shortcut", None))
    # retranslateUi

