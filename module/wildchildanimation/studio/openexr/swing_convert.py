'''
    Author: A Kanwal
    Date: 9 May 2022
    Version: 1.0.0.0
'''

# from importlib.metadata import metadata
import os
import sys
import traceback

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
            count += 1

            print("Progress::Emit -> {}".format(exr_file))
            self.callback.loaded.emit(count)

        return True            


class SwingConvert(QtCore.QObject):

    def __init__(self, media_file, source_dir, temp_dir, audio_path = None, preset_speed="veryfast", framerate=25, artist="WCA-Teams", album="WITW", genre="children-animation"):
        super(SwingConvert, self).__init__() 

        self.media_file = media_file
        self.source_dir = source_dir
        self.temp_dir = temp_dir

        self.shot_and_scene_name = os.listdir(self.source_dir)[0].split('.')[0]

        self.settings = SwingSettings.get_instance()
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.audio_path = audio_path
        self.preset_speed = preset_speed
        self.framerate = framerate

        self.source_files = []

        ## self.exr_files = os.listdir("{}/*.exr".format(self.exr_files_loc))
        
        # Creating -metadata string using is repeatingly
        # Creating list of metadata add information
        self.metadata = "-metadata"
        self.metalist = [f"title='{self.shot_and_scene_name}'", f"artist='{artist}'", f"album='{album}'", f"genre='{genre}'"]

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
                print(item_path)   
            else:
                print(f"Error: Please check your exr files directory, {item_path} is not exr file.")
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
            new_file_name = f"{self.shot_and_scene_name}.{z_fill}.png"
            src =f"{self.temp_dir}\{filename}"
            destination_dir = f"{self.temp_dir}\{new_file_name }"
            os.rename(src, destination_dir)
        
        return True

    def remove_temp_dir(self, temp_dir_path):
        for item in os.listdir(temp_dir_path):
            if item.lower().endswith(".png"):
                os.remove(os.path.join(temp_dir_path, item))
        return True

    def convert_progress(self, count):
        print("***{}".format(count))

        if self.progressBar:
            self.progressBar.setValue(count)

        print("Progress {}".format(count))

    # Converts files from EXR to PNG
    def convert(self, progressBar = None):
        for item in os.listdir(self.source_dir):
            if item.lower().endswith(".exr"):
                self.source_files.append(item)

        if not self.check_exr_files():
            return False

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)            

        if not self.check_png_folder_is_empty():
            self.remove_temp_dir(self.temp_dir)

        count = 0
        if progressBar:
            self.progressBar = progressBar
            self.progressBar.setMinimum(1)
            self.progressBar.setMaximum(len(self.source_files))
            self.progressBar.setValue(count)
        else:
            self.progressBar = None

        self.worker = ConvertRunnable(self.source_dir, self.temp_dir, self.source_files)
        self.worker.callback.loaded.connect(self.convert_progress)

        ##self.worker.run()
        self.threadpool.start(self.worker)
        return True

    # Returns complete ffmpeg return command
    def ffmpeg_convert_command(self):
        if self.audio_path:
            self.audio_path = f'-i "{self.audio_path}" -c:v copy -c:a aac'
        
        meta_information = self.add_meta_information()

        ffmpeg_command = self.settings.bin_ffmpeg()
           
        cmd = '{} -y -probesize 5000000 -f image2 -r {} -i "{}" {} -c:v libx265 -preset {} -crf 0 {} -y "{}"'.format( 
            ffmpeg_command,
            self.framerate, 
            os.path.join(self.temp_dir, f'{self.shot_and_scene_name}.%04d.png'),
            self.audio_path,
            self.preset_speed,
            meta_information,
            os.path.join(self.media_file, f'{self.shot_and_scene_name}.mov')
        )

        return cmd
    
    # Runs FFMPEG command using subprocess  
    def exr_to_png_mp4_convert(self, progressBar, textEdit):
        exr_to_png_convert_success = self.convert(progressBar=progressBar)

        # exr_to_png_convert_success = True
        cmd = self.ffmpeg_convert_command()
        if exr_to_png_convert_success:
            self.rename_png_files()
            print("Converting files to .mov file.")
            proc = subprocess.Popen(cmd, shell = True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            while True:
                output = proc.stderr.read(1)
                try:
                    log = output.decode('utf-8')
                    if log == '' and proc.poll() != None:
                        break
                    else:
                        sys.stdout.write(log)
                        sys.stdout.flush()
                except:
                    print("Byte Code Error: Ignoring")
                    print(traceback.format_exc())
        else:
            traceback.print_exc(file=sys.stdout)
            return False   
