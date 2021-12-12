import copy
import os
import sys
import traceback

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from shiboken2 import wrapInstance
try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om
    import maya.OpenMayaUI as omui
    _stand_alone = False
except:
    _stand_alone = True

from wildchildanimation.maya.swing_maya import SwingMaya
from wildchildanimation.gui.swing_sequence_playblast_dialog import Ui_SequencePlayblastDialog
from wildchildanimation.gui.swing_utils import load_settings, save_settings, open_folder
from wildchildanimation.gui.shot_list import ShotListDialog

class SwingSequencePlayblast(SwingMaya):

    DEFAULT_CONTAINER = "mp4"
    DEFAULT_ENCODER = "h264"
    DEFAULT_H264_QUALITY = "High"
    DEFAULT_H264_PRESET = "fast"
    DEFAULT_PADDING = 4
    DEFAULT_VISIBILITY = "Viewport"

    output_logged = QtCore.Signal(str)

    def __init__(self, ffmpeg_path = None, log_to_maya = True):
        super(SwingSequencePlayblast, self).__init__()

        self.set_maya_logging_enabled(log_to_maya)
        self.set_ffmpeg_path(ffmpeg_path)
        self.set_resolution(SwingSequencePlayblast.DEFAULT_RESOLUTION)
        self.set_encoding(SwingSequencePlayblast.DEFAULT_CONTAINER, SwingSequencePlayblast.DEFAULT_ENCODER)
        self.set_h264_settings(SwingSequencePlayblast.DEFAULT_H264_QUALITY, SwingSequencePlayblast.DEFAULT_H264_PRESET)
        self.set_visibility(SwingSequencePlayblast.DEFAULT_VISIBILITY)

        self.initialize_ffmpeg_process()

    def set_ffmpeg_path(self, ffmpeg_path):
        self._ffmpeg_path = ffmpeg_path

    def get_ffmpeg_path(self):
        return self._ffmpeg_path

    def set_resolution(self, resolution):
        self._resolution_preset = None

        try:
            widthHeight = self.preset_to_resolution(resolution)
            self._resolution_preset = resolution
        except:
            widthHeight = resolution

        valid_resolution = True
        try:
            if not (isinstance(widthHeight[0], int) and isinstance(widthHeight[1], int)):
                valid_resolution = False
        except:
            valid_resolution = False

        if valid_resolution:
            if widthHeight[0] <=0 or widthHeight[1] <= 0:
                self.log_error("Invalid resolution: {0}. Values must be greater than zero.".format(widthHeight))
                return
        else:
            presets = []
            for preset in SwingSequencePlayblast.RESOLUTION_LOOKUP.keys():
                presets.append("'{0}'".format(preset))

            self.log_error("Invalid resoluton: {0}. Expected one of [int, int], {1}".format(widthHeight, ", ".join(presets)))
            return

        self._widthHeight = (widthHeight[0], widthHeight[1])

    def get_resolution_width_height(self):
        if self._resolution_preset:
            return self.preset_to_resolution(self._resolution_preset)

        return self._widthHeight

    def preset_to_resolution(self, resolution_preset):
        if resolution_preset == "Render":
            width = cmds.getAttr("defaultResolution.width")
            height = cmds.getAttr("defaultResolution.height")
            return (width, height)
        elif resolution_preset in SwingSequencePlayblast.RESOLUTION_LOOKUP.keys():
            return SwingSequencePlayblast.RESOLUTION_LOOKUP[resolution_preset]
        else:
            raise RuntimeError("Invalid resolution preset: {0}".format(resolution_preset))

    def set_encoding(self, container_format, encoder):
        if container_format not in SwingSequencePlayblast.VIDEO_ENCODER_LOOKUP.keys():
            self.log_error("Invalid container: {0}. Expected one of {1}".format(container_format, SwingSequencePlayblast.VIDEO_ENCODER_LOOKUP.keys()))
            return

        if encoder not in SwingSequencePlayblast.VIDEO_ENCODER_LOOKUP[container_format]:
            self.log_error("Invalid encoder: {0}. Expected one of {1}".format(encoder, SwingSequencePlayblast.VIDEO_ENCODER_LOOKUP[container_format]))
            return

        self._container_format = container_format
        self._encoder = encoder

    def set_h264_settings(self, quality, preset):
        if not quality in SwingSequencePlayblast.H264_QUALITIES.keys():
            self.log_error("Invalid h264 quality: {0}. Expected one of {1}".format(quality, SwingSequencePlayblast.H264_QUALITIES.keys()))
            return

        if not preset in SwingSequencePlayblast.H264_PRESETS:
            self.log_error("Invalid h264 preset: {0}. Expected one of {1}".format(preset, SwingSequencePlayblast.H264_PRESETS))
            return

        self._h264_quality = quality
        self._h264_preset = preset

    def get_h264_settings(self):
        return {
            "quality": self._h264_quality,
            "preset": self._h264_preset,
        }


    # expects a directory and a shot list
    #
    def execute(self, target_file_name, shots= [], padding=4, overscan=False, show_ornaments=True, show_in_viewer=True, overwrite=False, time_code = True, time_code_border = True, frame_numbers = True, caption = None, artist = None, build_sequence = False):
        file_parts = os.path.split(target_file_name)

        output_dir = file_parts[0]
        filename = file_parts[1]

        if len(filename) == 0 or len(output_dir) == 0:
            self.log_error("playblast: invalid filename or directory [{}] [{}]".format(filename, output_dir))        
            return

        ## aokb_chr_atomic_toad_rig_v010 
        # E:\productions\aotkb\aotk\user\assets\ch_rig\atomic_toad\playblasts\aokb_chr_atomic_toad_rig_v010 // 
        self.log_output("playblast: filename [{}]".format(filename))        
        self.log_output("playblast: output_dir [{}]".format(output_dir))        

        if not self.validate_ffmpeg():
            self.log_error("ffmpeg executable is not configured. See script editor for details.")
            return

        viewport_model_panel = self.get_viewport_panel()
        if not viewport_model_panel:
            self.log_error("An active viewport is not selected. Select a viewport and retry.")
            return

        if padding <= 0:
            padding = SwingSequencePlayblast.DEFAULT_PADDING

        # create target dir if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # pop gui back to original settings no matter what happens with playblasting
        try:
            # sets target file name, adds' container extension
            playblasted_shots = []
            count = 1
            for shot in shots:
                shot_caption = None
                if caption:
                    shot_caption = "{} {}".format(caption, shot)
                    

                shot_start = cmds.getAttr(shot + ".startFrame")
                shot_end = cmds.getAttr(shot + ".endFrame")

                shot_cameras = cmds.listConnections(shot + ".currentCamera") 
                if len(shot_cameras) > 0:
                    shot_cam = shot_cameras[0]
                else:
                    self.log_error("Error loading camera {} for shot {}".format(shot_cameras, shot))
                    continue

                self.log_output("Shot {} starting at {} ending at {} using camera {}".format(shot, shot_start, shot_end, shot_cam))

                output_path = os.path.normpath(os.path.join(output_dir, "{0}_{1}.{2}".format(filename, shot, self._container_format)))
                self.log_output("{} Playblast: output_path: {}".format(count, output_path))

                if not overwrite and os.path.exists(output_path):
                    self.log_error("Output file already exists. Enable overwrite to ignore.")
                    return

                playblast_output_dir = os.path.join(output_dir, "playblast_temp")
                self.log_output("Playblast: playblast_output_dir: {}".format(playblast_output_dir))

                playblast_output = os.path.join(output_dir, "playblast_temp", filename)
                self.log_output("Playblast: playblast_output: {}".format(playblast_output))

                force_overwrite = True
                compression = "png"
                image_quality = 100
                index_from_zero = True
                viewer = False

                widthHeight = self.get_resolution_width_height()
                start_frame = shot_start
                end_frame = shot_end

                options = {
                    "filename": playblast_output,
                    "widthHeight": widthHeight,
                    "percent": 100,
                    "startTime": start_frame,
                    "endTime": end_frame,
                    "clearCache": True,
                    "forceOverwrite": force_overwrite,
                    "format": "image",
                    "compression": compression,
                    "quality": image_quality,
                    "indexFromZero": index_from_zero,
                    "framePadding": padding,
                    "showOrnaments": show_ornaments,
                    "viewer": viewer,
                }

                self.log_output("Playblast options: {0}".format(options))

                # Store original viewport settings
                orig_camera = self.get_active_camera()

                #camera = self._camera
                #camera = shot_cam
                #if not camera:
                #    camera = orig_camera

                #if not camera in cmds.listCameras():
                #    self.log_error("Camera does not exist: {0}".format(camera))
                #    return

                self.set_active_camera(shot_cam)

                orig_visibility_flags = self.create_viewport_visibility_flags(self.get_viewport_visibility())
                playblast_visibility_flags = self.create_viewport_visibility_flags(self.get_visibility())
                    
                model_editor = cmds.modelPanel(viewport_model_panel, q=True, modelEditor=True)
                self.set_viewport_visibility(model_editor, playblast_visibility_flags)
                
                # Store original camera settings
                if not overscan:
                    overscan_attr = "{0}.overscan".format(shot_cam)
                    orig_overscan = cmds.getAttr(overscan_attr)
                    cmds.setAttr(overscan_attr, 1.0)

                playblast_failed = False
                try:
                    cmds.playblast(**options)
                except:
                    traceback.print_exc()
                    self.log_error("Failed to create playblast. See script editor for details.")
                    playblast_failed = True
                #finally:
                #    # Restore original camera settings
                #    if not overscan:
                #        cmds.setAttr(overscan_attr, orig_overscan)
                #    
                #    # Restore original viewport settings
                #    self.set_active_camera(orig_camera)
                #    self.set_viewport_visibility(model_editor, orig_visibility_flags)

                if playblast_failed:
                    continue

                source_path = "{0}/{1}.%0{2}d.png".format(playblast_output_dir, os.path.basename(filename), padding)

                if self._encoder == "h264":
                    self.encode_h264(source_path, output_path, start_frame, time_code, time_code_border, frame_numbers, shot_caption, artist)
                    playblasted_shots.append(output_path)
                else:
                    self.log_error("Encoding failed. Unsupported encoder ({0}) for container ({1}).".format(self._encoder, self._container_format))
                    self.remove_temp_dir(playblast_output_dir)
                    return

                self.remove_temp_dir(playblast_output_dir)
                count += 1
            # playblast all shots

            if build_sequence:
                self.log_output("Building sequence from {} playblasts".format(len(playblasted_shots)))
                output_path = os.path.normpath(os.path.join(output_dir, "{0}.{1}".format(filename, self._container_format)))

                self.encode_h264_sequence(output_path, playblasted_shots)

        finally:
            # run through all the shots we have, and playblast them
            self.log_output("Playblasted {} shots".format(len(playblasted_shots)))

            # Restore original camera settings
            if not overscan:
                cmds.setAttr(overscan_attr, orig_overscan)
                
            # Restore original viewport settings
            self.set_active_camera(orig_camera)
            self.set_viewport_visibility(model_editor, orig_visibility_flags)            

            if show_in_viewer:
                self.open_in_viewer(output_path)

        # done playblasting sequence

    def validate_ffmpeg(self):
        if not self._ffmpeg_path:
            self.log_error("ffmpeg executable path not set")
            return False
        elif not os.path.exists(self._ffmpeg_path):
            self.log_error("ffmpeg executable path does not exist: {0}".format(self._ffmpeg_path))
            return False
        elif os.path.isdir(self._ffmpeg_path):
            self.log_error("Invalid ffmpeg path: {0}".format(self._ffmpeg_path))
            return False

        return True

    def initialize_ffmpeg_process(self):
        self._ffmpeg_process = QtCore.QProcess()
        self._ffmpeg_process.readyReadStandardError.connect(self.process_ffmpeg_output)

    def execute_ffmpeg_command(self, command):
        self._ffmpeg_process.start(command)
        if self._ffmpeg_process.waitForStarted():
            while self._ffmpeg_process.state() != QtCore.QProcess.NotRunning:
                QtCore.QCoreApplication.processEvents()
                QtCore.QThread.usleep(10)

    def process_ffmpeg_output(self):
        byte_array_output = self._ffmpeg_process.readAllStandardError()

        if sys.version_info.major < 3:
            output = str(byte_array_output)
        else:
            output = str(byte_array_output, "utf-8")

        self.log_output(output)

    def encode_h264(self, source_path, output_path, start_frame, time_code = True, time_code_background = True, frame_number = True, caption = None, artist = None):
        framerate = self.get_frame_rate()

        audio_file_path, audio_frame_offset = self.get_audio_attributes()
        if audio_file_path:
            audio_offset = self.get_audio_offset_in_sec(start_frame, audio_frame_offset, framerate)

        crf = SwingSequencePlayblast.H264_QUALITIES[self._h264_quality]
        preset = self._h264_preset

        ffmpeg_cmd = self._ffmpeg_path
        ffmpeg_cmd += ' -y -framerate {0} -i "{1}"'.format(framerate, source_path)

        if audio_file_path:
            ffmpeg_cmd += ' -ss {0} -i "{1}"'.format(audio_offset, audio_file_path)

        filters = []
        text_graph = ''

        if caption:
            if artist:
                caption = "{} - {}".format(caption, artist["full_name"])
            filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=(w-text_w)/2: y=20: text='{}' ".format(caption, 24))
                #ffmpeg_cmd += " -vf \"drawtext=font=Consolas: fontsize=24: fontcolor=white: text='{}': r={}: x=(w-tw-20): y=h-lh-20: box=1: boxcolor=black\" ".format(caption, 24)

        if time_code:
            if time_code_background:

                # Timecode Burn-In (w/background box)
                filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=5: y=20: timecode='00\:00\:00\:00': r={}: ".format(framerate))
            else:
                # Timecode Burn-In
                filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=5: y=20: timecode='00\:00\:00\:00': r={}: ".format(framerate))

        if frame_number:
            filters.append("drawtext=font=Consolas: fontsize=18: fontcolor=white: x=(w-text_w)-5: y=20: start_number=1: text='%{frame_num}' ")

        for i in range(len(filters)):
            text_graph += filters[i]
            if i < len(filters) - 1:
                text_graph += ', '

        if len(text_graph) > 0:
            ffmpeg_cmd += ' -vf "{}"'.format(text_graph)

        ffmpeg_cmd += ' -c:v libx264 -crf:v {0} -preset:v {1} -profile high -level 4.0 -pix_fmt yuv420p'.format(crf, preset)

        if audio_file_path:
            ffmpeg_cmd += ' -filter_complex "[1:0] apad" -shortest'

        ffmpeg_cmd += ' "{0}"'.format(output_path)

        self.log_output(ffmpeg_cmd)
        self.execute_ffmpeg_command(ffmpeg_cmd)        

    def encode_h264_sequence(self, target, shotlist):
        '''
        $ cat mylist.txt
        file '/path/to/file1'
        file '/path/to/file2'
        file '/path/to/file3'
            
        $ ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4
        '''
        working_dir = os.path.dirname(target)
        playlist = "{}/{}".format(working_dir, "playlist.txt")
        with open(playlist, 'w') as f:
            try:
                for item in shotlist:
                    f.write("file '{}'\r".format(item))
            finally:
                f.close()

        ffmpeg_cmd = self._ffmpeg_path
        ffmpeg_cmd += " -f concat -safe 0 -i {} -c copy {}".format(playlist, target)

        self.log_output(ffmpeg_cmd)
        self.execute_ffmpeg_command(ffmpeg_cmd)        

