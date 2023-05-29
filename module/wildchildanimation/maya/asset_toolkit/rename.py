import wildchildanimation.maya.asset_toolkit.utils.utils as ut
import pymel.core as pm

def rename(basename = None, select_bad_names = False):  
    pm.undoInfo(openChunk = True,undoName = 'rename')
    bad_names = []
    nodes = ut.get_selection(sel_type = 'world_or_selected')
    for node in nodes:
        if basename is None:
            base = base_name(node)
            base = base.lower()
        else:
            base = basename
            base = base.lower()
              
        suffix = ut.get_suffix(node) 
        
        if suffix != None:            
            
            for number in range(1, 999):                
                new_name = base + '_' + str(number).zfill(3) + '_' + suffix
                try:
                    if not pm.objExists(new_name):   
                        node.rename(new_name)
                        if is_bad_name(node):
                            bad_names.append(node)
                        break  
                except:
                    pass
                
    if select_bad_names and len(bad_names) != 0:
        pm.select(bad_names)
        pm.warning('Selected ' +  str(len(bad_names)) + ' bad base names in your selection. Fix them now. {(>_<)}')  
    elif len(bad_names) != 0:
        pm.warning('Selected ' +  str(len(bad_names)) + ' bad base names in your selection. Fix them now. {(>_<)}')  

    pm.undoInfo(closeChunk = True)
    
def search_bad_names():
    pm.undoInfo(openChunk = True,undoName = 'search_bad_names')
    bad_names = []
    selection = nodes = pm.ls(selection = True, transforms = True, shapes = False)
    ##### Check whether to rename all or just selection 
    if len(selection) == 0:
        nodes = pm.ls(transforms = True, shapes = False)
        target = 'scene'
    else:
        nodes = selection
        target = 'selection'
        
        
    for node in nodes:
        if is_bad_name(node):
            bad_names.append(node)
        
        
    pm.select(bad_names)
    if len(bad_names) != 0:
        pm.warning('Selected ' +  str(len(bad_names)) + ' bad base names in your ' + target + '. Fix them now. {(>_<)}')  
    else:
        pm.warning('Base names seem fine')  
    pm.undoInfo(closeChunk = True)
    
def shader_append():
    pm.undoInfo(openChunk = True,undoName = 'shader_append')
    selection = ut.get_selection(sel_type = 'world_or_selected')    
    default_shader = []
    weird_names = []
    for object in selection:
        object_name = object.name()
        if '|' in object_name:
            object_name = object_name.split('|')[-1]
        
        # get shapes of selection:
        shapesInSel = pm.listRelatives(object_name, shapes = True)
        # get shading groups from shapes:
        shadingGrps = pm.listConnections(shapesInSel,type='shadingEngine')
        # get the shaders:
        shaders = pm.ls(pm.listConnections(shadingGrps),materials=1)        
        name_split = object_name.split('_')
        suffix = name_split[-1]
        
        check = 0
        if ut.is_mesh(object) or ut.is_surface(object) or ut.is_curve(object):
            if ((len(name_split) == 4) or (len(name_split) == 3)) and ut.get_suffix(object) == suffix:          
                if len(name_split) == 4:            
                    del name_split[-2]                   
            else:
                weird_names.append(object) 
                check = check +  1  
                
            if 'lambert1' in str(shaders[0]):                     
                default_shader.append(object) 
                check = check + 1  
                
            elif check == 0:  
                new_name = name_split[0] + '_' + name_split[1] + '_' + shaders[0] + '_' +ut.get_suffix(object)
                pm.rename(object , new_name)
       
    pm.select(weird_names + default_shader)
    pm.warning(str(len(weird_names)) + ' objects have bad naming structures. ' + str(len(default_shader)) + ' objects has the initial shader.')
         
    pm.undoInfo(closeChunk = True)
    
def find_bad_name_structures():  
    pm.undoInfo(openChunk = True,undoName = 'find_bad_name_structures')  
    selection = ut.get_selection(sel_type = 'world_or_selected')
    weird_names = []
    for object in selection:
        object_name = object.name()
        if '|' in object_name:
            object_name = object_name.split('|')[-1]        
        name_split = object_name.split('_')        
        suffix = name_split[-1]
        
        check = 0 
        type_check = 0
        
        if ut.is_group(object) or ut.is_mesh(object) or ut.is_surface(object)or ut.is_curve(object):
            type_check = 1
            
            if ut.get_suffix(object) == suffix: 
                check = check + 1         
    
                if (len(name_split) == 4) or (len(name_split) == 3):            
                    check = check + 1
            
         
              
        if (check != 2) and (type_check == 1):
            print('sucess')
            weird_names.append(object)
                  
    if weird_names:
        pm.warning(str(len(weird_names)) + ' selected objects have bad naming structures. {(>_<)}')                 
        pm.select(weird_names, replace= True)  
    else:
        pm.warning('Selected objects naming structures seem good. \m/(>.<)\m/')

    pm.undoInfo(closeChunk = True)
    
def is_bad_name(node):
    bad_name_list = ['pCube', 'pCylinder', 'pCone', 'pPlane', 'pTorus', 'pPyramid', 'pPipe', 'nurbsCircle', 'nurbsSquare', 'nurbsSphere', 'nurbsCube', 'nurbsCylinder', 'nurbsCone', 'nurbsPlane', 'nurbsTorus', 'nurbsCircle', 'nurbsSquare', 'group', 'topnurbsSquare', 'leftnurbsSquare', 'bottomnurbsSquare', 'rightnurbsSquare', 'topnurbsCube', 'bottomnurbsCube', 'leftnurbsCube', 'rightnurbsCube', 'frontnurbsCube', 'backnurbsCube', 'pasted', 'pSphere']
    for bad_name in bad_name_list:
        if bad_name.lower() in node.name().lower():
            return True 
    return False

def select_same_base_name():
    pm.undoInfo(openChunk = True,undoName = 'select_same_base_name')
    nodes = pm.selected()
    all_nodes = pm.ls(transforms = True, shapes = False)
    target_selection = []
    
    for node in nodes:
        for each in all_nodes:
            print( base_name(node)  + '   ' +  base_name(each) )
            if base_name(node) ==  base_name(each) :
                target_selection.append(each)
            
    print(target_selection)
    pm.select(target_selection)
    
    pm.undoInfo(closeChunk = True)

def base_name(node):
    base = node.name().split('|')[-1].split('_')[0]
    base_no_digits = ''.join([i for i in base if not i.isdigit()])
    return base_no_digits
