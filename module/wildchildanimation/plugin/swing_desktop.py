# -*- coding: utf-8 -*-
#
# Swing Standalone command line runner
#

#
# Disable InsecureRequestWarning for now
#
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os
import sys

#
# add module root to sys path
module_path = "{}/../../".format(__file__)
module_path = os.path.dirname(os.path.realpath(module_path))
if not module_path in sys.path:
    sys.path.append(module_path)

from wildchildanimation.gui.swing_gui import SwingGUI
from wildchildanimation.studio.swing_studio_handler import SwingStudioHandler
#
#
try:
    import qdarkstyle
    darkStyle = True
except:
    darkStyle = False

# ==== auto Qt load ====
try:
    from PySide2.QtWidgets import QApplication
    qtMode = 0
except ImportError:
    from PyQt5.QtWidgets import QApplication
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
    
    SwingGUI.show_dialog(SwingStudioHandler())
    sys.exit(app.exec_())


