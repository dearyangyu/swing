import maya.cmds as cmds

# show's lenses for Lenskit  
lensKit = [14,22,32,40,55,80,135,180,240]    


#Find all non default cameras in the scene
def findAllCameras():
    allCams = cmds.ls(type='camera')
    seqCams = []
    for cam in allCams:
        if cam.find('persp') != -1:
            pass
        elif cam.find('top') != -1:
            pass 
        elif cam.find('front') != -1:
            pass
        elif cam.find('side') != -1:
            pass  
        else:
            seqCams.append(cam)    
    return(seqCams)

#Build a lenskit and set focalLength to closet currently set focalLenght
#Also sets all needed camera settings
def setupCamera(seqShots, image_path):
    #build focalLegnth lenskit
    lensKitString = ''
    lensKitString = str('')
    for lens in lensKit:
        lensKitString = lensKitString + (str(lens) + ':')
        
    lensKitString = lensKitString.rstrip(lensKitString[-1])
    print('Current lens kit : ' + lensKitString)
    for seqshot in seqShots:
        camTransform = cmds.listConnections( ("{}.currentCamera".format(seqshot)), d=False, s=True )
        #camTransform = cmds.listRelatives(cam, parent=True)
        cam = cmds.listRelatives(camTransform, shapes = True)
        animCurve = cmds.createNode('animCurveTL',n = (cam[0] + 'lensCurve'), ss=True)
        cmds.setKeyframe(animCurve, t=0, v=14, itt='linear', ott='linear')
        
        focal = getClosestFocal(cam[0])
        
        count = 0
        lensIndex = 0
        
        for lens in lensKit:
            cmds.setKeyframe(animCurve, t=count, v=lens, itt='linear', ott='linear')
            if lens == focal:
                lensIndex = count
            count = count +1
        try:
            cmds.addAttr(camTransform[0],ln = 'lensKit', at = 'enum', en = lensKitString)
        except:
            print("could not create Lenskit attribute for {} .. It may already exist".format(camTransform[0]))
        cmds.setAttr ((camTransform[0] + '.lensKit'),e = True, keyable = True)
        cmds.setAttr ((camTransform[0] + '.lensKit'), lensIndex)
        
        try:
            cmds.connectAttr((camTransform[0] + '.lensKit'),(animCurve + '.input'))
        except:
            print("{} Lenskit already connected".format(camTransform[0]))
        try:
            cmds.connectAttr((animCurve + '.output'),(cam[0] + '.focalLength'))
        except:
            print("{} Focal length already connected".format(cam[0]))
        
        #set camera filmback and gate masks
        cmds.setAttr ((camTransform[0] + '.verticalFilmAperture'), 0.79725)
        cmds.setAttr ((camTransform[0] + '.displayFilmGate'), 1)
        cmds.setAttr ((camTransform[0] + '.displayGateMask'), 1)
        cmds.setAttr ((camTransform[0] + '.displaySafeAction'), 1)
        
        #set far clip plane
        cmds.setAttr ((cam[0] + '.nearClipPlane'), 1)
        cmds.setAttr ((cam[0] + '.farClipPlane'), 1000000)
        #set the camera locator scale to make it appear larger in view
        cmds.setAttr ((cam[0] + '.locatorScale'), 10)
        
        #Create imageplane on currentCamera and place in corner
        ip = cmds.imagePlane(camera=cam[0],w = 16, h = 9, lt = True, sia = False)
        ipsx = cmds.getAttr(ip[1] + '.sizeX')
        ipsy = cmds.getAttr(ip[1] + '.sizeY')
        cmds.setAttr((ip[1] + '.depth'), 10)
        cmds.setAttr((ip[1] + '.offsetX'), -0.46)
        cmds.setAttr((ip[1] + '.offsetY'), 0.25)
        cmds.setAttr((ip[1] + '.sizeX'), (ipsx * 0.3))
        cmds.setAttr((ip[1] + '.sizeY'), (ipsy * 0.3))
        cmds.setAttr((ip[1] + '.alphaGain'), 0.5)

        
        assign_image_to_imageplane(ip[1],seqshot)
        cmds.setAttr((ip[1] + ".useFrameExtension"), 1)

        #parent camera to CAMERAS group
        try:
            cmds.parent( camTransform[0], "|CAMERAS" )
        except:
            print("could not parent {} to CAMERAS group".format(camTransform[0]))
        
def assign_image_to_imageplane(imageplane,seqshot):
    start_frame = cmds.getAttr("{}.startFrame".format(seqshot))  # Query shot's start frame.
    end_frame = end_frame = cmds.getAttr("{}.endFrame".format(seqshot))  # Query shot's end frame.
    cmds.setAttr((imageplane + ".imageName"),image_path ,type = "string" )
    cmds.currentTime(start_frame)
    cmds.setAttr(imageplane + ".frameExtension", 0)
    cmds.setKeyframe(imageplane + ".fe", inTangentType = "linear", outTangentType = "linear")
    cmds.currentTime(end_frame)
    cmds.setAttr(imageplane + ".frameExtension", (end_frame - start_frame))
    cmds.setKeyframe(imageplane + ".fe", inTangentType = "linear", outTangentType = "linear")
    cmds.selectKey(imageplane, at = "fe", r = True, k = True, time = (start_frame , end_frame))
    cmds.keyTangent(itt = "linear", ott = "linear")        
        
        
#function to get the closets focalLenth available in the lenskit
def getClosestFocal(seqCam): 
    focal = cmds.getAttr(str(seqCam) + '.focalLength')
    return lensKit[min(range(len(lensKit)), key = lambda i: abs(lensKit[i]-focal))]

#create layout groups
def createGroups():
    cmds.createNode('transform' , name = 'CAMERAS')
    cmds.createNode('transform' , name = 'ENVIRONMENT')
    cmds.createNode('transform' , name = 'PROPS')
    cmds.createNode('transform' , name = 'PROXY')
         
#Sets the scene settings like fps etc.
def setScene():
    cmds.currentUnit( time='pal' )
    cmds.setAttr('defaultResolution.width',1920)
    cmds.setAttr('defaultResolution.height',1080)


#Main execution part 
# get all sequencer shot nodes to set camera settings on       
seqShots = cmds.ls(type = "shot")   

#localization
image_path = ("Z:/productions/wotw/witw_post/master_output/witw_129cmn/old_exports/exports/witw_129cmn_sc010_sh030/images/witw_129cmn_sc010_sh030.0000.jpg")
#start and end frame - get these from sequencer node

createGroups()
setupCamera(seqShots, image_path)
setScene()
