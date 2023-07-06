import copy
import csv
import os
import glob
import traceback
import sys

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

    VERSION = "0.0.5"
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

        if ffmpeg_path:
            self.DEFAULT_FFMPEG_PATH = ffmpeg_path

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
            self.log_error("Invalid visibility preset: {0}".format(visibility_preset))
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
        self.log_output("set_frame_range {}".format(frame_range))

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

    def get_scene_path(self):
        file_name = cmds.file(q=True, sn=True)
        return os.path.dirname(file_name)

    def get_scene_name(self):
        scene_name = cmds.file(q= True, sceneName = True, shortName = True)
        if scene_name:
            scene_name = os.path.splitext(scene_name)[0]
        else:
            scene_name = "untitled"
    
        return scene_name
    
    def to_number(self, text):
        return ''.join(filter(str.isdigit, text))
        
    def get_scene_camera(self):
        scene = self.get_scene_name()
        scene_parts = scene.split('_')
        
        if len(scene_parts) > 4:
            scene_name = "{}_{}_{}".format(self.to_number(scene_parts[1]), self.to_number(scene_parts[3]), self.to_number(scene_parts[4]))
            
            cameras = cmds.ls(type = 'camera')
            
            for c in cameras:
                camera_parts = c.split('_')
                if len(camera_parts) >= 4:
                    camera_name = "{}_{}_{}".format(self.to_number(camera_parts[1]), self.to_number(camera_parts[2]), self.to_number(camera_parts[3]))
                    
                    if camera_name == scene_name:
                        return c
        return None        

    def get_working_file(self):
        return cmds.file(q=True, sn=True)

    def set_image_plane(self):
        '''
        select -r witw_ep101_seq010_sh010_cam ;
        setAttr "imagePlaneShape1.useFrameExtension" 1;
        setAttr "witw_ep101_seq010_sh010_camShape->imagePlaneShape1.alphaGain" 0.5;
        setAttr "witw_ep101_seq010_sh010_camShape->imagePlaneShape1.sizeX" 0.5;
        setAttr "witw_ep101_seq010_sh010_camShape->imagePlaneShape1.offsetX" 0.46;
        setAttr "witw_ep101_seq010_sh010_camShape->imagePlaneShape1.offsetY" 0.26;
        
        select -r witw_ep101_seq010_sh020_cam ;
        setAttr "imagePlaneShape2.useFrameExtension" 1;
        setAttr "witw_ep101_seq010_sh020_camShape->imagePlaneShape2.alphaGain" 0.5;
        setAttr "witw_ep101_seq010_sh020_camShape->imagePlaneShape2.sizeX" 0.5;
        setAttr "witw_ep101_seq010_sh020_camShape->imagePlaneShape2.offsetX" 0.46;
        setAttr "witw_ep101_seq010_sh020_camShape->imagePlaneShape2.offsetY" 0.26;
        
        '''
        pass

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
            sound_node = mel.eval("timeControl -q -sound $gPlayBackSlider;")
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

    ########################################################################################
    #Derik's added functions
    def get_shot_name_from_scene_name(self):
        scene_name = self.get_scene_name()
        scene_name_split = scene_name.split('_')
        length = len(scene_name_split)
        count = 0
        name = ['']
        while count < length:

            name.append(scene_name_split[count])   
            count = count + 1    
        
        proj = name[1]
        ep = name[2]
        scene = name[3]
        shot = name[4]

        return(proj, ep, scene, shot)

    def set_evaluation_mode(self, evaluation_mode): #("off" = DG ,  "serial", "serialUncached" and "parallel")
        cmds.evaluationManager( mode= evaluation_mode )


    def get_scene_framerange(self):
        timeline_start = cmds.playbackOptions(q = True, ast = True)
        timeline_end = cmds.playbackOptions(q = True, aet = True)
        playback_start = cmds.playbackOptions(q = True, min = True)
        playback_end = cmds.playbackOptions(q = True, max = True)
    
        return timeline_start, timeline_end, playback_start, playback_end 

    def unlock_attributes(self, transform):
        attrs = cmds.listAttr(transform, visible = True)
        if attrs:
            for attr in attrs:
                try:
                    cmds.setAttr(transform + "." + attr, lock = 0)
                except:
                    pass
                    #self.log_output(transform + "." + attr + "could not be set")

    def make_attr_keyable(self, transform):
        attrs = cmds.listAttr(transform, visible = True)
        if attrs:
            for attr in attrs:
                try:
                    cmds.setAttr(transform + "." + attr, keyable = 1)
                except:
                    pass
                    #self.log_output(transform + "." + attr + "could not be set")
        
    def check_referenced_anim_curve_lockstate(self):
        is_ref_files_locked = cmds.optionVar(q = 'refLockEditable')
        return is_ref_files_locked

    def unlock_referenced_anim_curves(self):
        cmds.optionVar( iv=('refLockEditable', True))

    def lock_referenced_anim_curves(self):
        cmds.optionVar( iv=('refLockEditable', False))
        
    def bake_hierarchy_to_keys(self, object, bake_shape, startframe, endframe):
        cmds.bakeResults(object, hi = 'below', simulation = True, t = (startframe,endframe), shape = False, sampleBy = 1, oversamplingRate = 1, disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = False)
    
    def import_references(self):
        all_ref_paths = cmds.file(q=True, reference=True) or []  # Get a list of all top-level references in the scene.

        for ref_path in all_ref_paths:
            if cmds.referenceQuery(ref_path, isLoaded=True):  # Only import it if it's loaded, otherwise it would throw an error.
                cmds.file(ref_path, importReference=True)  # Import the reference.

                new_ref_paths = cmds.file(q=True, reference=True)  # If the reference had any nested references they will now become top-level references, so recollect them.
                if new_ref_paths:
                    for new_ref_path in new_ref_paths:
                        if new_ref_path not in all_ref_paths:  # Only add on ones that we don't already have.
                            all_ref_paths.append(new_ref_path)

    #End of Derik's added functions
    ########################################################################################

    '''
        Get a list of all shots from the camera sequencer
    '''
    def get_shot_list(self):
        self.log_output("get_shot_list")

        shots = []
        shot_list = cmds.ls(type = "shot")

        for item in shot_list:
            shot = {}
            shot["id"] = item
            shot["name"] = cmds.shot(item, q=True, shotName = True)
            shot["frame_in"] = int(cmds.shot(item, q=True, st = True))
            shot["frame_out"] = int(cmds.shot(item, q=True, et = True))
            shot["start"] = int(cmds.shot(item, q=True, sst = True))
            shot["end"] = int(cmds.shot(item, q=True, set = True))
            shot["audio"] = cmds.shot(item, q=True, aud = True)

            if shot["audio"]:
                shot["audio_file"] = cmds.getAttr("{}.filename".format(shot["audio"]))
            else:
                shot["audio_file"] = None

            shots.append(shot)

        shots = sorted(shots, key = lambda d: d['frame_in'])
        #for item in shots:
        #    self.log_output("Added shot {} {} {} {}".format(item["name"], item["frame_in"], item["frame_out"], item["audio_file"]))

        ##self.shots = cmds.ls(type="shot")
        ##self.shots = sorted(self.shots)
        ##for s in self.shots:
        ##    self._playblast.log_output("shot {}".format(s))

        return shots

    def chainsaw_panel(self, csv_filename):
        self.log_output("chainsaw: exporting {}, csv: {}, path: ".format(self.get_scene_name(), csv_filename, self.get_scene_path()))
        try:
            break_out_dir = "{}/breakout".format(self.get_scene_path())

            if not os.path.exists(break_out_dir):
                os.makedirs(break_out_dir, mode=0o777, exist_ok=False)

            all_shots = cmds.ls(type="shot")

            self.log_output("chainsaw: found {} shots".format(len(all_shots)))

            with open("{}/{}".format(break_out_dir, csv_filename), 'w') as csv_file:
                writer = csv.writer(csv_file)            
                try:
                    for shot_name in all_shots:
                        self.log_output("chainsaw: processing {} ".format(shot_name))

                        shot_start = cmds.getAttr(shot_name + ".startFrame")
                        shot_end = cmds.getAttr(shot_name + ".endFrame")
                        shot_cam = cmds.listConnections(shot_name + ".currentCamera")         

                        # only interested in the first camera for the shot
                        if len(shot_cam) >= 1:
                            shot_cam = shot_cam[0]

                        self.log_output("chainsaw: shot_cam {} ".format(shot_cam))  
                        ## self.set_active_camera(shot_cam)                          

                        cmds.playbackOptions(animationStartTime=shot_start, minTime=shot_start, animationEndTime=shot_end, maxTime=shot_end)
                        ## cmds.lookThru(shot_cam)
                        cmds.currentTime(shot_start)                

                        shot_file_name = "{}/{}.ma".format(break_out_dir, shot_name)

                        self.log_output("chainsaw: processing {} -> {}".format(shot_name, shot_file_name))

                        cmds.file(rn = shot_file_name)
                        cmds.file(save=True, type='mayaAscii')                    

                        writer.writerow([shot_name, shot_start, shot_end, shot_cam])

                    return break_out_dir
                finally:
                    csv_file.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.log_error("chainsaw error: args {}".format(csv_filename))               

        return False


    #
    #
    # Exports the scene in layout format
    #
    # Source: Chainsaw002.py
    # Author: Miruna D. Mateescu
    # Last Modified: 2021/04/05
    #
    def chainsaw(self, csv_filename):
        self.log_output("chainsaw: exporting {}, csv: {}".format(self.get_scene_name(), csv_filename))
        try:
            break_out_dir = "{}/breakout".format(self.get_scene_path())

            if not os.path.exists(break_out_dir):
                os.makedirs(break_out_dir, mode=0o777, exist_ok=False)

            all_shots = cmds.ls(type="shot")

            self.log_output("chainsaw: found {} shots".format(len(all_shots)))
            with open("{}/{}".format(break_out_dir, csv_filename), 'w') as csv_file:
                writer = csv.writer(csv_file)            
                try:
                    for shot_name in all_shots:
                        self.log_output("chainsaw: processing {} ".format(shot_name))

                        shot_start = cmds.getAttr(shot_name + ".startFrame")
                        shot_end = cmds.getAttr(shot_name + ".endFrame")
                        shot_cam = cmds.listConnections(shot_name + ".currentCamera")         

                        # only interested in the first camera for the shot
                        if len(shot_cam) >= 1:
                            shot_cam = shot_cam[0]

                        self.log_output("chainsaw: shot_cam {} ".format(shot_cam))  
                        ## self.set_active_camera(shot_cam)                          

                        cmds.playbackOptions(animationStartTime=shot_start, minTime=shot_start, animationEndTime=shot_end, maxTime=shot_end)
                        cmds.lookThru(shot_cam)
                        cmds.currentTime(shot_start)                

                        shot_file_name = "{}/{}.ma".format(break_out_dir, shot_name)

                        self.log_output("chainsaw: processing {} -> {}".format(shot_name, shot_file_name))

                        cmds.file(rn = shot_file_name)
                        cmds.file(save=True, type='mayaAscii')                    

                        writer.writerow([shot_name, shot_start, shot_end, shot_cam])

                    return True
                finally:
                    csv_file.close()
        except:
            traceback.print_exc(file=sys.stdout)
            self.log_error("chainsaw error: args {}".format(csv_filename))               

        return False

    '''
        Derik vd Berg
        Prepares layout scene for anim
        - Remove unused cameras
        - Sets start and End of Shots
        - Shifts keys to frame 0 and removes out of shot keys

        - Assumes file name, shot name and camera name matches
        i.e. 
            file name: witw_ep101_seq010_sh010.ma
            shot name: witw_ep101_seq010_sh010
            camera name: witw_ep101_seq010_sh010_cam

    '''
    def anim_prep(self):
        filename = cmds.file(q=True, sn=True, shn=True)

        self.log_output("anim_prep: processing {}".format(filename))

        all_shots = cmds.ls(type = 'shot')
        self.log_output("anim_prep: found {} shots".format(len(all_shots)))

        shot_name, extension = os.path.splitext(filename)
        self.log_output("anim_prep: searching for camera for shot '{}'".format(shot_name))
        
        # delete unused cameras
        cameras = cmds.ls(type = 'camera')
        for cam in cameras:
            if cam in [ "frontShape", "perspShape", "sideShape", "topShape"]:
                self.log_output("Keeping cam {}".format(cam))
                continue

            cam_trans = cmds.shot(shot_name, q=True, cc=True)
            #seqcamtype = cmds.nodeType(seqcam)

            #if seqcamtype == 'camera':
            #    cam_trans = cmds.listRelatives(seqcam,type='transform',p=True)

            cam_trans = cmds.listRelatives(cam, f = True, p = True)
            self.log_output("anim_prep::checking if {} is in {}".format(shot_name, cam_trans))

            if str(shot_name) in str(cam_trans):
                self.log_output("anim_prep::keeping camera for shot '{}'".format(cam_trans))
                continue
            else:
                self.log_output("anim_prep::removing cam trans {}".format(cam_trans))

            ##print(cam_trans)
            cmds.delete(cam_trans)    
            self.log_output("anim_prep::removed cam '{}'".format(cam_trans))

        # delete unused sequencer shot nodes    
        for cur_shot in all_shots:
            if cur_shot != shot_name:
                cmds.lockNode(cur_shot, lock=False)                
                cmds.delete(cur_shot)
                self.log_output("anim_prep::removed shot '{}'".format(cur_shot))

        start = cmds.getAttr(shot_name + '.startFrame')
        end = cmds.getAttr(shot_name + '.endFrame')
        
        animCurves = cmds.ls(type = 'animCurve')
        allAnimCurves = cmds.ls(type = 'animCurve')

        cmds.select(clear = True) 

        animCurves = []
        for curveNode in allAnimCurves:
            if cmds.referenceQuery(curveNode, isNodeReferenced = True):
                pass
            else:
                animCurves.append(curveNode)

        for animCurve in animCurves:
            if 'lensCurve' in str(animCurve):
                pass
            else:
                cmds.select(animCurve, add = True)
        #Unlock graph editor keys
        mel.eval('GraphEditorUnlockChannel;')    
        #Key start and end of shot    
        cmds.currentTime(start)
        cmds.setKeyframe()
        cmds.currentTime(end)
        cmds.setKeyframe()
        cmds.currentTime(start-1)
        cmds.setKeyframe()
        cmds.currentTime(end+1)
        cmds.setKeyframe()
        self.log_output("Keyed start {} and end {}".format(start, end))
        
        # shift Keys to frame 0
        keys = cmds.ls(sl = True)
        for key in keys:
            cmds.select(key, r = True)
            cmds.selectKey(key, add = True, k = True)
            mel.eval('GraphEditorUnlockChannel;')
            con = cmds.listConnections(key) 
            if con == None:
                pass
            else:
                try:
                    cmds.keyframe(edit=True, iub=False, an = 'objects', o = 'move', fc = 0, relative=True, timeChange=-(start),time=((-500),(5000000)))
                    # self.log_output("Moved key {} {}".format(key, start))
                except:
                    print('I didn not move :{}'.format(key))

        #cmds.keyframe(edit=True, iub=False, an = 'objects', o = 'move', fc = 0, relative=True, timeChange=-(start),time=((-500),(5000000)))
        cmds.playbackOptions(animationStartTime=0, minTime=0, animationEndTime=(end - start), maxTime=(end - start))
        self.log_output("Shifted keys to origin: animationStartTime={} minTime={} animationEndTime={} maxtime={}".format(0, 0, (end - start), (end - start)))

        #delete keys outside shot range
        cmds.select(keys,r = True)
        
        frontcut_start = -5000
        frontcut_end = -2
        backcut_start = end - start + 2
        backcut_end = 10000000

        cmds.cutKey(time=(frontcut_start,frontcut_end), clear = True)
        cmds.cutKey(time=(backcut_start,backcut_end), clear = True)
        self.log_output("Removed keys out of bounds")

        #Delete current shot sequencer node    
        cmds.lockNode(shot_name, lock=False)               
        cmds.delete(shot_name)
        self.log_output("Removed sequencer node")

        try:
            self.removeHiddenReferences()
        except:
            self.log_output("anim_prep: error removing hidden references")        

        #Save file    
        cmds.file(save = True, type='mayaAscii') 
        self.log_output("Saved scene")       


    def removeHiddenReferences(self):
        cmds.currentTime(0, edit=True )
        rootNodes = cmds.ls(assemblies = True)
        self.log_output("removeHiddenReferences::Scanning root nodes: {}".format(rootNodes))

        for rootNode in rootNodes:
            if cmds.referenceQuery( rootNode, isNodeReferenced = True):
                vis = cmds.getAttr(rootNode + '.visibility')
                if vis:
                    pass
                else:
                    is_hiddenoutliner = cmds.getAttr(rootNode + ".hiddenInOutliner")
                    if is_hiddenoutliner:
                        pass
                    else:
                        refNode = cmds.referenceQuery(rootNode, referenceNode = True)
                        try:
                            cmds.file(removeReference = True, referenceNode = refNode)
                            self.log_output("removeHiddenReferences::Removed: {}".format(refNode))
                        except:
                            self.log_output("removeHiddenReferences::{} - Could not remove reference. hierarchy might be dirty".format(rootNode))
        
            else:
                children = cmds.listRelatives( rootNode, fullPath = True, c=True)
                if children:
                    self.log_output("Processing {}".format(children))

                    for child in children:
                        if rootNode == 'ENVIRONMENT':
                            pass
                        else:
                            if cmds.referenceQuery(child, isNodeReferenced = True):
                                vis = cmds.getAttr(child + '.visibility')
                                if vis:
                                    pass
                                else:
                                    refNode = cmds.referenceQuery(child, referenceNode = True)
                                    try:
                                        cmds.file(removeReference = True, referenceNode = refNode)
                                        self.log_output("removeHiddenReferences::Removed: {}".format(refNode))
                                    except:
                                        self.log_output("removeHiddenReferences::{} Could not remove reference. hierarchy might be dirty".format(child))

        fosterparents = cmds.ls(type = 'fosterParent')
        if fosterparents:
            for fp in fosterparents:
                cmds.delete(fp)      
                self.log_output("removeHiddenReferences::Removed fosterParent: {}".format(fp))

    # Mandi Matakovic / 2022-09-14
    # grab latest model file in directory
    def import_latest(self, asset_path):
        fileType = r".ma"
        file = glob.glob(r"{}/*{}".format(asset_path, fileType)) #filepath and extention
        latestFile = max(file, key=os.path.getctime) #look for the latest file

        cmds.file(latestFile, i=True, mergeNamespacesOnClash=True, namespace=':') #import the file

        print('----------------------------------')
        print('imported:')
        print(latestFile)
        print('----------------------------------')        


        
                                


