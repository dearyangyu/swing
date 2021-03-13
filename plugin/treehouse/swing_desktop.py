'''
    Set to folder containing module/ and plugin/
'''

# WCA_ROOT = "Z:/env/maya/treehouse/wca-maya/"
WCA_ROOT = "C:/DEV/Github/wca-maya"

import sys

sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))
from wildchildanimation.swing_gui import SwingGUI

# studio specific import callbacks 
sys.path.append("{0}/{1}".format(WCA_ROOT, "/plugin/treehouse"))
from maya_handlers import StudioHandler

import PySide2.QtWidgets
import PySide2.QtGui
from PySide2.QtWidgets import QApplication, QWidget

# studio specific import callbacks 
#from maya_handlers import StudioHandler
# handler = StudioHandler()    
handler = None

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = SwingGUI(handler)
    ex.show()
    sys.exit(app.exec_())
else:
    ex = SwingGUI(handler)
# entry point    