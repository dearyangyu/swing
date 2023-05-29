###usage
#copy script to your scripts folder
#
###To generate meta
#import squash_bend
#squash_bend.meta(name = 'Desired Name')
#
###To rig
#import squash_bend
#squash_bend.rig()

#from DS_rig import ctrl_shapes as ctrl_shapes
import pymel.core as pm

def meta(name = 'beak'):
    meta_base_name = name + '_Base_MET'
    meta_end_name = name + '_End_MET'
    pm.spaceLocator(name = meta_base_name, relative = True, position = [0,0,0] )
    
    pm.spaceLocator(name = meta_end_name, relative = True, position = [0,0,0] )
    pm.setAttr(meta_end_name + '.translateY', 5)
    
    pm.parent(meta_end_name, meta_base_name)
    pm.xform(meta_end_name, centerPivots = True)
    
    base_locks = ['scaleX','scaleY','scaleZ','visibility']
    end_locks = ['translateX','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility']
    
    for i in base_locks:
        pm.setAttr(meta_base_name + '.' + i, lock = True )
        
    for i in end_locks:
        pm.setAttr(meta_end_name + '.' + i, lock = True )
    
def rig():
    meta_root = pm.selected()[0].name()
    name = pm.selected()[0].name().split('_Base_')[0]
    mesh = pm.selected()[1].name()
    meta_end = name + '_End_MET'
    
    rig_GRP = name + '_rig_GRP'
    ctrl_GRP = name + '_CTRL_GRP_FRZ'
    
    ctrl = name + '_CTRL'
    
    root_JNT = name + '_Root_JNT'
    end_JNT = name + '_End_JNT'
    distance = name + '_Distance'
    bend = name + '_Bend'
    squash = name + '_Squash'
    
    pm.group(name = rig_GRP, world = True, empty = True)
    pm.group(name = ctrl_GRP, world = True, empty = True)
    
    ws_start = pm.xform(meta_root, worldSpace = True, matrix = True, query = True)
    ws_end = pm.xform(meta_end, worldSpace = True, matrix = True, query = True)
    
    pm.xform(rig_GRP, worldSpace = True, matrix = ws_start )
    pm.xform(ctrl_GRP, worldSpace = True, matrix = ws_end )
    
    pm.joint(name = root_JNT)
    pm.xform(root_JNT, worldSpace = True, matrix = ws_start )
    pm.parent(root_JNT,rig_GRP)
    
    
    pm.joint(name = end_JNT)
    pm.xform(end_JNT, worldSpace = True, matrix = ws_end )
    pm.parent(end_JNT,root_JNT)
    
    # ctrl_shapes.sphere_ctrl(name = ctrl, offset =[0,0,0] , orient = 'xy', size = [0.2, 0.2, 0.2])
    pm.xform(ctrl, worldSpace = True, matrix = ws_end )
    pm.parent(ctrl, ctrl_GRP)
    
    pm.aimConstraint(ctrl, end_JNT, worldUpType = 'objectrotation', worldUpObject = root_JNT )
    pm.setAttr(end_JNT + '.rotateOrder',2 )
        
    
    ######################## Squash Deformer
    
    pm.select( mesh , replace = True)
    squash_node = pm.nonLinear(name = squash, type='squash')
    
    for i in squash_node:
        if 'Handle' in i.name():
            pm.rename(i.name(), squash + '_Handle')
        else:
            squash_set = i.name() +'Set'
            pm.rename(i.name(), squash + '_DEF')
    
    pm.rename(squash_set, squash + '_SET')
    pm.parent( squash + '_Handle', root_JNT)
    pm.xform(squash + '_Handle', worldSpace = True, matrix = ws_start )
    pm.setAttr( squash + '_DEF.highBound' , pm.getAttr(end_JNT + '.translateY'))
    pm.setAttr( squash + '_DEF.lowBound' , 0)
    
    pm.createNode('multiplyDivide', name = squash + '_mult')
    
    pm.connectAttr(squash + '_mult.outputX', squash + '_DEF.factor' )
    pm.connectAttr( ctrl + '.translateY'  , squash + '_mult.input1X')
    pm.setAttr(squash + '_mult.input2X', pm.getAttr(end_JNT + '.translateY')/20 )


    ######################## Bend Deformer
    
    pm.select( mesh , replace = True)
    bend_node = pm.nonLinear(name = bend, type='bend')
    
    for i in bend_node:
        if 'Handle' in i.name():
            pm.rename(i.name(), bend + '_Handle')
        else:
            bend_set = i.name() +'Set'
            pm.rename(i.name(), bend + '_DEF')
    
    pm.rename(bend_set, bend + '_SET') 
    pm.parent( bend + '_Handle', root_JNT)
    pm.xform(bend + '_Handle', worldSpace = True, matrix = ws_start )
    pm.setAttr( bend + '_DEF.highBound' , pm.getAttr(end_JNT + '.translateY')*2)
    pm.setAttr( bend + '_DEF.lowBound' , 0)
    
    pm.connectAttr( end_JNT + '.rotateY' , bend + '_Handle.rotateY')
    
    
    pm.createNode('distanceBetween', name = distance)
    pm.createNode('multiplyDivide', name = name + '_Bend_mult')
    
    pm.connectAttr(end_JNT + '.translateX',distance + '.point1X' )
    pm.connectAttr(end_JNT + '.translateZ',distance + '.point1Z' ) 
       
    pm.connectAttr(ctrl + '.translateX',distance + '.point2X' )
    pm.connectAttr(ctrl + '.translateZ',distance + '.point2Z' )
    
    pm.connectAttr(distance + '.distance',  name + '_Bend_mult.input1X' )
    pm.connectAttr(name + '_Bend_mult.outputX', bend + '_DEF.curvature' )
    pm.setAttr(name + '_Bend_mult.input2X', 5 )


# Create an OK/Cancel prompt dialog.
#
# +-+---------------------+
# |-|    Rename Object    |
# +-----------------------+
# | Enter Name:           |
# | +-------------------+ |
# | |                   | |
# | |                   | |
# | +-------------------+ |
# +-----------------------+
# | +-------+  +--------+ |
# | |  OK   |  | Cancel | |
# | +-------+  +--------+ |
# +-----------------------+
#
def meta_dialog():
    
    result = pm.promptDialog(
                title='Rename Object',
                message='Enter Name:',
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')

    if result == 'OK':
        text = pm.promptDialog(query=True, text=True)
        meta(name = text)
