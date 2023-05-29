# -*- coding: utf-8 -*-
import sys

# ==== auto Qt load ====
try:
    from PySide2 import QtCore, QtGui
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets
    
    import sip
    qtMode = 1

import wildchildanimation.maya.asset_toolkit.camera.shake as camera_shake
import wildchildanimation.maya.asset_toolkit.modelling as mod
import wildchildanimation.maya.asset_toolkit.rename as fcrn
import wildchildanimation.maya.asset_toolkit.rigging.create_follicle_from_geo as fol_create
import wildchildanimation.maya.asset_toolkit.rigging.move_follicle as fol_move
import wildchildanimation.maya.asset_toolkit.rigging.prop_rigger as rigging
import wildchildanimation.maya.asset_toolkit.texturing as tx
import wildchildanimation.maya.asset_toolkit.utils.os_utils as os_utils
import wildchildanimation.maya.asset_toolkit.tx_database as tx_db    

from shiboken2 import wrapInstance  

from pymel.core import *
import maya.OpenMayaUI as omui

from wildchildanimation.maya.asset_toolkit.asset_toolkit_dialog import Ui_AssetToolkit

'''
    AssetToolkitDialog class
    ################################################################################
'''

class AssetToolkitDialog(QtWidgets.QMainWindow, Ui_AssetToolkit):

    working_dir = None
    
    def __init__(self, parent = None):
        try:
            if sys.version_info.major < 3:
                maya_main_window = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
            else:
                maya_main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)

            super(AssetToolkitDialog, self).__init__(maya_main_window)
        except:
            super(AssetToolkitDialog, self).__init__(parent) # Call the inherited classes __init__ method  

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint ^ QtCore.Qt.WindowMinMaxButtonsHint)

        self.naming_ui_connect()
        self.modeling_ui_connect()
        self.texturing_ui_connect()
        self.texturing_db_ui_connect()
        self.rigging_ui_connect()
        self.camera_ui_connect()

    def naming_ui_connect(self):
        self.btn_rename.clicked.connect(self.rename_method)
        self.btn_select_bad_names.clicked.connect(fcrn.search_bad_names)
        self.btn_select_objects_with_same_name.clicked.connect(fcrn.select_same_base_name)
        self.btn_append_shader_names.clicked.connect(fcrn.shader_append)
        self.btn_select_bad_structure.clicked.connect(fcrn.find_bad_name_structures)        
        
        regexp = QtCore.QRegExp('[A-Za-z]*')
        text_validator = QtGui.QRegExpValidator(regexp)
        self.txt_rename.setValidator(text_validator)
    
    def modeling_ui_connect(self):
        self.btn_mesh_check.clicked.connect(self.mesh_check_method)
        self.btn_mesh_refresh.clicked.connect(self.mesh_refresh_method)
        
        self.mesh_check_tree = self.tview_mesh_check
        self.mesh_check_tree.itemSelectionChanged.connect(self.mesh_check_select)
        
        # self.btn_optimize.clicked.connect(modeling.optimize_model)
        # self.btn_optimize.setToolTip(modeling.optimize_model.__doc__)
        
        self.btn_delete_history.clicked.connect(mod.deleteHistory)
        self.btn_center_pivots.clicked.connect(mod.center_pivots)
        self.btn_freeze_transforms.clicked.connect(mod.freeze_transforms)
        self.btn_unlock_normals.clicked.connect(mod.unlock_vertex_normals)
        self.btn_merge_uvs.clicked.connect(mod.merge_UVs)
        self.btn_initial_shader.clicked.connect(mod.initial_shader)
        
        self.btn_min_pivot.clicked.connect(mod.minYPivot)
        self.btn_min_pivot.setToolTip('Moves the pivot of isolated transforms to Minimum Y bbox')

        self.btn_rev_sides.clicked.connect(mod.reversesides)
        self.btn_rev_sides.setToolTip('Reverse the sidedness of a mesh when it has been scaled negatively and frozen.')
        
        self.btn_copypivot.clicked.connect(mod.copypivot)
        self.btn_copypivot.setToolTip('Copy the pivot of one object to another. Select source then target')
        
        self.btn_matchtransforms.clicked.connect(mod.matchtransforms)
        self.btn_matchtransforms.setToolTip('Copy the pivot of one object to another. Select source then target')
        
        
    def texturing_ui_connect(self):      
        self.btn_refresh_shader_setup_nav.clicked.connect(self.Tx_db_refresh)        
        self.tview_shader_setup_nav.itemSelectionChanged.connect(self.texture_nav_update_selection) 
        self.btn_import_tx_local_source.clicked.connect(self.refresh_tx_local_source)
        self.btn_import_tx_import.clicked.connect(self.import_tx_local_source)
        self.btn_import_tx_browse.clicked.connect(self.refresh_tx_browse)
        
        self.btn_rename_file_nodes.clicked.connect(tx.fix_file_nodes)
        self.btn_rename_file_nodes.setToolTip(tx.fix_file_nodes.__doc__)   
             
        self.btn_transfer_uv.clicked.connect(tx.transfer_UV)
        self.btn_transfer_uv.setToolTip(tx.transfer_UV.__doc__)
        
        self.btn_bad_shaders.clicked.connect(tx.find_bad_shader_names)
        self.btn_bad_shaders.setToolTip(tx.find_bad_shader_names.__doc__)
        
        self.btn_add_subdivs.clicked.connect(self.smooth_mesh)
        self.btn_remove_subdivs.clicked.connect(self.remove_smooth_mesh)
        

    def texturing_db_ui_connect(self):
        self.btn_scene_tx_refresh.clicked.connect(self.scene_tx_refresh)
        self.btn_scene_tx_publish.clicked.connect(self.scene_tx_refresh)
 
    def rigging_ui_connect(self):
        self.btn_rig_meta.clicked.connect(rigging.meta)
        self.btn_rig_meta.setToolTip(rigging.rig.__doc__)
        self.btn_rig_rig.clicked.connect(rigging.rig)
        self.btn_rig_rig.setToolTip(rigging.rig.__doc__)
        
        self.btn_create_follicles.clicked.connect(fol_create.create_follicle)
        self.btn_create_follicles.setToolTip(fol_create.create_follicle.__doc__)
        self.btn_move_follicles.clicked.connect(fol_move.move_folicles)
        self.btn_move_follicles.setToolTip(fol_move.move_folicles.__doc__)
        self.btn_clean_follicle_movers.clicked.connect(fol_move.remove_p_o_m)
        self.btn_clean_follicle_movers.setToolTip(fol_move.remove_p_o_m.__doc__)
        
    def camera_ui_connect(self):
        self.btn_shake_setup.clicked.connect(camera_shake.camera_shake)
        self.btn_shake_setup.setToolTip(camera_shake.camera_shake.__doc__)
        self.btn_shake_move.clicked.connect(camera_shake.camera_shake_move)
        self.btn_shake_move.setToolTip(camera_shake.camera_shake_move.__doc__)
        self.btn_shake_shake.clicked.connect(camera_shake.camera_shake_noise)
        self.btn_shake_shake.setToolTip(camera_shake.camera_shake_noise.__doc__)

    def rename_method(self):
        check_state = self.rbtn_rename.isChecked()
        text = self.txt_rename.text()

        warning_check = False
        if len(text) == 0 and check_state:
            warning('Specify a base name.')
            warning_check = True
            
        if not check_state:
            text = None
            
        if not warning_check: 
            fcrn.rename(basename = text) 

    def mesh_check_method(self):
        self.mesh_list = mod.get_mesh_list()
        
        triangles_dic = mod.triangles()  
        nGons_dic = mod.nGons()  
        non_quads_dic = mod.non_quads()
        non_manifold_dic = mod.non_manifold()
        lamina_dic = mod.lamina()
        
        self.triangle_status = self.cb_triangles.checkState()
        self.ngons_status  = self.cb_ngons.checkState()
        self.non_quads_status  = self.cb_non_quads.checkState()
        self.non_manifold_status  = self.cb_non_manifold.checkState()
        self.lamina_status  = self.cb_lamina.checkState()
        
        mesh_check_list = {}
        
        if self.triangle_status:
            mesh_check_list['Triangles'] = triangles_dic
                        
        if self.ngons_status:
            mesh_check_list['nGons'] = nGons_dic    
            
        if self.non_quads_status:
            mesh_check_list['non-Quads'] = non_quads_dic            
            
        if self.non_manifold_status:
            mesh_check_list['Non-Manifold'] = non_manifold_dic            
            
        if self.lamina_status:
            mesh_check_list['Lamina'] = lamina_dic            
        
        mesh_check_summery = {}
        for check_type, check_type_list in mesh_check_list.items():
            for object_name , value in check_type_list.items():
                length = len(check_type_list[object_name])
                
                if length:
                    if object_name not in mesh_check_summery:
                        mesh_check_summery[object_name] = {check_type: value}
                    else: 
                        mesh_check_summery[object_name][check_type] = value
        
        self.mesh_check_tree.clear()
        self.data_to_tree(self.mesh_check_tree, mesh_check_summery)
        select(self.mesh_list)
        
    def mesh_check_select(self):
        current_item = self.mesh_check_tree.currentItem()
        selection = current_item.selection
        select(selection)
    
    def data_to_tree(self, parent, data):
        if isinstance(data, dict):
            #parent.setFirstColumnSpanned(True)
            for key,value in data.items():
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, key)                
                child.selection = key                
                self.second_level(child, value)
    
    def second_level(self, parent, data):
        if isinstance(data, dict):
            #parent.setFirstColumnSpanned(True)
            for key,value in data.items():
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setForeground(0, QtCore.Qt.darkGray)  
                amount = str(len(data[key]))
                amount_padding = 4 - len(amount)
                child.setText(0, ('  '*amount_padding) + amount + '    ' + key)                   
                child.selection = value      
                
    def mesh_refresh_method(self):
        if self.mesh_list:
            select(self.mesh_list)    
                    
        self.mesh_check_method()

    #Texturing Methods
    def smooth_mesh(self):
        smooth_cs = self.rbtn_subdiv_smooth_all.isChecked()
        preserve_borders_cs= self.rbtn_subdiv_preserve_borders.isChecked()
        no_smooth_cs = self.rbtn_subdiv_no_smoothing.isChecked()
        
        if smooth_cs:
            options = 0
            
        elif preserve_borders_cs:
            options = 1
        
        elif no_smooth_cs:
            options = 2
        
        print(options)
        mod.smooth_mesh(options)

    def remove_smooth_mesh(self):
        mod.smooth_mesh(3)
        
    def Tx_db_refresh(self):
        tx_db.texture_db_nav(parent = self.tview_shader_setup_nav )

    def texture_nav_update_selection(self):
        pass
