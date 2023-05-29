import wildchildanimation.maya.asset_toolkit.utils.utils as ut

import pymel.core as pm
import maya.cmds as cmds

def get_mesh_list(mesh_list = []):
    '''
    Return a list of mesh objects to be used in the poly check scripts
    @param mesh_list: List of meshes to return as list. If empty, use all non intermediate meshes in the scene
    @type mesh_list: list
    '''
    mesh_list = []
    nodes = ut.get_selection(sel_type = 'world_or_selected')
    
    for node in nodes:
        if ut.is_mesh(node):
            mesh_list.append(node)

        
    # Return Result
    return mesh_list

def get_object_list(object_list = []):
    '''
    Return a list of mesh objects to be used in the poly check scripts
    @param mesh_list: List of meshes to return as list. If empty, use all non intermediate meshes in the scene
    @type mesh_list: list
    '''
    object_list = []
    nodes = ut.get_selection(sel_type = 'world_or_selected')
    
    for node in nodes:
        if ut.is_mesh(node) or ut.is_curve(node) or ut.is_group(node) or ut.is_surface(node):
            object_list.append(node)
    
    
    # Return Result
    return object_list

# ==========
# - Checks -
# ==========
    
def triangles(mesh_list = []):
    '''
    Return a list of all 3-sided polygon faces in a specified mesh list.
    @param mesh_list: List of meshes to check for triangles
    @type mesh_list: list
    '''
    # Check Mesh List
    mesh_list = get_mesh_list()
    if not mesh_list: return []
    
    tri_dic = {}
    # Find triangles    
    for mesh in mesh_list:
        pm.select(mesh)
        pm.polySelectConstraint(mode=3,type=0x0008,size=1)
        pm.polySelectConstraint(disable=True)
        tris = pm.filterExpand(ex=True,sm=34) or []
        tri_dic[mesh.name()] = tris
    
    
    pm.select(mesh_list)
    
    # Return Result
    return tri_dic

def nGons():
    '''
    Return a list of all polygon faces with more than 4 sides in a specified list of meshes.
    @param mesh_list: List of meshes to check for ngons
    @type mesh_list: list
    '''
    # Check Mesh List
    mesh_list = get_mesh_list()
    if not mesh_list: return []
    
    ngon_dic = {}
    # Find ngonangles    
    for mesh in mesh_list:
        pm.select(mesh)
        pm.polySelectConstraint(mode=3,type=0x0008,size=3)
        pm.polySelectConstraint(disable=True)
        ngons = pm.filterExpand(ex=True,sm=34) or []
        ngon_dic[mesh.name()] = ngons
    
    
    pm.select(mesh_list)
    
    # Return Result
    return ngon_dic

def non_quads():
    '''
    Return a list of all non 4-sided polygon faces in a specified list of meshes.
    @param mesh_list: List of meshes to check for non quads
    @type mesh_list: list
    '''
    # Return Result
    
    tri_dic = triangles()
    ngon_dic = nGons()
    
    if len(tri_dic) != 0 or len(ngon_dic) != 0:
        
        nQuad_dic = tri_dic.copy()
        nQuad_dic.update(ngon_dic)
        
        for mesh in nQuad_dic:
            nQuad_dic[mesh] = tri_dic[mesh] + ngon_dic[mesh]
            
        return nQuad_dic
    else:
        return None

