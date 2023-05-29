'''
Created on May 13, 2015

@author: Ivan Schoeman
@author: Dewald Swanepoel
'''
from wildchildanimation.maya.asset_toolkit.rigging import color_change as cc
from wildchildanimation.maya.asset_toolkit.rigging import color_change as cc
from wildchildanimation.maya.asset_toolkit.rigging import ctrl_shapes as cs
from wildchildanimation.maya.asset_toolkit.utils import utils as ut

import maya.cmds as cmds
import pymel.core as pm

def createRootGroup():
    if not pm.objExists("proprig_grp"):
        pm.group(name = "proprig_grp", empty = True) 

def createLayers():    
    try:
        pm.delete('propgeo_lyr')
    except:
        pass
    
    geo = pm.ls('*geo*', transforms = True, shapes = False)
    clean_list = []

    for i in geo:
        if i.type() == 'transform':
            clean_list.append(i)
            
    displayLayer = pm.createDisplayLayer(clean_list, name = "propgeo_lyr")   
    displayLayer.displayType.set(2)

def createControl(name = '', ctl_type = '', align_target = None,  color = None, size = 1):
    '''meta, rotation, circle, sphere, cube, 
    direction ,tongue, half_circle, line, mouth,
    eye, up_down, arrow, root,shoulder , cog 
    '''
    
    size = [4*size, 4*size, 4*size]
    curve = None
    eval_string = "curve = cs." + ctl_type + "_ctrl(name = '" + name + "', offset = [0,0,0], orient = 'yz', size = " + str(size) + ")"
    exec(eval_string)
    curve = curve.curve
    
    if color: cc.change(curve, color)
    if align_target:
        constraint = pm.parentConstraint(align_target, curve)
        pm.delete(constraint)
    
    return curve

def lock_transforms(targets):
    lock_list = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'visibility']
    for i in targets:
        for attr in lock_list:
            # print 
            i.setAttr(attr, keyable = False,  lock = True, channelBox = False)
    
def createGeoSets():  
    try:
        pm.delete('propgeo_set')
    except:
        pass
    geo = pm.ls('*_geo*', transforms = True, shapes = False)  
    clean_list = []

    for i in geo:
        if i.type() == 'transform':
            clean_list.append(i)
            
    pm.sets(clean_list, name = 'propgeo_set') 

def createControlSets(ctls = None):
    if not ctls:
        ctls = []
        all_ctls = pm.ls('*ctl*', transforms = True, shapes = False)
        for ctl in all_ctls:
            if ut.is_curve(ctl):
                ctls.append(ctl)
    
    try:
        pm.delete('propctl_set')
    except:
        pass
    
    pm.sets(ctls, name = 'propctl_set')
    
def meta():
    pm.undoInfo(openChunk = True,undoName = 'rig_meta')
    selection = cmds.ls(selection = True, long = True )
    rig_order_dic = {}
    for i in selection:
        split = i.split('|')
        rig_order_dic[i] = len(split)
        
    order_list =  sorted(rig_order_dic.items(), key=lambda x: x[1], reverse = True)
    print(order_list)

    for i in order_list:
        name = i[0]
        for n in order_list:
            if n[0] in i[0] and n[0] != i[0]:
                parent = n[0]
                break
            else:
                parent = 'world'
                
        
            meta_name = '_'.join(name.split('|')[-1].split('_')[0:2]) + '_meta'    
        
        try:            
            pm.deleteAttr(name + '.rig_parent')
        except:
            pass
        
        createControl(name = meta_name, ctl_type = 'axis', align_target = name, color = 'light_yellow')
   
        pm.addAttr(name,  attributeType = 'message', longName = 'rig_parent')
        pm.addAttr(meta_name,  dataType = 'string', longName = 'rig_parent')
        pm.addAttr(meta_name,  dataType = 'string', longName = 'constraint_target')
        pm.addAttr(meta_name,  attributeType = 'enum', longName = 'control_shape', enumName = ['cog', 'meta', 'rotation', 'circle', 'sphere', 'cube', 'direction' ,'tongue', 'half_circle', 'line', 'mouth', 'eye', 'up_down', 'arrow', 'root','shoulder' ])
        pm.addAttr(meta_name,  attributeType = 'enum', longName = 'control_color', enumName = ['light_blue', 'light_pink', 'light_orange'])
        pm.setAttr(meta_name + '.control_shape', channelBox = True)
        pm.setAttr(meta_name + '.control_color', channelBox = True)
        if parent != 'world': 
            pm.connectAttr(parent + '.message', name + '.rig_parent', f=True)   
            pm.setAttr(meta_name + '.rig_parent', parent)
            
        pm.setAttr(meta_name + '.constraint_target', i)
    
    pm.undoInfo(closeChunk = True)
    
    
def rig():
    '''
    1. Select geo groups that need its own controller and generate the meta shapes by hitting the 'Meta' button. 
    2. Refine the meta positions and set the control shapes in the extra attributes of the meta shapes. 
    3. Hit Rig
    '''

    pm.undoInfo(openChunk = True,undoName = 'rig_rig') 
    createRootGroup()
    loops = 0
    loopMax = 50
    
    while loops <= loopMax:  
        loops += 1
        meta = pm.ls('*_meta', transforms = True, shapes = False)
        for i in meta:
                
            if i.rig_parent.get() == None :    
                if pm.objExists('_'.join(i.name().split('|')[-1].split('_')[0:2])) == False:   
                    geo_root = i.constraint_target.get()
                    rigMeta(i)      
                            
            elif pm.objExists('_'.join(i.rig_parent.get().split('|')[-1].split('_')[0:2]) + '_ctl'):
                print('---------')
                rigMeta(i)
                
    pm.delete(meta)   
    createGeoSets()
    createControlSets()
    createLayers()
    
    pm.group(name = 'propgeo_grp', empty = True)
    pm.parent(geo_root, 'propgeo_grp' )
    pm.parent('propgeo_grp', 'proprig')
    
    lock_transforms(pm.ls(['*_npo', 'proprig', 'propgeo_grp'], transforms = True, shapes = False))
    
    pm.undoInfo(closeChunk = True)
    
    
def rigMeta(meta_node):
    base = '_'.join(meta_node.name().split('|')[-1].split('_')[0:2])  
    shape = meta_node.control_shape.getEnums()[meta_node.control_shape.get()]
    color = meta_node.control_color.getEnums()[meta_node.control_color.get()]
    ctl = createControl(name = base + '_ctl' , ctl_type = shape, align_target = meta_node, color = color)
    grp = pm.group(name =  base + '_npo', empty = True)
    constraint = pm.parentConstraint(ctl, grp)
    pm.delete(constraint)
    if meta_node.rig_parent.get() == None:
        global_grp = pm.group(name = 'global_001_npo', empty = True)
        global_ctl = createControl(name = 'global_001_ctl' , ctl_type = shape, align_target = meta_node, color = 'light_yellow', size = 1.2)
        
        constraint = pm.parentConstraint(global_ctl, global_grp)
        pm.delete(constraint)
        
        pm.parent(global_ctl, global_grp)
        pm.parent(global_grp, 'proprig_grp')         
        pm.parent(grp, global_ctl)
    else:
        pm.parent(grp, '_'.join(meta_node.rig_parent.get().split('|')[-1].split('_')[0:2]) + '_ctl')
    pm.parent(ctl, grp)
    pm.parentConstraint(ctl, meta_node.constraint_target.get() ,maintainOffset = True)
    pm.scaleConstraint(ctl, meta_node.constraint_target.get() ,maintainOffset = True)
    pm.delete(meta_node)


