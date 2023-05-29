import csv
import os
import sys

import maya.cmds as cmds
import maya.mel as mel

import json

def get_scene_name():
    scene_name = cmds.file(q= True, sceneName = True, shortName = True)
    if scene_name:
        scene_name = os.path.splitext(scene_name)[0]
    else:
        scene_name = "untitled"
    return scene_name

def get_scene_path():
    file_name = cmds.file(q=True, sn=True)
    return os.path.dirname(file_name)

def set_export_path() :
    path = get_scene_path()
    #Create a new directory path
    if not os.path.exists(path + "/cache/fbx"):
        os.makedirs(path + "/cache/fbx")
    
    return (path + "/cache/fbx/")


def get_ri_set():
    skeletal_set = cmds.ls('*_Ri_set', type = 'objectSet')
    if len(skeletal_set) < 1 :
        print("No set Found : Attempting to create new Export set")
        print("NB! Please check if the export worked as expected")

    return(skeletal_set)

def fbx_export_settings():

    mel.eval("FBXExportCameras -v 1;")
    mel.eval("FBXExportBakeComplexAnimation -v \"False\";")
    mel.eval("FBXExportBakeComplexStep -v 1;")
    mel.eval("FBXExportSmoothingGroups -v 1;")
    mel.eval("FBXExportAnimationOnly -v 0;")
    mel.eval("FBXExportApplyConstantKeyReducer -v 0;")
    mel.eval("FBXExportAxisConversionMethod \"convertAnimation\";")
    mel.eval("FBXExportCacheFile -v 0;")
    mel.eval("FBXExportConstraints -v 0;")
    mel.eval("FBXExportEmbeddedTextures -v 0;")
    mel.eval("FBXExportFileVersion -v FBX201800;")
    mel.eval("FBXExportGenerateLog -v 1;")
    mel.eval("FBXExportHardEdges -v 0;")
    mel.eval("FBXExportInAscii -v 1;")
    mel.eval("FBXExportInputConnections -v 1;")
    mel.eval("FBXExportInstances -v 0;")
    mel.eval("FBXExportLights -v 1;")
    mel.eval("FBXExportQuaternion -v euler;")
    mel.eval("FBXExportReferencedAssetsContent -v 1;")
    mel.eval("FBXExportScaleFactor 1;")
    mel.eval("FBXExportShapes -v 1;")
    mel.eval("FBXExportSkeletonDefinitions -v 1;")
    mel.eval("FBXExportSkins -v 1;")
    mel.eval("FBXExportSmoothMesh -v 1;")
    mel.eval("FBXExportTangents -v 1;")
    mel.eval("FBXExportTriangulate -v 0;")
    mel.eval("FBXExportUpAxis y;")
    mel.eval("FBXExportUseSceneName -v 0;")

def export_skeletal_fbx(polysmooth) :
    
    fbx_export_settings()
    ri_set = get_ri_set()
    path = set_export_path()
    
    sceneName = get_scene_name()
    exportName = ("")
    
    for export_set in ri_set:
        print(export_set)
        cmds.select(export_set)
        sel = cmds.ls(sl = True)
        if polysmooth:
            for geo in sel:
                shapenode = cmds.listRelatives( geo, ni = True, shapes=True )
                if shapenode:
                    cmds.select(shapenode)
                    mel.eval("polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 1 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 {};".format(geo))
                    cmds.select(geo)
                    delete_nondefhist_command = ("doBakeNonDefHistory( 1, {\"prePost\" });")
                    mel.eval(delete_nondefhist_command)

        asset_name = export_set.split("_")
        export_name = ("sk_" + asset_name[0])

        print("Exporting :{}".format(exportName))
        cmds.select(export_set)
        export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
        print(export_command)
        mel.eval(export_command)
    
def merge_static_meshes(prop):
    all_mesh_shapes = cmds.listRelatives( prop, allDescendents=True, f = True,type = "mesh" )
    all_meshes = cmds.listRelatives(all_mesh_shapes, parent=True, fullPath=True, f = True)

def get_world_pivot(prop):
    wm = cmds.getAttr(prop+'.worldMatrix[0]', time=0)
    rotPiv = cmds.getAttr(prop+'.rotatePivot', time=0)[0]
    rotPivWorld = [wm[0]*rotPiv[0] + wm[4]*rotPiv[1] + wm[8]*rotPiv[2] + wm[12],wm[1]*rotPiv[0] + wm[5]*rotPiv[1] + wm[9]*rotPiv[2] + wm[13],wm[2]*rotPiv[0] + wm[6]*rotPiv[1] + wm[10]*rotPiv[2] + wm[14]]
    return(rotPivWorld)

def move_to_origin(prop):
    sx = cmds.getAttr(prop + ".scaleX")
    sy = cmds.getAttr(prop + ".scaleY")
    sz = cmds.getAttr(prop + ".scaleZ") 
    cmds.setAttr((prop + ".scaleX"), 1)
    cmds.setAttr((prop + ".scaleY"), 1)
    cmds.setAttr((prop + ".scaleZ"), 1)
    cmds.makeIdentity(prop , apply = True, translate = True, rotate = False, scale = False)
    rotPivWorld = get_world_pivot(prop)

    cmds.setAttr(prop+".translateX",(-rotPivWorld[0]))
    cmds.setAttr(prop+".translateY",(-rotPivWorld[1]))
    cmds.setAttr(prop+".translateZ",(-rotPivWorld[2]))  
    cmds.setAttr((prop + ".rotateX"), 0)
    cmds.setAttr((prop + ".rotateY"), 0)
    cmds.setAttr((prop + ".rotateZ"), 0)

