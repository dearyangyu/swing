import opentimelineio as otio

def write_to_string(input_otio):
    """Turn a single track timeline into a very simple CSV."""
    result = "Clip,Start,Duration\n"

    for track in input_otio.tracks:
        for clip in track.each_clip():
            start = otio.opentime.to_seconds(clip.source_range.start_time)
            duration = otio.opentime.to_seconds(clip.source_range.duration)
            clip_data = "{} {} {}".format(clip.name, start, duration)

            print("A: {} Start Time {} Duration {}".format(clip_data, clip.trimmed_range().start_time, clip.trimmed_range().duration))
            print("B: {} Start Time {} Duration {}".format(clip_data, clip.visible_range().start_time, clip.visible_range().duration))            
            print("C: {} Start Time {} Duration {}".format(clip_data, clip.source_range.start_time, clip.source_range.duration))
            print("D: {} Start Time {} Duration {}".format(clip_data, clip.available_range().start_time, clip.available_range().duration))
            #print(clip)
        #print(track)

    return False

    if len(input_otio.tracks) != 1:
        raise Exception("This adapter does not support multiple tracks.")
    for item in input_otio.each_clip():
        start = otio.opentime.to_seconds(item.source_range.start_time)
        duration = otio.opentime.to_seconds(item.source_range.duration)
        result += ",".join([item.name, start, duration]) + "\n"
    return result

EP_XML = "Z:/productions/wotw/witw_post/sandbox/connla/For_Paul/witw_103rit_animatic_09_export_XML.xml"
mytimeline = otio.adapters.read_from_file(EP_XML)

test_string = write_to_string(mytimeline)
print(test_string)