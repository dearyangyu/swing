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

if __name__ == "__main__":
    try:
        swing_gui.close() # pylint: disable=E0601
        swing_gui.deleteLater()
    except:
        pass

    app = QApplication(sys.argv)

    swing_gui = SwingGUI()
    swing_gui.show()
    swing_gui.breakout_dialog()

    sys.exit(app.exec_())


