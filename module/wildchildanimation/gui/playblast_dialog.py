# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playblast_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PlayblastDialog(object):
    def setupUi(self, PlayblastDialog):
        if not PlayblastDialog.objectName():
            PlayblastDialog.setObjectName(u"PlayblastDialog")
        PlayblastDialog.resize(420, 453)
        self.verticalLayout_3 = QVBoxLayout(PlayblastDialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayoutProjectFile = QHBoxLayout()
        self.horizontalLayoutProjectFile.setObjectName(u"horizontalLayoutProjectFile")
        self.projectFileLabel = QLabel(PlayblastDialog)
        self.projectFileLabel.setObjectName(u"projectFileLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectFileLabel.sizePolicy().hasHeightForWidth())
        self.projectFileLabel.setSizePolicy(sizePolicy)
        self.projectFileLabel.setMinimumSize(QSize(80, 0))
        self.projectFileLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayoutProjectFile.addWidget(self.projectFileLabel)

        self.output_dir_path_le = QLineEdit(PlayblastDialog)
        self.output_dir_path_le.setObjectName(u"output_dir_path_le")

        self.horizontalLayoutProjectFile.addWidget(self.output_dir_path_le)

        self.output_dir_path_select_btn = QToolButton(PlayblastDialog)
        self.output_dir_path_select_btn.setObjectName(u"output_dir_path_select_btn")
        self.output_dir_path_select_btn.setMinimumSize(QSize(40, 0))
        self.output_dir_path_select_btn.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile.addWidget(self.output_dir_path_select_btn)

        self.output_dir_path_show_folder_btn = QPushButton(PlayblastDialog)
        self.output_dir_path_show_folder_btn.setObjectName(u"output_dir_path_show_folder_btn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.output_dir_path_show_folder_btn.sizePolicy().hasHeightForWidth())
        self.output_dir_path_show_folder_btn.setSizePolicy(sizePolicy1)
        self.output_dir_path_show_folder_btn.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayoutProjectFile.addWidget(self.output_dir_path_show_folder_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProjectFile)

        self.horizontalLayoutProjectFile_2 = QHBoxLayout()
        self.horizontalLayoutProjectFile_2.setObjectName(u"horizontalLayoutProjectFile_2")
        self.fbxFileLabel = QLabel(PlayblastDialog)
        self.fbxFileLabel.setObjectName(u"fbxFileLabel")
        sizePolicy.setHeightForWidth(self.fbxFileLabel.sizePolicy().hasHeightForWidth())
        self.fbxFileLabel.setSizePolicy(sizePolicy)
        self.fbxFileLabel.setMinimumSize(QSize(80, 0))
        self.fbxFileLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayoutProjectFile_2.addWidget(self.fbxFileLabel)

        self.output_filename_le = QLineEdit(PlayblastDialog)
        self.output_filename_le.setObjectName(u"output_filename_le")

        self.horizontalLayoutProjectFile_2.addWidget(self.output_filename_le)

        self.force_overwrite_cb = QCheckBox(PlayblastDialog)
        self.force_overwrite_cb.setObjectName(u"force_overwrite_cb")

        self.horizontalLayoutProjectFile_2.addWidget(self.force_overwrite_cb)

        self.fbxFileToolButton = QToolButton(PlayblastDialog)
        self.fbxFileToolButton.setObjectName(u"fbxFileToolButton")
        self.fbxFileToolButton.setMinimumSize(QSize(40, 0))
        self.fbxFileToolButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayoutProjectFile_2.addWidget(self.fbxFileToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayoutProjectFile_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(PlayblastDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(PlayblastDialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(80, 0))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.camera_select_cmb = QComboBox(PlayblastDialog)
        self.camera_select_cmb.setObjectName(u"camera_select_cmb")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.camera_select_cmb.sizePolicy().hasHeightForWidth())
        self.camera_select_cmb.setSizePolicy(sizePolicy2)
        self.camera_select_cmb.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_2.addWidget(self.camera_select_cmb)

        self.camera_select_hide_defaults_cb = QCheckBox(PlayblastDialog)
        self.camera_select_hide_defaults_cb.setObjectName(u"camera_select_hide_defaults_cb")

        self.horizontalLayout_2.addWidget(self.camera_select_hide_defaults_cb)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(PlayblastDialog)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(80, 0))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.resolution_select_cmb = QComboBox(PlayblastDialog)
        self.resolution_select_cmb.setObjectName(u"resolution_select_cmb")
        sizePolicy2.setHeightForWidth(self.resolution_select_cmb.sizePolicy().hasHeightForWidth())
        self.resolution_select_cmb.setSizePolicy(sizePolicy2)
        self.resolution_select_cmb.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.resolution_select_cmb)

        self.resolution_width_sb = QSpinBox(PlayblastDialog)
        self.resolution_width_sb.setObjectName(u"resolution_width_sb")
        self.resolution_width_sb.setFrame(True)
        self.resolution_width_sb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.resolution_width_sb.setMinimum(1)
        self.resolution_width_sb.setMaximum(9999)

        self.horizontalLayout_3.addWidget(self.resolution_width_sb)

        self.label_7 = QLabel(PlayblastDialog)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)
        self.label_7.setMaximumSize(QSize(16, 16777215))
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.resolution_height_sb = QSpinBox(PlayblastDialog)
        self.resolution_height_sb.setObjectName(u"resolution_height_sb")
        self.resolution_height_sb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.resolution_height_sb.setMinimum(1)
        self.resolution_height_sb.setMaximum(9999)

        self.horizontalLayout_3.addWidget(self.resolution_height_sb)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(PlayblastDialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(80, 0))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.frame_range_cmb = QComboBox(PlayblastDialog)
        self.frame_range_cmb.setObjectName(u"frame_range_cmb")
        sizePolicy2.setHeightForWidth(self.frame_range_cmb.sizePolicy().hasHeightForWidth())
        self.frame_range_cmb.setSizePolicy(sizePolicy2)
        self.frame_range_cmb.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.frame_range_cmb)

        self.frame_range_start_sb = QSpinBox(PlayblastDialog)
        self.frame_range_start_sb.setObjectName(u"frame_range_start_sb")
        self.frame_range_start_sb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.frame_range_start_sb.setMinimum(-9999)
        self.frame_range_start_sb.setMaximum(9999)

        self.horizontalLayout_4.addWidget(self.frame_range_start_sb)

        self.label_8 = QLabel(PlayblastDialog)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        self.label_8.setMaximumSize(QSize(16, 16777215))
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.frame_range_end_sb = QSpinBox(PlayblastDialog)
        self.frame_range_end_sb.setObjectName(u"frame_range_end_sb")
        self.frame_range_end_sb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.frame_range_end_sb.setMinimum(-9999)
        self.frame_range_end_sb.setMaximum(9999)

        self.horizontalLayout_4.addWidget(self.frame_range_end_sb)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(PlayblastDialog)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QSize(80, 0))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.encoding_container_cmb = QComboBox(PlayblastDialog)
        self.encoding_container_cmb.setObjectName(u"encoding_container_cmb")
        sizePolicy2.setHeightForWidth(self.encoding_container_cmb.sizePolicy().hasHeightForWidth())
        self.encoding_container_cmb.setSizePolicy(sizePolicy2)
        self.encoding_container_cmb.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_5.addWidget(self.encoding_container_cmb)

        self.encoding_video_codec_cmb = QComboBox(PlayblastDialog)
        self.encoding_video_codec_cmb.setObjectName(u"encoding_video_codec_cmb")
        sizePolicy2.setHeightForWidth(self.encoding_video_codec_cmb.sizePolicy().hasHeightForWidth())
        self.encoding_video_codec_cmb.setSizePolicy(sizePolicy2)
        self.encoding_video_codec_cmb.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_5.addWidget(self.encoding_video_codec_cmb)

        self.encoding_video_codec_settings_btn = QPushButton(PlayblastDialog)
        self.encoding_video_codec_settings_btn.setObjectName(u"encoding_video_codec_settings_btn")

        self.horizontalLayout_5.addWidget(self.encoding_video_codec_settings_btn)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(PlayblastDialog)
        self.label_6.setObjectName(u"label_6")
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QSize(80, 0))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.visibility_cmb = QComboBox(PlayblastDialog)
        self.visibility_cmb.setObjectName(u"visibility_cmb")
        sizePolicy2.setHeightForWidth(self.visibility_cmb.sizePolicy().hasHeightForWidth())
        self.visibility_cmb.setSizePolicy(sizePolicy2)
        self.visibility_cmb.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_6.addWidget(self.visibility_cmb)

        self.visibility_customize_btn = QPushButton(PlayblastDialog)
        self.visibility_customize_btn.setObjectName(u"visibility_customize_btn")

        self.horizontalLayout_6.addWidget(self.visibility_customize_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.ornaments_cb = QCheckBox(PlayblastDialog)
        self.ornaments_cb.setObjectName(u"ornaments_cb")
        sizePolicy2.setHeightForWidth(self.ornaments_cb.sizePolicy().hasHeightForWidth())
        self.ornaments_cb.setSizePolicy(sizePolicy2)
        self.ornaments_cb.setMinimumSize(QSize(100, 0))
        self.ornaments_cb.setChecked(True)

        self.verticalLayout.addWidget(self.ornaments_cb)

        self.viewer_cb = QCheckBox(PlayblastDialog)
        self.viewer_cb.setObjectName(u"viewer_cb")
        sizePolicy2.setHeightForWidth(self.viewer_cb.sizePolicy().hasHeightForWidth())
        self.viewer_cb.setSizePolicy(sizePolicy2)
        self.viewer_cb.setMinimumSize(QSize(100, 0))
        self.viewer_cb.setChecked(True)

        self.verticalLayout.addWidget(self.viewer_cb)

        self.output_edit = QPlainTextEdit(PlayblastDialog)
        self.output_edit.setObjectName(u"output_edit")

        self.verticalLayout.addWidget(self.output_edit)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.refresh_btn = QPushButton(PlayblastDialog)
        self.refresh_btn.setObjectName(u"refresh_btn")

        self.horizontalLayout.addWidget(self.refresh_btn)

        self.clear_btn = QPushButton(PlayblastDialog)
        self.clear_btn.setObjectName(u"clear_btn")

        self.horizontalLayout.addWidget(self.clear_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.playblast_btn = QPushButton(PlayblastDialog)
        self.playblast_btn.setObjectName(u"playblast_btn")

        self.horizontalLayout.addWidget(self.playblast_btn)

        self.close_btn = QPushButton(PlayblastDialog)
        self.close_btn.setObjectName(u"close_btn")

        self.horizontalLayout.addWidget(self.close_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(PlayblastDialog)

        self.playblast_btn.setDefault(True)


        QMetaObject.connectSlotsByName(PlayblastDialog)
    # setupUi

    def retranslateUi(self, PlayblastDialog):
        PlayblastDialog.setWindowTitle(QCoreApplication.translate("PlayblastDialog", u"Publish Asset for Task", None))
        self.projectFileLabel.setText(QCoreApplication.translate("PlayblastDialog", u"Directory:", None))
        self.output_dir_path_le.setText(QCoreApplication.translate("PlayblastDialog", u"{project}/movies", None))
#if QT_CONFIG(tooltip)
        self.output_dir_path_select_btn.setToolTip(QCoreApplication.translate("PlayblastDialog", u"Select Output Directory", None))
#endif // QT_CONFIG(tooltip)
        self.output_dir_path_select_btn.setText(QCoreApplication.translate("PlayblastDialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.output_dir_path_show_folder_btn.setToolTip(QCoreApplication.translate("PlayblastDialog", u"Show in Folder", None))
#endif // QT_CONFIG(tooltip)
        self.output_dir_path_show_folder_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Go", None))
        self.fbxFileLabel.setText(QCoreApplication.translate("PlayblastDialog", u"Filename", None))
        self.output_filename_le.setText(QCoreApplication.translate("PlayblastDialog", u"{scene}", None))
        self.force_overwrite_cb.setText(QCoreApplication.translate("PlayblastDialog", u"Force overwrite", None))
        self.fbxFileToolButton.setText(QCoreApplication.translate("PlayblastDialog", u"...", None))
        self.label.setText(QCoreApplication.translate("PlayblastDialog", u"Options", None))
        self.label_2.setText(QCoreApplication.translate("PlayblastDialog", u"Camera:", None))
        self.camera_select_hide_defaults_cb.setText(QCoreApplication.translate("PlayblastDialog", u"Hide defaults", None))
        self.label_3.setText(QCoreApplication.translate("PlayblastDialog", u"Resolution:", None))
        self.label_7.setText(QCoreApplication.translate("PlayblastDialog", u" x ", None))
        self.label_4.setText(QCoreApplication.translate("PlayblastDialog", u"Frame Range:", None))
        self.label_8.setText(QCoreApplication.translate("PlayblastDialog", u" - ", None))
        self.label_5.setText(QCoreApplication.translate("PlayblastDialog", u"Encoding:", None))
        self.encoding_video_codec_settings_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Settings ...", None))
        self.label_6.setText(QCoreApplication.translate("PlayblastDialog", u"Visibility:", None))
        self.visibility_customize_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Customise ...", None))
        self.ornaments_cb.setText(QCoreApplication.translate("PlayblastDialog", u"Ornaments", None))
        self.viewer_cb.setText(QCoreApplication.translate("PlayblastDialog", u"Show in Viewer", None))
        self.refresh_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Refresh", None))
        self.clear_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Clear", None))
        self.playblast_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Playblast", None))
        self.close_btn.setText(QCoreApplication.translate("PlayblastDialog", u"Close", None))
    # retranslateUi

