import os

import maya.cmds as cmds
import maya.mel as mel

from wildchildanimation.maya.swing_maya import SwingMaya

'''
    Exports Scene Cameras

    Author: Derik vd Berg

'''

class Camera_Export(SwingMaya):

    NAME = "Camera_Export"
    VERSION = "0.0.8"

    def __init__(self):
        super(Camera_Export, self).__init__()

        self.log_output("{} v{}".format(self.NAME, self.VERSION))

    def make_dir(self, path):
        """
        input a path to check if it exists, if not, it creates all the path
        :return: path string
        """
        if not os.path.exists(path):
            os.makedirs(path)
        return path        

    def export(self):
        path = (self.get_scene_path() + 'cache/camera/')
        self.make_dir(path) 

        print('Export path : ' + path)   
        all_shots = cmds.ls(type = 'shot')
        for shot_name in all_shots:
            shot_start = cmds.getAttr(shot_name + ".startFrame")
            shot_end = cmds.getAttr(shot_name + ".endFrame")
            shot_cam = cmds.listConnections(shot_name + ".currentCamera") 

            # cam_trans = cmds.listRelatives(shot_cam,p = True)
            
            #Set camera settings
            cmds.setAttr ((shot_cam[0] + '.horizontalFilmAperture'), 1.417)
            cmds.setAttr ((shot_cam[0] + '.verticalFilmAperture'), 0.79725)

            #Set fbx settings
            self.fbxSettings(shot_end, shot_start)
            print(shot_cam[0])
            shotExportCam = self.prepCam(shot_cam[0], shot_start,shot_end)
            
            cmds.currentTime(shot_start)
            cmds.select(shotExportCam,replace = True)
            cmds.setKeyframe()
            cmds.currentTime(shot_end)
            cmds.setKeyframe()

            #cmds.bakeResults(str(shot_cam[0]), t=(shot_start,shot_end), sb=1 )
            cam_animcurves = cmds.listConnections(shotExportCam, t="animCurve")
            
            camshapes = cmds.listRelatives(shotExportCam, shapes=True)
            camshape_animcurves = cmds.listConnections(camshapes[0], t="animCurve")
            
            for animcurve in cam_animcurves:
                cmds.select(animcurve)
                cmds.keyframe(edit=True,iub= False ,an = 'objects', o = 'move',fc = 0, relative=True,timeChange=-(shot_start),time=((-500),(5000000)))
                frontcut_start = -5000
                frontcut_end = -1
                backcut_start = shot_end - shot_start + 1
                backcut_end = 10000000
                cmds.cutKey( time=(frontcut_start,frontcut_end), clear = True )
                cmds.cutKey( time=(backcut_start,backcut_end), clear = True )
                
            for animcurve in camshape_animcurves:
                cmds.select(animcurve)
                cmds.keyframe(edit=True,iub= False ,an = 'objects', o = 'move',fc = 0, relative=True,timeChange=-(shot_start),time=((-500),(5000000)))
                frontcut_start = -5000
                frontcut_end = -1
                backcut_start = shot_end - shot_start + 1
                backcut_end = 10000000
                cmds.cutKey( time=(frontcut_start,frontcut_end), clear = True )
                cmds.cutKey( time=(backcut_start,backcut_end), clear = True )
            
            cmds.playbackOptions(animationStartTime=0, minTime=0, animationEndTime=(shot_end - shot_start), maxTime=(shot_end - shot_start))

            cmds.select(shotExportCam)
            
            mel.eval('FBXExport -f "' + path + str(shotExportCam) + '.fbx" -s;')
            cmds.delete(shotExportCam)
            cmds.rename((shot_cam[0] + '_anim'), shot_cam[0])


    def prepCam(self, shotCam, shot_start, shot_end):
        cmds.rename((shotCam), (shotCam + '_anim'))
        exportCam = cmds.duplicate ((shotCam + '_anim'))
        camAttr = cmds.listAttr(exportCam[0], k = True)

        for attr in camAttr:
            cmds.setAttr((exportCam[0] + '.' + attr), lock = 0)
        
        try:
            cmds.parent(exportCam, world = True)
        except:
            print ('Already on Root')
        
        child = ['']
        child = cmds.listRelatives(exportCam[0],c = True, typ = 'transform', f = True)
        #length = 0
        try:
            #length = len(child)
            for i in child:
                cmds.delete(i)
        except:
            print ('no children in camera')

        #mel.eval('doCreateParentConstraintArgList 1 { "1","0","0","0","0","0","0","0","1","","1" };')

        constraintNode = cmds.parentConstraint((shotCam +'_anim'),exportCam[0], mo = True, weight = 1)
        cmds.connectAttr((shotCam + '_anim.focalLength'), (exportCam[0] + '.focalLength'))
        cmds.bakeResults( exportCam[0], t=(shot_start,shot_end), s=True )
        cmds.delete(constraintNode)
        exportCam = cmds.rename(exportCam[0], shotCam)
        
        #cmds.rename((shotCam +'_anim'), shotCam)
        return exportCam
        
    def fbxSettings(self, shot_end, shot_start):
        mel.eval('FBXExportCameras -v 1')
        mel.eval('FBXExportBakeComplexAnimation -v "True";')
        mel.eval('FBXExportBakeComplexEnd -v ' + str(shot_end) + ';')
        mel.eval('FBXExportBakeComplexStart -v ' + str(shot_start) + ';')
        mel.eval('FBXExportBakeComplexStep -v 1;')
        mel.eval('FBXExportSmoothingGroups -v 1;')
        mel.eval('FBXExportAnimationOnly -v 0;')
        mel.eval('FBXExportApplyConstantKeyReducer -v 0;')
        mel.eval('FBXExportAxisConversionMethod "convertAnimation";')
        mel.eval('FBXExportCacheFile -v 0;')
        mel.eval('FBXExportConstraints -v 0;')
        mel.eval('FBXExportEmbeddedTextures -v 0;')
        mel.eval('FBXExportFileVersion -v FBX201800')
        mel.eval('FBXExportGenerateLog -v 1;')
        mel.eval('FBXExportHardEdges -v 0;')
        mel.eval('FBXExportInAscii -v 1;')
        mel.eval('FBXExportInputConnections -v 1;')
        mel.eval('FBXExportInstances -v 0;')
        mel.eval('FBXExportLights -v 1;')
        mel.eval('FBXExportQuaternion -v euler;')
        mel.eval('FBXExportReferencedAssetsContent -v 1;')
        mel.eval('FBXExportScaleFactor 1;')
        mel.eval('FBXExportShapes -v 1;')
        mel.eval('FBXExportSkeletonDefinitions -v 1;')
        mel.eval('FBXExportSkins -v 1;')
        mel.eval('FBXExportSmoothMesh -v 1;')
        mel.eval('FBXExportTangents -v 1;')
        mel.eval('FBXExportTriangulate -v 0;')
        mel.eval('FBXExportUpAxis y;')
        mel.eval('FBXExportUseSceneName -v 0;')
