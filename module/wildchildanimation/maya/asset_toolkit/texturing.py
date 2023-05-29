import pymel.core as pm

def transfer_UV():    
    '''Transfer UV of last selected object to the rest of selection.''' 
    selection = pm.selected()
    main_selection = selection[-1].name()

    del(selection[-1])

    for i in selection:
        target = i.name()
        shapes = pm.listRelatives(i.name(), shapes = True)
        
        for shape in shapes:
            shape_intermediate = pm.getAttr(shape + '.intermediateObject')
            shape_orig_status = True if 'Orig' in str(shape) else False
            
            if shape_intermediate and shape_orig_status:
            
                target = shape
                deformed = True
                print(shape + ' ' + str(shape_intermediate) + ' ' + str(shape_orig_status))
                pm.setAttr(shape + '.intermediateObject', 0)
            else:
                deformed = False
                
                
        pm.transferAttributes(main_selection, target , transferPositions = 0, transferNormals = 0, transferUVs = 1, sourceUvSet = "map1", targetUvSet = "map1", transferColors = 0, sampleSpace = 5, sourceUvSpace = "map1", targetUvSpace = "map1", searchMethod = 3, flipUVs = 0, colorBorders = 1)
        pm.delete(target, constructionHistory = True)
        
        if deformed :
            pm.setAttr(shape + '.intermediateObject', 1)
        
        deformed = False

def import_tx(tx_dic, setup_shaders):
            
    for key,value in tx_dic.items():
        object_name = key
        shader_name = object_name +'SHD'
        udim = tx_dic[key]['udims']
        ext = tx_dic[key]['extension']
        version = '_' + tx_dic[key]['version'] if tx_dic[key]['version'] != '000' else ''
        filename = object_name + '_' + 'channel' + version + '.' + udim[0] + '.' + ext
        filepath = os.path.join(tx_dic[key]['folder'],filename)
        channels =tx_dic[key]['channels']
        isUdim = len(udim)>1
        
        if setup_shaders :
            try:
                pm.delete(shader_name)
            except:
                pass
            pm.shadingNode('phongE', name = shader_name, asShader = True)
            pm.setAttr(shader_name + '.roughness', 0)
        
        if 'Color' in channels:
            file_node = object_name + '_' + 'Color' + '_file'
            if pm.objExists(file_node):
                pm.delete(file_node)
                
            pm.shadingNode('file', name = file_node, asTexture = True)
            pm.setAttr(file_node + '.fileTextureName', filepath.replace('channel', 'Color') )
            if isUdim: pm.setAttr(file_node + '.uvTilingMode', 3 )
            if setup_shaders:
                pm.connectAttr(file_node + '.outColor', shader_name + '.color', force = True)
            
        if 'SpecRough' in channels:
            file_node = object_name + '_' + 'SpecRough' + '_file'
            if pm.objExists(file_node):
                pm.delete(file_node)
            pm.shadingNode('file', name = file_node, asTexture = True)
            pm.setAttr(file_node + '.fileTextureName', filepath.replace('channel', 'SpecRough') )
            if isUdim: pm.setAttr(file_node + '.uvTilingMode', 3 )
            pm.setAttr(file_node + '.alphaIsLuminance', 1 )
            if setup_shaders:
                pm.connectAttr(file_node + '.outAlpha', shader_name + '.roughness', force = True)         
            
        if 'SpecColor' in channels:
            file_node = object_name + '_' + 'SpecColor' + '_file'
            if pm.objExists(file_node):
                pm.delete(file_node)
            pm.shadingNode('file', name = file_node, asTexture = True)
            pm.setAttr(file_node + '.fileTextureName', filepath.replace('channel', 'SpecRough') )
            if isUdim: pm.setAttr(file_node + '.uvTilingMode', 3 )
            if setup_shaders:
                pm.connectAttr(file_node + '.outColor', shader_name + '.specularColor', force = True)    
        
        if ('Disp' in channels) or ('Bump' in channels) or ('Normal' in channels):  
                             
            if 'Disp' in channels:            
                file_node = object_name + '_' + 'Disp' + '_file'
                channel = 'Disp'
                
            if 'Bump' in channels:
                file_node = object_name + '_' + 'Bump' + '_file'  
                channel = 'Bump'   
                       
            if 'Normal' in channels:
                file_node = object_name + '_' + 'Normal' + '_file'
                channel = 'Normal'
                
            if pm.objExists(file_node):
                pm.delete(file_node)
                
            bump_node = file_node + '_bump'
            if pm.objExists(bump_node): pm.delete(bump_node)
            pm.shadingNode('file', name = file_node, asTexture = True)
            pm.setAttr(file_node + '.alphaIsLuminance', 1 )
            pm.setAttr(file_node + '.fileTextureName', filepath.replace('channel', channel) )
            
            if setup_shaders:
                pm.shadingNode('bump2d', name = bump_node, asTexture = True)            
                pm.setAttr(bump_node + '.bumpDepth', 0.1)            
                pm.connectAttr(file_node + '.outAlpha', bump_node + '.bumpValue', force = True)    
                pm.connectAttr(bump_node + '.outNormal', shader_name + '.normalCamera', force = True) 
                
                if 'Normal' in channels:   
                    pm.setAttr(bump_node + '.bumpInterp', 1)

            if isUdim: pm.setAttr(file_node + '.uvTilingMode', 3 )         
    
def fix_file_nodes():
    '''Renames all file nodes'''
    nodes = pm.ls(textures = True)
    fix_counter = 0
    for node in nodes:
        if node.nodeType() == 'file':
            tmp_name = pm.getAttr(node + '.fileTextureName').split('/')[-1].split('.')[0].split('_')
            new_name = tmp_name[0] + '_' + tmp_name[1] + '_File'
            node.rename(new_name)
            fix_counter += 1
    
    
    pm.warning('Renamed ' + str(fix_counter) + ' file node(s)')
    
def find_bad_shader_names():
    '''Selects badly named shaders.'''
    bad_names = []
    nodes = pm.ls(materials = True)
    for node in nodes:
        bad_elements = ['_', 'lambert', 'phong', 'blinn', 'anisotropic']
        
        if any(x in node.name() for x in bad_elements): 
            if node.name() != 'lambert1':
                bad_names.append(node)

    pm.warning('Found ' + str(len(bad_names)) + ' badly named shader(s)')
    pm.select(bad_names)
        
        
