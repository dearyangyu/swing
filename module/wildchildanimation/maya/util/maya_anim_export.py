import os

import pymel
import maya.cmds as cmds
import maya.mel as mel

import json

'''
    ########################################################################################
    #Derik's added functions to Swing

    def check_referenced_anim_curve_lockstate(self):
        is_ref_files_locked = cmds.optionVar(q = 'refLockEditable')
        return is_ref_files_locked

    def unlock_referenced_anim_curves(self):
        cmds.optionVar( iv=('refLockEditable', False))

    def lock_referenced_anim_curves(self):
        cmds.optionVar( iv=('refLockEditable', True))
        
    def bake_to_keys(self, object, bake_shape, startframe, endframe):
        cmds.bakeResults(object, simulation = True, t = (startframe,endframe), shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
    
    #End of Derik's added functions
    ########################################################################################'''
from wildchildanimation.studio.utils.asset_utils import get_server_path
from wildchildanimation.maya.swing_maya import SwingMaya

class MayaAnimationHandler(SwingMaya):

    NAME = 'MayaAnimationHandler'
    VERSION = '1.0'

    def __init__(self):
        super(MayaAnimationHandler, self).__init__()
        self.log_output("{} v{}".format(self.NAME, self.VERSION))   

    def set_export_path(self, type) :
        path = self.get_scene_path()

        #Create a new directory path
        if not os.path.exists("{}/cache/{}".format(path,type)):
            os.makedirs("{}/cache/{}".format(path,type))

        return ("{}/cache/{}/".format(path,type))

    def cam_fbx_export_settings(self):

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

    def anim_fbx_export_settings(self, anim):
        
        if anim:
            start_frame, end_frame, timline_start, timeline_end = self.get_scene_framerange()
            
        
        else:
            start_frame = cmds.currentTime(q = True)
            end_frame = start_frame

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

    def build_scene_name_prefix(self):
        try:
            proj, ep, scene, shot = self.get_shot_name_from_scene_name()
            scene_name_prefix = ('{}_{}_{}_{}'.format(proj, ep, scene, shot))
        except:
            scene_name_prefix = self.get_scene_name()
        return(scene_name_prefix)

    def export_camera_fbx(self, polysmooth, export_set):
        
        self.skel_fbx_export_settings()
        path = '{}'.format(self.get_scene_path())
        
        scene_name_prefix = self.build_scene_name_prefix()
        exportName = ("")

        cmds.select(export_set)
        sel = cmds.ls(sl = True)

        #asset_name = self.get_asset_name()
        export_name = ("{}_cam".format(scene_name_prefix))
        self.log_output("Exporting :{}".format(exportName))
        cmds.select(export_set)
        export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
        mel.eval(export_command)

    def export_animation_fbx(self, export_set, polysmooth, asset_type, range):
        
        if range == 'anim':
            self.anim_fbx_export_settings(True)
        if range == 'pose':
            self.anim_fbx_export_settings(False)
        
        path = self.set_export_path('fbx')
        
        exportName = ("")
        
        cmds.select(export_set)
        sel = cmds.ls(sl = True)
        if polysmooth:
            self.smooth_meshes(sel)

        scene_name_prefix = self.build_scene_name_prefix()
        asset_name = self.get_anim_asset_name(export_set)
        #export_name = ("{}_sk_{}".format(scene_name_prefix, asset_name))
        export_name = ("an_{}".format(asset_name))
        self.log_output("Exporting :{}".format(exportName))
        cmds.select(export_set)
        export_command = ('FBXExport -f ("' + str(path) + str(export_name) + '.fbx") -s;')
        mel.eval(export_command)
    
    def smooth_meshes(self, meshes):
        print(meshes)
        for mesh in meshes:
                shapenode = cmds.listRelatives(mesh, ni = True, shapes=True , type = 'mesh')
                if shapenode:
                    cmds.select(shapenode)
                    mel.eval("polySmooth  -mth 0 -sdt 2 -ovb 1 -ofb 3 -ofc 0 -ost 0 -ocr 0 -dv 1 -bnr 1 -c 1 -kb 1 -ksb 1 -khe 0 -kt 1 -kmb 1 -suv 1 -peh 0 -sl 1 -dpe 1 -ps 0.1 -ro 1 -ch 1 {};".format(mesh))
                    cmds.select(mesh)
                    print('smoothing : {}'.format(mesh))
                    delete_nondefhist_command = ("doBakeNonDefHistory( 1, {\"prePost\" });")
                    mel.eval(delete_nondefhist_command)

    def get_all_sequencer_shots(self):
        shots = cmds.ls(type='shot')
        return(shots)

    def get_sequencer_shot_camera(self, shot):
        camera = cmds.shot(shot, cc = True, q = True)
        return(camera)

    def get_sequencer_shot_startframe(self, shot):
        startframe = cmds.shot(shot, startTime = True, q = True)
        return(startframe)

    def get_sequencer_shot_endframe(self, shot):
        endframe = cmds.shot(shot, endTime = True, q = True)
        return(endframe)

    def get_sequencer_shot_seq_startframe(self, shot):
        seq_startframe = cmds.shot(shot, sequenceStartTime = True, q = True)
        return(seq_startframe)

    def get_sequencer_shot_seq_endframe(self, shot):
        seq_endframe = cmds.shot(shot, sequenceEndTime = True, q = True)
        return(seq_endframe)

    def get_asset_name(self, fbx_set):
        #scene_name = self.get_scene_name()
        #asset_name = scene_name.split("_")
        ns = fbx_set.split(':')
        asset = ns[-1].split('_')[0]
        #ns_nr = ns[-2].split('_')[-1]
        #print(fbx_set)
        return('{}'.format(asset))

    def get_anim_asset_name(self, fbx_set):
        scene_name = self.get_scene_name()
        proj, ep, scene, shot = self.get_shot_name_from_scene_name()
        asset_name = scene_name.split("_")
        ns = fbx_set.split(':')
        asset = ns[-1].split('_')[0]
        ns_nr = ns[-2].split('_')[-1]
        print(fbx_set)
        return('{}_{}_{}_{}_{}_{}'.format(proj, ep, scene, shot, asset,ns_nr))

    def bake_joints_to_keys(self, fbx_set, hi_setting, bake_shape, startframe, endframe):
        #cmds.bakeResults(object, simulation = True, hi = 'below', t = (startframe,endframe), shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
        cmds.select(fbx_set)
        sel = cmds.ls(sl = True)
        for s in sel:
            #cmds.bakeResults(s, simulation = True, hi = 'below', t = (0,186), shape = False, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
            if hi_setting == 'below':
                try:
                    cmds.bakeResults(s, simulation = True, hi = hi_setting, t = (startframe,endframe), at = ['tx','ty','tz','rx','ry','rz','sx','sy','sz'], shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
                except:
                    print('Exception :{}'.format(s))
            
            else:
                try:
                    cmds.bakeResults(s, simulation = True, t = (startframe,endframe), at = ['tx','ty','tz','rx','ry','rz','sx','sy','sz'], shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
                except:
                    print('Exception :{}'.format(s))
                rel = cmds.listRelatives(s,ad = True, type = ['joint','transform'])

                if rel:
                    for r in rel:
                        cmds.select(r,r = True)
                        try:
                            cmds.bakeResults(r, simulation = True, t = (startframe,endframe), at = ['tx','ty','tz','rx','ry','rz','sx','sy','sz'], shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
                        except:
                            try:
                                cmds.bakeResults(r, simulation = True, t = (startframe,endframe), at = ['tx','ty','tz','rx','ry','rz','sx','sy','sz'], shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
                            except:
                                print('Exception :{}'.format(r))

    def export_selected_as_usda(self, usd_file, startframe, endframe):

        if os.path.exists(usd_file):
            os.remove(usd_file)
        else:
            pass

        cmds.file(usd_file, force = True, exportSelected = True, preserveReferences = True, type = 'USD Export', options = ';exportUVs=1;exportSkels=auto;exportSkin=auto;exportBlendShapes=1;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=1;staticSingleSample=0;startTime={};endTime={};frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface,MaterialX];exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;materialsScopeName=mtl'.format(startframe, endframe))
        os.rename((usd_file + '.usd'), usd_file)

    '''def export_selected_as_usda(self, usd_file, startframe, endframe):

        path = self.set_export_path('usd')
        
        sceneName = self.get_scene_name()

        if os.path.exists(usd_file):
            os.remove(usd_file)
        else:
            pass

        cmds.file(usd_file, force = True, exportSelected = True, preserveReferences = True, type = 'USD Export', options = ';exportUVs=1;exportSkels=auto;exportSkin=auto;exportBlendShapes=1;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=1;staticSingleSample=0;startTime={};endTime={};frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface,MaterialX];exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;materialsScopeName=mtl'.format(startframe, endframe))
        os.rename((usd_file + '.usd'), usd_file)'''

    def build_usd_export_path(self):
        scene_name = self.get_scene_name()
        self.log_output(str.lower(scene_name))

    def get_animation_scene_camera(self):
        proj, ep, scene, shot = self.get_shot_name_from_scene_name()
        '''proj = 'wca'
        ep = '00'
        scene = '000'
        shot = '0000'''
        camera_name = ('{}_{}_{}_{}_cam'.format(proj, ep, scene, shot))
        scene_cameras = []
        if cmds.objExists(camera_name):
            return(camera_name)
        else:
            cameras = cmds.ls(type = 'camera')
            for camera in cameras:
                if 'perspShape' in camera or 'sideShape' in camera or 'topShape' in camera or 'frontShape' in camera:
                    pass
                else:
                    scene_cameras.append(camera)
            if len(scene_cameras) > 1:
                print('There are more than one possible cameras in the scene to export.')
                print('please rename the main shot camera to {}_{}_{}_{}_cam')
                return(None)
            if len(scene_cameras) == 1:
                print('Exporting: {}'.format(scene_cameras[0]))
                return(scene_cameras[0])
            else:
                print('There are no usable cameras in the scene, please create a camera with the correct naming to export camera animation')
                print('Naming should follow the following convention:')
                print('"project"_"episode"_"scene"_"shot"_cam   (the _cam at the end should be the postfix)')
                print('eg. : wca_01_001_0010_cam    - this will be the camera for project wca, episode 01, scene 001, shot 0010 (depending on the naming convention set out for the show)')
                return(None)
        
    def get_camera_export_path(self):
        proj, ep, scene, shot = self.get_shot_name_from_scene_name()
        local_path = self.get_scene_path()

        shared_path = '{}/'.format(get_server_path(local_path))
        shared_path_split = shared_path.spilt('/')
        path = ''
        for folder in shared_path_split:
            if folder == proj:
                break
            else:
                path = path + ('{}/'.format(folder))
        export_path = path + '{}/{}_build/episodes/{}_{}/{}/{}/camera/'.format(proj, proj, proj, ep, scene, shot )

        if not os.path.exists(export_path):
            os.makedirs(export_path)

        return(export_path)

    #get export sets - up to 3 nested namespaces
    def get_fbx_export_sets(self):
        export_sets = []    
        export_sets_no_namespace = cmds.ls('*_fbx_set', type = 'objectSet')
        export_sets_one_namespace = cmds.ls('*:*_fbx_set', type = 'objectSet')
        export_sets_two_namespace = cmds.ls('*:*:*_fbx_set', type = 'objectSet')
        export_sets_three_namespace = cmds.ls('*:*:*:*_fbx_set', type = 'objectSet')
        if export_sets_no_namespace:
            export_sets.append(export_sets_no_namespace)
        if export_sets_one_namespace:
            export_sets.append(export_sets_one_namespace)
        if export_sets_two_namespace:
            export_sets.append(export_sets_two_namespace)
        if export_sets_three_namespace:
            export_sets.append(export_sets_three_namespace)
        
        return export_sets[0]

    def get_asset_type(self, fbx_set):
        namespace_name = fbx_set.split(':')
        array_len = len(namespace_name)
        print(array_len)
        if array_len > 1:
            asset_type = namespace_name[-2].split('_')[1]
            return(asset_type)
        else:
            return(None)

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
        if prepostfix == "actor":
            short_name = namespace[-1].split('|')
            if len(namespace) > 1:
                asset_name = (short_name[-1] + '_' + postfix)
            else:
                asset_name = (short_name[-1])
        return(asset_name)

    def get_anim_attr(self, export_assets, sys_path, local_path, export_type):
        
        proj, ep, scene, shot = self.get_shot_name_from_scene_name()
        startframe, endframe, timelinestart, timelineend = self.get_scene_framerange()    
        anim_dictionary = []
        anim_dictionary.append({'file_type': export_type, 'game_path': '/Game/animation/' + ep + '/' + scene + '/' + shot + '/', 'local_path': local_path, 'shared_path': sys_path, 'startframe': startframe, 'endframe': endframe})
        
        for asset in export_assets:
            
            anim_asset_name = self.get_anim_asset_name(asset)
            asset_name = self.get_asset_name(asset)
            asset_type = self.get_asset_type(asset)
            #actor_name = self.get_geo_name(asset_name, "actor")

            dictionary = ({'anim_asset_name': 'an_{}'.format(anim_asset_name),'mayaname': (asset), 'skeleton_name': 'sk_{}_Skeleton'.format(asset_name), 'asset_type': asset_type})
        
        anim_dictionary.append(dictionary)
        return(anim_dictionary, '', '', '', '')

    def write_json_file(self, export_type, export_assets, json_filename):
        startframe, endframe, playbackstart, playbackend = self.get_scene_framerange()
        #json_filename = (self.get_scene_name() + ".json") 
        self.log_output("Wheelbarrow: exporting {}, json: {}, path: {}, startframe: {}, endframe: {}".format(self.get_scene_name(), json_filename, self.get_scene_path(), startframe, endframe))
        # MayaAssetHandler: Wheelbarrow: exporting SDMP_HeroPupA_Ri_v11, json: SDMP_HeroPupA_Ri_v11.json, path: C:/Users/pniemandt.STUDIO/Downloads

        local_path = self.get_scene_path()
        json_dir = "{}/cache/".format(local_path)
        print('json :{}'.format(json_dir))

        shared_path = '{}/'.format(get_server_path(local_path))

        self.log_output("Wheelbarrow: shared path {}, json: {} ".format(shared_path, json_filename))

        self.log_output("Wheelbarrow: Target: {}".format(json_dir))

        if not os.path.exists(json_dir):
            os.makedirs(json_dir, mode=0o777, exist_ok=False)

        with open(json_dir + json_filename, 'w') as json_file:

            if export_type == "anim":
                asset_dictionary = self.get_anim_attr(export_assets, shared_path, json_dir, export_type)

            json.dump(asset_dictionary[0],json_file , indent=4)
            return(json_file)

    # execution

    def export_camera_as_usda(self):
        startframe, endframe, playbackstart, playbackend = self.get_scene_framerange()
        camera = self.get_animation_scene_camera()
        export_path = self.get_camera_export_path()
        cmds.select(camera, r = True)
        usd_file = '{}{}.usda'.format(export_path, camera)
        self.export_selected_as_usda(self, usd_file, startframe, endframe)

    def export_lo_cameras(self):
        sequencer_shots = self.get_all_sequencer_shots()
        for sequencer_shot in sequencer_shots:
            shot_camera = self.get_sequencer_shot_camera(sequencer_shot)
            startframe = self.get_sequencer_shot_startframe(sequencer_shot)
            endframe = self.get_sequencer_shot_endframe(sequencer_shot)
            self.bake_to_keys(shot_camera, True, startframe, endframe)
            self.export_selected_as_usda(self, usd_file, startframe, endframe)

    def export_fbx_animation(self):
        self.set_evaluation_mode("off") #("off" = DG ,  "serial", "serialUncached" and "parallel")
        self.import_references() #import all references for baking process
        self.anim_fbx_export_settings(True) #set Maya FBX export settings
        startframe, endframe, timelinestart, timelineend = self.get_scene_framerange()
        #sceneName = self.get_scene_name()
        fbx_sets = self.get_fbx_export_sets() #get all fbx export setsa (char and rigged props)
        json_filename = (self.get_scene_name() + ".json")
        self.write_json_file("anim", fbx_sets, json_filename)
        for fbx_set in fbx_sets:
            cmds.select(fbx_set, r = True)

            self.bake_joints_to_keys(fbx_set, "below", True, startframe, endframe) # hierarchy options (2nd variable) are ("above," "below", "both," and "none.")
            
            print('Baking done, exporting animation')

            asset_type = self.get_asset_type(fbx_set)
            
            if asset_type == 'char':
                do_polysmooth = True
                self.export_animation_fbx(fbx_set, do_polysmooth, asset_type, 'anim')
            if asset_type == 'prop':
                do_polysmooth = False
                self.export_animation_fbx(fbx_set, do_polysmooth, asset_type, 'anim')

    def export_fbx_pose(self):
        self.set_evaluation_mode("off") #("off" = DG ,  "serial", "serialUncached" and "parallel")
        self.import_references() #import all references for baking process
        self.anim_fbx_export_settings(False) #set Maya FBX export settings
        startframe, endframe, timelinestart, timelineend = self.get_scene_framerange()
        currentframe = cmds.currentTime(q = True)
        #sceneName = self.get_scene_name()
        fbx_sets = self.get_fbx_export_sets() #get all fbx export setsa (char and rigged props)
        json_filename = (self.get_scene_name() + ".json")
        self.write_json_file("anim", fbx_sets, json_filename)
        for fbx_set in fbx_sets:
            cmds.select(fbx_set, r = True)

            self.bake_joints_to_keys(fbx_set, "below", True, startframe, endframe) # hierarchy options (2nd variable) are ("above," "below", "both," and "none.")
            
            print('Baking done, exporting animation')

            asset_type = self.get_asset_type(fbx_set)
            
            if asset_type == 'char':
                do_polysmooth = True
                self.export_animation_fbx(fbx_set, do_polysmooth, asset_type, 'pose')
            if asset_type == 'prop':
                do_polysmooth = False
                self.export_animation_fbx(fbx_set, do_polysmooth, asset_type, 'pose')

    '''
    import maya.cmds as cmds
    import os

    #Localization
    startFrame = 0
    endFrame = 22

    usd_path = 'D:/a/'
    usd_filename = 'bob.usda'
    usd_file = usd_path + usd_filename

    def export_selected_as_usda(self, usd_file, type):
        if os.path.exists(usd_file):
            os.remove(usd_file)
        else:
            print("The file does not exist")

        cmds.file(usd_file, force = True, exportSelected = True, preserveReferences = True, type = 'USD Export', options = ';exportUVs=1;exportSkels=auto;exportSkin=auto;exportBlendShapes=1;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=1;staticSingleSample=0;startTime={};endTime={};frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface,MaterialX];exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;materialsScopeName=mtl'.format(startFrame, endFrame))
        os.rename((usd_file + '.usd'), usd_file)

        print(usd_file)

    self.export_selected_as_usda(usd_file, 'camera')
    '''