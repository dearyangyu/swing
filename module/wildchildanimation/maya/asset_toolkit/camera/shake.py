import pymel.core as pm

def camera_shake():
    '''Setup camera shaker'''
    pm.undoInfo(openChunk = True,undoName = 'camera_shake')   
    pm.loadPlugin('sineNode.py')
    camera = pm.selected()[-1].name()

    if '|' in camera:        
        pm.warning('Selection\'s name is not unique')
        
    else:
        sineTrans = camera + '_sineTrans'
        noiseTrans = camera + '_noiseTrans'
        noiseRot = camera + '_noiseRot'

        shakeTrans = camera + '_shakeTrans'
        shakeRot = camera + '_shakeRot'

        time = 'time1'

        #Check for keys and add some if there is None
        channels = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']

        for i in channels:
            if not pm.objExists(camera + '_' + i):
                pm.setKeyframe(camera + '.' + i)

        #Create required sine and add nodes
        pm.createNode('sineNode', name = sineTrans)
        pm.connectAttr(time + '.outTime', sineTrans + '.input')

        pm.createNode('sineNode', name = noiseTrans)
        pm.connectAttr(time + '.outTime', noiseTrans + '.input')

        pm.createNode('sineNode', name = noiseRot)
        pm.connectAttr(time + '.outTime', noiseRot + '.input')

        pm.createNode('plusMinusAverage', name = shakeTrans)
        pm.createNode('plusMinusAverage', name = shakeRot)

        #Connect Attributes sine and add nodes
        pm.connectAttr(camera + '_translateX.output',shakeTrans + '.input3D[0].input3Dx')
        pm.connectAttr(camera + '_translateY.output',shakeTrans + '.input3D[0].input3Dy')
        pm.connectAttr(camera + '_translateZ.output',shakeTrans + '.input3D[0].input3Dz')

        pm.connectAttr(sineTrans + '.output', shakeTrans + '.input3D[1]')
        pm.connectAttr(noiseTrans + '.output', shakeTrans + '.input3D[2]')

        pm.connectAttr(camera + '_rotateX.output',shakeRot + '.input3D[0].input3Dx')
        pm.connectAttr(camera + '_rotateY.output',shakeRot + '.input3D[0].input3Dy')
        pm.connectAttr(camera + '_rotateZ.output',shakeRot + '.input3D[0].input3Dz')

        pm.connectAttr(noiseRot + '.output', shakeRot + '.input3D[1]')

        #Add atributes to camera

        extraAttributes = [
                        ['shakeR_X_A',0]
                        ,['shakeR_X_F',0.1]
                        ,['shakeR_Y_A',0]
                        ,['shakeR_Y_F',0.1]
                        ,['shakeR_Z_A',0]
                        ,['shakeR_Z_F',0.1]
                        ,['shakeRNoise',1]

                        ,['shakeT_X_A',0]
                        ,['shakeT_X_F',0.1]
                        ,['shakeT_Y_A',0]
                        ,['shakeT_Y_F',0.1]
                        ,['shakeT_Z_A',0]
                        ,['shakeT_Z_F',0.1]
                        ,['shakeTNoise',1]

                        ,['shakeT2_X_A',0]
                        ,['shakeT2_X_F',0.1]
                        ,['shakeT2_Y_A',0]
                        ,['shakeT2_Y_F',0.1]
                        ,['shakeT2_Z_A',0]
                        ,['shakeT2_Z_F',0.1]
                        ,['shakeT2Noise',0]
                        ]

        for i in extraAttributes:
            attr = i[0]
            attrValue = i[1]
            pm.addAttr(camera,longName =  attr, defaultValue = attrValue)
            pm.setAttr(camera + '.' + attr, channelBox = True)
            pm.setAttr(camera + '.' + attr,lock = False)
            pm.setAttr(camera + '.' + attr, keyable = True)
            

        #Connect camera attr to sine nodes
        attrConnections = [
                        ['shakeR_X_A','_noiseRot.amplitudeX']
                        ,['shakeR_X_F', '_noiseRot.frequencyX']
                        ,['shakeR_Y_A', '_noiseRot.amplitudeY']
                        ,['shakeR_Y_F', '_noiseRot.frequencyY']
                        ,['shakeR_Z_A', '_noiseRot.amplitudeZ']
                        ,['shakeR_Z_F', '_noiseRot.frequencyZ']
                        ,['shakeRNoise', '_noiseRot.noise']

                        ,['shakeT_X_A', '_noiseTrans.amplitudeX']
                        ,['shakeT_X_F', '_noiseTrans.frequencyX']
                        ,['shakeT_Y_A', '_noiseTrans.amplitudeY']
                        ,['shakeT_Y_F', '_noiseTrans.frequencyY']
                        ,['shakeT_Z_A', '_noiseTrans.amplitudeZ']
                        ,['shakeT_Z_F', '_noiseTrans.frequencyZ']
                        ,['shakeTNoise', '_noiseTrans.noise']

                        ,['shakeT2_X_A', '_sineTrans.amplitudeX']
                        ,['shakeT2_X_F', '_sineTrans.frequencyX']
                        ,['shakeT2_Y_A', '_sineTrans.amplitudeY']
                        ,['shakeT2_Y_F', '_sineTrans.frequencyY']
                        ,['shakeT2_Z_A', '_sineTrans.amplitudeZ']
                        ,['shakeT2_Z_F', '_sineTrans.frequencyZ']
                        ,['shakeT2Noise', '_sineTrans.noise']
                        ]

        for i in attrConnections:
            
            input = camera + '.' + i[0]
            output = camera + i[1]
            
            pm.connectAttr(input, output)
        
        
        camera_shake_noise(camera = camera)
        pm.undoInfo(closeChunk = True)
        
def camera_shake_noise(camera = None):    
    '''Shake mode for the camera shaker'''
    pm.undoInfo(openChunk = True,undoName = 'camera_shake_noise')   
    
    if camera is None:
        camera = pm.selected()[-1].name()

    print("Shaking camera: {}".format(camera))
    
    transNode = camera + '_shakeTrans'
    rotNode = camera + '_shakeRot'

    targets = {camera + '.translateX': transNode + '.output3Dx', camera + '.translateY': transNode + '.output3Dy' , camera + '.translateZ':transNode + '.output3Dz', camera + '.rotateX': rotNode + '.output3Dx', camera + '.rotateY': rotNode + '.output3Dy', camera + '.rotateZ': rotNode + '.output3Dz'}

    for _, v in enumerate(targets):
        output = targets[v]
        input = v
        try:
            pm.disconnectAttr(input)
        except:
            pass
        
        if 'rotate' in input:
            try :
                connected = pm.listConnections(output, destination = True)
                pm.delete(connected)
            except:
                pass
            
        
        pm.connectAttr(output, input)
    
    pm.select(camera)
    pm.undoInfo(closeChunk = True)
 
 
def camera_shake_move():
    '''Move mode for the camera shaker'''
    pm.undoInfo(openChunk = True,undoName = 'camera_shake_move')   
    camera = pm.selected()[-1].name()
    
    targets = {camera + '.translateX': camera + '_translateX.output', camera + '.translateY': camera + '_translateY.output' , camera + '.translateZ':camera + '_translateZ.output', camera + '.rotateX': camera + '_rotateX.output', camera + '.rotateY': camera + '_rotateY.output', camera + '.rotateZ': camera + '_rotateZ.output'}

    for i, v in enumerate(targets):
        output = targets[v]
        input = v
        try:
            pm.disconnectAttr(input)
        except:
            pass
        
        pm.connectAttr(output, input)
    pm.select(camera)
    pm.undoInfo(closeChunk = True)