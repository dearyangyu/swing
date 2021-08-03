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
    pass

# Maya Utility Library
class SwingMaya(QtCore.QObject):

    output_logged = QtCore.Signal(str)

    DEFAULT_FFMPEG_PATH = "C:/ffmpeg/ffmpeg-4.2.1/bin/ffmpeg.exe"

    VERSION = "0.0.1"
    TITLE = "Swing Maya"

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

    def __init__(self, ffmpeg_path = None, log_to_maya = True):
        super(SwingMaya, self).__init__()

        self.set_maya_logging_enabled(log_to_maya)
        self.set_camera(SwingMaya.DEFAULT_CAMERA)
        self.set_resolution(SwingMaya.DEFAULT_RESOLUTION)
        self.set_frame_range(SwingMaya.DEFAULT_FRAME_RANGE)

    def set_maya_logging_enabled(self, enabled):
        self._log_to_maya = enabled
        if enabled:
            self.log_output("[info] maya logging enabled")

    def log_error(self, text):
        if self._log_to_maya:
            om.MGlobal.displayError("{}: {}".format(self.__class__.__name__, text))
        else:
            print("[error] {}".format(text))
        self.output_logged.emit("[error] {}".format(text))
        
    def log_warning(self, text):
        if self._log_to_maya:
            om.MGlobal.displayWarning("{}: {}".format(self.__class__.__name__, text))
        else:
            print("[warn] {}".format(text))

        self.output_logged.emit("[warning] {}".format(text))
        
    def log_output(self, text):
        if self._log_to_maya:
            om.MGlobal.displayInfo("{}: {}".format(self.__class__.__name__, text))
        else:
            print("[info] {}".format(text))

    def set_camera(self, camera):
        if camera and camera not in cmds.listCameras():
            self.log_output("Camera does not exist {}".format(camera))
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
            for preset in SwingMaya.RESOLUTION_LOOKUP.keys():
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
        elif resolution_preset in SwingMaya.RESOLUTION_LOOKUP.keys():
            return SwingMaya.RESOLUTION_LOOKUP[resolution_preset]
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
        if not visibility_preset in SwingMaya.VIEWPORT_VISIBILITY_PRESETS.keys():
            self.log_error("Invaild visibility preset: {0}".format(visibility_preset))
            return None

        visibility_data = []

        preset_names = SwingMaya.VIEWPORT_VISIBILITY_PRESETS[visibility_preset]
        if preset_names:
            for lookup_item in SwingMaya.VIEWPORT_VISIBILITY_LOOKUP:
                visibility_data.append(lookup_item[0] in preset_names)

        return visibility_data

    def get_viewport_visibility(self):
        model_panel = self.get_viewport_panel()
        if not model_panel:
            self.log_error("Failed to get viewport visibility. A viewport is not active.")
            return None

        viewport_visibility = []
        try:
            for item in SwingMaya.VIEWPORT_VISIBILITY_LOOKUP:
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
        for item in SwingMaya.VIEWPORT_VISIBILITY_LOOKUP:
            visibility_flags[item[1]] = visibility_data[data_index]
            data_index += 1

        return visibility_flags

    def set_frame_range(self, frame_range):
        resolved_frame_range = self.resolve_frame_range(frame_range)
        if not resolved_frame_range:
            return

        self._frame_range_preset = None
        if frame_range in SwingMaya.FRAME_RANGE_PRESETS:
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
            for preset in SwingMaya.FRAME_RANGE_PRESETS:
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

    def get_scene_path(self):
        file_name = cmds.file(q=True, sn=True)
        return os.path.dirname(file_name)

    def set_frame_rate(self, fps):
        unit = 'ntscf'
        if fps == 15:
            unit = 'game'
        elif fps == 24:
            unit = 'film'
        elif fps == 25:
            unit = 'pal'
        elif fps == 30:
            unit = 'ntsc'
        elif fps == 48:
            unit = 'show'
        elif fps == 50:
            unit = 'palf'
        elif fps == 60:
            unit = 'ntscf'
        else:
            unit = str(fps) + 'fps'

        cmds.currentUnit( time=unit )
        return mel.eval('currentTimeUnitToFPS')

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
            raise RuntimeError("Unsupported frame rate: {0}".format(rate_str))

        return frame_rate

    def get_audio_attributes(self):
        try:
            sound_node = mel.eval("timeControl -q sound $gPlayBackSlider;")
            if sound_node:
                file_path = cmds.getAttr("{0}.filename".format(sound_node))
                file_info = QtCore.QFileInfo(file_path)

                if file_info.exists():
                    offset = cmds.getAttr("{0}.offset".format(sound_node))
                    return (file_path, offset)
        except:
            self.log_warning("No audio track found")
        return (None, None)

    def get_audio_offset_in_sec(self, start_frame, audio_frame_offset, frame_rate):
        return (start_frame - audio_frame_offset) / frame_rate

    def resolve_output_directory_path(self, dir_path):
        if "{project}" in dir_path:
            dir_path = dir_path.replace("{project}", self.get_project_dir_path())

        return dir_path

