''' 
    Original Author: Piotr Karbowski 
    Version: 1.00
    Date: 2022/06/15
'''

import os
import glob

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

def import_task_settings():
    taskoptions = unreal.AbcImportSettings()
    taskoptions.import_type = unreal.AlembicImportType.SKELETAL
    taskoptions.compression_settings.merge_meshes = True
    taskoptions.material_settings.find_materials = True
    taskoptions.conversion_settings.rotation = (90, 0, 0)
    taskoptions.normal_generation_settings.hard_edge_angle_threshold = 0
    taskoptions.compression_settings.base_calculation_type = unreal.BaseCalculationType.NO_COMPRESSION
    taskoptions.sampling_settings = unreal.AbcSamplingSettings(skip_empty=True)
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

def import_alembic(project, episode, abc_files, localization):
    for abc in abc_files:
        head, tail = os.path.split(abc)
        file_parts = tail.split("_")

        if len(file_parts) < 7:
            print("Invalid naming convention found in: {}, skipping item".format(abc))
            continue

        scene = file_parts[2]
        shot = file_parts[3]

        asset_type = file_parts[5]
        asset_name = "{}_{}_abc".format(file_parts[6], file_parts[7])

        asset_path = "/Game/animation/episodes/{}/{}/{}/{}/{}".format(episode, scene, shot, asset_type, asset_name)
        unreal.EditorAssetLibrary.make_directory(directory_path=asset_path)

        options = import_task_settings()
        abc_task = build_import_task(abc, asset_path, options)
        
        execute_import_tasks([abc_task])
        print(abc + ' IMPORTED SUCCESFULLY')

def process(args):
    source = args.dir
    loc = args.loc
    project = args.project
    episode = args.episode

    #dir = r"C:\WILDCHILD\UNREAL_ENGINE\ue_tmp_for_rigging\abc_folder\*.abc"

    abc_files = []
    for file in glob.glob("{}/*.abc".format(source)):
        abc_files.append(file)

    print("ALEMBIC directory paths for imported files to UE: {0}".format(abc_files))

    # localization = '/Game/animation/episodes/101_alickofpaint/sc010/sh010/char/'    
    import_alembic(project, episode, abc_files, loc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project', default='None')
    parser.add_argument('-e', '--episode', help='Episode', default='None')

    parser.add_argument('-d', '--dir', help='Source directory', default='None')
    parser.add_argument('-l', '--loc', help='Localization', default='None')


    args = parser.parse_args()
    process(args)        





