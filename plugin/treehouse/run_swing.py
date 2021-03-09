'''
    Set to folder containing module/ and plugin/
'''

WCA_ROOT = "Z:/env/maya/treehouse/wca-maya/"

import sys

sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))
from wildchildanimation.swing_gui import SwingGUI

# studio specific import callbacks 
sys.path.append("{0}/{1}".format(WCA_ROOT, "/plugin/treehouse"))
from maya_handlers import StudioHandler

if __name__ == '__main__':
    ex = SwingGUI(StudioHandler())
    ex.show()
# entry point    
