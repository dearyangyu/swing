## Run from within Unreal Editor
##
import sys

from PySide2 import QtWidgets

import qdarkstyle
from wildchildanimation.gui.swing_gui import SwingGUI
from wildchildanimation.studio.unreal_studio_handler import UnrealStudioHandler

import unreal

window = None # Required to be a global variable due to Unreals garbage collector
def main():
    app = None

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    app.setStyleSheet(qdarkstyle.load_stylesheet())
    global window

    dlg_instance = SwingGUI(studio_handler = UnrealStudioHandler())

    unreal.parent_external_window_to_slate(dlg_instance.winId())
    dlg_instance.exec_()

if __name__ == "__main__":
    main()