class SwingSequencePlayblastEncoderSettingsDialog(QtWidgets.QDialog):

    ENCODER_PAGES = {
        "h264": 0
    }

    H264_QUALITIES = [
        "Very High",
        "High",
        "Medium",
        "Low",
    ]

    def __init__(self, parent):
        super(SwingSequencePlayblastEncoderSettingsDialog, self).__init__(parent)

        self.setWindowTitle("Encoder Settings")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setModal(True)
        self.setMinimumWidth(220)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        # h264
        self.h264_quality_combo = QtWidgets.QComboBox()
        self.h264_quality_combo.addItems(SwingSequencePlayblastEncoderSettingsDialog.H264_QUALITIES)

        self.h264_preset_combo = QtWidgets.QComboBox()
        self.h264_preset_combo.addItems(SwingSequencePlayblast.H264_PRESETS)

        h264_layout = QtWidgets.QFormLayout()
        h264_layout.addRow("Quality:", self.h264_quality_combo)
        h264_layout.addRow("Preset:", self.h264_preset_combo)

        h264_settings_wdg = QtWidgets.QGroupBox("h264 Options")
        h264_settings_wdg.setLayout(h264_layout)

        self.settings_stacked_wdg = QtWidgets.QStackedWidget()
        self.settings_stacked_wdg.addWidget(h264_settings_wdg)

        self.accept_btn = QtWidgets.QPushButton("Accept")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(4)
        main_layout.addWidget(self.settings_stacked_wdg)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.close)

    def set_page(self, page):
        if not page in SwingSequencePlayblastEncoderSettingsDialog.ENCODER_PAGES:
            return False

        self.settings_stacked_wdg.setCurrentIndex(SwingSequencePlayblastEncoderSettingsDialog.ENCODER_PAGES[page])
        return True

    def set_h264_settings(self, quality, preset):
        self.h264_quality_combo.setCurrentText(quality)
        self.h264_preset_combo.setCurrentText(preset)

    def get_h264_settings(self):
        return {
            "quality": self.h264_quality_combo.currentText(),
            "preset": self.h264_preset_combo.currentText(),
        }

class SwingSequencePlayblastVisibilityDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(SwingSequencePlayblastVisibilityDialog, self).__init__(parent)

        self.setWindowTitle("Customize Visibility")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        visibility_layout = QtWidgets.QGridLayout()

        index = 0
        self.visibility_checkboxes = []

        for i in range(len(SwingSequencePlayblast.VIEWPORT_VISIBILITY_LOOKUP)):
            checkbox = QtWidgets.QCheckBox(SwingSequencePlayblast.VIEWPORT_VISIBILITY_LOOKUP[i][0])

            visibility_layout.addWidget(checkbox, index / 3, index % 3)
            self.visibility_checkboxes.append(checkbox)

            index += 1

        visibility_grp = QtWidgets.QGroupBox("")
        visibility_grp.setLayout(visibility_layout)

        apply_btn = QtWidgets.QPushButton("Apply")
        apply_btn.clicked.connect(self.accept)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)
        main_layout.addWidget(visibility_grp)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def get_visibility_data(self):
        data = []
        for checkbox in self.visibility_checkboxes:
            data.append(checkbox.isChecked())

        return data

    def set_visibility_data(self, data):
        if len(self.visibility_checkboxes) != len(data):
            raise RuntimeError("Visibility property/data mismatch")

        for i in range(len(data)):
            self.visibility_checkboxes[i].setChecked(data[i]) 



