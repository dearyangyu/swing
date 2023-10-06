''' 
    Original Author: Piotr Karbowski 
    Version: 1.00
    Date: 2022/06/15




'''

'''import os
import glob
import traceback
from pathlib import Path

from datetime import datetime

try:
    import unreal
except:
    print("Unreal module not found")

import argparse
"""
    Alembic Batch Importer
    :param str dir: Directory path to folder with alembic files. Change until * .
    :param str localization: Directory path to folder where alembic files should be imported.

"""

def write_log(*args):
    log = "swing [batch-import]: "
    for log_data in args:
        log += " {}".format(log_data)
    log += "\n"
    print(log, flush=True, end='')

def abc_import_task_settings(startframe,endframe):
    taskoptions = unreal.AbcImportSettings()
    taskoptions.import_type = unreal.AlembicImportType.SKELETAL

    taskoptions.compression_settings.merge_meshes = True
    taskoptions.compression_settings.bake_matrix_animation = True
    taskoptions.compression_settings.base_calculation_type = unreal.BaseCalculationType.NO_COMPRESSION
        
    taskoptions.material_settings.find_materials = True
    taskoptions.conversion_settings.rotation = (90, 0, 0)

    taskoptions.sampling_settings = unreal.AbcSamplingSettings(skip_empty=True)
    taskoptions.sampling_settings.frame_start = startframe
    #taskoptions.sampling_settings.frame_end = 106
    if endframe:
        taskoptions.sampling_settings.frame_end = endframe

    taskoptions.sampling_settings.skip_empty = False

    taskoptions.normal_generation_settings.hard_edge_angle_threshold = 0
    taskoptions.normal_generation_settings.recompute_normals = True
    return taskoptions

def get_skeletalmesh_path(asset_type, asset_variant, parent):
    if asset_type == 'char':
        skeleton_path = "/Game/assets/characters/{}/components/{}/sk_hnl_{}_{}_Skeleton.sk_hnl_{}_{}_Skeleton".format(asset_variant, parent, asset_type, asset_variant,asset_type, asset_variant)
        print('\n')
        print('\n')
        print('**************************************************************************************************************************************************************\n')
        print('SKELETON PATH:\n')
        print(skeleton_path)
        print('\n**************************************************************************************************************************************************************\n')
        print('\n')
        print('\n')
        return(skeleton_path)

#Import settings for FBX animation
def fbx_anim_import_task_settings(skeleton_path):
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations', True)
    options.set_editor_property('create_physics_asset', True)
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_rigid_mesh',False)
    options.set_editor_property('import_materials',False)
    options.set_editor_property('import_textures' , False)
    options.set_editor_property('import_as_skeletal', True)
    #options.set_editor_property('automated_import_should_detect_type', False)
    #options.set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    #options.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_ANIMATION)

    #options.set_editor_property('Skeleton', unreal.find_asset(skeleton_path))
    options.skeleton = unreal.load_asset(skeleton_path)

    #options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    #options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    #options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)

    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    return options

def build_import_task(filename, destination_path, options):
    task = unreal.AssetImportTask()
    task.set_editor_property('filename', filename)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('save', True)
    task.set_editor_property('automated', True)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('options', options)
    return task

def execute_import_tasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

#Import alembic caches as Skeletal mesh (depreciated)
def import_alembic(episode, abc_files):
    for abc in abc_files:
        try:
            head, tail = os.path.split(abc)
            file_parts = tail.split("_")

            if len(file_parts) < 7:
                write_log("Invalid naming convention found in: {}, skipping item".format(abc))
                continue

            scene = file_parts[2]
            shot = file_parts[3]

            asset_type = file_parts[5]
            asset_name = "{}_{}_abc".format(file_parts[6], file_parts[7])

            # get parent dir name for grouping {abc/head/etc}
            parent = Path(abc).parent.absolute().stem            

            asset_path = "/Game/animation/episodes/{}/{}/{}/{}/{}/{}".format(episode, scene, shot, asset_type, asset_name, parent)
            unreal.EditorAssetLibrary.make_directory(directory_path=asset_path)

            if "_abc.abc" in abc:
                # unchunked
                startframe = (-2)
                endframe = None

            else:
                # chunked
                startframe = int(file_parts[-3])
                endframe = int(file_parts[-2])

            write_log("start frame: {} ".format(startframe))
            write_log("end frame: {} ".format(endframe))
            options = abc_import_task_settings(startframe,endframe)
            abc_task = build_import_task(abc, asset_path, options)
            
            execute_import_tasks([abc_task])
            write_log(abc + ' IMPORTED SUCCESFULLY')
        except:
            write_log(abc + ' ****** ERROR IMPORTING ABC *****')
            print(traceback.format_exc())    

#Import FBX animation onto skeletal mesh
def import_fbx_anim(episode, fbx_files):
    for fbx in fbx_files:
        try:
            head, tail = os.path.split(fbx)
            file_parts = tail.split("_")

            if len(file_parts) < 7:
                write_log("Invalid naming convention found in: {}, skipping item".format(fbx))
                continue

            scene = file_parts[1]
            shot = file_parts[2]

            asset_type = file_parts[3]
            asset_name = "{}_{}_fbx".format(file_parts[4], file_parts[5])
            asset_variant = "{}_{}".format(file_parts[4], file_parts[5])

            # get parent dir name for grouping {abc/head/etc}
            parent = Path(fbx).parent.absolute().stem            

            asset_path = "/Game/animation/episodes/{}/{}/{}/{}/{}/{}".format(episode, scene, shot, asset_type, asset_variant, parent)
            unreal.EditorAssetLibrary.make_directory(directory_path=asset_path)

            if "_fbx.fbx" in fbx:
                # unchunked
                startframe = None
                endframe = None

            else:
                # chunked
                startframe = int(file_parts[-3])
                endframe = int(file_parts[-2])
            print('FBX:{}'.format(fbx))
            skeleton_path = get_skeletalmesh_path(asset_type, asset_variant, parent)

            options = fbx_anim_import_task_settings(skeleton_path)
            fbx_task = build_import_task(fbx, asset_path, options)
            
            execute_import_tasks([fbx_task])
            write_log(fbx + ' IMPORTED SUCCESFULLY')
        except:
            write_log(fbx + ' ****** ERROR IMPORTING FBX *****')
            print(traceback.format_exc())         

def process(args):
    print("Arg {}".format(args))
    
    source = args.dir
    episode = args.episode

    #dir = r"C:\WILDCHILD\UNREAL_ENGINE\ue_tmp_for_rigging\abc_folder\*.abc"

    write_log("ALEMBIC directory paths for imported files to UE: {0}".format(source))

    abc_files = []
    for file in glob.glob("{}/**/*.abc".format(source), recursive=True):
        abc_files.append(file)
        write_log("Appended file {}".format(file))

    # localization = '/Game/animation/episodes/101_alickofpaint/sc010/sh010/char/'    
    #import_alembic(episode, abc_files)

    write_log("FBX directory paths for imported files to UE: {0}".format(source))

    fbx_files = []
    for file in glob.glob("{}/**/*.fbx".format(source), recursive=True):
        fbx_files.append(file)
        write_log("Appended file {}".format(file))

    # localization = '/Game/animation/episodes/101_alickofpaint/sc010/sh010/char/'    
    import_fbx_anim(episode, fbx_files)

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--episode', help='Episode', default='None')
    parser.add_argument('-d', '--dir', help='Source directory', default='None')
    args = parser.parse_args()

    args_test = Namespace(episode='hnl_ep000', dir='D:\\productions\\HNL\\hnl_build\\shots\\hnl_ep000\\sc010\\sh030\\cache\\sc010_sh030_cache\\shot_cache\\cache')

    print("Server Args: Episode: {} Dir {}".format(args.episode, args.dir))
    print("UE Args Episode: {} Dir {}".format(args_test.episode, args.dir))

    process(args)        
'''

import unreal

#Import settings for FBX animation
def fbx_anim_import_task_settings(skeleton_path):
    options = unreal.FbxImportUI()
    options.set_editor_property('import_animations', True)
    options.set_editor_property('create_physics_asset', True)
    options.set_editor_property('import_mesh',True)
    options.set_editor_property('import_rigid_mesh',False)
    options.set_editor_property('import_materials',False)
    options.set_editor_property('import_textures' , False)
    options.set_editor_property('import_as_skeletal', True)
    #options.set_editor_property('automated_import_should_detect_type', False)
    #options.set_editor_property('original_import_type', unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    #options.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_ANIMATION)

    #options.set_editor_property('Skeleton', unreal.find_asset(skeleton_path))
    options.skeleton = unreal.load_asset(skeleton_path)

    #options.anim_sequence_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    #options.anim_sequence_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    #options.anim_sequence_import_data.set_editor_property('import_uniform_scale', 1.0)

    options.anim_sequence_import_data.set_editor_property('animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property('remove_redundant_keys', False)
    return options

def build_import_task(filename, destination_path, options):
    task = unreal.AssetImportTask()
    task.set_editor_property('filename', filename)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('save', True)
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