def non_manifold():
    '''
    Check for non manifold geometry in a specified list of meshes.
    @param mesh_list: List of meshes to check for non manifold topology. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    # Check Mesh List
    mesh_list = get_mesh_list()
    if not mesh_list: return []
    
    nonManifold_dic = {}
    # Find nonManifoldangles    
    for mesh in mesh_list:
        pm.select(mesh)
        pm.polySelectConstraint(mode=3,type=0x0001,nm=1)
        pm.polySelectConstraint(disable=True)
        nonManifolds = pm.filterExpand(ex=True,sm=31) or []
        nonManifold_dic[mesh.name()] = nonManifolds
    
    
    pm.select(mesh_list)
    
    # Return Result
    return nonManifold_dic
    
    # Check Mesh List
    mesh_list = get_mesh_list()
    if not mesh_list: return []
    
    # Check Non Manifold
    pm.select(mesh_list)
    pm.polySelectConstraint(mode=3,type=0x0001,nm=1)
    pm.polySelectConstraint(disable=True)
    nonManifoldList = pm.filterExpand(ex=True,sm=31) or []
    pm.select(mesh_list)
    
    # Return result
    return nonManifoldList

def lamina():
    '''
    Check for lamina faces
    @param mesh_list: List of meshes to check for lamina faces. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    # Check Mesh List
    mesh_list = get_mesh_list()
    if not mesh_list: return []
    
    lamina_dic = {}
    # Find laminaangles    
    for mesh in mesh_list:
        pm.select(mesh)
        pm.polySelectConstraint(mode=3,type=0x0008,topology=2)
        pm.polySelectConstraint(disable=True)
        lamina_list = pm.filterExpand(ex=True,sm=34) or []
        lamina_dic[mesh.name()] = lamina_list
    
    
    pm.select(mesh_list)
    
    # Return Result
    return lamina_dic   

def unlock_vertex_normals():
    '''
    Unlocked vertex normals
    @param mesh_list: List of meshes to unlocked normals on. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    pm.undoInfo(openChunk = True,undoName = 'unlock_vertex_normals')
    # Check mesh_list
    mesh_list = get_mesh_list()
    
    # Unlock Normals
    for mesh in mesh_list: pm.polyNormalPerVertex(mesh,ufn=True)
    
    pm.select(mesh_list)
    pm.undoInfo(closeChunk = True)

def deleteHistory():
    '''
    Deletes the history on the selected Meshes
    @param mesh_list: List of meshes to freeze transform on. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    pm.undoInfo(openChunk = True,undoName = 'deleteHistory')
    # Check Mesh List
    mesh_list = get_mesh_list()
    
    # Freeze Vertex Transforms
    for mesh in mesh_list:
        pm.delete(mesh,ch=True)

    pm.select(mesh_list)
    pm.undoInfo(closeChunk = True)

def merge_UVs(dist = 0.0001):
    '''
    Merge UVs
    @param mesh_list: List of meshes to merge UVs on. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    pm.undoInfo(openChunk = True,undoName = 'merge_UVs')
    # Check Mesh List
    mesh_list = get_mesh_list()
    
    
    # Merge UVs
    for mesh in mesh_list:
        pm.polyMergeUV(mesh,d=dist,ch=False)
    
    pm.select(mesh_list)
    pm.undoInfo(closeChunk = True)

def center_pivots():
    '''
    Center Pivots
    @param mesh_list: List of meshes to merge UVs on. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    pm.undoInfo(openChunk = True,undoName = 'center_pivots')
    # Check Mesh List
    object_list = get_object_list()
    
    
    # Merge UVs
    for object in object_list:
        pm.xform(object, centerPivots = True)
    
    pm.select(object_list)
    pm.undoInfo(closeChunk = True)

def freeze_transforms():
    '''
    Freeze Transforms
    @param mesh_list: List of meshes to merge UVs on. If empty, check all mesh objects in the scene.
    @type mesh_list: list
    '''
    pm.undoInfo(openChunk = True,undoName = 'freeze_transforms')
    # Check Mesh List
    object_list = get_object_list()
    
    
    # Merge UVs
    for object in object_list:
        pm.makeIdentity(object, apply = True, translate = True, scale = True, rotate = True)
    
    pm.select(object_list)
    pm.undoInfo(closeChunk = True)

