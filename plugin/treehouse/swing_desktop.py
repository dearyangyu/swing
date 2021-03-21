# -*- coding: utf-8 -*-
# Swing Standalone command line runner
#

#
# local import wildchildanimation module by adding to the path
WCA_ROOT = "C:/DEV/github/wca-maya/"

import sys

sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))
from wildchildanimation.swing import SwingGUI
from wildchildanimation.gui.breakout import BreakoutUploadDialog

#
#
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False


# ==== auto Qt load ====
try:
    from PySide2.QtWidgets import QApplication, QWidget    
    qtMode = 0
except ImportError:
    from PyQt5.QtWidgets import QApplication, QWidget
    qtMode = 1

if __name__ == "__main__":
    try:
        swing_gui.close() # pylint: disable=E0601
        swing_gui.deleteLater()
    except:
        pass

    app = QApplication(sys.argv)
    if darkStyle:
        # setup stylesheet
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        # or in new API
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))        

    swing_gui = SwingGUI()
    swing_gui.show()

    sys.exit(app.exec_())


