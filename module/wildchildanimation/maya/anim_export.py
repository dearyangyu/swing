from wildchildanimation.maya.swing_maya import SwingMaya
from wildchildanimation.studio.studio_interface import StudioInterface

_maya_loaded = False    
try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.utils as mutils    

    import pymel.core as pm
    from pymel.util import putEnv

    from PySide2 import QtWidgets   
    import shiboken2 as shiboken 

    _maya_loaded = True
except:
    pass

class SwingAnimExport(SwingMaya, StudioInterface):

    NAME = "SwingAnimExport"
    VERSION = "0.0.7"

    def __init__(self):
        super(SwingAnimExport, self).__init__()
        self.log_output("{} v{}".format(self.NAME, self.VERSION))    