class SwingSequencePlayblastUi(QtWidgets.QDialog, Ui_SequencePlayblastDialog):

    TITLE = "Swing Sequence Playblast"

    _caption = False

    CONTAINER_PRESETS = [
        "mp4"
    ]

    RESOLUTION_PRESETS = [
        "Render",
        "HD 1080",
        "HD 720",
        "HD 540",
    ]

    VISIBILITY_PRESETS = [
        "Viewport",
        "Geo",
        "Dynamics",
    ]

    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = SwingSequencePlayblastUi()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()


    def __init__(self):
        try:
            maya_main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
            super(SwingSequencePlayblastUi, self).__init__(maya_main_window)
        except:
            super(SwingSequencePlayblastUi, self).__init__()

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self._playblast = SwingSequencePlayblast()

        self._encoder_settings_dialog = None
        self._visibility_dialog = None

        self.load_app_settings()

        self.create_actions()
        self.create_menus()

        # Set shots
        self.refresh_shots()

        # Select Resolution
        self.resolution_select_cmb.addItems(SwingSequencePlayblastUi.RESOLUTION_PRESETS)
        self.resolution_select_cmb.addItem("Custom")
        self.resolution_select_cmb.setCurrentText(SwingSequencePlayblast.DEFAULT_RESOLUTION)

        self.resolution_width_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.resolution_width_sb.setRange(1, 9999)
        self.resolution_width_sb.setMinimumWidth(40)
        self.resolution_width_sb.setAlignment(QtCore.Qt.AlignRight)

        self.resolution_height_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.resolution_height_sb.setRange(1, 9999)
        self.resolution_height_sb.setMinimumWidth(40)
        self.resolution_height_sb.setAlignment(QtCore.Qt.AlignRight)

        # Encoding
        self.encoding_container_cmb.addItems(SwingSequencePlayblastUi.CONTAINER_PRESETS)
        self.encoding_container_cmb.setCurrentText(SwingSequencePlayblast.DEFAULT_CONTAINER)

        # Visibility
        self.visibility_cmb.addItems(SwingSequencePlayblastUi.VISIBILITY_PRESETS)
        self.visibility_cmb.addItem("Custom")
        self.visibility_cmb.setCurrentText(SwingSequencePlayblast.DEFAULT_VISIBILITY)

        # Options
        self.overscan_cb.setChecked(False)
        self.ornaments_cb.setChecked(True)
        self.viewer_cb.setChecked(True)              

        self.output_edit.setReadOnly(True)
        self.output_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)  

        self.create_connections()

        self.load_defaults()
        self.load_user_settings()

    def set_artist(self, artist):
        self.artist = artist

    def create_actions(self):
        self.save_defaults_action = QtWidgets.QAction("Save Defaults", self)
        self.save_defaults_action.triggered.connect(self.save_defaults)

        self.load_defaults_action = QtWidgets.QAction("Load Defaults", self)
        self.load_defaults_action.triggered.connect(self.load_defaults)

        self.show_about_action = QtWidgets.QAction("About", self)
        self.show_about_action.triggered.connect(self.show_about_dialog)

    def create_menus(self):
        self.main_menu = QtWidgets.QMenuBar()

        edit_menu = self.main_menu.addMenu("Edit")
        edit_menu.addAction(self.save_defaults_action)
        edit_menu.addAction(self.load_defaults_action)
        edit_menu.addSeparator()

        help_menu = self.main_menu.addMenu("Help")
        help_menu.addAction(self.show_about_action)        

    def create_connections(self):

        # Encoding
        self.encoding_container_cmb.currentTextChanged.connect(self.refresh_video_encoders)
        self.encoding_video_codec_cmb.currentTextChanged.connect(self.on_video_encoder_changed)
        self.encoding_video_codec_settings_btn.clicked.connect(self.show_encoder_settings_dialog)

        # Resolution
        self.resolution_select_cmb.currentTextChanged.connect(self.refresh_resolution)
        self.resolution_width_sb.editingFinished.connect(self.on_resolution_changed)
        self.resolution_height_sb.editingFinished.connect(self.on_resolution_changed)

        # Visibility
        self.visibility_cmb.currentTextChanged.connect(self.on_visibility_preset_changed)
        self.visibility_customize_btn.clicked.connect(self.show_visibility_dialog)

        # Buttons    
        self.refresh_btn.clicked.connect(self.refresh)
        self.clear_btn.clicked.connect(self.output_edit.clear)
        self.playblast_btn.clicked.connect(self.do_playblast)
        self.close_btn.clicked.connect(self.do_close)
        #

        self.select_shots_btn.clicked.connect(self.do_select_shots)


        self.output_dir_path_select_btn.clicked.connect(self.select_output_filename)
        self.output_dir_path_show_folder_btn.clicked.connect(self.open_output_folder)

        self._playblast.output_logged.connect(self.append_output) # pylint: disable=E1101

    def set_caption_text(self, text):
        self._caption = text

    def set_burn_time_code(self, should_burn):
        self.checkBoxTimeCode.setChecked(should_burn)

    def set_burn_frame_number(self, should_burn):
        self.checkBoxFrameNumber.setChecked(should_burn)

    def open_output_folder(self):
        dir_path = self.output_filename_le.text()
        open_folder(os.path.dirname(dir_path))

    def do_select_shots(self):
        self.shotDialog.show()

    def do_close(self):
        self.write_settings()
        self.close()

    def do_playblast(self):
        filename = self.output_filename_le.text()
        padding = SwingSequencePlayblast.DEFAULT_PADDING

        overscan = self.overscan_cb.isChecked()
        show_ornaments = self.ornaments_cb.isChecked()
        show_in_viewer = self.viewer_cb.isChecked()
        overwrite = self.force_overwrite_cb.isChecked()
        build_sequence = self.checkBoxBuildSequence.isChecked()

        if self.checkBoxTimeCode.isChecked():
            self._playblast.log_output("Burn time code")

        #if self.checkBoxBackground.isChecked():
        #    self._playblast.log_output("Burn time code border")
            
        if self.checkBoxFrameNumber.isChecked():
            self._playblast.log_output("Burn Frame Number")

        caption = False
        if self.checkBoxBurnCaption.isChecked():
            caption = self._caption
            if caption:
                self._playblast.log_output("Burn Caption: {}".format(caption))

        artist = None
        if self.checkBoxArtistName.isChecked():
            artist = self.artist
            if artist:
                self._playblast.log_output("Burn Artist Name: {}".format(artist))

        selected_shots = self.shotDialog.get_selected()

        self._playblast.log_output("Playblasting {} shots".format(len(selected_shots)))

        self._playblast.execute(target_file_name = filename, 
            shots = selected_shots,
            padding = padding, 
            overscan = overscan, show_ornaments = show_ornaments, show_in_viewer = show_in_viewer, overwrite = overwrite,  
            time_code = self.checkBoxTimeCode.isChecked(), time_code_border = False, frame_numbers=self.checkBoxFrameNumber.isChecked(), 
            caption=caption, artist = artist, build_sequence = build_sequence)

    def select_output_filename(self):
        current_filename = self.output_filename_le.text()
        if not current_filename:
            current_filename = self.output_filename_le.placeholderText()

        selected_file = os.path.normpath(current_filename)

        format = self.encoding_container_cmb.currentText()
        filter = "mp4 (*.mp4);;All files (*.*)"

        new_filename = QtWidgets.QFileDialog.getSaveFileName(self, "Select file name", selected_file, filter)
        if new_filename:
            self.set_output_file_name(new_filename[0])
            #file_name = os.path.basename(new_filename[0])
            #self.output_filename_le.setText(file_name)

            #new_dir_path = os.path.dirname(new_filename[0])
            #self.output_dir_path_le.setText(new_dir_path)

    def set_output_file_name(self, new_file_name):
        self.output_filename_le.setText(new_file_name)

    def refresh(self):
        self.refresh_shots()
        self.refresh_resolution()
        #self.refresh_frame_range()
        self.refresh_video_encoders()

    def refresh_shots(self):
        self.shots = cmds.ls(type="shot")
        self.shotDialog = ShotListDialog(self, self.shots)

    def refresh_resolution(self):
        resolution_preset = self.resolution_select_cmb.currentText()
        if resolution_preset != "Custom":
            self._playblast.set_resolution(resolution_preset)

            resolution = self._playblast.get_resolution_width_height()
            self.resolution_width_sb.setValue(resolution[0])
            self.resolution_height_sb.setValue(resolution[1])

    def on_resolution_changed(self):
        resolution = (self.resolution_width_sb.value(), self.resolution_height_sb.value())

        for key in SwingSequencePlayblast.RESOLUTION_LOOKUP.keys():
            if SwingSequencePlayblast.RESOLUTION_LOOKUP[key] == resolution:
                self.resolution_select_cmb.setCurrentText(key)
                return

        self.resolution_select_cmb.setCurrentText("Custom")

        self._playblast.set_resolution(resolution)

    def refresh_video_encoders(self):
        self.encoding_video_codec_cmb.clear()

        container = self.encoding_container_cmb.currentText()
        self.encoding_video_codec_cmb.addItems(SwingSequencePlayblast.VIDEO_ENCODER_LOOKUP[container])

    def on_video_encoder_changed(self):
        container = self.encoding_container_cmb.currentText()
        encoder = self.encoding_video_codec_cmb.currentText()

        if container and encoder:
            self._playblast.set_encoding(container, encoder)

    def show_encoder_settings_dialog(self):
        if not self._encoder_settings_dialog:
            self._encoder_settings_dialog = SwingSequencePlayblastEncoderSettingsDialog(self)
            self._encoder_settings_dialog.accepted.connect(self.on_encoder_settings_dialog_modified)

        encoder = self.encoding_video_codec_cmb.currentText()
        if encoder == "h264":
            self._encoder_settings_dialog.set_page("h264")

            h264_settings = self._playblast.get_h264_settings()
            self._encoder_settings_dialog.set_h264_settings(h264_settings["quality"], h264_settings["preset"])
        else:
            self.append_output("[ERROR] Settings page not found for encoder: {0}".format(encoder))

        self._encoder_settings_dialog.show()

    def on_encoder_settings_dialog_modified(self):
        if self.encoding_container_cmb.currentText() == "Image":
            image_settings = self._encoder_settings_dialog.get_image_settings()
            self._playblast.set_image_settings(image_settings["quality"])
        else:
            encoder = self.encoding_video_codec_cmb.currentText()
            if encoder == "h264":
                h264_settings = self._encoder_settings_dialog.get_h264_settings()
                self._playblast.set_h264_settings(h264_settings["quality"], h264_settings["preset"])
            else:
                self.append_output("[ERROR] Failed to set encoder settings. Unknown encoder: {0}".format(encoder))

    def on_visibility_preset_changed(self):
        visibility_preset = self.visibility_cmb.currentText()
        if visibility_preset != "Custom":
            self._playblast.set_visibility(visibility_preset)

    def show_visibility_dialog(self):
        if not self._visibility_dialog:
            self._visibility_dialog = SwingSequencePlayblastVisibilityDialog(self)
            self._visibility_dialog.accepted.connect(self.on_visibility_dialog_modified)

        self._visibility_dialog.set_visibility_data(self._playblast.get_visibility())
        self._visibility_dialog.show()

    def on_visibility_dialog_modified(self):
        self.visibility_cmb.setCurrentText("Custom")
        self._playblast.set_visibility(self._visibility_dialog.get_visibility_data())

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        # self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))
        self.settings.endGroup()          

    def load_user_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.output_filename_le.setText(self.settings.value("output_filename_le", self.output_filename_le.placeholderText()))
        self.settings.endGroup()          

    def save_settings(self):
        save_settings("ffmpeg_bin", self._playblast.get_ffmpeg_path())   

    def load_app_settings(self):
        self.read_settings()
        ffmpeg_path = load_settings("ffmpeg_bin", None)
        if ffmpeg_path:
            self._playblast.set_ffmpeg_path(ffmpeg_path)
        else:
            print("Error: ffmpeg not loaded")

    def save_defaults(self):
        cmds.optionVar(sv=("SwingSequencePlayblastUiOutputFilename", self.output_filename_le.text()))
        cmds.optionVar(iv=("SwingSequencePlayblastUiForceOverwrite", self.force_overwrite_cb.isChecked()))

        cmds.optionVar(sv=("SwingSequencePlayblastUiCamera", self.camera_select_cmb.currentText()))
        cmds.optionVar(iv=("SwingSequencePlayblastUiHideDefaultCameras", self.camera_select_hide_defaults_cb.isChecked()))

        cmds.optionVar(sv=("SwingSequencePlayblastUiResolutionPreset", self.resolution_select_cmb.currentText()))
        cmds.optionVar(iv=("SwingSequencePlayblastUiResolutionWidth", self.resolution_width_sb.value()))
        cmds.optionVar(iv=("SwingSequencePlayblastUiResolutionHeight", self.resolution_height_sb.value()))

        cmds.optionVar(sv=("SwingSequencePlayblastUiEncodingContainer", self.encoding_container_cmb.currentText()))
        cmds.optionVar(sv=("SwingSequencePlayblastUiEncodingVideoCodec", self.encoding_video_codec_cmb.currentText()))

        h264_settings = self._playblast.get_h264_settings()
        cmds.optionVar(sv=("SwingSequencePlayblastUiH264Quality", h264_settings["quality"]))
        cmds.optionVar(sv=("SwingSequencePlayblastUiH264Preset", h264_settings["preset"]))

        image_settings = self._playblast.get_image_settings()
        cmds.optionVar(iv=("SwingSequencePlayblastUiImageQuality", image_settings["quality"]))

        cmds.optionVar(sv=("SwingSequencePlayblastUiVisibilityPreset", self.visibility_cmb.currentText()))

        visibility_data = self._playblast.get_visibility()
        visibility_str = ""
        for item in visibility_data:
            visibility_str = "{0} {1}".format(visibility_str, int(item))
        cmds.optionVar(sv=("SwingSequencePlayblastUiVisibilityData", visibility_str))

        cmds.optionVar(iv=("SwingSequencePlayblastUiOverscan", self.overscan_cb.isChecked()))
        cmds.optionVar(iv=("SwingSequencePlayblastUiOrnaments", self.ornaments_cb.isChecked()))
        cmds.optionVar(iv=("SwingSequencePlayblastUiViewer", self.viewer_cb.isChecked()))

        cmds.optionVar(iv=("SwingSequencePlayblastBurnTimeCode", self.checkBoxTimeCode.isChecked()))
        cmds.optionVar(iv=("SwingSequencePlayblastBurnFrameNumbers", self.checkBoxFrameNumber.isChecked()))


    def load_defaults(self):
        if _stand_alone:
            return 

        if cmds.optionVar(exists="SwingSequencePlayblastUiOutputFilename"):
            self.output_filename_le.setText(cmds.optionVar(q="SwingSequencePlayblastUiOutputFilename"))
        if cmds.optionVar(exists="SwingSequencePlayblastUiForceOverwrite"):
            self.force_overwrite_cb.setChecked(cmds.optionVar(q="SwingSequencePlayblastUiForceOverwrite"))

        if cmds.optionVar(exists="SwingSequencePlayblastUiResolutionPreset"):
            self.resolution_select_cmb.setCurrentText(cmds.optionVar(q="SwingSequencePlayblastUiResolutionPreset"))
        if self.resolution_select_cmb.currentText() == "Custom":
            if cmds.optionVar(exists="SwingSequencePlayblastUiResolutionWidth"):
                self.resolution_width_sb.setValue(cmds.optionVar(q="SwingSequencePlayblastUiResolutionWidth"))
            if cmds.optionVar(exists="SwingSequencePlayblastUiResolutionHeight"):
                self.resolution_height_sb.setValue(cmds.optionVar(q="SwingSequencePlayblastUiResolutionHeight"))
            self.on_resolution_changed()

        if cmds.optionVar(exists="SwingSequencePlayblastUiEncodingContainer"):
            self.encoding_container_cmb.setCurrentText(cmds.optionVar(q="SwingSequencePlayblastUiEncodingContainer"))
        if cmds.optionVar(exists="SwingSequencePlayblastUiEncodingVideoCodec"):
            self.encoding_video_codec_cmb.setCurrentText(cmds.optionVar(q="SwingSequencePlayblastUiEncodingVideoCodec"))

        if cmds.optionVar(exists="SwingSequencePlayblastUiH264Quality") and cmds.optionVar(exists="SwingSequencePlayblastUiH264Preset"):
            self._playblast.set_h264_settings(cmds.optionVar(q="SwingSequencePlayblastUiH264Quality"), cmds.optionVar(q="SwingSequencePlayblastUiH264Preset"))

        if cmds.optionVar(exists="SwingSequencePlayblastUiImageQuality"):
            self._playblast.set_image_settings(cmds.optionVar(q="SwingSequencePlayblastUiImageQuality"))

        if cmds.optionVar(exists="SwingSequencePlayblastUiVisibilityPreset"):
            self.visibility_cmb.setCurrentText(cmds.optionVar(q="SwingSequencePlayblastUiVisibilityPreset"))
        if self.visibility_cmb.currentText() == "Custom":
            if cmds.optionVar(exists="SwingSequencePlayblastUiVisibilityData"):
                visibility_str_list = cmds.optionVar(q="SwingSequencePlayblastUiVisibilityData").split()
                visibility_data = []
                for item in visibility_str_list:
                    if item:
                        visibility_data.append(bool(int(item)))

                self._playblast.set_visibility(visibility_data)

        if cmds.optionVar(exists="SwingSequencePlayblastUiOverscan"):
            self.overscan_cb.setChecked(cmds.optionVar(q="SwingSequencePlayblastUiOverscan"))
        if cmds.optionVar(exists="SwingSequencePlayblastUiOrnaments"):
            self.ornaments_cb.setChecked(cmds.optionVar(q="SwingSequencePlayblastUiOrnaments"))
        if cmds.optionVar(exists="SwingSequencePlayblastUiViewer"):
            self.viewer_cb.setChecked(cmds.optionVar(q="SwingSequencePlayblastUiViewer"))

        if cmds.optionVar(exists="SwingSequencePlayblastBurnTimeCode"):
            self.checkBoxTimeCode.setChecked(cmds.optionVar(q="SwingSequencePlayblastBurnTimeCode"))
        #if cmds.optionVar(exists="SwingSequencePlayblastBurnBorder"):
        #    self.checkBoxBackground.setChecked(cmds.optionVar(q="SwingSequencePlayblastBurnBorder"))
        if cmds.optionVar(exists="SwingSequencePlayblastBurnFrameNumbers"):
            self.checkBoxFrameNumber.setChecked(cmds.optionVar(q="SwingSequencePlayblastBurnFrameNumbers"))

    def show_about_dialog(self):
        text = '<h2>{0}</h2>'.format(SwingSequencePlayblastUi.TITLE)
        text += '<p>Version: {0}</p>'.format(SwingSequencePlayblast.VERSION)

        QtWidgets.QMessageBox().about(self, "About", "{0}".format(text))

    def append_output(self, text):
        self.output_edit.appendPlainText(text)

    def keyPressEvent(self, event):
        super(SwingSequencePlayblastUi, self).keyPressEvent(event)

        event.accept()

    def showEvent(self, event):
        self.refresh()
