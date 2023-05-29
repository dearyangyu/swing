'''
    Author: A Kanwal
    Date: 9 May 2022
    Version: 1.0.0.0
'''

# from importlib.metadata import metadata
import os
import sys
import traceback
import time

try:
    import OpenEXR
    import Imath
    import traceback
    import numpy
    from PIL import Image
except:
    traceback.print_exc(file=sys.stdout)
    print("Error: OpenEXR not configured correctly, check env")
    
import subprocess

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    from PyQt5.QtCore import pyqtSignal

from wildchildanimation.gui.settings import SwingSettings

class LoadedSignal(QtCore.QObject):
    loaded = pyqtSignal(object)     

class ConvertRunnable(QtCore.QRunnable):

    def __init__(self, source_dir, target_dir, file_list):
        super(ConvertRunnable, self).__init__(self)

        self.source_dir = source_dir
        self.target_dir = target_dir
        self.file_list = file_list

        self.callback = LoadedSignal()

    def run(self):
        count = 0
        for exr_file in self.file_list:
            exr_path = os.path.join(self.source_dir, exr_file)
            exr = OpenEXR.InputFile(exr_path)
            header = exr.header()
            dw = header['dataWindow']
            size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
            pixel_type = Imath.PixelType(Imath.PixelType.FLOAT)
            rgb = [numpy.fromstring(exr.channel(
                c, pixel_type), dtype=numpy.float32) for c in 'RGB'
            ]
            for i in range(3):
                rgb[i] = numpy.where(
                    rgb[i] <= 0.0031308,
                    (rgb[i] * 12.92) * 255.0,
                    (1.055 * (rgb[i] ** (1.0 / 2.4)) - 0.055) * 255.0)
        
            rgb8 = [Image.frombytes('F', size, c.tostring()).convert('L') for c in rgb]

            # Providing new png file path every time using exr file name to create png file with same name
            png_path = os.path.join(self.target_dir, os.path.splitext(exr_file)[0] + '.png')
            Image.merge('RGB', rgb8).save(png_path, 'PNG')

            print("{}/{}: EXR::PNG -> {}".format(count, len(self.file_list), exr_file))
            self.callback.loaded.emit(count)
            count += 1

        return True            


