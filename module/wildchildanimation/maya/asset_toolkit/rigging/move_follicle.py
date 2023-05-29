import pymel.core as pm

def move_folicles():
    '''
    Creates Follicle movers
    Select follicles and the target mesh last
    '''
    
    folicle_group = 'Fol_Mov_GRP'

    selection = pm.selected()
    
    target = selection[-1].name()
    mesh = selection[-1].name()
    mesh_shape = pm.listRelatives(target, shapes= True)[0].name()

    if pm.objExists(folicle_group):
        pm.delete(folicle_group)
        
    pm.group(empty = True, world = True, name = folicle_group )


    del selection[-1]
    for i in selection:
        name = i.name()
        dup_name = name + '_DUP'
        loc_name = name + '_LOC'
        fol_name = pm.listRelatives(i, children = True)[0].name()
        pom_name = name + '_Point_On_Mesh'
        parent_name = name
        print(parent_name)
        decomp_matrix = name + 'Decompose_Matrix'
        plus =  name + '_Plus_Minus_Average'
        
        ws = pm.xform(name, worldSpace = True, matrix = True, query = True )
        if pm.objExists(loc_name):
            pm.delete(loc_name)
            
        pm.spaceLocator(name = loc_name)
        
        loc_shape = pm.listRelatives(loc_name, shapes = True)[0].name()
        pm.setAttr(loc_shape + '.localScaleX', 0.1)
        pm.setAttr(loc_shape + '.localScaleY', 0.1)
        pm.setAttr(loc_shape + '.localScaleZ', 0.1)
        
        pm.parent(loc_name, folicle_group)
        pm.xform(loc_name, worldSpace = True, matrix = ws)
        if pm.objExists(pom_name):
            pm.delete(pom_name)
            
        pm.createNode('closestPointOnMesh', name = pom_name)
        pm.createNode('decomposeMatrix', name = decomp_matrix)
        pm.createNode('plusMinusAverage', name = plus)
        
        
        pm.connectAttr(mesh_shape + '.worldMesh', pom_name + '.inMesh')
        pm.connectAttr(mesh_shape + '.worldMatrix', pom_name + '.inputMatrix')
        pm.connectAttr(loc_name + '.worldMatrix', decomp_matrix + '.inputMatrix')
        pm.connectAttr(decomp_matrix + '.outputTranslate', pom_name + '.inPosition')
        
        
        pm.connectAttr(pom_name + '.parameterU', fol_name + '.parameterU')
        pm.connectAttr(pom_name + '.parameterV', fol_name + '.parameterV')
        

def remove_p_o_m():
    '''Cleans up the follicle movers'''
    objects = pm.ls(type = 'closestPointOnMesh')
    for i in objects:
        name = i.name()
        check_string = 'Point_On_Mesh'
        if check_string in name:
            pm.delete(i)
    if pm.objExists('Fol_Mov_GRP'):
        pm.delete('Fol_Mov_GRP')
