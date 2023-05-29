# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'asset_toolkit_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_AssetToolkit(object):
    def setupUi(self, AssetToolkit):
        if not AssetToolkit.objectName():
            AssetToolkit.setObjectName(u"AssetToolkit")
        AssetToolkit.resize(808, 553)
        self.centralwidget = QWidget(AssetToolkit)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tab_window = QTabWidget(self.centralwidget)
        self.tab_window.setObjectName(u"tab_window")
        self.tab_window.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_window.sizePolicy().hasHeightForWidth())
        self.tab_window.setSizePolicy(sizePolicy)
        self.tab_window.setTabShape(QTabWidget.Rounded)
        self.modelling_tab = QWidget()
        self.modelling_tab.setObjectName(u"modelling_tab")
        sizePolicy.setHeightForWidth(self.modelling_tab.sizePolicy().hasHeightForWidth())
        self.modelling_tab.setSizePolicy(sizePolicy)
        self.modelling_tab.setAutoFillBackground(True)
        self.horizontalLayout_3 = QHBoxLayout(self.modelling_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_32 = QVBoxLayout()
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.groupBox_4 = QGroupBox(self.modelling_tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.meshFrame = QFrame(self.groupBox_4)
        self.meshFrame.setObjectName(u"meshFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.meshFrame.sizePolicy().hasHeightForWidth())
        self.meshFrame.setSizePolicy(sizePolicy1)
        self.horizontalLayout_5 = QHBoxLayout(self.meshFrame)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.cb_triangles = QCheckBox(self.meshFrame)
        self.cb_triangles.setObjectName(u"cb_triangles")
        self.cb_triangles.setChecked(False)

        self.verticalLayout_12.addWidget(self.cb_triangles)

        self.cb_ngons = QCheckBox(self.meshFrame)
        self.cb_ngons.setObjectName(u"cb_ngons")
        self.cb_ngons.setChecked(True)

        self.verticalLayout_12.addWidget(self.cb_ngons)

        self.cb_non_quads = QCheckBox(self.meshFrame)
        self.cb_non_quads.setObjectName(u"cb_non_quads")
        self.cb_non_quads.setChecked(False)

        self.verticalLayout_12.addWidget(self.cb_non_quads)


        self.horizontalLayout_5.addLayout(self.verticalLayout_12)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(10)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.cb_non_manifold = QCheckBox(self.meshFrame)
        self.cb_non_manifold.setObjectName(u"cb_non_manifold")
        self.cb_non_manifold.setChecked(True)

        self.verticalLayout_11.addWidget(self.cb_non_manifold)

        self.cb_lamina = QCheckBox(self.meshFrame)
        self.cb_lamina.setObjectName(u"cb_lamina")
        self.cb_lamina.setChecked(True)

        self.verticalLayout_11.addWidget(self.cb_lamina)


        self.horizontalLayout_5.addLayout(self.verticalLayout_11)


        self.verticalLayout_15.addWidget(self.meshFrame)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_mesh_check = QPushButton(self.groupBox_4)
        self.btn_mesh_check.setObjectName(u"btn_mesh_check")

        self.horizontalLayout_6.addWidget(self.btn_mesh_check)

        self.btn_mesh_refresh = QPushButton(self.groupBox_4)
        self.btn_mesh_refresh.setObjectName(u"btn_mesh_refresh")

        self.horizontalLayout_6.addWidget(self.btn_mesh_refresh)


        self.verticalLayout_15.addLayout(self.horizontalLayout_6)

        self.groupBox_5 = QGroupBox(self.groupBox_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy2)
        self.groupBox_5.setMinimumSize(QSize(0, 250))
        self.horizontalLayout = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.btn_optimize = QPushButton(self.groupBox_5)
        self.btn_optimize.setObjectName(u"btn_optimize")

        self.verticalLayout_14.addWidget(self.btn_optimize)

        self.btn_delete_history = QPushButton(self.groupBox_5)
        self.btn_delete_history.setObjectName(u"btn_delete_history")

        self.verticalLayout_14.addWidget(self.btn_delete_history)

        self.btn_center_pivots = QPushButton(self.groupBox_5)
        self.btn_center_pivots.setObjectName(u"btn_center_pivots")

        self.verticalLayout_14.addWidget(self.btn_center_pivots)

        self.btn_freeze_transforms = QPushButton(self.groupBox_5)
        self.btn_freeze_transforms.setObjectName(u"btn_freeze_transforms")

        self.verticalLayout_14.addWidget(self.btn_freeze_transforms)

        self.btn_copypivot = QPushButton(self.groupBox_5)
        self.btn_copypivot.setObjectName(u"btn_copypivot")

        self.verticalLayout_14.addWidget(self.btn_copypivot)

        self.btn_matchtransforms = QPushButton(self.groupBox_5)
        self.btn_matchtransforms.setObjectName(u"btn_matchtransforms")

        self.verticalLayout_14.addWidget(self.btn_matchtransforms)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_5)


        self.horizontalLayout.addLayout(self.verticalLayout_14)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.btn_unlock_normals = QPushButton(self.groupBox_5)
        self.btn_unlock_normals.setObjectName(u"btn_unlock_normals")

        self.verticalLayout_13.addWidget(self.btn_unlock_normals)

        self.btn_merge_uvs = QPushButton(self.groupBox_5)
        self.btn_merge_uvs.setObjectName(u"btn_merge_uvs")

        self.verticalLayout_13.addWidget(self.btn_merge_uvs)

        self.btn_initial_shader = QPushButton(self.groupBox_5)
        self.btn_initial_shader.setObjectName(u"btn_initial_shader")

        self.verticalLayout_13.addWidget(self.btn_initial_shader)

        self.btn_min_pivot = QPushButton(self.groupBox_5)
        self.btn_min_pivot.setObjectName(u"btn_min_pivot")

        self.verticalLayout_13.addWidget(self.btn_min_pivot)

        self.btn_rev_sides = QPushButton(self.groupBox_5)
        self.btn_rev_sides.setObjectName(u"btn_rev_sides")

        self.verticalLayout_13.addWidget(self.btn_rev_sides)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout_13)


        self.verticalLayout_15.addWidget(self.groupBox_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer)


        self.verticalLayout_32.addWidget(self.groupBox_4)


        self.horizontalLayout_3.addLayout(self.verticalLayout_32)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.modellingFrameResults = QFrame(self.modelling_tab)
        self.modellingFrameResults.setObjectName(u"modellingFrameResults")
        sizePolicy.setHeightForWidth(self.modellingFrameResults.sizePolicy().hasHeightForWidth())
        self.modellingFrameResults.setSizePolicy(sizePolicy)
        self.verticalLayout_9 = QVBoxLayout(self.modellingFrameResults)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_9.setContentsMargins(10, 10, 10, 10)
        self.tview_mesh_check = QTreeWidget(self.modellingFrameResults)
        self.tview_mesh_check.setObjectName(u"tview_mesh_check")

        self.verticalLayout_9.addWidget(self.tview_mesh_check)

        self.horizontalSpacer_3 = QSpacerItem(40, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_9.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_14.addWidget(self.modellingFrameResults)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_14)

        self.tab_window.addTab(self.modelling_tab, "")
        self.naming_tab = QWidget()
        self.naming_tab.setObjectName(u"naming_tab")
        self.naming_tab.setAutoFillBackground(True)
        self.horizontalLayout_2 = QHBoxLayout(self.naming_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.namingFrame = QFrame(self.naming_tab)
        self.namingFrame.setObjectName(u"namingFrame")
        sizePolicy.setHeightForWidth(self.namingFrame.sizePolicy().hasHeightForWidth())
        self.namingFrame.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QVBoxLayout(self.namingFrame)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.groupBox_6 = QGroupBox(self.namingFrame)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_19 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.rbtn_rename = QRadioButton(self.groupBox_6)
        self.rbtn_rename.setObjectName(u"rbtn_rename")
        self.rbtn_rename.setMinimumSize(QSize(0, 0))

        self.verticalLayout_19.addWidget(self.rbtn_rename)

        self.txt_rename = QLineEdit(self.groupBox_6)
        self.txt_rename.setObjectName(u"txt_rename")
        sizePolicy1.setHeightForWidth(self.txt_rename.sizePolicy().hasHeightForWidth())
        self.txt_rename.setSizePolicy(sizePolicy1)
        self.txt_rename.setInputMethodHints(Qt.ImhLowercaseOnly)

        self.verticalLayout_19.addWidget(self.txt_rename)

        self.btn_rename = QPushButton(self.groupBox_6)
        self.btn_rename.setObjectName(u"btn_rename")
        self.btn_rename.setMaximumSize(QSize(3000, 16777215))

        self.verticalLayout_19.addWidget(self.btn_rename)


        self.verticalLayout_4.addWidget(self.groupBox_6)

        self.line_4 = QFrame(self.namingFrame)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.groupBox_7 = QGroupBox(self.namingFrame)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.btn_select_objects_with_same_name = QPushButton(self.groupBox_7)
        self.btn_select_objects_with_same_name.setObjectName(u"btn_select_objects_with_same_name")

        self.verticalLayout_20.addWidget(self.btn_select_objects_with_same_name)

        self.btn_select_bad_names = QPushButton(self.groupBox_7)
        self.btn_select_bad_names.setObjectName(u"btn_select_bad_names")

        self.verticalLayout_20.addWidget(self.btn_select_bad_names)

        self.btn_select_bad_structure = QPushButton(self.groupBox_7)
        self.btn_select_bad_structure.setObjectName(u"btn_select_bad_structure")

        self.verticalLayout_20.addWidget(self.btn_select_bad_structure)


        self.verticalLayout_4.addWidget(self.groupBox_7)

        self.btn_append_shader_names = QPushButton(self.namingFrame)
        self.btn_append_shader_names.setObjectName(u"btn_append_shader_names")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_append_shader_names.sizePolicy().hasHeightForWidth())
        self.btn_append_shader_names.setSizePolicy(sizePolicy3)
        self.btn_append_shader_names.setMaximumSize(QSize(3000, 16777215))

        self.verticalLayout_4.addWidget(self.btn_append_shader_names)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)


        self.verticalLayout_6.addWidget(self.namingFrame)


        self.horizontalLayout_2.addLayout(self.verticalLayout_6)

        self.namingFrameResults = QFrame(self.naming_tab)
        self.namingFrameResults.setObjectName(u"namingFrameResults")
        sizePolicy.setHeightForWidth(self.namingFrameResults.sizePolicy().hasHeightForWidth())
        self.namingFrameResults.setSizePolicy(sizePolicy)
        self.namingFrameResults.setFrameShape(QFrame.NoFrame)
        self.namingFrameResults.setFrameShadow(QFrame.Raised)
        self.namingFrameResults.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.namingFrameResults)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.horizontalLayout_2.addWidget(self.namingFrameResults)

        self.tab_window.addTab(self.naming_tab, "")
        self.texturing_tab = QWidget()
        self.texturing_tab.setObjectName(u"texturing_tab")
        self.texturing_tab.setAutoFillBackground(True)
        self.horizontalLayout_4 = QHBoxLayout(self.texturing_tab)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.verticalLayout_33 = QVBoxLayout()
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.groupBox = QGroupBox(self.texturing_tab)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy4)
        self.groupBox.setMinimumSize(QSize(0, 150))
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.rbtn_subdiv_smooth_all = QRadioButton(self.groupBox)
        self.rbtn_subdiv_smooth_all.setObjectName(u"rbtn_subdiv_smooth_all")
        self.rbtn_subdiv_smooth_all.setChecked(True)

        self.verticalLayout_5.addWidget(self.rbtn_subdiv_smooth_all)

        self.rbtn_subdiv_preserve_borders = QRadioButton(self.groupBox)
        self.rbtn_subdiv_preserve_borders.setObjectName(u"rbtn_subdiv_preserve_borders")

        self.verticalLayout_5.addWidget(self.rbtn_subdiv_preserve_borders)

        self.rbtn_subdiv_no_smoothing = QRadioButton(self.groupBox)
        self.rbtn_subdiv_no_smoothing.setObjectName(u"rbtn_subdiv_no_smoothing")

        self.verticalLayout_5.addWidget(self.rbtn_subdiv_no_smoothing)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.btn_add_subdivs = QPushButton(self.groupBox)
        self.btn_add_subdivs.setObjectName(u"btn_add_subdivs")

        self.horizontalLayout_9.addWidget(self.btn_add_subdivs)

        self.btn_remove_subdivs = QPushButton(self.groupBox)
        self.btn_remove_subdivs.setObjectName(u"btn_remove_subdivs")

        self.horizontalLayout_9.addWidget(self.btn_remove_subdivs)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.verticalLayout_33.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.texturing_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy4.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy4)
        self.groupBox_3.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_21 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(10, 10, 10, 10)
        self.frame_6 = QFrame(self.groupBox_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_6)
        self.verticalLayout_18.setSpacing(6)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.btn_bad_shaders = QPushButton(self.frame_6)
        self.btn_bad_shaders.setObjectName(u"btn_bad_shaders")
        sizePolicy1.setHeightForWidth(self.btn_bad_shaders.sizePolicy().hasHeightForWidth())
        self.btn_bad_shaders.setSizePolicy(sizePolicy1)

        self.verticalLayout_18.addWidget(self.btn_bad_shaders)


        self.horizontalLayout_21.addWidget(self.frame_6)

        self.frame_8 = QFrame(self.groupBox_3)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_8)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.btn_rename_file_nodes = QPushButton(self.frame_8)
        self.btn_rename_file_nodes.setObjectName(u"btn_rename_file_nodes")
        sizePolicy1.setHeightForWidth(self.btn_rename_file_nodes.sizePolicy().hasHeightForWidth())
        self.btn_rename_file_nodes.setSizePolicy(sizePolicy1)

        self.verticalLayout_28.addWidget(self.btn_rename_file_nodes)


        self.horizontalLayout_21.addWidget(self.frame_8)


        self.verticalLayout_33.addWidget(self.groupBox_3)

        self.groupBox_9 = QGroupBox(self.texturing_tab)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.horizontalLayout_13 = QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.frame_9 = QFrame(self.groupBox_9)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_9)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.btn_transfer_uv = QPushButton(self.frame_9)
        self.btn_transfer_uv.setObjectName(u"btn_transfer_uv")

        self.verticalLayout_17.addWidget(self.btn_transfer_uv)


        self.horizontalLayout_13.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.groupBox_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_10)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_13.addWidget(self.frame_10)


        self.verticalLayout_33.addWidget(self.groupBox_9)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_3)


        self.horizontalLayout_15.addLayout(self.verticalLayout_33)

        self.groupBox_11 = QGroupBox(self.texturing_tab)
        self.groupBox_11.setObjectName(u"groupBox_11")
        sizePolicy4.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy4)
        self.verticalLayout_25 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.btn_import_tx_local_source = QPushButton(self.groupBox_11)
        self.btn_import_tx_local_source.setObjectName(u"btn_import_tx_local_source")

        self.horizontalLayout_19.addWidget(self.btn_import_tx_local_source)

        self.btn_import_tx_browse = QPushButton(self.groupBox_11)
        self.btn_import_tx_browse.setObjectName(u"btn_import_tx_browse")

        self.horizontalLayout_19.addWidget(self.btn_import_tx_browse)


        self.verticalLayout_25.addLayout(self.horizontalLayout_19)

        self.tview_import_tx = QTreeWidget(self.groupBox_11)
        self.tview_import_tx.setObjectName(u"tview_import_tx")

        self.verticalLayout_25.addWidget(self.tview_import_tx)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.cb_import_tx_create_shaders = QCheckBox(self.groupBox_11)
        self.cb_import_tx_create_shaders.setObjectName(u"cb_import_tx_create_shaders")
        self.cb_import_tx_create_shaders.setChecked(True)

        self.horizontalLayout_17.addWidget(self.cb_import_tx_create_shaders)

        self.btn_import_tx_import = QPushButton(self.groupBox_11)
        self.btn_import_tx_import.setObjectName(u"btn_import_tx_import")

        self.horizontalLayout_17.addWidget(self.btn_import_tx_import)


        self.verticalLayout_25.addLayout(self.horizontalLayout_17)


        self.horizontalLayout_15.addWidget(self.groupBox_11)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_15)

        self.tab_window.addTab(self.texturing_tab, "")
        self.texture_database_tab = QWidget()
        self.texture_database_tab.setObjectName(u"texture_database_tab")
        self.texture_database_tab.setEnabled(False)
        self.texture_database_tab.setAutoFillBackground(True)
        self.horizontalLayout_7 = QHBoxLayout(self.texture_database_tab)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox_12 = QGroupBox(self.texture_database_tab)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_26 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.tview_scene_tx = QTreeWidget(self.groupBox_12)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tview_scene_tx.setHeaderItem(__qtreewidgetitem)
        self.tview_scene_tx.setObjectName(u"tview_scene_tx")
        self.tview_scene_tx.header().setVisible(False)

        self.verticalLayout_26.addWidget(self.tview_scene_tx)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btn_scene_tx_refresh = QPushButton(self.groupBox_12)
        self.btn_scene_tx_refresh.setObjectName(u"btn_scene_tx_refresh")

        self.horizontalLayout_8.addWidget(self.btn_scene_tx_refresh)

        self.btn_scene_tx_publish = QPushButton(self.groupBox_12)
        self.btn_scene_tx_publish.setObjectName(u"btn_scene_tx_publish")

        self.horizontalLayout_8.addWidget(self.btn_scene_tx_publish)


        self.verticalLayout_26.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_7.addWidget(self.groupBox_12)

        self.groupBox_8 = QGroupBox(self.texture_database_tab)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.tview_shader_setup_nav = QTreeWidget(self.groupBox_8)
        self.tview_shader_setup_nav.setObjectName(u"tview_shader_setup_nav")
        self.tview_shader_setup_nav.setEnabled(False)
        sizePolicy.setHeightForWidth(self.tview_shader_setup_nav.sizePolicy().hasHeightForWidth())
        self.tview_shader_setup_nav.setSizePolicy(sizePolicy)
        self.tview_shader_setup_nav.setMinimumSize(QSize(0, 150))
        self.tview_shader_setup_nav.setMaximumSize(QSize(16777215, 5000))

        self.verticalLayout_16.addWidget(self.tview_shader_setup_nav)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.btn_refresh_shader_setup_nav = QPushButton(self.groupBox_8)
        self.btn_refresh_shader_setup_nav.setObjectName(u"btn_refresh_shader_setup_nav")

        self.horizontalLayout_10.addWidget(self.btn_refresh_shader_setup_nav)

        self.btn_new_asset = QPushButton(self.groupBox_8)
        self.btn_new_asset.setObjectName(u"btn_new_asset")

        self.horizontalLayout_10.addWidget(self.btn_new_asset)


        self.verticalLayout_16.addLayout(self.horizontalLayout_10)

        self.line = QFrame(self.groupBox_8)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_16.addWidget(self.line)

        self.tview_textures_db_nav = QTreeWidget(self.groupBox_8)
        self.tview_textures_db_nav.setObjectName(u"tview_textures_db_nav")

        self.verticalLayout_16.addWidget(self.tview_textures_db_nav)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.checkBox_2 = QCheckBox(self.groupBox_8)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.horizontalLayout_11.addWidget(self.checkBox_2)

        self.checkBox = QCheckBox(self.groupBox_8)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_11.addWidget(self.checkBox)

        self.pushButton_6 = QPushButton(self.groupBox_8)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_11.addWidget(self.pushButton_6)


        self.verticalLayout_16.addLayout(self.horizontalLayout_11)


        self.horizontalLayout_7.addWidget(self.groupBox_8)

        self.frame_7 = QFrame(self.texture_database_tab)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_7)
        self.verticalLayout_22.setSpacing(10)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.groupBox_13 = QGroupBox(self.frame_7)
        self.groupBox_13.setObjectName(u"groupBox_13")
        sizePolicy.setHeightForWidth(self.groupBox_13.sizePolicy().hasHeightForWidth())
        self.groupBox_13.setSizePolicy(sizePolicy)
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_23.setSpacing(6)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(9, -1, -1, 9)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.groupBox_13)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_12.addWidget(self.label_2)

        self.comboBox_2 = QComboBox(self.groupBox_13)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_12.addWidget(self.comboBox_2)


        self.verticalLayout_23.addLayout(self.horizontalLayout_12)

        self.textBrowser_3 = QTextBrowser(self.groupBox_13)
        self.textBrowser_3.setObjectName(u"textBrowser_3")

        self.verticalLayout_23.addWidget(self.textBrowser_3)


        self.verticalLayout_22.addWidget(self.groupBox_13)

        self.groupBox_14 = QGroupBox(self.frame_7)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_14)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.textBrowser_4 = QTextBrowser(self.groupBox_14)
        self.textBrowser_4.setObjectName(u"textBrowser_4")

        self.verticalLayout_24.addWidget(self.textBrowser_4)


        self.verticalLayout_22.addWidget(self.groupBox_14)


        self.horizontalLayout_7.addWidget(self.frame_7)

        self.tab_window.addTab(self.texture_database_tab, "")
        self.rigging_tab = QWidget()
        self.rigging_tab.setObjectName(u"rigging_tab")
        self.rigging_tab.setAutoFillBackground(True)
        self.horizontalLayout_23 = QHBoxLayout(self.rigging_tab)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.verticalLayout_29 = QVBoxLayout()
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.groupBox_15 = QGroupBox(self.rigging_tab)
        self.groupBox_15.setObjectName(u"groupBox_15")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_15.sizePolicy().hasHeightForWidth())
        self.groupBox_15.setSizePolicy(sizePolicy5)
        self.horizontalLayout_24 = QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.btn_rig_meta = QPushButton(self.groupBox_15)
        self.btn_rig_meta.setObjectName(u"btn_rig_meta")

        self.horizontalLayout_24.addWidget(self.btn_rig_meta)

        self.btn_rig_rig = QPushButton(self.groupBox_15)
        self.btn_rig_rig.setObjectName(u"btn_rig_rig")

        self.horizontalLayout_24.addWidget(self.btn_rig_rig)


        self.verticalLayout_29.addWidget(self.groupBox_15)

        self.groupBox_16 = QGroupBox(self.rigging_tab)
        self.groupBox_16.setObjectName(u"groupBox_16")
        self.horizontalLayout_25 = QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.btn_create_follicles = QPushButton(self.groupBox_16)
        self.btn_create_follicles.setObjectName(u"btn_create_follicles")

        self.horizontalLayout_25.addWidget(self.btn_create_follicles)

        self.btn_move_follicles = QPushButton(self.groupBox_16)
        self.btn_move_follicles.setObjectName(u"btn_move_follicles")

        self.horizontalLayout_25.addWidget(self.btn_move_follicles)

        self.btn_clean_follicle_movers = QPushButton(self.groupBox_16)
        self.btn_clean_follicle_movers.setObjectName(u"btn_clean_follicle_movers")

        self.horizontalLayout_25.addWidget(self.btn_clean_follicle_movers)


        self.verticalLayout_29.addWidget(self.groupBox_16)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_9)


        self.horizontalLayout_23.addLayout(self.verticalLayout_29)

        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.frame_12 = QFrame(self.rigging_tab)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Raised)

        self.verticalLayout_30.addWidget(self.frame_12)


        self.horizontalLayout_23.addLayout(self.verticalLayout_30)

        self.tab_window.addTab(self.rigging_tab, "")
        self.camera_tab = QWidget()
        self.camera_tab.setObjectName(u"camera_tab")
        self.camera_tab.setAutoFillBackground(True)
        self.horizontalLayout_26 = QHBoxLayout(self.camera_tab)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.frame_13 = QFrame(self.camera_tab)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.frame_13)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.groupBox_17 = QGroupBox(self.frame_13)
        self.groupBox_17.setObjectName(u"groupBox_17")
        self.horizontalLayout_27 = QHBoxLayout(self.groupBox_17)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.btn_shake_setup = QPushButton(self.groupBox_17)
        self.btn_shake_setup.setObjectName(u"btn_shake_setup")

        self.horizontalLayout_27.addWidget(self.btn_shake_setup)

        self.btn_shake_move = QPushButton(self.groupBox_17)
        self.btn_shake_move.setObjectName(u"btn_shake_move")

        self.horizontalLayout_27.addWidget(self.btn_shake_move)

        self.btn_shake_shake = QPushButton(self.groupBox_17)
        self.btn_shake_shake.setObjectName(u"btn_shake_shake")

        self.horizontalLayout_27.addWidget(self.btn_shake_shake)


        self.verticalLayout_31.addWidget(self.groupBox_17)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_10)


        self.horizontalLayout_26.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.camera_tab)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_26.addWidget(self.frame_14)

        self.tab_window.addTab(self.camera_tab, "")

        self.verticalLayout.addWidget(self.tab_window)

        AssetToolkit.setCentralWidget(self.centralwidget)

        self.retranslateUi(AssetToolkit)

        self.tab_window.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AssetToolkit)
    # setupUi

    def retranslateUi(self, AssetToolkit):
        AssetToolkit.setWindowTitle(fakestr(u"WCA Toolkit", None))
        self.groupBox_4.setTitle(fakestr(u"Mesh Check", None))
        self.cb_triangles.setText(fakestr(u"Triangles", None))
        self.cb_ngons.setText(fakestr(u"nGons", None))
        self.cb_non_quads.setText(fakestr(u"Non quads", None))
        self.cb_non_manifold.setText(fakestr(u"Non Manifold", None))
        self.cb_lamina.setText(fakestr(u"Lamina", None))
        self.btn_mesh_check.setText(fakestr(u"Check", None))
        self.btn_mesh_refresh.setText(fakestr(u"Refresh", None))
        self.groupBox_5.setTitle(fakestr(u"Other Tools", None))
        self.btn_optimize.setText(fakestr(u"Optimize", None))
        self.btn_delete_history.setText(fakestr(u"Delete History", None))
        self.btn_center_pivots.setText(fakestr(u"Center Pivots", None))
        self.btn_freeze_transforms.setText(fakestr(u"Freeze Transforms", None))
        self.btn_copypivot.setText(fakestr(u"Copy Pivot", None))
        self.btn_matchtransforms.setText(fakestr(u"Match Transforms", None))
        self.btn_unlock_normals.setText(fakestr(u"Unlock Normals", None))
        self.btn_merge_uvs.setText(fakestr(u"Merge UVs", None))
        self.btn_initial_shader.setText(fakestr(u"Initial Shader", None))
        self.btn_min_pivot.setText(fakestr(u"Move Pivot to minY", None))
        self.btn_rev_sides.setText(fakestr(u"Reverse Sidedness", None))
        ___qtreewidgetitem = self.tview_mesh_check.headerItem()
        ___qtreewidgetitem.setText(0, fakestr(u"Mesh Check Results", None));
        self.tab_window.setTabText(self.tab_window.indexOf(self.modelling_tab), fakestr(u"Modelling", None))
        self.groupBox_6.setTitle(fakestr(u"Rename", None))
        self.rbtn_rename.setText(fakestr(u"Specify Base Name", None))
        self.txt_rename.setPlaceholderText(fakestr(u"Base Name", None))
        self.btn_rename.setText(fakestr(u"Rename", None))
        self.groupBox_7.setTitle(fakestr(u"Select", None))
        self.btn_select_objects_with_same_name.setText(fakestr(u"Select Objects With Same Base Name", None))
        self.btn_select_bad_names.setText(fakestr(u"Select Objects With Bad Base Names", None))
        self.btn_select_bad_structure.setText(fakestr(u"Select Objects With Bad Name Structures", None))
        self.btn_append_shader_names.setText(fakestr(u"Append Shader Name", None))
        self.tab_window.setTabText(self.tab_window.indexOf(self.naming_tab), fakestr(u"Naming", None))
        self.groupBox.setTitle(fakestr(u"Subdiv Schemes UV", None))
        self.rbtn_subdiv_smooth_all.setText(fakestr(u"Preserve Corners(Recommended)", None))
        self.rbtn_subdiv_preserve_borders.setText(fakestr(u"Preserve Borders", None))
        self.rbtn_subdiv_no_smoothing.setText(fakestr(u"No Smoothing", None))
        self.btn_add_subdivs.setText(fakestr(u"Add Subdivs", None))
        self.btn_remove_subdivs.setText(fakestr(u"Remove Subdivs", None))
        self.groupBox_3.setTitle(fakestr(u"Naming", None))
        self.btn_bad_shaders.setText(fakestr(u"Check Shader Names", None))
        self.btn_rename_file_nodes.setText(fakestr(u"Rename File Nodes", None))
        self.groupBox_9.setTitle(fakestr(u"UV", None))
        self.btn_transfer_uv.setText(fakestr(u"Transfer UVs", None))
        self.groupBox_11.setTitle(fakestr(u"Import Textures", None))
        self.btn_import_tx_local_source.setText(fakestr(u"Local Source", None))
        self.btn_import_tx_browse.setText(fakestr(u"Browse", None))
        ___qtreewidgetitem1 = self.tview_import_tx.headerItem()
        ___qtreewidgetitem1.setText(0, fakestr(u"Local Source", None));
        self.cb_import_tx_create_shaders.setText(fakestr(u"Create Shaders", None))
        self.btn_import_tx_import.setText(fakestr(u"Import Texture", None))
        self.tab_window.setTabText(self.tab_window.indexOf(self.texturing_tab), fakestr(u"Texturing", None))
        self.groupBox_12.setTitle(fakestr(u"Scene Textures", None))
        self.btn_scene_tx_refresh.setText(fakestr(u"Refresh", None))
        self.btn_scene_tx_publish.setText(fakestr(u"Publish", None))
        self.groupBox_8.setTitle(fakestr(u"Database", None))
        ___qtreewidgetitem2 = self.tview_shader_setup_nav.headerItem()
        ___qtreewidgetitem2.setText(0, fakestr(u"Assets", None));
        self.btn_refresh_shader_setup_nav.setText(fakestr(u"Refresh", None))
        self.btn_new_asset.setText(fakestr(u"New Asset", None))
        ___qtreewidgetitem3 = self.tview_textures_db_nav.headerItem()
        ___qtreewidgetitem3.setText(0, fakestr(u"Textures", None));
        self.checkBox_2.setText(fakestr(u"Viewport", None))
        self.checkBox.setText(fakestr(u"Renderman", None))
        self.pushButton_6.setText(fakestr(u"Import", None))
        self.groupBox_13.setTitle(fakestr(u"Texture Asset Info", None))
        self.label_2.setText(fakestr(u"Version:", None))
        self.groupBox_14.setTitle(fakestr(u"Version Info", None))
        self.tab_window.setTabText(self.tab_window.indexOf(self.texture_database_tab), fakestr(u"Texture Database", None))
        self.groupBox_15.setTitle(fakestr(u"Prop Rigger", None))
        self.btn_rig_meta.setText(fakestr(u"Meta", None))
        self.btn_rig_rig.setText(fakestr(u"Rig", None))
        self.groupBox_16.setTitle(fakestr(u"Follicles", None))
        self.btn_create_follicles.setText(fakestr(u"Create Follicles", None))
        self.btn_move_follicles.setText(fakestr(u"Move Follicles", None))
        self.btn_clean_follicle_movers.setText(fakestr(u"Clean Movers", None))
        self.tab_window.setTabText(self.tab_window.indexOf(self.rigging_tab), fakestr(u"Rigging", None))
        self.groupBox_17.setTitle(fakestr(u"Camera Shake", None))
        self.btn_shake_setup.setText(fakestr(u"Setup", None))
        self.btn_shake_move.setText(fakestr(u"Move", None))
        self.btn_shake_shake.setText(fakestr(u"Shake", None))
        self.tab_window.setTabText(self.tab_window.indexOf(self.camera_tab), fakestr(u"Camera", None))
    # retranslateUi

