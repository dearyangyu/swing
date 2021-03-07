import copy
import os
import traceback

from PySide2 import QtCore
from PySide2 import QtGui

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om
    import maya.OpenMayaUI as omui
except:
    print("Maya not loaded")

class SwingPlayblast(QtCore.QObject):

    DEFAULT_FFMPEG_PATH = "C:/ffmpeg/ffmpeg-4.2.1/bin/ffmpeg.exe"

    VERSION = "0.0.1"
    TITLE = "Swing Playblaster"

    RESOLUTION_LOOKUP = {
        "Render": (),
        "HD 1080": (1920, 1080),
        "HD 720": (1280, 720),
        "HD 540": (960, 540)
    }

    FRAME_RANGE_PRESETS = [
        "Render",
        "Playback",
        "Animation"
    ]

    VIDEO_ENCODER_LOOKUP = {
        "mov": ["h264"],
        "mp4": ["h264"],
        "Image": ["jpg", "png", "tif"]
    }
    
    H264_QUALITIES = {
        "Very High": 18,
        "High": 20,
        "Medium": 23,
        "Low": 26
    }

    H264_PRESETS = {
        "veryslow",
        "slow",
        "medium",
        "fast",
        "faster"
        "ultrafast"
    }

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
    DEFAULT_PADDING = 4
    DEFAULT_VISIBILITY = "Viewport"

    output_logged = QtCore.Signal(str)

    def __init__(self, ffmpeg_path = None, log_to_maya = True):
        super(SwingPlayblast, self).__init__()

        self.set_maya_logging_enabled(log_to_maya)
        self.set_ffmpeg_path(ffmpeg_path)
        self.set_camera(SwingPlayblast.DEFAULT_CAMERA)
        self.set_resolution(SwingPlayblast.DEFAULT_RESOLUTION)
        self.set_frame_range(SwingPlayblast.DEFAULT_FRAME_RANGE)
        self.set_encoding(SwingPlayblast.DEFAULT_CONTAINER, SwingPlayblast.DEFAULT_ENCODER)
        self.set_h264_settings(SwingPlayblast.DEFAULT_H264_QUALITY, SwingPlayblast.DEFAULT_H264_PRESET)
        self.set_image_settings(SwingPlayblast.DEFAULT_IMAGE_QUALITY)
        self.set_visibility(SwingPlayblast.DEFAULT_VISIBILITY)

        self.initialize_ffmpeg_process()

    def set_maya_logging_enabled(self, enabled):
        self._log_to_maya = enabled
        if enabled:
            self.log_output("[info] maya logging enabled")

    def log_error(self, text):
        if self._log_to_maya:
            om.MGlobal.displayError("[swingplayblast] {0}".format(text))
        self.output_logged.emit("[error] {0}".format(text))
        print("[error] {}".format(text))

    def log_warning(self, text):
        if self._log_to_maya:
            om.MGlobal.displayWarning("[swingplayblast] {0}".format(text))
        self.output_logged.emit("[warning] {0}".format(text))
        print("[warn] {}".format(text))

    def log_output(self, text):
        if self._log_to_maya:
            om.MGlobal.displayInfo(text)
        self.output_logged.emit(text)
        print("[info] {}".format(text))

    def set_ffmpeg_path(self, path):
        if path:
            self._ffmpeg_path = path
        else:
            self._ffmpeg_path = self.DEFAULT_FFMPEG_PATH

    def get_ffmpeg_path(self):
        return self._ffmpeg_path

    def set_camera(self, camera):
        if camera and camera not in cmds.listCameras():
            self.log_output("Camera does not exist {0}".format(camera))
            camera = None

        self._camera = camera

    def get_viewport_panel(self):
        model_panel = cmds.getPanel(withFocus = True)
        try:
            cmds.modelPanel(model_panel, q = True, modelEditor = True)
            return model_panel
        except:
            self.log_error("Failed to get active view")

    def get_active_camera(self):
        model_panel = self.get_viewport_panel()
        if not model_panel:
            self.log_error("Failed to get active camera. A viewport is not active")
            return None

        return cmds.modelPanel(model_panel, q = True, camera = True)

    def set_active_camera(self, camera):
        model_panel = self.get_viewport_panel()
        if model_panel:
            mel.eval("lookThroughModelPanel {0} {1}".format(camera, model_panel))
        else:
            self.log_error("Failed to set active camera. A viewport is not active")
            return None

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
            self.log_error("Invalid container {0}. Expected one of {1}".format(container_format, SwingPlayblast.VIDEO_ENCODER_LOOKUP))
            return 

        if encoder not in SwingPlayblast.VIDEO_ENCODER_LOOKUP[container_format]:
            self.log_error("Invalid encoder {0}. Expected one of {1}".format(encoder, SwingPlayblast.VIDEO_ENCODER_LOOKUP[container_format]))
            return

        self._container_format = container_format
        self._encoder = encoder

    def set_h264_settings(self, quality, preset):
        if not quality in SwingPlayblast.H264_QUALITIES.keys():
            self.log_error("Invalid h264 quality {0}. Expected one of {1}".format(quality, SwingPlayblast.H264_QUALITIES.keys()))
            return 

        if preset not in SwingPlayblast.H264_PRESETS:
            self.log_error("Invalid h264 preset {0}. Expected one of {1}".format(preset, SwingPlayblast.H264_PRESETS[quality]))
            return

        self._h264_quality = quality
        self._h264_preset = preset

    def get_h264_settings(self):
        return {
            "quality": self._h264_quality,
            "preset": self._h264_preset
        }

    def set_image_settings(self, quality):
        if quality > 0 and quality <= 100:
            self._image_quality = quality
        else:
            self.log_error("Invalid image quality {0}. Expected value between 1 - 100".format(quality))

    def get_image_settings(self):
        return {
            "quality": self._image_quality
        }
    
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

    def requires_ffmpeg(self):
        return self._container_format != "Image"

    def validate_ffmpeg(self):
        if not self._ffmpeg_path:
            self.log_output("ffmpeg path not set")
            return False
        
        if not os.path.exists(self._ffmpeg_path):
            self.log_error("ffmpeg path not found: {0}".format(self._ffmpeg_path))
            return False

        if not os.path.isfile(self._ffmpeg_path):
            self.log_error("ffmpeg path not found: {0}".format(self._ffmpeg_path))
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

    ## ENCODE start
    def encode_h264(self, source_path, output_path, start_frame):
        framerate = self.get_frame_rate()

        audio_file_path, audio_frame_offset = self.get_audio_attributes()
        if audio_frame_offset:
            audio_offset = self.get_audio_offset_in_sec(start_frame, audio_frame_offset, framerate)

        crf = SwingPlayblast.H264_QUALITIES[self._h264_quality]
        preset = self._h264_quality

        ffmpeg_cmd = self._ffmpeg_path
        ffmpeg_cmd += ' -y -framerate {0} -i "{1}"'.format(framerate, source_path)

        if audio_frame_offset:
            ffmpeg_cmd += ' -ss {0} -i "{1}" '.format(audio_frame_offset, audio_file_path)

        ffmpeg_cmd += ' -c:v libx264 -crf:v {0} -preset:v {1} -profile high -level 4.0 -pix_fmt yuv420p'.format(crf, preset)

        if audio_frame_offset:
            ffmpeg_cmd += ' -filter_complex "[1:0] apad" -shortest '

        ffmpeg_cmd += ' "{0}"'.format(output_path)

        self.log_output(ffmpeg_cmd)
        self.execute_ffmpeg_command(ffmpeg_cmd)
    ## ENCODE end

    ## EXECUTE start
    def execute(self, output_dir, filename, padding = 4, show_ornaments = True, show_in_viewer = True, overwrite = False):
        if self.requires_ffmpeg() and not self.validate_ffmpeg():
            self.log_error("ffmpeg executable is not configured. See script for details")
            return 

        viewport_model_panel = self.get_viewport_panel()
        if not viewport_model_panel:
            self.log_error("Viewport is not selected. Select a viewport and retry")
            return

        if not output_dir:
            self.log_error("Output directory path not set")
            return 

        if not filename:
            self.log_error("File name not set")
            return

        output_dir = self.resolve_output_directory_path(output_dir)
        filename = self.resolve_output_file_name(filename)

        if padding <= 0:
            padding = SwingPlayblast.DEFAULT_PADDING 

        if self.requires_ffmpeg():
            output_path = os.path.normcase(os.path.join(output_dir, "{0}.{1}".format(filename, self._container_format)))
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
            # image sequence
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

        # store viewport settings
        orig_camera = self.get_active_camera()
        camera = self._camera
        if not camera:
            camera = orig_camera

        if not camera not in cmds.listCameras():
            self.log_error("Camera does not exist {0}".format(camera))
            return

        self.set_active_camera(camera)

        orig_visibility_flags = self.create_viewport_visibility_flags(self.get_viewport_visibility())
        playblast_visibility_flags = self.create_viewport_visibility_flags(self.get_visibility())

        model_editor = cmds.modelPanel(viewport_model_panel, q = True, modelEditor = True)
        self.set_viewport_visibility(model_editor, playblast_visibility_flags)

        playblast_failed = False
        try:
            cmds.playblast(**options)
        except:
            traceback.print_exc()
            self.log_error("Failed to create playblast. See script editor for details")
            playblast_failed = True
        finally:
            # pop viewport
            self.set_active_camera(orig_camera)
            self.set_viewport_visibility(model_editor, orig_visibility_flags)

        if playblast_failed:
            return

        if self.requires_ffmpeg():
            source_path = "{0}/{1}.%0{2}d.png".format(playblast_output_dir, filename, padding)

            if self._encoder == "h264":
                self.encode_h264(source_path, output_path, start_frame)
            else:
                self.log_error("Encoding failed. Unsupported encoder {0} for container {1}".format(self._encoder, self._container_format))
                self.remove_temp_dir(playblast_output_dir)
                return

            self.remove_temp_dir(playblast_output_dir)

            if show_in_viewer:
                self.show_in_viewer(output_path)
    ## EXECUTE end

    def remove_temp_dir(self, temp_dir_path):
        playblast_dir = QtCore.QDir(temp_dir_path)
        playblast_dir.setNameFilters(["*.png"])
        playblast_dir.setFilter(QtCore.QDir.Files)
        for f in playblast_dir.entryList():
            playblast_dir.remove(f)

        if not playblast_dir.rmdir(temp_dir_path):
            self.log_warning("Failed to remove temporary directory {0}".format(temp_dir_path))

    def open_in_viewer(self, path):
        if not os.path.exists(path):
            self.log_error("Failed to open viewer. File does not exist: {0}".format(path))
            return

        if self._container_format in ("mov", "mp4") and cmds.optionVar(exists="PlayblastCmdQuicktime"):
            executable_path = cmds.optionVar(q="PlayblastCmdQuicktime")
            if executable_path:
                QtCore.QProcess.startDetached(executable_path, [path])
                return

        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))

    def get_project_dir_path(self):
        return cmds.workspace(q = True, rootDirectory = True)

    def get_scene_name(self):
        scene_name = cmds.file(q= True, sceneName = True, shortName = True)
        if scene_name:
            scene_name = os.path.splitext(scene_name)[0]
        else:
            scene_name = "untitled"

        return scene_name

    def get_frame_rate(self):
        rate_str = cmds.currentUnit(q = True, time = True)

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
        elif rate_str == "film":
            frame_rate = 24.0
        elif rate_str.endswith("fps"):
            frame_rate = float(rate_str[0:-3])
        else:
            raise RuntimeError("Unsupported framr rate: {0}".format(rate_str))

        return frame_rate

    def get_audio_attributes(self):
        sound_node = mel.eval("timeControl -q sound $gPlayBackSlider;")
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

    def resolve_output_file_name(self, filename):
        if "{scene}" in filename:
            filename = filename.replace("{scene}", self.get_project_dir_path())

        return filename


if __name__ == "__main__":
    pb = SwingPlayblast()
    pb.log_error("Error")
    pb.log_warning("Warning")
    pb.log_output("Output")