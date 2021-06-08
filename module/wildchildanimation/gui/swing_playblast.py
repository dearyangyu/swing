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
    _log_to_maya = True
except:
    print("Maya not found")
    _stand_alone = True
    _log_to_maya = False

from wildchildanimation.gui.swing_utils import load_settings, save_settings

class SwingPlayblast(QtCore.QObject):

    VERSION = "0.0.2"

    RESOLUTION_LOOKUP = {
        "Render": (),
        "HD 1080": (1920, 1080),
        "HD 720": (1280, 720),
        "HD 540": (960, 540),
    }

    FRAME_RANGE_PRESETS = [
        "Render",
        "Playback",
        "Animation",
    ]

    VIDEO_ENCODER_LOOKUP = {
        "mov": ["h264"],
        "mp4": ["h264"],
        "Image": ["jpg", "png", "tif"],
    }

    H264_QUALITIES = {
        "Very High": 18,
        "High": 20,
        "Medium": 23,
        "Low": 26,
    }

    H264_PRESETS = [
        "veryslow",
        "slow",
        "medium",
        "fast",
        "faster",
        "ultrafast",
    ]

    VIEWPORT_VISIBILITY_LOOKUP = [
        ["Controllers", "controllers"],
        ["NURBS Curves", "nurbsCurves"],
        ["NURBS Surfaces", "nurbsSurfaces"],
        ["NURBS CVs", "cv"],
        ["NURBS Hulls", "hulls"],
        ["Polygons", "polymeshes"],
        ["Subdiv Surfaces", "subdivSurfaces"],
        ["Planes", "planes"],
        ["Lights", "lights"],
        ["Cameras", "cameras"],
        ["Image Planes", "imagePlane"],
        ["Joints", "joints"],
        ["IK Handles", "ikHandles"],
        ["Deformers", "deformers"],
        ["Dynamics", "dynamics"],
        ["Particle Instancers", "particleInstancers"],
        ["Fluids", "fluids"],
        ["Hair Systems", "hairSystems"],
        ["Follicles", "follicles"],
        ["nCloths", "nCloths"],
        ["nParticles", "nParticles"],
        ["nRigids", "nRigids"],
        ["Dynamic Constraints", "dynamicConstraints"],
        ["Locators", "locators"],
        ["Dimensions", "dimensions"],
        ["Pivots", "pivots"],
        ["Handles", "handles"],
        ["Texture Placements", "textures"],
        ["Strokes", "strokes"],
        ["Motion Trails", "motionTrails"],
        ["Plugin Shapes", "pluginShapes"],
        ["Clip Ghosts", "clipGhosts"],
        ["Grease Pencil", "greasePencils"],
        ["Grid", "grid"],
        ["HUD", "hud"],
        ["Hold-Outs", "hos"],
        ["Selection Highlighting", "sel"],
    ]

    VIEWPORT_VISIBILITY_PRESETS = {
        "Viewport": [],
        "Geo": ["NURBS Surfaces", "Polygons"],
        "Dynamics": ["NURBS Surfaces", "Polygons", "Dynamics", "Fluids", "nParticles"],
    }


    DEFAULT_CAMERA = None
    DEFAULT_RESOLUTION = "Render"
    DEFAULT_FRAME_RANGE = "Render"

    DEFAULT_CONTAINER = "mp4"
    DEFAULT_ENCODER = "h264"
    DEFAULT_H264_QUALITY = "High"
    DEFAULT_H264_PRESET = "fast"
    DEFAULT_IMAGE_QUALITY = 100

    DEFAULT_VISIBILITY = "Viewport"

    DEFAULT_PADDING = 4

    output_logged = QtCore.Signal(str)


    def __init__(self, ffmpeg_path=None, log_to_maya=_log_to_maya):
        super(SwingPlayblast, self).__init__()

        self.set_ffmpeg_path(ffmpeg_path)
        self.set_maya_logging_enabled(log_to_maya)

        self.set_camera(SwingPlayblast.DEFAULT_CAMERA)
        self.set_resolution(SwingPlayblast.DEFAULT_RESOLUTION)
        self.set_frame_range(SwingPlayblast.DEFAULT_FRAME_RANGE)

        self.set_encoding(SwingPlayblast.DEFAULT_CONTAINER, SwingPlayblast.DEFAULT_ENCODER)
        self.set_h264_settings(SwingPlayblast.DEFAULT_H264_QUALITY, SwingPlayblast.DEFAULT_H264_PRESET)
        self.set_image_settings(SwingPlayblast.DEFAULT_IMAGE_QUALITY)

        self.set_visibility(SwingPlayblast.DEFAULT_VISIBILITY)

        self.initialize_ffmpeg_process()

    def set_ffmpeg_path(self, ffmpeg_path):
        self._ffmpeg_path = ffmpeg_path

    def get_ffmpeg_path(self):
        return self._ffmpeg_path

    def set_maya_logging_enabled(self, enabled):
        self._log_to_maya = enabled

    def set_camera(self, camera):
        if camera and camera not in cmds.listCameras():
            self.log_error("Camera does not exist: {0}".format(camera))
            camera = None

        self._camera = camera

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
            for preset in SwingPlayblast.RESOLUTION_LOOKUP.keys():
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
        elif resolution_preset in SwingPlayblast.RESOLUTION_LOOKUP.keys():
            return SwingPlayblast.RESOLUTION_LOOKUP[resolution_preset]
        else:
            raise RuntimeError("Invalid resolution preset: {0}".format(resolution_preset))

    def set_frame_range(self, frame_range):
        resolved_frame_range = self.resolve_frame_range(frame_range)
        if not resolved_frame_range:
            return

        self._frame_range_preset = None
        if frame_range in SwingPlayblast.FRAME_RANGE_PRESETS:
            self._frame_range_preset = frame_range

        self._start_frame = resolved_frame_range[0]
        self._end_frame = resolved_frame_range[1]

    def get_start_end_frame(self):
        if self._frame_range_preset:
            return self.preset_to_frame_range(self._frame_range_preset)

        return (self._start_frame, self._end_frame)

    def resolve_frame_range(self, frame_range):
        try:
            if type(frame_range) in [list, tuple]:
                start_frame = frame_range[0]
                end_frame = frame_range[1]
            else:
                start_frame, end_frame = self.preset_to_frame_range(frame_range)

            return (start_frame, end_frame)

        except:
            presets = []
            for preset in SwingPlayblast.FRAME_RANGE_PRESETS:
                presets.append("'{0}'".format(preset))
            self.log_error('Invalid frame range. Expected one of (start_frame, end_frame), {0}'.format(", ".join(presets)))

        return None

    def preset_to_frame_range(self, frame_range_preset):
        if frame_range_preset == "Render":
            start_frame = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
            end_frame = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
        elif frame_range_preset == "Playback":
            start_frame = int(cmds.playbackOptions(q=True, minTime=True))
            end_frame = int(cmds.playbackOptions(q=True, maxTime=True))
        elif frame_range_preset == "Animation":
            start_frame = int(cmds.playbackOptions(q=True, animationStartTime=True))
            end_frame = int(cmds.playbackOptions(q=True, animationEndTime=True))
        else:
            raise RuntimeError("Invalid frame range preset: {0}".format(frame_range_preset))

        return (start_frame, end_frame)

    def set_visibility(self, visibility_data):
        if not visibility_data:
            visibility_data = []

        if not type(visibility_data) in [list, tuple]:
            visibility_data = self.preset_to_visibility(visibility_data)

            if visibility_data is None:
                return

        self._visibility = copy.copy(visibility_data)

    def get_visibility(self):
        if not self._visibility:
            return self.get_viewport_visibility()

        return self._visibility

    def preset_to_visibility(self, visibility_preset):
        if not visibility_preset in SwingPlayblast.VIEWPORT_VISIBILITY_PRESETS.keys():
            self.log_error("Invaild visibility preset: {0}".format(visibility_preset))
            return None

        visibility_data = []

        preset_names = SwingPlayblast.VIEWPORT_VISIBILITY_PRESETS[visibility_preset]
        if preset_names:
            for lookup_item in SwingPlayblast.VIEWPORT_VISIBILITY_LOOKUP:
                visibility_data.append(lookup_item[0] in preset_names)

        return visibility_data

    def get_viewport_visibility(self):
        model_panel = self.get_viewport_panel()
        if not model_panel:
            self.log_error("Failed to get viewport visibility. A viewport is not active.")
            return None

        viewport_visibility = []
        try:
            for item in SwingPlayblast.VIEWPORT_VISIBILITY_LOOKUP:
                kwargs = {item[1]: True}
                viewport_visibility.append(cmds.modelEditor(model_panel, q=True, **kwargs))
        except:
            traceback.print_exc()
            self.log_error("Failed to get active viewport visibility. See script editor for details.")
            return None

        return viewport_visibility

    def set_viewport_visibility(self, model_editor, visibility_flags):
        cmds.modelEditor(model_editor, e=True, **visibility_flags)

    def create_viewport_visibility_flags(self, visibility_data):
        visibility_flags = {}

        data_index = 0
        for item in SwingPlayblast.VIEWPORT_VISIBILITY_LOOKUP:
            visibility_flags[item[1]] = visibility_data[data_index]
            data_index += 1

        return visibility_flags

    def set_encoding(self, container_format, encoder):
        if container_format not in SwingPlayblast.VIDEO_ENCODER_LOOKUP.keys():
            self.log_error("Invalid container: {0}. Expected one of {1}".format(container_format, SwingPlayblast.VIDEO_ENCODER_LOOKUP.keys()))
            return

        if encoder not in SwingPlayblast.VIDEO_ENCODER_LOOKUP[container_format]:
            self.log_error("Invalid encoder: {0}. Expected one of {1}".format(encoder, SwingPlayblast.VIDEO_ENCODER_LOOKUP[container_format]))
            return

        self._container_format = container_format
        self._encoder = encoder

    def set_h264_settings(self, quality, preset):
        if not quality in SwingPlayblast.H264_QUALITIES.keys():
            self.log_error("Invalid h264 quality: {0}. Expected one of {1}".format(quality, SwingPlayblast.H264_QUALITIES.keys()))
            return

        if not preset in SwingPlayblast.H264_PRESETS:
            self.log_error("Invalid h264 preset: {0}. Expected one of {1}".format(preset, SwingPlayblast.H264_PRESETS))
            return

        self._h264_quality = quality
        self._h264_preset = preset

    def get_h264_settings(self):
        return {
            "quality": self._h264_quality,
            "preset": self._h264_preset,
        }

    def set_image_settings(self, quality):
        if quality > 0 and quality <= 100:
            self._image_quality = quality
        else:
            self.log_error("Invalid image quality: {0}. Expected value between 1-100")

    def get_image_settings(self):
        return {
            "quality": self._image_quality,
        }

    def execute(self, output_dir, filename, padding=4, overscan=False, show_ornaments=True, show_in_viewer=True, overwrite=False):

        if self.requires_ffmpeg() and not self.validate_ffmpeg():
            self.log_error("ffmpeg executable is not configured. See script editor for details.")
            return

        viewport_model_panel = self.get_viewport_panel()
        if not viewport_model_panel:
            self.log_error("An active viewport is not selected. Select a viewport and retry.")
            return

        if not output_dir:
            self.log_error("Output directory path not set")
            return
        if not filename:
            self.log_error("Output file name not set")
            return

        output_dir = self.resolve_output_directory_path(output_dir)
        filename = self.resolve_output_filename(filename)

        if padding <= 0:
            padding = SwingPlayblast.DEFAULT_PADDING

        if self.requires_ffmpeg():
            output_path = os.path.normpath(os.path.join(output_dir, "{0}.{1}".format(filename, self._container_format)))
            if not overwrite and os.path.exists(output_path):
                self.log_error("Output file already exists. Enable overwrite to ignore.")
                return

            playblast_output_dir = "{0}/playblast_temp".format(output_dir)
            playblast_output = os.path.normpath(os.path.join(playblast_output_dir, filename))
            force_overwrite = True
            compression = "png"
            image_quality = 100
            index_from_zero = True
            viewer = False
        else:
            playblast_output = os.path.normpath(os.path.join(output_dir, filename))
            force_overwrite = overwrite
            compression = self._encoder
            image_quality = self._image_quality
            index_from_zero = False
            viewer = show_in_viewer

        widthHeight = self.get_resolution_width_height()
        start_frame, end_frame = self.get_start_end_frame()

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

        camera = self._camera
        if not camera:
            camera = orig_camera

        if not camera in cmds.listCameras():
            self.log_error("Camera does not exist: {0}".format(camera))
            return

        self.set_active_camera(camera)

        orig_visibility_flags = self.create_viewport_visibility_flags(self.get_viewport_visibility())
        playblast_visibility_flags = self.create_viewport_visibility_flags(self.get_visibility())
            
        model_editor = cmds.modelPanel(viewport_model_panel, q=True, modelEditor=True)
        self.set_viewport_visibility(model_editor, playblast_visibility_flags)
        
        # Store original camera settings
        if not overscan:
            overscan_attr = "{0}.overscan".format(camera)
            orig_overscan = cmds.getAttr(overscan_attr)
            cmds.setAttr(overscan_attr, 1.0)

        playblast_failed = False
        try:
            cmds.playblast(**options)
        except:
            traceback.print_exc()
            self.log_error("Failed to create playblast. See script editor for details.")
            playblast_failed = True
        finally:
            # Restore original camera settings
            if not overscan:
                cmds.setAttr(overscan_attr, orig_overscan)
            
            # Restore original viewport settings
            self.set_active_camera(orig_camera)
            self.set_viewport_visibility(model_editor, orig_visibility_flags)

        if playblast_failed:
            return

        if self.requires_ffmpeg():
            source_path = "{0}/{1}.%0{2}d.png".format(playblast_output_dir, filename, padding)

            if self._encoder == "h264":
                self.encode_h264(source_path, output_path, start_frame)
            else:
                self.log_error("Encoding failed. Unsupported encoder ({0}) for container ({1}).".format(self._encoder, self._container_format))
                self.remove_temp_dir(playblast_output_dir)
                return

            self.remove_temp_dir(playblast_output_dir)

            if show_in_viewer:
                self.open_in_viewer(output_path)


    def remove_temp_dir(self, temp_dir_path):
        playblast_dir = QtCore.QDir(temp_dir_path)
        playblast_dir.setNameFilters(["*.png"])
        playblast_dir.setFilter(QtCore.QDir.Files)
        for f in playblast_dir.entryList():
            playblast_dir.remove(f)

        if not playblast_dir.rmdir(temp_dir_path):
            self.log_warning("Failed to remove temporary directory: {0}".format(temp_dir_path))

    def open_in_viewer(self, path):
        if not os.path.exists(path):
            self.log_error("Failed to open in viewer. File does not exists: {0}".format(path))
            return

        if self._container_format in ("mov", "mp4") and cmds.optionVar(exists="PlayblastCmdQuicktime"):
            executable_path = cmds.optionVar(q="PlayblastCmdQuicktime")
            if executable_path:
                QtCore.QProcess.startDetached(executable_path, [path])
                return

        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))

    def requires_ffmpeg(self):
        return self._container_format != "Image"

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


    def encode_h264(self, source_path, output_path, start_frame):
        framerate = self.get_frame_rate()

        audio_file_path, audio_frame_offset = self.get_audio_attributes()
        if audio_file_path:
            audio_offset = self.get_audio_offset_in_sec(start_frame, audio_frame_offset, framerate)

        crf = SwingPlayblast.H264_QUALITIES[self._h264_quality]
        preset = self._h264_preset

        ffmpeg_cmd = self._ffmpeg_path
        ffmpeg_cmd += ' -y -framerate {0} -i "{1}"'.format(framerate, source_path)

        if audio_file_path:
            ffmpeg_cmd += ' -ss {0} -i "{1}"'.format(audio_offset, audio_file_path)

        ffmpeg_cmd += ' -c:v libx264 -crf:v {0} -preset:v {1} -profile high -level 4.0 -pix_fmt yuv420p'.format(crf, preset)

        if audio_file_path:
            ffmpeg_cmd += ' -filter_complex "[1:0] apad" -shortest'

        ffmpeg_cmd += ' "{0}"'.format(output_path)

        self.log_output(ffmpeg_cmd)

        self.execute_ffmpeg_command(ffmpeg_cmd)


    def get_frame_rate(self):
        rate_str = cmds.currentUnit(q=True, time=True)

        if rate_str == "game":
            frame_rate = 15.0
        elif rate_str == "film":
            frame_rate = 24.0
        elif rate_str == "pal":
            frame_rate = 25.0
        elif rate_str == "ntsc":
            frame_rate = 30.0
        elif rate_str == "show":
            frame_rate = 48.0
        elif rate_str == "palf":
            frame_rate = 50.0
        elif rate_str == "ntscf":
            frame_rate = 60.0
        elif rate_str.endswith("fps"):
            frame_rate = float(rate_str[0:-3])
        else:
            raise RuntimeError("Unsupported frame rate: {0}".format(rate_str))

        return frame_rate

    def get_audio_attributes(self):
        sound_node = mel.eval("timeControl -q -sound $gPlayBackSlider;")
        if sound_node:
            file_path = cmds.getAttr("{0}.filename".format(sound_node))
            file_info = QtCore.QFileInfo(file_path)
            if file_info.exists():
                offset = cmds.getAttr("{0}.offset".format(sound_node))

                return (file_path, offset)

        return (None, None)

    def get_audio_offset_in_sec(self, start_frame, audio_frame_offset, frame_rate):
        return (start_frame - audio_frame_offset) / frame_rate

    def resolve_output_directory_path(self, dir_path):
        if "{project}" in dir_path:
            dir_path = dir_path.replace("{project}", self.get_project_dir_path())

        return dir_path

    def resolve_output_filename(self, filename):
        if "{scene}" in filename:
            filename = filename.replace("{scene}", self.get_scene_name())

        return filename

    def get_project_dir_path(self):
        return cmds.workspace(q=True, rootDirectory=True)

    def get_scene_name(self):
        scene_name = cmds.file(q=True, sceneName=True, shortName=True)
        if scene_name:
            scene_name = os.path.splitext(scene_name)[0]
        else:
            scene_name = "untitled"

        return scene_name

    def get_viewport_panel(self):
        model_panel = cmds.getPanel(withFocus=True)
        try:
            cmds.modelPanel(model_panel, q=True, modelEditor=True)
        except:
            self.log_error("Failed to get active view.")
            return None

        return model_panel

    def get_active_camera(self):
        model_panel = self.get_viewport_panel()
        if not model_panel:
            self.log_error("Failed to get active camera. A viewport is not active.")
            return None

        return cmds.modelPanel(model_panel, q=True, camera=True)

    def set_active_camera(self, camera):
        model_panel = self.get_viewport_panel()
        if model_panel:
            mel.eval("lookThroughModelPanel {0} {1}".format(camera, model_panel))
        else:
            self.log_error("Failed to set active camera. A viewport is not active.")


    def log_error(self, text):
        if self._log_to_maya:
            om.MGlobal.displayError("[SwingPlayblast] {0}".format(text))

        self.output_logged.emit("[ERROR] {0}".format(text)) # pylint: disable=E1101

    def log_warning(self, text):
        if self._log_to_maya:
            om.MGlobal.displayWarning("[SwingPlayblast] {0}".format(text))

        self.output_logged.emit("[WARNING] {0}".format(text)) # pylint: disable=E1101

    def log_output(self, text):
        if self._log_to_maya:
            om.MGlobal.displayInfo(text)

        self.output_logged.emit(text) # pylint: disable=E1101
