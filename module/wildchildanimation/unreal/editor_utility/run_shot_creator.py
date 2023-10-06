## Run from within Unreal Editor
##
import sys
from PySide2 import QtWidgets

from wildchildanimation.gui.swing_gui import SwingGUI
from wildchildanimation.studio.unreal_studio_handler import UnrealStudioHandler

import unreal

def dark_style(app):
    try:
        from PySide2.QtCore import Qt
        from PySide2.QtWidgets import QApplication
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
        print("Error loading dark style, reverting to default")

    return app

window = None # Required to be a global variable due to Unreals garbage collector
def main():
    app = None

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    app = dark_style(app)

    global window

    window = SwingGUI(studio_handler = UnrealStudioHandler())

    unreal.parent_external_window_to_slate(window.winId())
    window.handler.on_create_shots()

if __name__ == "__main__":
    main()
