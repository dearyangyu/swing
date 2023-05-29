import os

# ==== auto Qt load ====
try:
    from PySide2 import QtCore, QtGui
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtGui, QtWidgets
    import sip
    qtMode = 1

import pymel.core as pm


#from fs_asset_toolkit.ringmaster import rmAssetDB_cmd as db_CMDS
# reload(db_CMDS)
#   
# def texture_db_nav(parent, rootfolder = ''):
#     
#     db = db_CMDS.connectAssetDBDict()
#     TxDB_Dic = db_CMDS.TxDicTree(db_CMDS.listTextures(db))
#     db_CMDS.closeAssetDB(db)
#     
#     
#     parent.clear()
#     
#     
#     TxDB_nav_data_to_tree(parent , TxDB_Dic)
#     parent.sortItems(0,QtCore.Qt.SortOrder(0))


def TxDB_nav_data_to_tree(parent, data, counter = 0, group = ''):
    if isinstance(data, dict) and counter <=1:
        for key,value in data.items():
            child = QtGui.QTreeWidgetItem(parent)
            child.setText(0, str(key))
            if counter == 0:
                group = key
            if counter == 1:
                value['group'] = group
                child.dataTree = {key:value}
                print(child.dataTree)
            TxDB_nav_data_to_tree(child, value, counter+1, group)   


def tx_dir_to_dic(rootfolder):    
    tx_dic = {}    
    files = os.listdir(rootfolder)
    file_types = ['.tif', '.jpg', '.exr', '.tex', '.png']
    for f in files:
        tmp_file_list = []
        if os.path.isdir(os.path.join(rootfolder, f)) and '.' not in f:
            for sub_file in os.listdir(os.path.join(rootfolder,f)):
                if any(x in sub_file for x in file_types): 
                    tmp_file_list.append(tx_name_deconstruct(os.path.join(rootfolder,f, sub_file)))

        if any(x in f for x in file_types): 
            tmp_file_list.append(tx_name_deconstruct(os.path.join(rootfolder,f)))
    

        tx_dic =  tx_dic_combine(tmp_file_list, tx_dic)
        
    return tx_dic

def tx_dic_combine(tmp_file_list, tx_dic):
    for i in tmp_file_list:
        f_name = i.keys()[0]
        
        if f_name not in tx_dic:
            tx_dic[f_name] = i[f_name]
            tx_dic[f_name]['extension'] = i[f_name]['extension']
        else:
            if i[f_name]['channels'][0] not in tx_dic[f_name]['channels']:
                tx_dic[f_name]['channels'].append(i[f_name]['channels'][0])
                tx_dic[f_name]['channels'].sort()
            if i[f_name]['udims'][0] not in tx_dic[f_name]['udims']:
                tx_dic[f_name]['udims'].append(i[f_name]['udims'][0])                    
                tx_dic[f_name]['udims'].sort()
                
            if not i[f_name]['version'] < max(tx_dic[f_name]['version']):
                tx_dic[f_name]['version'] = i[f_name]['version']
                
    return tx_dic
   
def tx_name_deconstruct(filepath):
    filename = filepath.split('/')[-1]
    name = filename.split('_')[0]            
    channel = filename.split('_')[1].split('.')[0]
    udim =  filename.split('.')[1]
    folder = filepath.rsplit('/', 1)[0]
    ext = filepath.rsplit('.', 1)[-1]
    if len(filename.split('_')) == 3:
        version = filename.split('_')[2].split('.')[0]
    else:
        version = '000'         
    return {name:{'channels':[channel], 'udims': [udim], 'folder':folder, 'extension': ext, 'version': version}}

def texture_nav_tree(parent, data):
    if isinstance(data, dict):
        root = parent
        for key,value in data.items():
            parent = QtGui.QTreeWidgetItem(root)
            parent.setText(0, key)
            parent.setCheckState(0,QtCore.Qt.Checked )
            parent.details = {key:value}
            parent.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.Checked | QtCore.Qt.ItemIsUserCheckable)
        
            for index,child_value in enumerate(value['channels']):
                child = QtGui.QTreeWidgetItem(parent)
                child.setText(0, str(child_value)) 
                child.setFlags(QtCore.Qt.ItemIsEnabled)

def get_scene_tx():
    tx_dic = {}
    tx_node_list = []
    nodes = pm.ls(textures = True)
    for node in nodes:
        if node.nodeType() == 'file':        
            tx_node_list.append(tx_name_deconstruct(pm.getAttr(node.name() + '.fileTextureName')))

    tx_node_list = tx_dic_combine(tx_node_list, tx_dic)
    return tx_node_list
