from wildchildanimation.maya.asset_toolkit.rigging import move_follicle as m_v
import pymel.core as pm

def create_follicle():
    '''Creates follicles as well as movers to tweak the position of the follicles
First select the position objects and then the target mesh last'''
    selection = pm.selected()
    target = selection[-1].name()
    del selection[-1]
    mesh_shape = pm.listRelatives(target, shapes= True)[0].name()

    if pm.objExists('Fol_GRP'):
        pm.delete('Fol_GRP')
        
    if pm.objExists('Fol_Mov_GRP'):
        m_v.remove_p_o_m()
        
    pm.group( empty = True, world = True, name = 'Fol_Mov_GRP')
    pm.group( empty = True, world = True, name = 'Fol_GRP')

    for i in selection:
        name = i.name()
        dup_name = name + '_DUP'
        loc_name = name + '_LOC'
        fol_name = name + '_FOL'
        pom_name = name + '_Point_On_Mesh'
        parent_name = fol_name + '_TF'
        decomp_matrix = name + 'Decompose_Matrix'
        
        pm.duplicate(name, name = dup_name)
        pm.xform(dup_name, cp = True)

        ws = pm.xform(name, query = True,  worldSpace = True, rotatePivot = True)

        pm.spaceLocator(name = loc_name)
        pm.setAttr(loc_name + '.localScaleX', 0.1)
        pm.setAttr(loc_name + '.localScaleY', 0.1)
        pm.setAttr(loc_name + '.localScaleZ', 0.1)
        pm.parent(loc_name, 'Fol_Mov_GRP')
        
        
        pm.move(loc_name, ws, absolute = True, worldSpace = True, rotatePivotRelative = True)
        pm.align(loc_name, dup_name, alignToLead = True, xAxis = 'Mid', yAxis = 'Mid', zAxis = 'Mid')    
        pm.delete(dup_name)
        
        pm.createNode('follicle', name = fol_name)
        pm.createNode('closestPointOnMesh', name = pom_name)
        pm.createNode('decomposeMatrix', name = decomp_matrix)
        
        parent = pm.listRelatives(fol_name, parent = True)[0].name()
        pm.rename(parent, parent_name )
        pm.parent(parent_name, 'Fol_GRP')
        
        pm.connectAttr(mesh_shape + '.worldMesh', fol_name + '.inputMesh')
        pm.connectAttr(mesh_shape + '.worldMatrix[0]', fol_name + '.inputWorldMatrix')
        
        pm.connectAttr(mesh_shape + '.worldMesh', pom_name + '.inMesh')
        pm.connectAttr(mesh_shape + '.worldMatrix', pom_name + '.inputMatrix')
        pm.connectAttr(loc_name + '.worldMatrix', decomp_matrix + '.inputMatrix')
        pm.connectAttr(decomp_matrix + '.outputTranslate', pom_name + '.inPosition')
        
        
        pm.connectAttr(pom_name + '.parameterU', fol_name + '.parameterU')
        pm.connectAttr(pom_name + '.parameterV', fol_name + '.parameterV')
        
        pm.connectAttr(fol_name + '.outTranslate', parent_name + '.translate')
        pm.connectAttr(fol_name + '.outRotate', parent_name + '.rotate')
        