def initial_shader():  
    '''
    Setup default shader
    '''  
    pm.undoInfo(openChunk = True,undoName = 'initial_shader')
    mesh_list = get_mesh_list()
    
    for node in mesh_list:
        pm.select(node.name())
        pm.hyperShade(assign= 'initialShadingGroup' )
    
    pm.select(mesh_list)
    pm.undoInfo(closeChunk = True)

def optimize_model():
    """
    Optimizes scene with all items checked
    """
    pm.mel.eval("cleanUpScene 3")
    

def crease_attr():  
    '''
    Add crease attr to selected objects
    '''  
    pm.undoInfo(openChunk = True,undoName = 'crease_attr')    
    shapes = pm.listRelatives(get_mesh_list())  
    count = 0
    for i in shapes:  
        if 'Orig' not in i.name():
            exists = pm.attributeQuery( 'SubDivisionMesh', node=i, exists = True)
            if exists != True:
                count += 1
                pm.addAttr(i, longName = 'SubDivisionMesh', attributeType = 'bool', defaultValue = True)
                
    else:
        pm.warning(str(count) + ' crease attribute(s) added')
        
    pm.undoInfo(closeChunk = True)

def smooth_mesh(options):
    '''0:Smooth All    1:Preserve Borders     2:Smooth None   3:No Subdiv'''    
    pm.undoInfo(openChunk = True,undoName = 'smooth_mesh')
    
    nodes = ut.get_selection(sel_type = 'world_or_selected')
    
    if options == 3:
        for node in nodes:
            try: node.getShape().rman__torattr___subdivFacevaryingInterp.delete()              
            except: pass                
            try: node.getShape().rman__torattr___subdivScheme.delete()              
            except: pass
            
            node.getShape().displaySmoothMesh.set(0)
    
    else:
        for node in nodes:
            if options == 0:
                subdiv_face = 1
                subdive_scheme = 0
                osdFvarBoundary = 1
                maya_subdiv_boundary = 0
                maya_smooth_uv = 1
                display_smooth_mesh = 2
                
            elif options == 1:
                subdiv_face = 3
                subdive_scheme = 0
                osdFvarBoundary = 3
                maya_subdiv_boundary = 2
                maya_smooth_uv = 1
                display_smooth_mesh = 2
                
            elif options == 2:             
                subdiv_face = 0
                subdive_scheme = 0
                osdFvarBoundary = 0
                maya_subdiv_boundary = 2
                maya_smooth_uv = 0
                display_smooth_mesh = 2
        
            node.getShape().displaySmoothMesh.set(display_smooth_mesh)
            node.getShape().keepMapBorders.set(maya_subdiv_boundary)
            node.getShape().smoothUVs.set(maya_smooth_uv)
            node.getShape().osdFvarBoundary.set(osdFvarBoundary)
            
            try: node.getShape().rman__torattr___subdivFacevaryingInterp.set(subdiv_face)    
            except: pm.addAttr(node.getShape(), longName = 'rman__torattr___subdivFacevaryingInterp', attributeType = 'long', defaultValue = subdiv_face )   
            
            try:node.getShape().rman__torattr___subdivScheme.set(subdive_scheme)
            except:pm.addAttr(node.getShape(), longName = 'rman__torattr___subdivScheme', attributeType = 'long', defaultValue = subdive_scheme )  
            
    pm.undoInfo(closeChunk = True)


