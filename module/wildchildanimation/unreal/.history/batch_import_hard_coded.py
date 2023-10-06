import unreal
from unreal import EditorAssetLibrary
import time

#Import settings for FBX animation
def fbx_anim_import_task_settings(skeleton_path):
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations', True)
    options.set_editor_property('create_physics_asset', False)
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_rigid_mesh',False)
    options.set_editor_property('import_materials',False)
    options.set_editor_property('import_textures' , False)
    options.set_editor_property('import_as_skeletal', True)
    
    options.set_editor_property('automated_import_should_detect_type', False)
    options.set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    options.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_ANIMATION)

    #options.set_editor_property('Skeleton', unreal.find_asset(skeleton_path))
    options.skeleton = unreal.load_asset(skeleton_path)

    #options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    #options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    #options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)

    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)

    options.anim_sequence_import_data.set_editor_property('import_meshes_in_bone_hierarchy', True)
    options.anim_sequence_import_data.set_editor_property('use_default_sample_rate', False)
    #task.options.anim_sequence_import_data.set_editor_property('custom_sample_rate', asset_doc.get("data", {}).get("fps"))
    options.anim_sequence_import_data.set_editor_property('import_custom_attribute', True)
    options.anim_sequence_import_data.set_editor_property('import_bone_tracks', True)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    options.anim_sequence_import_data.set_editor_property('convert_scene', True)

    #options.FbxSceneImportOptionsSkeletalMesh.set_editor_property('import_morph_targets', True)

    return options

def build_import_task(filename, destination_path, options):
    task = unreal.AssetImportTask()
    task.set_editor_property('filename', filename)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('save', False)
    task.set_editor_property('automated', True)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('options', options)
    
    return task


if __name__ == "__main__":
    skeleton_path = '/Game/assets/characters/honey_ava/components/fbx/sk_hnl_char_honey_ava_Skeleton.sk_hnl_char_honey_ava_Skeleton'
    fbx_file = 'D:\\productions\\HNL\\hnl_build\\shots\\hnl_ep000\\sc010\\sh010\\cache\\sc010_sh010_cache\\shot_cache\\cache\\fbx\\ep000_sc010_sh010_char_honey_ava_0000_fbx.fbx'
    asset_path = '/Game/animation/tmp/'

    options = fbx_anim_import_task_settings(skeleton_path)
    fbx_task = build_import_task(fbx_file, asset_path, options)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([fbx_task]) 

    asset_content = EditorAssetLibrary.list_assets(asset_path, recursive=True, include_folder=True)

    for a in asset_content:
        EditorAssetLibrary.save_asset(a)

    #while (True):
        #time.sleep(100)