class SwingConvert(QtCore.QObject):

    def __init__(self, media_file, source_dir, temp_dir, audio_path = None, preset_speed="veryfast", framerate=25, caption="Render", artist="WCA-Teams", album="WITW", genre="children-animation"):
        super(SwingConvert, self).__init__() 

        self.media_file = media_file
        self.source_dir = source_dir
        self.temp_dir = temp_dir

        self.caption = caption

        self.settings = SwingSettings.get_instance()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.audio_path = audio_path
        self.preset_speed = preset_speed
        self.framerate = framerate

        self.source_files = []

        self.artist = artist
        self.album = album

        ## self.exr_files = os.listdir("{}/*.exr".format(self.exr_files_loc))
        
        # Creating -metadata string using is repeatingly
        # Creating list of metadata add information
        self.metadata = "-metadata"
        self.metalist = [f"title='{self.caption}'", f"artist='{self.artist}'", f"album='{self.album}'", f"genre='{genre}'"]

    # Fuction returns add metadata section of to ffmpeg command
    def add_meta_information(self):
        metadata = ""
        for meta_info_item in self.metalist:
            string = self.metadata + " " + meta_info_item + " "
            metadata += string
        return metadata

    # Checking if files are correct exr files
    def check_exr_files(self):
        print("Checking if all exr files are correct exr files in folder.")
        for item in self.source_files:
            item_path = os.path.join(self.source_dir, item)
            exr_files_exist = OpenEXR.isOpenExrFile(item_path)

            if exr_files_exist:
                print("OpenEXR.isOpenExrFile::{}".format(item_path))
            else:
                print(f"OpenEXR.isOpenExrFile: Invalid file - Please check your exr files directory, {item_path} is not exr file.")
                return False
        return True

    # Checking PNGs folder is empty
    def check_png_folder_is_empty(self):
        file_list = os.listdir(self.temp_dir)
        if len(file_list) > 0:
            ## print("Error: There are already files inside you PNG directory please remove.")
            return False

        return True

    # Function rename file to match regular expression %04d
    def rename_png_files(self):
        for count, filename in enumerate(os.listdir(self.temp_dir)):
            z_fill = str(count).zfill(4)
            new_file_name = f"{self.caption}.{z_fill}.png"
            src =f"{self.temp_dir}\{filename}"
            target = f"{self.temp_dir}\{new_file_name }"
            os.rename(src, target)

            print("{} -> {}".format(src, target))
        
        return True

    def remove_temp_dir(self, temp_dir_path):
        for item in os.listdir(temp_dir_path):
            if item.lower().endswith(".png"):
                os.remove(os.path.join(temp_dir_path, item))
        return True

    # Converts files from EXR to PNG
    def convert(self):
        for item in os.listdir(self.source_dir):
            if item.lower().endswith(".exr"):
                self.source_files.append(item)

        if not self.check_exr_files():
            return False

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)            

        if not self.check_png_folder_is_empty():
            self.remove_temp_dir(self.temp_dir)

        self.worker = ConvertRunnable(self.source_dir, self.temp_dir, self.source_files)
        self.worker.run()
    
        return True
        
        ## self.threadpool.start(self.worker)
        ## return True

    # Returns complete ffmpeg return command
    def ffmpeg_convert_command2(self):
        if self.audio_path:
            self.audio_path = f'-i "{self.audio_path}" -c:v copy -c:a aac'
        
        meta_information = self.add_meta_information()

        ffmpeg_command = self.settings.bin_ffmpeg()

        filters = []
        text_graph = ''
        caption = ''

        #caption = "{} - {}".format(self.title, self.artist)            
        #filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=(w-text_w)/2: y=20: text='{}' ".format(caption, 24))
                #ffmpeg_cmd += " -vf \"drawtext=font=Consolas: fontsize=24: fontcolor=white: text='{}': r={}: x=(w-tw-20): y=h-lh-20: box=1: boxcolor=black\" ".format(caption, 24)

        # Timecode Burn-In
        #filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=5: y=20: timecode='00\:00\:00\:00': r={}: ".format(self.framerate))
        #filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=(w-text_w)-5: y=20: start_number=1: text='%{frame_num}' ")

        for i in range(len(filters)):
            text_graph += filters[i]
            if i < len(filters) - 1:
                text_graph += ', '

        cmd = '{} -y -probesize 5000000 -f image2 -r -i "{}" {} {} -c:v libx265 -preset {} -crf 0 {} -y "{}"'.format( 
            ffmpeg_command,
            self.framerate, 
            os.path.join(self.temp_dir, f'{self.caption}.%04d.png'),
            self.audio_path,
            self.preset_speed,
            meta_information,
            os.path.join(self.media_file, f'{self.caption}.mov')
        )

        return cmd

    def ffmpeg_convert_command(self):
        meta_information = self.add_meta_information()

        ffmpeg_cmd = self.settings.bin_ffmpeg()
        ffmpeg_cmd += r' -y -framerate {0} -i "{1}"'.format(self.framerate, os.path.join(self.temp_dir, f'{self.caption}.%04d.png'))        

        if self.audio_path:
            ffmpeg_cmd += f'-i "{self.audio_path}" -c:v copy -c:a aac'

        filters = []
        text_graph = ''

        title = self.caption
        if self.artist:
            title = "{} - {}".format(self.caption, self.artist)            

        filters.append(r"drawtext=font=Consolas: fontsize=18: fontcolor=white: x=(w-text_w)/2: y=20: text='{}' ".format(title.strip(), 24))
            #ffmpeg_cmd += " -vf \"drawtext=font=Consolas: fontsize=24: fontcolor=white: text='{}': r={}: x=(w-tw-20): y=h-lh-20: box=1: boxcolor=black\" ".format(caption, 24)

        # Timecode Burn-In
        filters.append(r"drawtext=font=Consolas: fontsize=18: fontcolor=white: x=5: y=20: timecode='00\:00\:00\:00': r={}: ".format(self.framerate))
        filters.append(r"drawtext=font=Consolas: fontsize=18: fontcolor=white: x=(w-text_w)-5: y=20: start_number=1: text='%{frame_num}' ")

        for i in range(len(filters)):
            text_graph += filters[i]
            if i < len(filters) - 1:
                text_graph += ', '

        if len(text_graph) > 0:
            ffmpeg_cmd += r' -vf "{}"'.format(text_graph)

        ffmpeg_cmd += r' -c:v libx265 '

        if self.audio_path:
            ffmpeg_cmd += r' -filter_complex "[1:0] apad" -shortest'      

        ffmpeg_cmd += r' "{0}"'.format(self.media_file)             
        return ffmpeg_cmd        
    
    # Runs FFMPEG command using subprocess  
    def exr_to_png_mp4_convert(self):
        exr_to_png_convert_success = self.convert()

        # exr_to_png_convert_success = True
        cmd = self.ffmpeg_convert_command()

        print("***********")
        print("{}".format(cmd))
        print("***********")

        if exr_to_png_convert_success:
            self.rename_png_files()
            print("Converting files to .mov file.")
            proc = subprocess.Popen(cmd, shell = False, stdout=subprocess.PIPE)
            while True:
                #output = proc.stdout.read(1)
                output = proc.stdout.readline()
                try:
                    log = output.decode('utf-8')
                    if log == '' and proc.poll() != None:
                        break
                    else:
                        print(log)
                except:
                    self.server_log("Byte Code Error: Ignoring")
                    print(traceback.format_exc())
                # continue

                return os.path.join(self.source_dir, self.media_file)
        else:
            return False   


