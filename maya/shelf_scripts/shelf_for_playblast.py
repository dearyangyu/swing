import sys

WCA_MAYA = "Z://env//wca//lib//maya_2020"
WCA_ROOT = "Z://env//wca//swing//swing-main//module"

if not any('wca' in p for p in sys.path):
    sys.path.append(WCA_MAYA)
    sys.path.append(WCA_ROOT)    
    
import wildchildanimation.maya.swing_maya
import wildchildanimation.maya
from wildchildanimation.maya.maya_swing_control import *
from wildchildanimation.gui.swing_playblast import SwingPlayblastUi

dialog = SwingPlayblastUi()
dialog.show()
