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

#
# Enable PyQT5 fix for Mac Big Sur / 
os.environ['QT_MAC_WANTS_LAYER'] = '1'

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

def fusion_dark_style(app):
    try:
        from PySide2.QtCore import Qt
        from PySide2.QtGui import QPalette, QColor

        # Force the style to be the same on all OSs:
        app.setStyle("Fusion")

        # Now use a palette to switch to dark colors:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
    except:
        print("Error loading fusion dark style, reverting to default")

    return app    

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
        if qtMode == 0:
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))
        elif qtMode == 1:
            app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))        
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet())
    
    SwingGUI.show_dialog(SwingStudioHandler())
    sys.exit(app.exec_())


