# -*- coding: utf-8 -*-
# 
# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore
    qtMode = 1    

class StudioInterface(QtCore.QObject):

    

    '''
        Naming Lookups
    '''
    # ==== auto Qt load ====
    ASSET_TYPE_LOOKUP = {
        "Camera": "cam",
        "Character": "chr",
        "Environment": "env",
        "Library": "lib",
        "Model": "mod",
        "Prop": "prp",
        "Rig": "rig",
        "Test": "test"
    }

    FRAME_RANGE_PRESETS = [
        "Render",
        "Playback",
        "Animation",
        "Custom"
    ]        

    NAME = "StudioInterface"
    VERSION = "0.0.0"
    SUPPORTED_TYPES = [ ]

    def get_param(self, option, value):
        ### runs a custom value request against the local dcc
        '''
            --- get_param('frame_range', 'Render') ==>

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
        '''        
        pass

    def log_error(self, text):
        ### log error
        return True

    def log_warning(self, text):
        ### log warning
        return True

    def log_output(self, text):
        ### log output
        return True

    def set_globals(self, **kwargs):
        ### set global parameters
        return True

    def list_unresolved(self):
        ### return a json list of unresolved references
        return True

    def import_reference(self, **kwargs):
        # tries to import the file specified in source into the currently open scene
        return True
    
    def load_file(self, **kwargs):
        # tries to import the file specified in source into the currently open scene
        return True

    def on_save(self, **kwargs):
        # return the currently open file
        return True

        '''
        file_path = cmds.file(q = True, sn = True)
        file_base = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(file_base)

        request = {
            "source": file_base,
            "file_path": file_path,
            "file_name": file_name,
            "file_ext": file_ext,            
        }
        return request
        '''

    def on_create(self, **kwargs):
        # create a project file
        pass

    def on_playblast(self, **kwargs):
        # calls local playblast
        pass

    def fbx_export(self, **kwargs):
        # exports to fbx file
        pass
        '''
        source = kwargs["target"]
        working_dir = kwargs["working_dir"]

        self.log_output("calling fbx export {0} {1}".format(source, working_dir))

        target = os.path.join(working_dir, source)
        target = os.path.normpath(target)        

        cmds.FBXExport('-file', target, '-s')
        ##self.log_output("fbx_export", kwargs)
        return True
        '''
