import opentimelineio as otio
import argparse
from datetime import datetime
import os
import traceback

ROOT_DIR = "Z:/productions/wotw/witw_post/master_output/witw_102cpt"

EP_XML = "{}/{}".format(ROOT_DIR, "witw_102_layout_v15_export.xml")
VIDEO_SOURCE = "{}/{}".format(ROOT_DIR, "witw_102_layout_v15.mp4")
TARGET_FOLDER = "{}/{}".format(ROOT_DIR, "exports")

CLEAN_NAME = [
    ".mp4"
]

FFMPEG = "C:/ffmpeg/ffmpeg-2021-03-09-git-c35e456f54-full_build/bin/ffmpeg.exe -hide_banner -loglevel error"

ONE_FRAME = otio.opentime.RationalTime(1, 25)


def _process_shot(prefix, item, track_range, source, target_dir):
    item_name = item.name
    for clip_item in CLEAN_NAME:
        if clip_item in item_name:
            item_name = item_name.replace(clip_item, "")

    item_name = item_name.lower()
    if not item_name.startswith("sc"):
        return False

    ## frames
    seqStart = track_range.start_time.value
    seqEnd = track_range.end_time_exclusive().value    

    ## seconds
    seqStart = 1 / 25 * seqStart
    seqEnd = 1 / 25 * seqEnd

    start_time = datetime.fromtimestamp(seqStart).strftime('%H:%M:%S.%f')
    end_time = datetime.fromtimestamp(seqEnd).strftime('%H:%M:%S.%f')

    print("{} {}:{}".format(item_name, seqStart, seqEnd))

    images_dir = os.path.join(target_dir, "{}_{}".format(prefix, item_name), "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    audio_dir = os.path.join(target_dir, "{}_{}".format(prefix, item_name), "audio")
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)    

    video_output = "{}/{}_{}.%04d.jpg".format(images_dir, prefix, item_name)
    
    command = FFMPEG + " -y -ignore_chapters 1 -i " + source + " -start_number 0" + " -ss  " + start_time + " -to " + end_time + " " + video_output
    try:
        os.system(command)
    except:
        traceback.print_exc()

    audio_output = "{}/{}_{}.wav".format(audio_dir, prefix, item_name)
    try:
        ###command = FFMPEG + " -i " + source + frame_select + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + audio_output

        command = FFMPEG + " -y -i " + source + " -ss  " + start_time + " -to " + end_time + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + audio_output
        os.system(command)
    except:
        traceback.print_exc()  

    ###print("{} {} {}".format(sequenceStartTime.to_time_string(), sequenceEndTime.to_time_string(), video_output))
    # print("Video {}: {} {}".format(item_name, start_time, end_time))
    video_output = "{}/{}_{}.mp4".format(target_dir, prefix, item_name)    
    try:
        command = FFMPEG + " -y -i " + source + " -ss  " + start_time + " -to " + end_time + " -c:v libx264 -crf 30 -an " + video_output
        
        os.system(command)
    except:
        traceback.print_exc()                

def _process_track(prefix, track, track_no, source, target_dir):

    for n, item in enumerate(track):
        if not isinstance(item, otio.schema.Clip):
            continue

        track_range = track.range_of_child_at_index(n)

        _process_shot(prefix, item, track_range, source, target_dir)


def build_sequence(prefix, timeline, source, target_dir):
    tracks = [
        track for track in timeline.tracks
        if track.kind == otio.schema.TrackKind.Video
    ]

    track_index = 1

    for track_no, track in enumerate(reversed(tracks)):
        if len(track) > 0:

            #_build_track(track, track_no, existing_shots=existing_shots)
            _process_track(prefix, track, track_index, source, target_dir)
            track_index += 1


def read_from_file(path, source, target_dir):
    file_parts = os.path.basename(source).split("_")
    prefix = "{}_{}".format(file_parts[0], file_parts[1])

    print("Processing {} using prefix {} into {}".format(source, prefix, target_dir))

    timeline = otio.adapters.read_from_file(path)
    build_sequence(prefix, timeline, source, target_dir)

    print("Processing complete")

def process(args):
    source = args.dir
    xml = args.xml
    video = args.video
    target = args.target

    xml_file = os.path.join(source, xml)
    if not os.path.exists(xml_file):
        print("Error: XML file [{}] not found".format(xml_file))
        return False

    if not os.path.isfile(xml_file):
        print("Error: Invalid XML file [{}]".format(xml_file))
        return False 

    video_file = os.path.join(source, video)
    if not os.path.exists(video_file):
        print("Error: Video file [{}] not found".format(video_file))
        return False

    if not os.path.isfile(video_file):
        print("Error: Invalid video file [{}]".format(video_file))
        return False                     
        
    target_folder = os.path.join(source, target)
    if os.path.exists(target_folder):
        print("Error: Target already exists [{}]".format(target_folder))
        return False

    read_from_file(xml_file, video_file, target_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='Source directory', default='None')
    parser.add_argument('-x', '--xml', help='XML file', default='None')
    parser.add_argument('-v', '--video', help='Video reference', default='None')
    parser.add_argument('-t', '--target', help='Target directory', default='None')

    args = parser.parse_args()
    process(args)

