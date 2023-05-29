import opentimelineio as otio
import argparse
from datetime import datetime
import os
import traceback

from glob import glob

ROOT_DIR = r"S:\productions\sdmp\sdmp_post\master_output\SDMP061"

EP_XML = "{}/{}".format(ROOT_DIR, r"sdmp061.xml")
VIDEO_SOURCE = "{}/{}".format(ROOT_DIR, r"sdmp061.mov")
TARGET_FOLDER = "{}/{}".format(ROOT_DIR, r"exporttest")

CLEAN_NAME = [
    ".mp4", ".mov"
]

FFMPEG = "C:/ffmpeg/ffmpeg-2021-03-09-git-c35e456f54-full_build/bin/ffmpeg.exe -hide_banner -loglevel error"

ONE_FRAME = otio.opentime.RationalTime(1, 25)

def export(video_list, target_dir):
    for item in video_list:
        print("Processing {}".format(item))

        fn, _ = os.path.splitext(item)
        item_name = os.path.basename(fn)

        shot_parts = item_name.split("_")
        item_name = "{}_{}_{}".format(shot_parts[0], shot_parts[1], shot_parts[2])        

        for clip_item in CLEAN_NAME:
            if clip_item in item_name:
                item_name = item_name.replace(clip_item, "")

        images_dir = os.path.join(target_dir, "{}".format(item_name), "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        audio_dir = os.path.join(target_dir, "{}".format(item_name), "audio")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)    

        video_output = "{}/{}.%04d.jpg".format(images_dir, item_name)            

        command = FFMPEG + " -y -ignore_chapters 1 -i " + item + " -start_number 0" " " + video_output
        try:
            os.system(command)
        except:
            traceback.print_exc()

        audio_output = "{}/{}.wav".format(audio_dir, item_name)
        try:
            command = FFMPEG + " -y -i " + item + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + audio_output
            os.system(command)
        except:
            traceback.print_exc()  

def process(args):
    source = args.dir
    xml = args.xml    
    target = args.target

    source_videos = []

    for item in glob("{}/**".format(source)):
        _, ext = os.path.splitext(item)
        if ext.lower() in [".mov", ".mp4"]:
            source_videos.append(item)


    target_folder = os.path.join(source, target)

    print(source_videos)
    export(source_videos, target_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='Source directory', default='None')
    parser.add_argument('-x', '--xml', help='XML file', default='None')    
    parser.add_argument('-t', '--target', help='Target directory', default='None')

    args = parser.parse_args()
    process(args)

