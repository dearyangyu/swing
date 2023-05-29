import opentimelineio as otio
import argparse
from datetime import datetime
import os
import traceback

ROOT_DIR = r"S:\productions\sdmp\sdmp_post\master_output\SDMP061"

EP_XML = "{}/{}".format(ROOT_DIR, r"sdmp061.xml")
VIDEO_SOURCE = "{}/{}".format(ROOT_DIR, r"sdmp061.mov")
TARGET_FOLDER = "{}/{}".format(ROOT_DIR, r"exporttest")

CLEAN_NAME = [
    ".mp4", ".mov"
]

FFMPEG = "C:/ffmpeg/ffmpeg-2021-03-09-git-c35e456f54-full_build/bin/ffmpeg.exe -hide_banner -loglevel error"

ONE_FRAME = otio.opentime.RationalTime(1, 25)

def tcToSec(timecode, fps):
    h, m, s, f = timecode.split(':')
    return float(h) * 3600 + float(m) * 60 + float(s) + float(f) / float(eval(fps))

def _process_shot(prefix, item, track_range, source, target_dir):
    item_name = item.name
    for clip_item in CLEAN_NAME:
        if clip_item in item_name:
            item_name = item_name.replace(clip_item, "")

    item_name = item_name.lower()
    if not (item_name.startswith("sc") or item_name.startswith("sdmp")):
        return False

    ## frames
    seqStartVal = track_range.start_time.value
    seqEndVal = track_range.end_time_exclusive().value    

    if "sdmp" in prefix.lower():
        # for SDMP: set fps to 23.976 and use the full name from the file
        fps = 24
    else:
        fps = 25

    ## seconds
    seqStart = 1 / fps * seqStartVal
    seqEnd = 1 / fps * seqEndVal

    start_time = datetime.fromtimestamp(seqStart).strftime('%H:%M:%S.%f')
    end_time = datetime.fromtimestamp(seqEnd).strftime('%H:%M:%S.%f')

    print("{} {}:{}".format(item_name, start_time, seqEnd))

    if "sdmp" in prefix.lower():
        images_dir = os.path.join(target_dir, "{}".format(item_name), "images")
    else:
        images_dir = os.path.join(target_dir, "{}_{}".format(prefix, item_name), "images")

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)


    if "sdmp" in prefix.lower():
        audio_dir = os.path.join(target_dir, "{}".format(item_name), "audio")
    else:
        audio_dir = os.path.join(target_dir, "{}_{}".format(prefix, item_name), "audio")

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)    

    if "sdmp" in prefix.lower():
        video_output = "{}/{}.%04d.jpg".format(images_dir, item_name)
    else:
        video_output = "{}/{}_{}.%04d.jpg".format(images_dir, prefix, item_name)
    
    command = FFMPEG + " -y -ignore_chapters 1 -i " + source + " -start_number 0" + " -ss  " + start_time + " -to " + end_time + " " + video_output
    try:
        os.system(command)
    except:
        traceback.print_exc()

    if "sdmp" in prefix.lower():        
        audio_output = "{}/{}.wav".format(audio_dir, item_name)
    else:
        audio_output = "{}/{}_{}.wav".format(audio_dir, prefix, item_name)

    try:
        ###command = FFMPEG + " -i " + source + frame_select + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + audio_output
        command = FFMPEG + " -y -i " + source + " -ss  " + start_time + " -to " + end_time + " -acodec pcm_s16le" + " -ac 1" + " -ar 16000 " + audio_output
        os.system(command)
    except:
        traceback.print_exc()  

    ###print("{} {} {}".format(sequenceStartTime.to_time_string(), sequenceEndTime.to_time_string(), video_output))
    # print("Video {}: {} {}".format(item_name, start_time, end_time))

    if "sdmp" in prefix.lower():       
        video_output = "{}/{}.mp4".format(target_dir, item_name)    
    else:
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
    fn, _ = os.path.splitext(source)
    file_parts = os.path.basename(fn).split("_")
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

