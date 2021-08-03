'''
    Set to folder containing module/ and plugin/
'''
WCA_ROOT = "C:/wca/env/Lib/site-packages/"
import sys

sys.path.append("{0}".format(WCA_ROOT))
from PyQt5.QtWidgets import QApplication, QWidget
from wildchildanimation.gui.swing_gui import SwingGUI

# studio specific import callbacks 
#sys.path.append("{0}/{1}".format(WCA_ROOT, "/plugin/treehouse"))
#from maya_handlers import StudioHandler

SwingGUI.show_dialog(None)

if __name__ == '__main__':
    houdini_handler = None
    SwingGUI.show_dialog(houdini_handler)
# entry point    
