import pymel.core as pm

def align(translation = True, rotation = True):
    selection = pm.selected()
    
    if len(selection) < 2:
        pm.warning('Select more objects with the last being the target')
        
    objects = selection
    target = objects[-1]

    del objects[-1]

    target_trans = pm.xform(target, query = True, worldSpace = True, rotatePivot = True)
    target_rot = pm.xform(target, query = True, worldSpace = True, rotation = True)

    for object in objects:
        if translation == True:
            pm.xform(object.name(), worldSpace = True, translation = target_trans )
            
        if rotation == True:
            pm.xform(object.name(), worldSpace = True, rotation = target_rot )
    print( 'Object(s) aligned to: ' + target)
