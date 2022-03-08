def camexport():
    import maya.cmds as cmds
    import maya.mel as mel

    path = 'Y:/productions/archive/tmp_files/101_test/cameras/layout_export/'

    mel.eval('FBXExportCameras -v 1');
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

    all_shots = cmds.ls(type = 'shot')
    for shot_name in all_shots:
        shot_start = cmds.getAttr(shot_name + ".startFrame")
        shot_end = cmds.getAttr(shot_name + ".endFrame")
        shot_cam = cmds.listConnections(shot_name + ".currentCamera") 
        cam_trans = cmds.listRelatives(shot_cam,p = True)
        
        cmds.currentTime(shot_start)
        cmds.select(shot_cam,replace = True)
        cmds.setKeyframe()
        cmds.currentTime(shot_end)
        cmds.setKeyframe()
        cmds.bakeResults(str(shot_cam[0]), t=(shot_start,shot_end), sb=1 )
        cam_animcurves = cmds.listConnections(shot_cam[0], t="animCurve")
        #print(cam_animcurves)
        camshapes = cmds.listRelatives(shot_cam[0], shapes=True)
        camshape_animcurves = cmds.listConnections(camshapes[0], t="animCurve")
        #print(camshape_animcurves)
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


        cmds.select(shot_cam[0])
        pa = cmds.listRelatives(shot_cam[0], p = True)
        print(pa)
        if pa:
            cmds.parent(w = True)
        
        mel.eval('FBXExport -f "' + path + str(shot_cam[0]) + '.fbx" -s;')