def minYPivot():
    """
    Moves the pivot of isolated transforms to the Minimum Y bbox
    """
    curSel = cmds.ls(long = True, selection = True, type = 'transform')
    print(curSel)
    
    for t in curSel:
    
        try:
            
            children = cmds.listRelatives(t,ad=True,f=True, typ='transform')
            #print children
            
            bbottom = []
            transformlist = []
            for n in children:
                #print n
                bbox = cmds.exactWorldBoundingBox(n)
                bbottom.append( bbox[1])
                transformlist.append(n) 
                
            #print bbottom    
            index =  bbottom.index(min(bbottom))   
 
            print("THIS SEEMS TO BE A GROUP OF TRANSFORMS - ATTEMPTING TO FIND LOWEST POINT")
            lowestbbox = cmds.exactWorldBoundingBox(transformlist[index])
            bottom = [(lowestbbox[0] + lowestbbox[3])/2, lowestbbox[1], (lowestbbox[2] + lowestbbox[5])/2]
            cmds.xform(t, piv=bottom, ws=True)
            
            getOffset = cmds.xform(t,q=True,worldSpace=True,rp=True)
            cmds.move(-(getOffset[0]),-(getOffset[1]),-(getOffset[2]),t, r=True)
            cmds.makeIdentity(t,apply=True,translate=True)
            cmds.xform(t,worldSpace=True,translation=((getOffset[0]),(getOffset[1]),(getOffset[2])))
            
        except:
            print("THIS SEEMS TO BE AN ISOLATED TRANSFORM - ATTEMPTING TO FIND LOWEST POINT")
  
            bbox = cmds.exactWorldBoundingBox(t)
            bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
            cmds.xform(t, piv=bottom, ws=True)
            
            #getOffset = cmds.xform(t,q=True,ws=True,rp=True)
            #cmds.move(-(getOffset[0]),-(getOffset[1]),-(getOffset[2]),t, r=True)
            #cmds.makeIdentity(t,apply=True,translate=True)
            #cmds.xform(t,ws=True,translation=((getOffset[0]),(getOffset[1]),(getOffset[2])))

            getOffset = cmds.xform(t,q=True,worldSpace=True,rp=True)
            cmds.move(-(getOffset[0]),-(getOffset[1]),-(getOffset[2]),t, r=True)
            cmds.makeIdentity(t,apply=True,translate=True)
            cmds.xform(t,worldSpace=True,translation=((getOffset[0]),(getOffset[1]),(getOffset[2])))

def reversesides():
    """
    Reverse the sidedness of a mesh when it has been scaled negatively and frozen.
    """
    curSel = cmds.ls(long = True, typ = 'mesh')

    for obj in curSel:
        cmds.setAttr((obj+'.doubleSided'), 0)
        cmds.setAttr((obj+'.opposite'), 0)
        cmds.setAttr((obj+'.doubleSided'), 1)
		
def copypivot():
    sourceObj = cmds.ls(sl = True)[len(cmds.ls(sl = True))-1]
    targetObj = cmds.ls(sl = True)[0:(len(cmds.ls(sl = True))-1)]
    parentList = []
    for obj in targetObj:
        if cmds.listRelatives( obj, parent = True):
            parentList.append(cmds.listRelatives( obj, parent = True)[0])
        else:
            parentList.append('')

    if len(cmds.ls(sl = True)) < 2:
        cmds.error('select 2 or more objects.')
        return

    pivotTranslate = cmds.xform (sourceObj, q = True, ws = True, rotatePivot = True)
    cmds.parent(targetObj, sourceObj)
    cmds.makeIdentity(targetObj, a = True, t = True, r = True, s = True)
    cmds.xform (targetObj, ws = True, pivots = pivotTranslate)

    for ind in range(len(targetObj)):
        if parentList[ind] != '' :
            cmds.parent(targetObj[ind], parentList[ind])
        else:
            cmds.parent(targetObj[ind], world = True)

def matchtransforms():
    
    #mel.eval('source "/job/common/maya/scripts/anm_matchtrans.mel";')
    #mel.eval('matchTransform()')
    print("Not implemented")

def clean_crease_sets():
    '''Cleans crease sets in the outliner.'''
    crease_sets = pm.ls(type = 'creaseSet')
    crease_sets_grp = 'crease_set'
    
    if not pm.objExists(crease_sets_grp):
        pm.sets(name = crease_sets_grp, empty = True)
          
    pm.sets(crease_sets_grp, add = crease_sets)


