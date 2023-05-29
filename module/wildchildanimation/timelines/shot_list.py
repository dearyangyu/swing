from xml.dom import minidom
from datetime import timedelta

test = "C:/DEV/incoming/shot_numbers_test_2.xml"

def process_xml(file_name):
    dat = open(file_name)
    dom = minidom.parse(dat)

    sequence = dom.getElementsByTagName('sequence')

    shot_list = []

    if len(sequence) == 0:
        return None

    main_sequence = sequence[0]

    sequence_name = main_sequence.getElementsByTagName("name")[0].firstChild.data
    sequence_duration = main_sequence.getElementsByTagName("duration")[0].firstChild.data
    sequence_rate = float(main_sequence.getElementsByTagName("rate")[0].getElementsByTagName("timebase")[0].firstChild.data)

    #print("Sequence Name: {} Duration: {} frames {} fps".format(sequence_name, sequence_duration, sequence_rate))

    shots = main_sequence.getElementsByTagName("clipitem")

    start = 0
    end = 0
    frame_in = 0
    frame_out = 0

    #print("Shot Name\tFrame Start\tFrame End\tStart Time\t\tEnd Time")

    for shot in shots:
        shot_name = shot.getElementsByTagName("name")[0].firstChild.data
        #shot_duration = shot.getElementsByTagName("duration")[0].firstChild.data

        shot_start = int(shot.getElementsByTagName("start")[0].firstChild.data)
        start += shot_start

        shot_end = int(shot.getElementsByTagName("end")[0].firstChild.data)
        end += shot_end

        shot_frame_in = int(shot.getElementsByTagName("in")[0].firstChild.data)
        frame_in += shot_frame_in

        shot_frame_out = int(shot.getElementsByTagName("out")[0].firstChild.data)
        frame_out += shot_frame_out

        time_start = timedelta(seconds=(int(shot_start) / sequence_rate))
        time_end = timedelta(seconds=(int(shot_end) / sequence_rate))

        #print("{} {} {} {} {}".format(shot_name, shot_start, shot_end, shot_frame_in, shot_frame_out))
        # print("{}\t\t{}\t\t{}\t{}\t\t{}".format(shot_name, shot_start, shot_end - 1, time_start, time_end))

        shot_list.append({
            "name": shot_name, "frame_in": shot_start, "frame_out": shot_end - 1, "start": time_start, "end": time_end
        })

    return sequence_name, sequence_rate, sequence_duration, shot_list

      # 09:36:05 in the edit starting from 0 - I havn't included intro and end credits, and this edit is still rough, so should be 09:30:00 once it's locked
      # New
      # 2:30
      # that's 14406 frames long (or 14405 from 0)
      # print("{} {} {} {} {}".format(x1, x2, x3, x4, x5))
      #print(shot_name)


    #for shot in shots:
    #  shot_name = shot.attrib["name"]
    #  print(shot_name)


  #for child in root:
  #  print(child.tag, child.attrib)


if __name__ == "__main__":
  process_xml(test)