#         try:
#             filepath = self.tview_shader_setup_nav.selectedItems()[0].filepath
#         except:
#             pass
#         self.tview_textures_db_nav.clear()
#         if filepath:      
#             tx_dir_dic = tx.tx_to_dic(os.listdir(filepath))
#             
#             tx.texture_nav_tree(self.tview_textures_db_nav, tx_dir_dic)

    def refresh_tx_local_source(self):
        ###modify to check in sub-directories
        sourceimages = os_utils.get_project_folder('sourceimages')
        
        self.tx_import_list = tx_db.tx_dir_to_dic(sourceimages)
        
        self.tview_import_tx.clear()
        tx_db.texture_nav_tree(self.tview_import_tx, self.tx_import_list)
        self.tview_import_tx.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)
        
    def refresh_tx_browse(self):
        ###modify to check in sub-directories
        sourceimages = promptForPath()
        
        sourceimages = sourceimages.rsplit('/', 1)[0]
        
        self.tx_import_list = tx_db.tx_dir_to_dic(sourceimages)
        
        self.tview_import_tx.clear()
        tx_db.texture_nav_tree(self.tview_import_tx, self.tx_import_list)
        self.tview_import_tx.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)

    def import_tx_local_source(self):
        undoInfo(openChunk = True,undoName = 'import_tx_local_source')
        self.import_tx_dic = {}
        self.import_tx_create_shaders = bool(self.cb_import_tx_create_shaders.checkState())
        for i in range(self.tview_import_tx.topLevelItemCount()):
            tree_item = self.tview_import_tx.topLevelItem(i)
            if tree_item.checkState(0):
                self.import_tx_dic[tree_item.details.keys()[0]] = tree_item.details[tree_item.details.keys()[0]]

        tx.import_tx(self.import_tx_dic, self.import_tx_create_shaders)
        undoInfo(closeChunk = True)

    def send_to_mari(self):
        subdivs = int(self.le_mari_subdiv.text())
        new_scene= self.rbtn_mari_new_scene.isChecked()
        scene_name = self.le_mari_scene_name.text()
        combine = self.rbtn_mari_combine.isChecked()
        texture_set_name = self.le_mari_texture_set_name.text()
        
        tx.send_to_mari(scene_name = scene_name, texture_set_name = texture_set_name, new_scene = new_scene, combine =combine, subdivs =subdivs)

    def scene_tx_refresh(self):  
        self.scene_tx_list = tx_db.get_scene_tx()   
        self.tview_scene_tx.clear()
        tx_db.texture_nav_tree(self.tview_scene_tx, self.scene_tx_list)
        self.tview_scene_tx.sortItems(0,QtCore.Qt.SortOrder.AscendingOrder)                   