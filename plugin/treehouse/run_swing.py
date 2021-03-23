'''
    Set to folder containing module/ and plugin/
'''

#WCA_ROOT = "Z:/env/maya/treehouse/wca-maya/"
#WCA_ROOT = "C:/DEV/github/wca-maya/"
WCA_ROOT = "C:/WCA/wca-maya/"


import sys

sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))
from wildchildanimation.swing_gui import SwingGUI

# studio specific import callbacks 
sys.path.append("{0}/{1}".format(WCA_ROOT, "/plugin/treehouse"))
from maya_handlers import StudioHandler

if __name__ == '__main__':
    SwingGUI.show_dialog(StudioHandler())
# entry point    
