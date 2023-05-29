import os

import pymel
import maya.cmds as cmds
import maya.mel as mel

import json

from wildchildanimation.maya.swing_maya import SwingMaya

class MayaAssetHandler(SwingMaya):

    NAME = 'MayaAssetHandler'
    VERSION = '1.0'

    def __init__(self):
        super(MayaAssetHandler, self).__init__()
        self.log_output("{} v{}".format(self.NAME, self.VERSION))   

    def set_export_path(self) :
        path = self.get_scene_path()

        #Create a new directory path
        if not os.path.exists(path + "/cache/fbx"):
            os.makedirs(path + "/cache/fbx")

        return (path + "/cache/fbx/")

    def get_ri_set(self):
        skeletal_set = cmds.ls('*_Ri_set', type = 'objectSet')
        if len(skeletal_set) < 1 :
            self.log_output("No set Found : Attempting to create new Export set")
            self.log_output("NB! Please check if the export worked as expected")

        return(skeletal_set)

    def get_fbx_set(self):
        fbx_set = cmds.ls('*_fbx_set', type = 'objectSet')
        if len(fbx_set) < 1 :
            fbx_set = cmds.ls('*:*_fbx_set', type = 'objectSet')
            if len(fbx_set) < 1 :
                self.log_output("No set Found : Attempting to create new Export set")
                self.log_output("NB! Please check if the export worked as expected")

        return(fbx_set)

    def env_fbx_export_settings(self):

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

    def skel_fbx_export_settings(self):

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

    def pose_fbx_export_settings(self, anim):

        if anim:
            start_frame = cmds.currentTime(q = True)
            end_frame = start_frame
        
        else:
            start_frame = cmds.playbackOptions( q = True,animationStartTime=True )
            end_frame = cmds.playbackOptions( q = True,animationEndTime=True )

        mel.eval("FBXExportCameras -v 1;")
        mel.eval("FBXExportBakeComplexAnimation -v \"True\";")
        mel.eval("FBXExportBakeComplexEnd -v {};".format(end_frame))
        mel.eval("FBXExportBakeComplexStart -v {};".format(start_frame))
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

    def export_skeletal_fbx(self, polysmooth, export_set, export_type):
		
        self.skel_fbx_export_settings()
        path = self.set_export_path()
        
        sceneName = self.get_scene_name()
        exportName = ("")

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

        asset_name = self.get_asset_name()
        if export_type == "no_shadow":
            export_name = ("sk_" + asset_name + "_whiskars")
        else:
            export_name = ("sk_" + asset_name)
        self.log_output("Exporting :{}".format(exportName))
        cmds.select(clear = True)
        print(export_set)
        cmds.select(export_set, r = True)
        export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
        mel.eval(export_command)
        
    def merge_static_meshes(self, prop):
        all_mesh_shapes = cmds.listRelatives( prop, allDescendents=True, f = True,type = "mesh" )
        all_meshes = cmds.listRelatives(all_mesh_shapes, parent=True, fullPath=True, f = True)

    def get_world_pivot(self, prop):
        wm = cmds.getAttr(prop + '.worldMatrix[0]', time=0)
        rotPiv = cmds.getAttr(prop + '.rotatePivot', time=0)[0]
        rotPivWorld = [wm[0]*rotPiv[0] + wm[4]*rotPiv[1] + wm[8]*rotPiv[2] + wm[12],wm[1]*rotPiv[0] + wm[5]*rotPiv[1] + wm[9]*rotPiv[2] + wm[13],wm[2]*rotPiv[0] + wm[6]*rotPiv[1] + wm[10]*rotPiv[2] + wm[14]]
        return(rotPivWorld)

    def move_to_origin(self, prop):
        sx = cmds.getAttr(prop + ".scaleX")
        sy = cmds.getAttr(prop + ".scaleY")
        sz = cmds.getAttr(prop + ".scaleZ") 
        cmds.setAttr((prop + ".scaleX"), 1)
        cmds.setAttr((prop + ".scaleY"), 1)
        cmds.setAttr((prop + ".scaleZ"), 1)
        cmds.makeIdentity(prop , apply = True, translate = True, rotate = False, scale = False)
        rotPivWorld = self.get_world_pivot(prop)

        cmds.setAttr(prop+".translateX",(-rotPivWorld[0]))
        cmds.setAttr(prop+".translateY",(-rotPivWorld[1]))
        cmds.setAttr(prop+".translateZ",(-rotPivWorld[2]))  
        cmds.setAttr((prop + ".rotateX"), 0)
        cmds.setAttr((prop + ".rotateY"), 0)
        cmds.setAttr((prop + ".rotateZ"), 0)

    def get_asset_name(self):
        scene_name = self.get_scene_name()
        asset_name = scene_name.split("_")
        return(asset_name[1])

    def delete_keys(self, prop):
        cmds.cutKey(prop, s=True) #delete key command
        prop_children = cmds.listRelatives(prop, type = "transform", allDescendents = True, f = True)
        if prop_children:
            for child in prop_children:
                cmds.cutKey(child, s=True) #delete key command

    def find_parent(self, prop, export_set):
        cmds.select(export_set)
        export_props_longname = cmds.ls(sl = True, l = True)
        parents = cmds.listRelatives(prop, parent=True, fullPath=True, f = True)
        if parents == None:
            prop_parent = ["root"]
        else:
            #if parents[0] in export_props_longname: # => True
            prop_parent = parents[0].split("|")
            #else:
            #    prop_parent = ["root"]
        return(prop_parent[-1])
    
    def is_group(self, node):
        children = node.getChildren()
        for child in children:
            if type(child) is not pymel.core.nodetypes.Transform:
                return False
        return True

    def get_geo_name(self, prop, prepostfix):
    
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

    def export_static_fbx(self, polysmooth, do_combine, set_to_origin) :
        export_collection_longname = cmds.ls(sl = True, l = True)
        
        self.env_fbx_export_settings()
        path = self.set_export_path()
        
        sceneName = self.get_scene_name()
        exportName = ("")
    

        for prop in export_collection_longname:
            self.delete_keys(prop)
            cmds.makeIdentity(prop, apply=True, translate=True )
            if set_to_origin:
                self.move_to_origin(prop)
            cmds.select(prop)
            
            sel = cmds.ls(sl = True)
            if do_combine:
                self.merge_static_meshes(prop)
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
            asset_name = self.get_geo_name(prop, "prop")
            export_name = ("sm_" + asset_name)

            self.log_output("Exporting :{}".format(export_name))
            cmds.select(prop)
            export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
            mel.eval(export_command)


    # getting attributes to write to json
    def get_prop_attr(self, export_props):
        asset_name = self.get_asset_name()

        count = 0
        prop_dictionary = []
        prop_dictionary.append({'game_path': '/Game/assets/environments/' + asset_name + '/components/'})
        for prop in export_props:
            namespace = self.get_geo_name(prop, "namespace")
            prop_name = self.get_geo_name(prop, "prop")
            prop_parent = self.find_parent(prop, export_props)

            parent_list = []
            check_parent = True
            if prop_parent == 'root':
                check_parent = False
            else:
                parent_list.append(prop_parent)
                while check_parent:
                    prop_parent = self.find_parent(prop_parent, export_props)
                    
                    if prop_parent == 'root':
                        check_parent = False
                    else:
                        parent_list.append(prop_parent)
                        
            if len(parent_list) == 0:
                parent_list.append('root')

            parent_rx = 0
            parent_ry = 0
            parent_rz = 0
            
            if parent_list[0] == 'root':
                pass
            else:
                for parent in parent_list:
                    parent_rx += cmds.getAttr(parent + ".rotateX")
                    parent_ry += cmds.getAttr(parent + ".rotateY")
                    parent_rz += cmds.getAttr(parent + ".rotateZ")

            self.log_output("pub: processing {} ".format(prop))
            self.delete_keys(prop)
            sx = cmds.getAttr(prop + ".scaleX")
            sy = cmds.getAttr(prop + ".scaleY")
            sz = cmds.getAttr(prop + ".scaleZ") 
            cmds.setAttr((prop + ".scaleX"), 1)
            cmds.setAttr((prop + ".scaleY"), 1)
            cmds.setAttr((prop + ".scaleZ"), 1)
                    
            cmds.makeIdentity(prop , apply = True, translate = True, rotate = False, scale = False)
                    
            world_pivot = self.get_world_pivot(prop)
                        
            tx = world_pivot[0]
            ty = world_pivot[1]
            tz = world_pivot[2]
            rx = cmds.getAttr(prop + ".rotateX")
            ry = cmds.getAttr(prop + ".rotateY")
            rz = cmds.getAttr(prop + ".rotateZ")
            cmds.setAttr((prop + ".scaleX"), sx)
            cmds.setAttr((prop + ".scaleY"), sy)
            cmds.setAttr((prop + ".scaleZ"), sz)                                          
                
            if len(namespace) > 0:
                dictionary = {'name':('sm_' + prop_name), 'tx':tx, 'ty':ty, 'tz':tz, 'rx':(rx + parent_rx), 'ry':(ry + parent_ry), 'rz':(rz + parent_rz), 'sx':sx, 'sy':sy, 'sz':sz, 'fullname':(prop + '_' + namespace), 'parent':prop_parent}
            else:
                dictionary = {'name':('sm_' + prop_name), 'tx':tx, 'ty':ty, 'tz':tz, 'rx':(rx + parent_rx), 'ry':(ry + parent_ry), 'rz':(rz + parent_rz), 'sx':sx, 'sy':sy, 'sz':sz, 'fullname':(prop), 'parent':prop_parent}
            prop_dictionary.append(dictionary)
            
        return(prop_dictionary)

    def get_rig_attr(self, export_assets):
        asset_name = self.get_asset_name()
            
        rig_dictionary = []
        rig_dictionary.append({'game_path': '/Game/assets/characters/' + asset_name + '/components/fbx/'})

        return(rig_dictionary)

    def disconnectAll(self, node, source, destination):
        connectionPairs = []
        if source:
            conns = cmds.listConnections(node, plugs=True, connections=True, destination=False)
            if conns:
                connectionPairs.extend(zip(conns[1::2], conns[::2]))
        
        if destination:
            conns = cmds.listConnections(node, plugs=True, connections=True, source=False)
            if conns:
                connectionPairs.extend(zip(conns[::2], conns[1::2]))
        
        for srcAttr, destAttr in connectionPairs:
            cmds.disconnectAttr(srcAttr, destAttr)

    def breakAnimCurveConnections(self, export_collection):
        cmds.select(cl = True)
        cmds.select(export_collection)
        sel = cmds.ls(sl=True, l=True, type=('transform'))
        for group in sel:
            
            heirarchy = cmds.listRelatives( group, f=True, ad=True, type=('transform') )
            animcurves = cmds.listConnections(group, t='animCurve')
            if animcurves:
                for animcurve in animcurves:
                    self.disconnectAll(animcurve, True, True)

            if heirarchy:
                for obj in heirarchy:
                    animcurves = cmds.listConnections(obj, t='animCurve')
                    if animcurves:
                        for animcurve in animcurves:
                            self.disconnectAll(animcurve, True, True)
                    
            else:
                self.log_output('no children')
    

    #json
    def write_json_file(self, export_type, export_assets):
        json_filename = (self.get_scene_name() + ".json") 
        self.log_output("Hurlie: exporting {}, json: {}, path: {}".format(self.get_scene_name(), json_filename, self.get_scene_path()))
        # MayaAssetHandler: Hurlie: exporting SDMP_HeroPupA_Ri_v11, json: SDMP_HeroPupA_Ri_v11.json, path: C:/Users/pniemandt.STUDIO/Downloads
        json_dir = "{}/cache/".format(self.get_scene_path())
        self.log_output("Hurlie: Target: {}".format(json_dir))

        if not os.path.exists(json_dir):
            os.makedirs(json_dir, mode=0o777, exist_ok=False)
            
        with open(json_dir + json_filename, 'w') as json_file:
            if export_type == "env":
                asset_dictionary = self.get_prop_attr(export_assets)

            if export_type == "rig":
                asset_dictionary = self.get_rig_attr(export_assets)

            json.dump(asset_dictionary,json_file , indent=4)

    # execution

    def export_selected_staticmesh_env(self):
        export_collection = cmds.ls(sl = True)
        self.breakAnimCurveConnections(export_collection)
        self.write_json_file("env", export_collection)
        #self.breakAnimCurveConnections(export_collection)
        self.export_static_fbx(False, True, True)

    def export_character_seperate_shadow_meshes(self):
        ri_sets = self.get_ri_set()
        for ri_set in ri_sets:
            cmds.select(ri_set)
            ri_selection = cmds.ls(sl = True)
            export_collection = ri_selection
            no_shadow_collection = []
            shadow_collection = []

            for obj in ri_selection:
                
                if "whiskars" in obj or "eyelashes" in obj:
                    no_shadow_collection.append(obj)
                    print(obj + " whiskars")

                if "jnt_org" in obj:
                    print(obj + " jnt_org")
                    no_shadow_collection.append(obj)
                    shadow_collection.append(obj)

                if "whiskars" not in obj and "eyelashes" not in obj and "jnt_org" not in obj:
                    print(obj + " NO_whiskars")
                    shadow_collection.append(obj)
            
            self.write_json_file("rig", ri_set)
            self.export_skeletal_fbx(True, shadow_collection, "shadow")
            self.export_skeletal_fbx(True, no_shadow_collection, "no_shadow")
            
            
    def export_rig_chr(self):
        ri_sets = self.get_ri_set()
        for ri_set in ri_sets:
            cmds.select(ri_set)
            ri_selection = cmds.ls(sl = True)
            export_collection = ri_selection

            self.write_json_file("rig", export_collection)
            do_polySmooth = False
            self.export_skeletal_fbx(do_polySmooth, ri_set, "shadow")
	
    def get_root_grp(self, sel):
        node_path = cmds.listRelatives(sel[0], path = True, f = True)
        root = node_path[0].split('|')
        asset_name = root[1].split('_')

        return(asset_name[0])

    def get_asset_root_name(self, fbx_set):
        if cmds.referenceQuery(fbx_set, isNodeReferenced = True):
            namespace = fbx_set.split(':')
            asset_name = namespace[0].split('_')
            chr_name = (asset_name[2] + '_' + asset_name[3])
            

        else:
            cmds.select(fbx_set)
            sel = cmds.ls(sl = True)
            root_grp = self.get_root_grp(sel)
            chr_name = root_grp            

        return(chr_name)

    def export_fbx_chr_pose(self, fbx_set, polysmooth):
        cmds.select(fbx_set)
        fbx_selection = cmds.ls(sl = True)
        path = self.set_export_path()
        asset_name = self.get_asset_root_name(fbx_set)
        scene_name = self.get_scene_name()
        export_name = ('{}_{}_fbx'.format(scene_name, asset_name))
        self.import_all_references()

        if polysmooth:
            for geo in fbx_selection:
                shapenode = cmds.listRelatives( geo, ni = True, shapes=True )
                if shapenode:
                    cmds.select(shapenode)
                    mel.eval("polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 1 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 {};".format(geo))
                    cmds.select(geo)
                    delete_nondefhist_command = ("doBakeNonDefHistory( 1, {\"prePost\" });")
                    mel.eval(delete_nondefhist_command)
        
        cmds.select(fbx_set, r = True)
        export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
        mel.eval(export_command)

    def import_all_references(self):
        all_ref_paths = cmds.file(q=True, reference=True) or []  # Get a list of all top-level references in the scene.

        for ref_path in all_ref_paths:
            if cmds.referenceQuery(ref_path, isLoaded=True):  # Only import it if it's loaded, otherwise it would throw an error.
                cmds.file(ref_path, importReference=True)  # Import the reference.

                new_ref_paths = cmds.file(q=True, reference=True)  # If the reference had any nested references they will now become top-level references, so recollect them.
                if new_ref_paths:
                    for new_ref_path in new_ref_paths:
                        if new_ref_path not in all_ref_paths:  # Only add on ones that we don't already have.
                            all_ref_paths.append(new_ref_path)


    def export_anim_animation(self):
        fbx_sets = self.get_fbx_set()
        polySmooth = False
        self.pose_fbx_export_settings(True)
        for fbx_set in fbx_sets:
            self.export_fbx_chr_pose(fbx_set, polySmooth)

    def export_anim_pose(self):
        fbx_sets = self.get_fbx_set()
        polySmooth = True
        self.pose_fbx_export_settings(False)
        for fbx_set in fbx_sets:
            self.export_fbx_chr_pose(fbx_set, polySmooth)