def get_asset_name():
    scene_name = get_scene_name()
    asset_name = scene_name.split("_")
    return(asset_name[1])

def delete_keys(prop):
    cmds.cutKey(prop, s=True)#delete key command
    prop_children = cmds.listRelatives(prop, type = "transform", allDescendents = True, f = True)
    if prop_children:
        for child in prop_children:
            cmds.cutKey(child, s=True)#delete key command

def find_parent(prop, export_set):
    cmds.select(export_set)
    export_props_longname = cmds.ls(sl = True, l = True)
    parents = cmds.listRelatives(prop, parent=True, fullPath=True, f = True)
    if parents == None:
        prop_parent = ["root"]
    else:
        if parents[0] in export_props_longname: # => True
            prop_parent = parents[0].split("|")
        else:
            prop_parent = ["root"]
    return(prop_parent[-1])
    
def is_group(node):
    children = node.getChildren()
    for child in children:
        if type(child) is not pymel.core.nodetypes.Transform:
            return False
    return True

def get_aset_name(prop, prepostfix):
   
    #get shot name of prop
    cmds.select(prop, r = True)

    postfix = ''
    prop_name = ''
    namespace = prop.split(':')
    if len(namespace) > 1:
        namespace_version = namespace[-2].split('_')
        postfix = (namespace_version[-1])
        
    else:
        pass
    if prepostfix == "prop":
        short_name = namespace[-1].split('|')
        prop_name = short_name[-1].split('_')
        asset_name = prop_name[0]
    if prepostfix == "namespace":
        asset_name = postfix    
       
    return(asset_name)

def export_static_fbx(polysmooth, do_combine, set_to_origin) :
    export_collection_longname = cmds.ls(sl = True, l = True)
    
    fbx_export_settings()
    path = set_export_path()
    
    sceneName = get_scene_name()
    exportName = ("")
    

    for prop in export_collection_longname:
        delete_keys(prop)
        cmds.makeIdentity(prop, apply=True, translate=True )
        if set_to_origin:
            move_to_origin(prop)
        cmds.select(prop)
        
        sel = cmds.ls(sl = True)
        if do_combine:
            merge_static_meshes(prop)
        if polysmooth:
            for geo in sel:
                shapenode = cmds.listRelatives( geo, ni = True, shapes=True )
                if shapenode:
                    cmds.select(shapenode)
                    mel.eval("polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 1 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 {};".format(geo))
                    cmds.select(geo)
                    delete_nondefhist_command = ("doBakeNonDefHistory( 1, {\"prePost\" });")
                    mel.eval(delete_nondefhist_command)
        cmds.select(prop)
        #asset_name = cmds.ls(sl = True)
        #asset_name = asset_name[0].split("_")
        asset_name = get_aset_name(prop, "prop")
        export_name = ("sm_" + asset_name)

        print("Exporting :{}".format(export_name))
        cmds.select(prop)
        export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
        print(export_command)
        mel.eval(export_command)

def get_prop_attr(export_props):
    asset_name = get_asset_name()
    print(asset_name)
    #try:
        
    count = 0
    prop_dictionary = []
    prop_dictionary.append({'game_path': '/Game/assets/environments/' + asset_name + '/components/'})
    for prop in export_props:
        namespace = get_aset_name(prop, "namespace")
        prop_name = get_aset_name(prop, "prop")
        prop_parent = find_parent(prop, export_props)

        print(prop_parent + " ... Parent")
        print("pub: processing {} ".format(prop))
        delete_keys(prop)
        sx = cmds.getAttr(prop + ".scaleX")
        sy = cmds.getAttr(prop + ".scaleY")
        sz = cmds.getAttr(prop + ".scaleZ") 
        cmds.setAttr((prop + ".scaleX"), 1)
        cmds.setAttr((prop + ".scaleY"), 1)
        cmds.setAttr((prop + ".scaleZ"), 1)
                   
        cmds.makeIdentity(prop , apply = True, translate = True, rotate = False, scale = False)
                
        world_pivot = get_world_pivot(prop)
                    
        tx = world_pivot[0]
        ty = world_pivot[1]
        tz = world_pivot[2]
        rx = cmds.getAttr(prop + ".rotateX")
        ry = cmds.getAttr(prop + ".rotateY")
        rz = cmds.getAttr(prop + ".rotateZ")
        cmds.setAttr((prop + ".scaleX"), sx)
        cmds.setAttr((prop + ".scaleY"), sy)
        cmds.setAttr((prop + ".scaleZ"), sz)                                          
            
        #propname = prop.split("_")
        dictionary = {'name':('sm_' + prop_name), 'tx':tx, 'ty':ty, 'tz':tz, 'rx':rx, 'ry':ry, 'rz':rz, 'sx':sx, 'sy':sy, 'sz':sz, 'fullname':(prop_name + '_' + namespace), 'parent':prop_parent}
        prop_dictionary.append(dictionary)
    return(prop_dictionary)

def write_json_file(export_props):
    json_filename = (get_scene_name() + ".json") 
    print("wheelbarrow: exporting {}, json: {}, path: {}".format(get_scene_name(), json_filename, get_scene_path()))
    json_dir = "{}/cache/".format(get_scene_path())

    if not os.path.exists(json_dir):
        os.makedirs(json_dir, mode=0o777, exist_ok=False)
        
    with open(json_dir + json_filename, 'w') as json_file:
        prop_dictionary = get_prop_attr(export_props)
        print(prop_dictionary)
        #json_object = json.dumps(prop_dictionary, indent=4)
        json.dump(prop_dictionary,json_file , indent=4)

def export_selected_staticmesh_env():

    export_collection = cmds.ls(sl = True)

    write_json_file(export_collection)
    export_static_fbx(False, True, True)
