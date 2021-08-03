# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import sys
import os
import requests
import gazu
import tempfile
from wildchildanimation.gui.settings import SwingSettings

# ==== auto Qt load ====
try:
    from PySide2 import QtCore, QtGui
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import pyqtSignal

from wildchildanimation.gui.swing_utils import load_settings, load_keyring

class ImageLoaderSignal(QtCore.QObject):

    # setting up custom signal
    results = pyqtSignal(object)        

class PreviewImageLoader(QtCore.QRunnable):

    def __init__(self, parent, file_id):
        super(PreviewImageLoader, self).__init__(self, parent)
        self.parent = parent

        self.swing_settings = SwingSettings.get_instance()
        self.password = self.swing_settings.swing_password()
        self.server = self.swing_settings.swing_server()
        self.email = self.swing_settings.swing_user()

        self.file_id = file_id
        self.callback = ImageLoaderSignal()

    def run(self):
        preview_file = gazu.files.get_preview_file(self.file_id)

        fp = tempfile.mkstemp(".{0}".format(preview_file["extension"]))
        target = fp[1]
        gazu.files.download_preview_file_thumbnail(preview_file, target)

        pixmap = QtGui.QPixmap(target)
        self.callback.results.emit(pixmap)

        return pixmap