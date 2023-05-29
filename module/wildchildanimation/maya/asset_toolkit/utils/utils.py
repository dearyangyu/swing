import pymel.core as pm

def is_group(node):
    children = node.getChildren()
    for child in children:
        if type(child) != pm.nodetypes.Transform:
            return False
    return True

def is_mesh(node):
    children = node.getChildren()
    for child in children:
        if type(child) != pm.nodetypes.Mesh:
            return False
    return True

def is_surface(node):
    children = node.getChildren()
    for child in children:
        if type(child) != pm.nodetypes.NurbsSurface:
            return False
    return True

def is_curve(node):
    children = node.getChildren()
    for child in children:
        if type(child) == pm.nodetypes.NurbsCurve:
            return True
    return False

def get_selection(sel_type = 'world_or_selected'):
    if sel_type == 'world_or_selected':
        selection = pm.ls(selection = True, transforms = True, shapes = False)
    
        ##### Check whether to rename all or just selection 
        if len(selection) == 0:
            nodes = pm.ls(transforms = True, shapes = False)
        else:
            nodes = selection  
         
        return nodes
        

def get_suffix(node):
    suffix = { "time": "tme",
             "sequenceManager": "sma",
             "hardwareRenderingGlobals": "hrg",
             "partition": "par",
             "renderGlobalsList": "rgl",
             "defaultLightList": "lgl",
             "defaultShaderList": "dsl",
             "postProcessList": "ppl",
             "defaultRenderUtilityList": "utl",
             "defaultRenderingList": "drl",
             "lightList": "lgl",
             "defaultTextureList": "dtl",
             "lambert": "mat",
             "particleCloud": "pcl",
             "shadingEngine": "seg",
             "materialInfo": "inf",
             "shaderGlow": "glw",
             "dof": "dof",
             "renderGlobals": "rgl",
             "renderQuality": "rqy",
             "resolution": "res",
             "objectSet": "set",
             "viewColorManager": "vcm",
             "colorManagementGlobals": "cmg",
             "hardwareRenderGlobals": "hrg",
             "hwRenderGlobals": "hrg",
             "ikSystem": "iks",
             "hyperGraphInfo": "hgi",
             "hyperLayout": "hyl",
             "globalCacheControl": "gcc",
             "strokeGlobals": "sgl",
             "dynController": "dct",
             "RenderMan": "rmn",
             "transform": "grp",
             "camera": "cam",
             "mesh": "geo",
             "nurbsCurve": "crv",
             "nurbsSurface": "geo",
             "aimConstraint": "aim",
             "pointConstraint": "poi",
             "parentConstraint": "par",
             "orientConstraint": "ori",
             "locator": "loc",
             "scaleConstraint": "sca",
             "joint": "jnt",
             "ikEffector": "ike",
             "ikHandle": "ikh",
             "follicle": "fol",
             "lightLinker": "lgl",
             "displayLayer": "lyr",
             "renderLayer": "lyr",
             "script": "scr",
             "ilrOptionsNode": "utl",
             "ilrUIOptionsNode": "utl",
             "ilrBakeLayerManager": "utl",
             "ilrBakeLayer": "utl",
             "unknown": "unk",
             "groupId": "gid",
             "nodeGraphEditorBookmarkInfo": "utl",
             "phong": "mat",
             "nodeGraphEditorInfo": "inf",
             "creaseSet": "cst",
             "animCurveTA": "ani",
             "multiplyDivide": "mdn",
             "plusMinusAverage": "pma",
             "animCurveUU": "ani",
             "fcgear_curveCns": "fcc",
             "groupParts": "prt",
             "tweak": "twk",
             "rebuildSurface": "rbs",
             "loft": "lof",
             "subCurve": "suc",
             "decomposeMatrix": "dmx",
             "fcgear_mulMatrix": "fcx",
             "rebuildCurve": "rbc",
             "ikSplineSolver": "iks",
             "blendShape": "bls",
             "wrap": "wrp",
             "distanceBetween": "dib",
             "fcgear_slideCurve2": "fcs",
             "curveInfo": "cin",
             "motionPath": "mpa",
             "fcgear_intMatrix": "fcx",
             "fcgear_squashStretch2": "fcs",
             "blendColors": "bco",
             "unitConversion": "uco",
             "addDoubleLinear": "adl",
             "clamp": "cla",
             "condition": "con",
             "reverse": "rev",
             "fcgear_ikfk2Bone": "fci",
             "fcgear_rollSplineKine": "fcr",
             "fcgear_inverseRotOrder": "fci",
             "dagPose": "dpo",
             "skinCluster": "skn",
             "blendWeighted": "blw",
             "polyReduce": "prd",
             "ngSkinLayerData": "ngs",
             }
    
    try:
        if node.getShape() != None:
            t = node.getShape().type()
        else:
            t =  node.type()
    except:
        t =  node.type()
    
    try:
        suff = suffix[t]
    except:
        suff = "utl"
        
    return suff
        
def data_merge(a, b):
    """merges b into a and return merged result

    NOTE: tuples and arbitrary objects are not handled as it is totally ambiguous what should happen"""
    key = None
    # ## debug output
    # sys.stderr.write("DEBUG: %s to %s\n" %(b,a))
    try:
        if a is None or isinstance(a, str) or isinstance(a, u''.__class__) or isinstance(a, int) or isinstance(a, float):
            # border case for first run or if a is a primitive
            a = b
        elif isinstance(a, list):
            # lists can be only appended
            if isinstance(b, list):
                # merge lists
                a.extend(b)
            else:
                # append to list
                a.append(b)
        elif isinstance(a, dict):
            # dicts must be merged
            if isinstance(b, dict):
                for key in b:
                    if key in a:
                        a[key] = data_merge(a[key], b[key])
                    else:
                        a[key] = b[key]
            else:
                #raise YamlReaderError('Cannot merge non-dict "%s" into dict "%s"' % (b, a))
                pass
        else:
            #raise YamlReaderError('NOT IMPLEMENTED "%s" into "%s"' % (b, a))
            pass
    except TypeError:
        #raise YamlReaderError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, b, a))
        pass
    return a