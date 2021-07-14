'''
    Set to folder containing module/ and plugin/
'''
WCA_ROOT = "C:/WCA/wca-maya-main"

import sys
sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))

# Load Zurbrigg Playblaster
from wildchildanimation.gui.swing_playblast import ZurbriggPlayblastUi
SwingPlayblastUi.show_dialog()



# Swing
import sys

import PySide2.QtWidgets
import PySide2.QtGui
from PySide2.QtWidgets import QApplication, QWidget

sys.path.append("Z:/env/maya/treehouse/wca-maya/module")
from wildchildanimation.swing_gui import SwingGUI

sys.path.append("Z:/env/maya/treehouse/wca-maya/plugin/treehouse")
# studio specific import callbacks 
from maya_handlers import StudioHandler
handler = StudioHandler()    

if __name__ == '__main__':
#    app = QApplication(sys.argv)
    SwingGUI.show_dialog(handler)
    ex = SwingGUI(handler)
    ex.show()
    sys.exit(app.exec_())
else:
    ex = SwingGUI(handler)
# entry point    