# -*- coding: utf-8 -*-
'''
    Given CSV and Media files, update Edit Task
'''
import sys
import shutil
import os
import re
import argparse
import json
import csv

import traceback

from pathlib import Path

import time
import mimetypes

from datetime import datetime, timedelta

import glob

import gazu

task_types = {
    "34401781-750a-4afb-a31f-8e11f263b066",
    "a28bba26-de47-485b-89e3-3b66358f298d",
    "5cae9028-d062-49f0-b5e1-b405c28b46fa",
    "4c349ee1-46e3-4aa2-8dc7-2592c2abaffc",
    "655e97b8-adaf-43d0-b0be-d72ab8328229"
}

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def just_numbers(not_just_numbers):
    return re.findall(r'\d+', not_just_numbers)

def get_shot_task(shot, task_type_name, task_status):
    tasks = gazu.task.all_tasks_for_shot(shot)
    for t in tasks:
        if t["task_type_name"] == task_type_name and t["task_status_name"] == task_status["name"]:
                return t
    return False

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")    

def process(project_name, episode_name, task_type_name, task_status_name, edit_list_csv):
    gazu.client.set_host("https://production.wildchildanimation.com/api")
    gazu.log_in("showadmin@digitalevolution.co.za", "Monday@01")

    project = gazu.project.get_project_by_name(project_name)
    episode = gazu.shot.get_episode_by_name(project, episode_name)
    task_status = gazu.task.get_task_status_by_name(task_status_name)
    

    working_path = Path(edit_list_csv).parent

    ln = 0
    with open(edit_list_csv, encoding="utf16") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')

        for row in csv_reader:
            # skip header
            if ln == 0:
                ln = ln + 1
                continue

            shot_field = row[0]

            shot_details = shot_field.split('_')

            print("<-- {}".format(shot_details))

            if len(shot_details) < 3:
                print("Skipping {}".format(shot_field))
                continue

            ep = shot_details[0]
            sc = just_numbers(shot_details[1])
            sh = just_numbers(shot_details[2])

            # desc = row[1]
            frame_in = row[2]
            frame_out = row[3]
            duration = row[4]

            number = sc[0]

            scene_name = "sc{}".format(number.zfill(3))

            number = sh[0]
            shot_name = "sh{}".format(number.zfill(3))
            #for sequence in gazu.shot.all_sequences_for_episode(episode):
            #    print(sequence)

            sequence = gazu.shot.get_sequence_by_name(project, scene_name, episode)
            if not sequence:
                sequence = gazu.shot.new_sequence(project, scene_name, episode)
                print("added sequence {}".format(sequence["name"]))

            shot = gazu.shot.get_shot_by_name(sequence, shot_name)

            if not shot:
                shot = gazu.shot.new_shot(project, sequence, shot_name)
                print("added shot {}".format(shot["name"]))

            tasks = gazu.task.all_tasks_for_shot(shot)
            if not tasks:
               
                for tt in task_types:
                    task_type = gazu.task.get_task_type(tt)
                    try:
                        gazu.task.new_task(shot, task_type)
                        print("{} added".format(task_type["name"]))
                    except:
                        print("{} exists".format(task_type["name"]))

            shot["nb_frames"] = duration

            data = {}
            data["frame_in"] = frame_in
            data["frame_out"] = frame_out

            shot = gazu.shot.update_shot(shot)
            gazu.shot.update_shot_data(shot, data)

            if "tg108bisc_animatic_v011.csv" in edit_list_csv:
                shot_field = shot_field.replace("tg108_", "tg108bisc_")

            if "wd_0" in shot_field:
                shot_field = shot_field.replace('wd_0', 'wd_')

            if "tg112out_" in shot_field:
                shot_field = shot_field.replace('tg112out_', 'tg112_')

            if "TG113zom_" in shot_field:
                shot_field = shot_field.replace('TG113zom_', 'tg113_')   

            if "tg114_0" in shot_field:
                shot_field = shot_field.replace("tg114_0", "tg114air_")  

            if 'tg111tea_80sng_010.mp4' in shot_field:
                shot_field = shot_field.replace('tg111tea_80sng_010.mp4', 'tg111tea_80sng_010.mp4')

            if 'tg117les_' in shot_field:
                shot_field = shot_field.replace('tg117les_', 'tg1117les_')


            preview = Path("{}/{}.mp4".format(working_path.as_posix(), shot_field))
            if preview.exists():
                task = get_shot_task(shot, task_type_name, task_status)

                if not task:
                    continue
                
                previews = gazu.files.get_all_preview_files_for_task(task)

                if len(previews) == 0:                
                    comment = gazu.task.add_comment(task, task_status, current_time())
                    gazu.task.add_preview(task["id"], comment, preview.as_posix())
                    print("{} added".format(preview.as_posix()))
            # shot = gazu.shot.get_shot_by_name(sequence, "sh{}".format(sh))

            print("{} {} {} {} {} {}".format(ep, sc, sh, frame_in, frame_out, duration))
            ln = ln + 1 # line num

    print("{}: Completed project: {}".format(current_time(), project["name"]))

def main(args):
    parser = argparse.ArgumentParser(args)
    parser.add_argument("-p", "--project", default = "Tom Gates S1", help="Project Name")
    parser.add_argument("-e", "--episode", default = "tg_2d_ep000", help="Epsiode Name")

    parser.add_argument("-t", "--task", default = "Anim-Block", help="Task Type")
    parser.add_argument("-s", "--status", default = "WFA", help="Task Status")
    parser.add_argument("-a", "--source", default = "edit_list.csv", help="Edit list CSV with media files in same dir")

    args = parser.parse_args()
    process(args.project, args.episode, args.task, args.status, args.source)


if __name__ == '__main__':
    executable = sys.argv[0]
    args = sys.argv[1:]
    main(args)