class SwingPlayblastEncoderSettingsDialog(QtWidgets.QDialog):

    ENCODER_PAGES = {
        "h264": 0,
        "Image": 1,
    }

    H264_QUALITIES = [
        "Very High",
        "High",
        "Medium",
        "Low",
    ]


    def __init__(self, parent):
        super(SwingPlayblastEncoderSettingsDialog, self).__init__(parent)

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
        self.h264_quality_combo.addItems(SwingPlayblastEncoderSettingsDialog.H264_QUALITIES)

        self.h264_preset_combo = QtWidgets.QComboBox()
        self.h264_preset_combo.addItems(SwingPlayblast.H264_PRESETS)

        h264_layout = QtWidgets.QFormLayout()
        h264_layout.addRow("Quality:", self.h264_quality_combo)
        h264_layout.addRow("Preset:", self.h264_preset_combo)

        h264_settings_wdg = QtWidgets.QGroupBox("h264 Options")
        h264_settings_wdg.setLayout(h264_layout)

        # image
        self.image_quality_sb = QtWidgets.QSpinBox()
        self.image_quality_sb.setMinimumWidth(40)
        self.image_quality_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.image_quality_sb.setMinimum(1)
        self.image_quality_sb.setMaximum(100)

        image_layout = QtWidgets.QFormLayout()
        image_layout.addRow("Quality:", self.image_quality_sb)

        image_settings_wdg = QtWidgets.QGroupBox("Image Options")
        image_settings_wdg.setLayout(image_layout)

        self.settings_stacked_wdg = QtWidgets.QStackedWidget()
        self.settings_stacked_wdg.addWidget(h264_settings_wdg)
        self.settings_stacked_wdg.addWidget(image_settings_wdg)

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
        if not page in SwingPlayblastEncoderSettingsDialog.ENCODER_PAGES:
            return False

        self.settings_stacked_wdg.setCurrentIndex(SwingPlayblastEncoderSettingsDialog.ENCODER_PAGES[page])
        return True

    def set_h264_settings(self, quality, preset):
        self.h264_quality_combo.setCurrentText(quality)
        self.h264_preset_combo.setCurrentText(preset)

    def get_h264_settings(self):
        return {
            "quality": self.h264_quality_combo.currentText(),
            "preset": self.h264_preset_combo.currentText(),
        }

    def set_image_settings(self, quality):
        self.image_quality_sb.setValue(quality)

    def get_image_settings(self):
        return {
            "quality": self.image_quality_sb.value(),
        }


class SwingPlayblastVisibilityDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(SwingPlayblastVisibilityDialog, self).__init__(parent)

        self.setWindowTitle("Customize Visibility")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setModal(True)

        visibility_layout = QtWidgets.QGridLayout()

        index = 0
        self.visibility_checkboxes = []

        for i in range(len(SwingPlayblast.VIEWPORT_VISIBILITY_LOOKUP)):
            checkbox = QtWidgets.QCheckBox(SwingPlayblast.VIEWPORT_VISIBILITY_LOOKUP[i][0])

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


class SwingPlayblastUi(QtWidgets.QDialog):

    TITLE = "Zurbrigg Playblast"

    CONTAINER_PRESETS = [
        "mov",
        "mp4",
        "Image",
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
            cls.dlg_instance = SwingPlayblastUi()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()


    def __init__(self):
        try:
            if sys.version_info.major < 3:
                maya_main_window = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
            else:
                maya_main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)

            super(SwingPlayblastUi, self).__init__(maya_main_window)
        except:
            super(SwingPlayblastUi, self).__init__()

        self.setWindowTitle(SwingPlayblastUi.TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(500)

        self._playblast = SwingPlayblast()

        self._encoder_settings_dialog = None
        self._visibility_dialog = None

        self.load_app_settings()

        self.create_actions()
        self.create_menus()
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.load_defaults()
        self.load_user_settings()
        self.append_output("Playblast v{0}".format(SwingPlayblast.VERSION))


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

    def create_widgets(self):
        self.output_dir_path_le = QtWidgets.QLineEdit()
        self.output_dir_path_le.setPlaceholderText("{project}/movies")

        self.output_dir_path_select_btn = QtWidgets.QPushButton("...")
        self.output_dir_path_select_btn.setFixedSize(24, 19)
        self.output_dir_path_select_btn.setToolTip("Select Output Directory")

        self.output_dir_path_show_folder_btn = QtWidgets.QPushButton(QtGui.QIcon(":fileOpen.png"), "")
        self.output_dir_path_show_folder_btn.setFixedSize(24, 19)
        self.output_dir_path_show_folder_btn.setToolTip("Show in Folder")

        self.output_filename_le = QtWidgets.QLineEdit()
        self.output_filename_le.setPlaceholderText("{scene}")
        self.output_filename_le.setMaximumWidth(200)

        self.output_filename_select_btn = QtWidgets.QPushButton("...")
        self.output_filename_select_btn.setFixedSize(24, 19)
        self.output_filename_select_btn.setToolTip("Select File")

        self.output_filename_path_show_folder_btn = QtWidgets.QPushButton(QtGui.QIcon(":fileOpen.png"), "")
        self.output_filename_path_show_folder_btn.setFixedSize(24, 19)
        self.output_filename_path_show_folder_btn.setToolTip("Show in Folder")


        self.force_overwrite_cb = QtWidgets.QCheckBox("Force overwrite")

        self.resolution_select_cmb = QtWidgets.QComboBox()
        self.resolution_select_cmb.addItems(SwingPlayblastUi.RESOLUTION_PRESETS)
        self.resolution_select_cmb.addItem("Custom")
        self.resolution_select_cmb.setCurrentText(SwingPlayblast.DEFAULT_RESOLUTION)

        self.resolution_width_sb = QtWidgets.QSpinBox()
        self.resolution_width_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.resolution_width_sb.setRange(1, 9999)
        self.resolution_width_sb.setMinimumWidth(40)
        self.resolution_width_sb.setAlignment(QtCore.Qt.AlignRight)
        self.resolution_height_sb = QtWidgets.QSpinBox()
        self.resolution_height_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.resolution_height_sb.setRange(1, 9999)
        self.resolution_height_sb.setMinimumWidth(40)
        self.resolution_height_sb.setAlignment(QtCore.Qt.AlignRight)

        self.camera_select_cmb = QtWidgets.QComboBox()
        self.camera_select_hide_defaults_cb = QtWidgets.QCheckBox("Hide defaults")
        self.refresh_cameras()

        self.frame_range_cmb = QtWidgets.QComboBox()
        self.frame_range_cmb.addItems(SwingPlayblast.FRAME_RANGE_PRESETS)
        self.frame_range_cmb.addItem("Custom")
        self.frame_range_cmb.setCurrentText(SwingPlayblast.DEFAULT_FRAME_RANGE)

        self.frame_range_start_sb = QtWidgets.QSpinBox()
        self.frame_range_start_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.frame_range_start_sb.setRange(-9999, 9999)
        self.frame_range_start_sb.setMinimumWidth(40)
        self.frame_range_start_sb.setAlignment(QtCore.Qt.AlignRight)

        self.frame_range_end_sb = QtWidgets.QSpinBox()
        self.frame_range_end_sb.setButtonSymbols(QtWidgets.QSpinBox.NoButtons)
        self.frame_range_end_sb.setRange(-9999, 9999)
        self.frame_range_end_sb.setMinimumWidth(40)
        self.frame_range_end_sb.setAlignment(QtCore.Qt.AlignRight)

        self.encoding_container_cmb = QtWidgets.QComboBox()
        self.encoding_container_cmb.addItems(SwingPlayblastUi.CONTAINER_PRESETS)
        self.encoding_container_cmb.setCurrentText(SwingPlayblast.DEFAULT_CONTAINER)

        self.encoding_video_codec_cmb = QtWidgets.QComboBox()
        self.encoding_video_codec_settings_btn = QtWidgets.QPushButton("Settings...")
        self.encoding_video_codec_settings_btn.setFixedHeight(19)

        self.visibility_cmb = QtWidgets.QComboBox()
        self.visibility_cmb.addItems(SwingPlayblastUi.VISIBILITY_PRESETS)
        self.visibility_cmb.addItem("Custom")
        self.visibility_cmb.setCurrentText(SwingPlayblast.DEFAULT_VISIBILITY)

        self.visibility_customize_btn = QtWidgets.QPushButton("Customize...")
        self.visibility_customize_btn.setFixedHeight(19)
        
        self.overscan_cb = QtWidgets.QCheckBox()
        self.overscan_cb.setChecked(False)

        self.ornaments_cb = QtWidgets.QCheckBox()
        self.ornaments_cb.setChecked(True)

        self.viewer_cb = QtWidgets.QCheckBox()
        self.viewer_cb.setChecked(True)

        self.output_edit = QtWidgets.QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.playblast_btn = QtWidgets.QPushButton("Playblast")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        output_path_layout = QtWidgets.QHBoxLayout()
        output_path_layout.setSpacing(4)
        output_path_layout.addWidget(self.output_dir_path_le)
        output_path_layout.addWidget(self.output_dir_path_select_btn)
        output_path_layout.addWidget(self.output_dir_path_show_folder_btn)

        output_file_layout = QtWidgets.QHBoxLayout()
        output_file_layout.setSpacing(4)
        output_file_layout.addWidget(self.output_filename_le)
        output_file_layout.addWidget(self.output_filename_select_btn)
        output_file_layout.addWidget(self.force_overwrite_cb)

        output_layout = QtWidgets.QFormLayout()
        output_layout.setSpacing(4)
        output_layout.addRow("Directory:", output_path_layout)
        output_layout.addRow("Filename:", output_file_layout)

        output_grp = QtWidgets.QGroupBox("Output")
        output_grp.setLayout(output_layout)

        camera_options_layout = QtWidgets.QHBoxLayout()
        camera_options_layout.setSpacing(4)
        camera_options_layout.addWidget(self.camera_select_cmb)
        camera_options_layout.addWidget(self.camera_select_hide_defaults_cb)

        resolution_layout = QtWidgets.QHBoxLayout()
        resolution_layout.setSpacing(4)
        resolution_layout.addWidget(self.resolution_select_cmb)
        resolution_layout.addWidget(self.resolution_width_sb)
        resolution_layout.addWidget(QtWidgets.QLabel("x"))
        resolution_layout.addWidget(self.resolution_height_sb)

        frame_range_layout = QtWidgets.QHBoxLayout()
        frame_range_layout.setSpacing(4)
        frame_range_layout.addWidget(self.frame_range_cmb)
        frame_range_layout.addWidget(self.frame_range_start_sb)
        frame_range_layout.addWidget(self.frame_range_end_sb)

        encoding_layout = QtWidgets.QHBoxLayout()
        encoding_layout.setSpacing(4)
        encoding_layout.addWidget(self.encoding_container_cmb)
        encoding_layout.addWidget(self.encoding_video_codec_cmb)
        encoding_layout.addWidget(self.encoding_video_codec_settings_btn)

        visibility_layout = QtWidgets.QHBoxLayout()
        visibility_layout.setSpacing(4)
        visibility_layout.addWidget(self.visibility_cmb)
        visibility_layout.addWidget(self.visibility_customize_btn)

        options_layout = QtWidgets.QFormLayout()
        options_layout.addRow("Camera:", camera_options_layout)
        options_layout.addRow("Resolution:", resolution_layout)
        options_layout.addRow("Frame Range:", frame_range_layout)
        options_layout.addRow("Encoding:", encoding_layout)
        options_layout.addRow("Visiblity:", visibility_layout)
        options_layout.addRow("Overscan:", self.overscan_cb)
        options_layout.addRow("Ornaments:", self.ornaments_cb)
        options_layout.addRow("Show in Viewer:", self.viewer_cb)

        options_grp = QtWidgets.QGroupBox("Options")
        options_grp.setLayout(options_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.playblast_btn)
        button_layout.addWidget(self.close_btn)

        status_bar_layout = QtWidgets.QHBoxLayout()
        status_bar_layout.addStretch()
        status_bar_layout.addWidget(QtWidgets.QLabel("v{0}".format(SwingPlayblast.VERSION)))

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)
        main_layout.setMenuBar(self.main_menu)
        main_layout.addWidget(output_grp)
        main_layout.addWidget(options_grp)
        main_layout.addWidget(self.output_edit)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(status_bar_layout)

    def create_connections(self):
        self.output_dir_path_select_btn.clicked.connect(self.select_output_directory)
        self.output_dir_path_show_folder_btn.clicked.connect(self.open_output_directory)

        self.output_filename_select_btn.clicked.connect(self.select_output_filename)

        self.camera_select_cmb.currentTextChanged.connect(self.on_camera_changed)
        self.camera_select_hide_defaults_cb.toggled.connect(self.refresh_cameras)

        self.frame_range_cmb.currentTextChanged.connect(self.refresh_frame_range)
        self.frame_range_start_sb.editingFinished.connect(self.on_frame_range_changed)
        self.frame_range_end_sb.editingFinished.connect(self.on_frame_range_changed)

        self.encoding_container_cmb.currentTextChanged.connect(self.refresh_video_encoders)
        self.encoding_video_codec_cmb.currentTextChanged.connect(self.on_video_encoder_changed)
        self.encoding_video_codec_settings_btn.clicked.connect(self.show_encoder_settings_dialog)

        self.resolution_select_cmb.currentTextChanged.connect(self.refresh_resolution)
        self.resolution_width_sb.editingFinished.connect(self.on_resolution_changed)
        self.resolution_height_sb.editingFinished.connect(self.on_resolution_changed)

        self.visibility_cmb.currentTextChanged.connect(self.on_visibility_preset_changed)
        self.visibility_customize_btn.clicked.connect(self.show_visibility_dialog)

        self.refresh_btn.clicked.connect(self.refresh)
        self.clear_btn.clicked.connect(self.output_edit.clear)
        self.playblast_btn.clicked.connect(self.do_playblast)
        self.close_btn.clicked.connect(self.do_close)

        self._playblast.output_logged.connect(self.append_output) # pylint: disable=E1101

    def do_close(self):
        self.write_settings()
        self.close()

    def do_playblast(self):
        output_dir_path = self.output_dir_path_le.text()
        if not output_dir_path:
            output_dir_path = self.output_dir_path_le.placeholderText()

        filename = self.output_filename_le.text()
        if not filename:
            filename = self.output_filename_le.placeholderText()

        padding = SwingPlayblast.DEFAULT_PADDING

        overscan = self.overscan_cb.isChecked()
        show_ornaments = self.ornaments_cb.isChecked()
        show_in_viewer = self.viewer_cb.isChecked()
        overwrite = self.force_overwrite_cb.isChecked()

        self._playblast.execute(output_dir_path, filename, padding, overscan, show_ornaments, show_in_viewer, overwrite)

    def select_output_directory(self):
        current_dir_path = self.output_dir_path_le.text()
        if not current_dir_path:
            current_dir_path = self.output_dir_path_le.placeholderText()

        current_dir_path = self._playblast.resolve_output_directory_path(current_dir_path)

        file_info = QtCore.QFileInfo(current_dir_path)
        if not file_info.exists():
            current_dir_path = self._playblast.get_project_dir_path()

        new_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", current_dir_path)
        if new_dir_path:
            self.output_dir_path_le.setText(new_dir_path)

    def select_output_filename(self):
        current_dir_path = self.output_dir_path_le.text()
        if not current_dir_path:
            current_dir_path = self.output_dir_path_le.placeholderText()

        current_filename = self.output_filename_le.text()
        if not current_filename:
            current_filename = self.output_filename_le.placeholderText()

        current_dir_path = self._playblast.resolve_output_directory_path(current_dir_path)
        current_filename = self._playblast.resolve_output_filename(current_filename)

        selected_file = os.path.join(current_dir_path, current_filename)

        file_info = QtCore.QFileInfo(selected_file)
        if not file_info.exists():
            current_dir_path = self._playblast.get_project_dir_path()

        new_filename = QtWidgets.QFileDialog.getSaveFileName(self, "Select Directory", selected_file)
        if new_filename:
            self.output_filename_le.setText("{}".format(new_filename[0]))

    def open_output_directory(self):
        output_dir_path = self.output_dir_path_le.text()
        if not output_dir_path:
            output_dir_path = self.output_dir_path_le.placeholderText()

        output_dir_path = self._playblast.resolve_output_directory_path(output_dir_path)

        file_info = QtCore.QFileInfo(output_dir_path)
        if file_info.isDir():
            QtGui.QDesktopServices.openUrl(output_dir_path)
        else:
            self.append_output("[ERROR] Invalid directory path: {0}".format(output_dir_path))

    def refresh(self):
        if _stand_alone:
            return

        self.refresh_cameras()
        self.refresh_resolution()
        self.refresh_frame_range()
        self.refresh_video_encoders()

    def refresh_cameras(self):
        if _stand_alone:
            return 

        current_camera = self.camera_select_cmb.currentText()
        self.camera_select_cmb.clear()

        self.camera_select_cmb.addItem("<Active>")

        cameras = cmds.listCameras()
        if self.camera_select_hide_defaults_cb.isChecked():
            for camera in cameras:
                if camera not in ["front", "persp", "side", "top"]:
                    self.camera_select_cmb.addItem(camera)
        else:
            self.camera_select_cmb.addItems(cameras)

        self.camera_select_cmb.setCurrentText(current_camera)

    def on_camera_changed(self):
        camera = self.camera_select_cmb.currentText()
        if camera == "<Active>":
            camera = None

        self._playblast.set_camera(camera)

    def refresh_resolution(self):
        resolution_preset = self.resolution_select_cmb.currentText()
        if resolution_preset != "Custom":
            self._playblast.set_resolution(resolution_preset)

            resolution = self._playblast.get_resolution_width_height()
            self.resolution_width_sb.setValue(resolution[0])
            self.resolution_height_sb.setValue(resolution[1])

    def on_resolution_changed(self):
        resolution = (self.resolution_width_sb.value(), self.resolution_height_sb.value())

        for key in SwingPlayblast.RESOLUTION_LOOKUP.keys():
            if SwingPlayblast.RESOLUTION_LOOKUP[key] == resolution:
                self.resolution_select_cmb.setCurrentText(key)
                return

        self.resolution_select_cmb.setCurrentText("Custom")

        self._playblast.set_resolution(resolution)

    def refresh_frame_range(self):
        frame_range_preset = self.frame_range_cmb.currentText()
        if frame_range_preset != "Custom":
            frame_range = self._playblast.preset_to_frame_range(frame_range_preset)

            self.frame_range_start_sb.setValue(frame_range[0])
            self.frame_range_end_sb.setValue(frame_range[1])

            self._playblast.set_frame_range(frame_range_preset)

    def on_frame_range_changed(self):
        self.frame_range_cmb.setCurrentText("Custom")

        frame_range = (self.frame_range_start_sb.value(), self.frame_range_end_sb.value())
        self._playblast.set_frame_range(frame_range)

    def refresh_video_encoders(self):
        self.encoding_video_codec_cmb.clear()

        container = self.encoding_container_cmb.currentText()
        self.encoding_video_codec_cmb.addItems(SwingPlayblast.VIDEO_ENCODER_LOOKUP[container])

    def on_video_encoder_changed(self):
        container = self.encoding_container_cmb.currentText()
        encoder = self.encoding_video_codec_cmb.currentText()

        if container and encoder:
            self._playblast.set_encoding(container, encoder)

    def show_encoder_settings_dialog(self):
        if not self._encoder_settings_dialog:
            self._encoder_settings_dialog = SwingPlayblastEncoderSettingsDialog(self)
            self._encoder_settings_dialog.accepted.connect(self.on_encoder_settings_dialog_modified)

        if self.encoding_container_cmb.currentText() == "Image":
            self._encoder_settings_dialog.set_page("Image")

            image_settings = self._playblast.get_image_settings()
            self._encoder_settings_dialog.set_image_settings(image_settings["quality"])

        else:
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

    def show_visibility_dialog(self):
        if not self._visibility_dialog:
            self._visibility_dialog = SwingPlayblastVisibilityDialog(self)
            self._visibility_dialog.accepted.connect(self.on_visibility_dialog_modified)

        self._visibility_dialog.set_visibility_data(self._playblast.get_visibility())

        self._visibility_dialog.show()

    def on_visibility_dialog_modified(self):
        self.visibility_cmb.setCurrentText("Custom")
        self._playblast.set_visibility(self._visibility_dialog.get_visibility_data())

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("Playblast")

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("Playblast")

        self.resize(self.settings.value("size", QtCore.QSize(400, 400)))
        self.move(self.settings.value("pos", QtCore.QPoint(200, 200)))
        self.settings.endGroup()          

    def load_user_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup("Playblast")
        self.output_dir_path_le.setText(self.settings.value("output_dir_path_le", self.output_dir_path_le.placeholderText()))
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
        if _stand_alone:
            return 

        cmds.optionVar(sv=("SwingPlayblastUiOutputDir", self.output_dir_path_le.text()))
        cmds.optionVar(sv=("SwingPlayblastUiOutputFilename", self.output_filename_le.text()))
        cmds.optionVar(iv=("SwingPlayblastUiForceOverwrite", self.force_overwrite_cb.isChecked()))

        cmds.optionVar(sv=("SwingPlayblastUiCamera", self.camera_select_cmb.currentText()))
        cmds.optionVar(iv=("SwingPlayblastUiHideDefaultCameras", self.camera_select_hide_defaults_cb.isChecked()))

        cmds.optionVar(sv=("SwingPlayblastUiResolutionPreset", self.resolution_select_cmb.currentText()))
        cmds.optionVar(iv=("SwingPlayblastUiResolutionWidth", self.resolution_width_sb.value()))
        cmds.optionVar(iv=("SwingPlayblastUiResolutionHeight", self.resolution_height_sb.value()))

        cmds.optionVar(sv=("SwingPlayblastUiFrameRangePreset", self.frame_range_cmb.currentText()))
        cmds.optionVar(iv=("SwingPlayblastUiFrameRangeStart", self.frame_range_start_sb.value()))
        cmds.optionVar(iv=("SwingPlayblastUiFrameRangeEnd", self.frame_range_end_sb.value()))

        cmds.optionVar(sv=("SwingPlayblastUiEncodingContainer", self.encoding_container_cmb.currentText()))
        cmds.optionVar(sv=("SwingPlayblastUiEncodingVideoCodec", self.encoding_video_codec_cmb.currentText()))

        h264_settings = self._playblast.get_h264_settings()
        cmds.optionVar(sv=("SwingPlayblastUiH264Quality", h264_settings["quality"]))
        cmds.optionVar(sv=("SwingPlayblastUiH264Preset", h264_settings["preset"]))

        image_settings = self._playblast.get_image_settings()
        cmds.optionVar(iv=("SwingPlayblastUiImageQuality", image_settings["quality"]))

        cmds.optionVar(sv=("SwingPlayblastUiVisibilityPreset", self.visibility_cmb.currentText()))

        visibility_data = self._playblast.get_visibility()
        visibility_str = ""
        for item in visibility_data:
            visibility_str = "{0} {1}".format(visibility_str, int(item))
        cmds.optionVar(sv=("SwingPlayblastUiVisibilityData", visibility_str))

        cmds.optionVar(iv=("SwingPlayblastUiOverscan", self.overscan_cb.isChecked()))
        cmds.optionVar(iv=("SwingPlayblastUiOrnaments", self.ornaments_cb.isChecked()))
        cmds.optionVar(iv=("SwingPlayblastUiViewer", self.viewer_cb.isChecked()))

    def load_defaults(self):
        if _stand_alone:
            return 

        if cmds.optionVar(exists="SwingPlayblastUiOutputDir"):
            self.output_dir_path_le.setText(cmds.optionVar(q="SwingPlayblastUiOutputDir"))
        if cmds.optionVar(exists="SwingPlayblastUiOutputFilename"):
            self.output_filename_le.setText(cmds.optionVar(q="SwingPlayblastUiOutputFilename"))
        if cmds.optionVar(exists="SwingPlayblastUiForceOverwrite"):
            self.force_overwrite_cb.setChecked(cmds.optionVar(q="SwingPlayblastUiForceOverwrite"))

        if cmds.optionVar(exists="SwingPlayblastUiCamera"):
            self.camera_select_cmb.setCurrentText(cmds.optionVar(q="SwingPlayblastUiCamera"))
        if cmds.optionVar(exists="SwingPlayblastUiHideDefaultCameras"):
            self.camera_select_hide_defaults_cb.setChecked(cmds.optionVar(q="SwingPlayblastUiHideDefaultCameras"))

        if cmds.optionVar(exists="SwingPlayblastUiResolutionPreset"):
            self.resolution_select_cmb.setCurrentText(cmds.optionVar(q="SwingPlayblastUiResolutionPreset"))
        if self.resolution_select_cmb.currentText() == "Custom":
            if cmds.optionVar(exists="SwingPlayblastUiResolutionWidth"):
                self.resolution_width_sb.setValue(cmds.optionVar(q="SwingPlayblastUiResolutionWidth"))
            if cmds.optionVar(exists="SwingPlayblastUiResolutionHeight"):
                self.resolution_height_sb.setValue(cmds.optionVar(q="SwingPlayblastUiResolutionHeight"))
            self.on_resolution_changed()

        if cmds.optionVar(exists="SwingPlayblastUiFrameRangePreset"):
            self.frame_range_cmb.setCurrentText(cmds.optionVar(q="SwingPlayblastUiFrameRangePreset"))
        if self.frame_range_cmb.currentText() == "Custom":
            if cmds.optionVar(exists="SwingPlayblastUiFrameRangeStart"):
                self.frame_range_start_sb.setValue(cmds.optionVar(q="SwingPlayblastUiFrameRangeStart"))
            if cmds.optionVar(exists="SwingPlayblastUiFrameRangeEnd"):
                self.frame_range_end_sb.setValue(cmds.optionVar(q="SwingPlayblastUiFrameRangeEnd"))
            self.on_frame_range_changed()

        if cmds.optionVar(exists="SwingPlayblastUiEncodingContainer"):
            self.encoding_container_cmb.setCurrentText(cmds.optionVar(q="SwingPlayblastUiEncodingContainer"))
        if cmds.optionVar(exists="SwingPlayblastUiEncodingVideoCodec"):
            self.encoding_video_codec_cmb.setCurrentText(cmds.optionVar(q="SwingPlayblastUiEncodingVideoCodec"))

        if cmds.optionVar(exists="SwingPlayblastUiH264Quality") and cmds.optionVar(exists="SwingPlayblastUiH264Preset"):
            self._playblast.set_h264_settings(cmds.optionVar(q="SwingPlayblastUiH264Quality"), cmds.optionVar(q="SwingPlayblastUiH264Preset"))

        if cmds.optionVar(exists="SwingPlayblastUiImageQuality"):
            self._playblast.set_image_settings(cmds.optionVar(q="SwingPlayblastUiImageQuality"))

        if cmds.optionVar(exists="SwingPlayblastUiVisibilityPreset"):
            self.visibility_cmb.setCurrentText(cmds.optionVar(q="SwingPlayblastUiVisibilityPreset"))
        if self.visibility_cmb.currentText() == "Custom":
            if cmds.optionVar(exists="SwingPlayblastUiVisibilityData"):
                visibility_str_list = cmds.optionVar(q="SwingPlayblastUiVisibilityData").split()
                visibility_data = []
                for item in visibility_str_list:
                    if item:
                        visibility_data.append(bool(int(item)))

                self._playblast.set_visibility(visibility_data)

        if cmds.optionVar(exists="SwingPlayblastUiOverscan"):
            self.overscan_cb.setChecked(cmds.optionVar(q="SwingPlayblastUiOverscan"))
        if cmds.optionVar(exists="SwingPlayblastUiOrnaments"):
            self.ornaments_cb.setChecked(cmds.optionVar(q="SwingPlayblastUiOrnaments"))
        if cmds.optionVar(exists="SwingPlayblastUiViewer"):
            self.viewer_cb.setChecked(cmds.optionVar(q="SwingPlayblastUiViewer"))



    def show_about_dialog(self):
        text = '<h2>{0}</h2>'.format(SwingPlayblastUi.TITLE)
        text += '<p>Version: {0}</p>'.format(SwingPlayblast.VERSION)

        QtWidgets.QMessageBox().about(self, "About", "{0}".format(text))

    def append_output(self, text):
        self.output_edit.appendPlainText(text)

    def keyPressEvent(self, event):
        super(SwingPlayblastUi, self).keyPressEvent(event)

        event.accept()

    def showEvent(self, event):
        self.refresh()


if __name__ == "__main__":
    try:
        swing_playblast_dialog.close() # pylint: disable=E0601
        swing_playblast_dialog.deleteLater()
    except:
        pass

    swing_playblast_dialog = SwingPlayblastUi()
    swing_playblast_dialog.show()




