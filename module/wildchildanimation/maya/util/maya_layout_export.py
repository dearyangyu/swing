import os

import pymel
import maya.cmds as cmds
import maya.mel as mel

import json

from wildchildanimation.maya.swing_maya import SwingMaya

class MayaLayoutHandler(SwingMaya):

    NAME = 'MayaAnimationHandler'
    VERSION = '1.0'

    

    def __init__(self):
        super(MayaLayoutHandler, self).__init__()
        self.log_output("{} v{}".format(self.NAME, self.VERSION))   

    def set_export_path(self, type) :
        path = self.get_scene_path()

        #Create a new directory path
        if not os.path.exists("{}/cache/{}".format(path,type)):
            os.makedirs("{}/cache/{}".format(path,type))

        return ("{}/cache/{}".format(path,type))

    def cam_fbx_export_settings(self, startframe, endframe):
        mel.eval("FBXExportCameras -v 1;")
        mel.eval('FBXExportBakeComplexAnimation -v "True";')
        mel.eval('FBXExportBakeComplexEnd -v ' + str(startframe) + ';')
        mel.eval('FBXExportBakeComplexStart -v ' + str(endframe) + ';')
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
    
    def get_all_sequencer_shots(self):
        shots = cmds.ls(type='shot')
        return(shots)

    def get_sequencer_shot_camera(self, shot):
        camera = cmds.shot(shot, cc = True, q = True)
        return(camera)

    def get_sequencer_shot_startendframe(self, shot):
        startframe = cmds.shot(shot, startTime = True, q = True)
        endframe = cmds.shot(shot, endTime = True, q = True)
        return(startframe, endframe)

    def get_sequencer_shot_seq_startendframe(self, shot):
        seq_startframe = cmds.shot(shot, sequenceStartTime = True, q = True)
        seq_endframe = cmds.shot(shot, sequenceEndTime = True, q = True)
        return(seq_startframe, seq_endframe)

    def bake_to_keys(self, object, bake_shape, framerange):
        cmds.bakeResults(object, simulation = True, t = (framerange[0],framerange[1]), shape = bake_shape, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
    
    def export_camera_as_fbx(self, fbx_file, shot_camera, startframe, endframe):
        
        self.cam_fbx_export_settings(startframe, endframe)

        cmds.select(shot_camera)
        sel = cmds.ls(sl = True)

        self.log_output("Exporting :{}".format(shot_camera))

        export_command = ('FBXExport -f ("' + fbx_file + '") -s;')
        mel.eval(export_command)        

    def export_camera_as_usda(self, usd_file, shot_camera, startframe, endframe):

        if os.path.exists(usd_file):
            os.remove(usd_file)
        else:
            pass
        cmds.select(shot_camera, r = True)
        self.log_output(usd_file)
        cmds.file(usd_file, force = True, exportSelected = True, preserveReferences = True, type = 'USD Export', options = ';exportUVs=1;exportSkels=auto;exportSkin=auto;exportBlendShapes=1;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=1;staticSingleSample=0;startTime={};endTime={};frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface,MaterialX];exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;materialsScopeName=mtl'.format(startframe, endframe))
        os.rename((usd_file + '.usd'), usd_file)

    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def build_camera_export_path(self, camera, USD_BASE_PATH):
        
        chunks = camera.split('_')
        episode_nr = camera[4] + camera[5] + camera[6]
        episode = chunks[0]
        scene = chunks[1]
        shot = chunks[2]
        task = chunks[3]
        
        shot_path = '{}/{}/{}/camera/'.format(episode, scene, shot)
        path = str.lower(USD_BASE_PATH + shot_path)

        self.create_directory(path)
        
        usd_file_name = '{}_{}_{}_camera.usda'.format(episode, scene, shot)
        fbx_file_name = '{}_{}_{}_camera.fbx'.format(episode, scene, shot)
        return(path, usd_file_name, fbx_file_name)

    def set_framerange_to_origin(self, object, framerange):
        animcurves = cmds.keyframe('SDMP069_020_0010_cam1',query=True,name=True)
        for animcurve in animcurves:
            if 'lensCurve' in animcurve:
                pass
            else:
                keyTimes = cmds.keyframe(animcurve,sl=True,query=True,tc=True)
                cmds.keyframe(animcurve, edit = True, relative = True, timeChange = -(framerange[0]))
        return('0', (framerange[1] - framerange[0]))        

    def create_export_camera(self, shot_camera):
        cmds.select(shot_camera)
        export_camera = cmds.duplicate(rr = True)
        cmds.rename(shot_camera, (shot_camera + '_anim'))
        cmds.rename(export_camera, shot_camera)
        try:
            cmds.parent(shot_camera, w = True)
        except:
            self.log_output('{} already in root'.format(shot_camera))
        cmds.parentConstraint( (shot_camera + '_anim'), shot_camera )



    # execution

    def export_lo_cameras(self):
        USD_BASE_PATH = 'S:/productions/sdmp/sdmp_build/episodes/'
        sequencer_shots = self.get_all_sequencer_shots()
        for sequencer_shot in sequencer_shots:
            shot_camera = self.get_sequencer_shot_camera(sequencer_shot)
            framerange = self.get_sequencer_shot_startendframe(sequencer_shot)
            seq_framerange = self.get_sequencer_shot_seq_startendframe(sequencer_shot)

            #delete sequencer_shot
            cmds.delete(sequencer_shot)
            export_camera = self.create_export_camera(shot_camera)
            self.bake_to_keys(shot_camera, True, framerange)
            unit_framerange = self.set_framerange_to_origin(shot_camera, framerange)
            file_data = self.build_camera_export_path(shot_camera, USD_BASE_PATH)
            
            usd_file = file_data[0] + file_data[1]
            fbx_file = file_data[0] + file_data[2]
            self.export_camera_as_usda(usd_file, shot_camera, unit_framerange[0], unit_framerange[1])
            self.export_camera_as_fbx(fbx_file, shot_camera, unit_framerange[0], unit_framerange[1])

