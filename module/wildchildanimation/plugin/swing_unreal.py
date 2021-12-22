import sys

from PySide2 import QtGui
from PySide2 import QtWidgets

import qdarkstyle
from wildchildanimation.gui.swing_gui import SwingGUI
from wildchildanimation.studio.unreal_studio_handler import UnrealStudioHandler

import unreal


app = None
if not QtWidgets.QApplication.instance():
    app = QtWidgets.QApplication(sys.argv)
else:
    app = QtWidgets.QApplication.instance()

app.setStyleSheet(qdarkstyle.load_stylesheet())

dlg_instance = SwingGUI(studio_handler = UnrealStudioHandler())
dlg_instance.show()
unreal.parent_external_window_to_slate(dlg_instance.winId())