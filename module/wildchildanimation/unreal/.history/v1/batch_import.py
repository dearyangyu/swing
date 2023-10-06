''' 
    Original Author: Piotr Karbowski 
    Version: 1.00
    Date: 2022/06/15
'''

import os
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
    log = "{} swing [abc-import]: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
    for log_data in args:
        log += " {}".format(log_data)
    log += "\n"
    print(log, flush=True, end='')

def import_task_settings(startframe,endframe):
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
            options = import_task_settings(startframe,endframe)
            abc_task = build_import_task(abc, asset_path, options)
            
            execute_import_tasks([abc_task])
            write_log(abc + ' IMPORTED SUCCESFULLY')
        except:
            write_log(abc + ' ****** ERROR IMPORTING ABC *****')
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
    import_alembic(episode, abc_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--episode', help='Episode', default='None')
    parser.add_argument('-d', '--dir', help='Source directory', default='None')


    args = parser.parse_args()
    process(args)        
