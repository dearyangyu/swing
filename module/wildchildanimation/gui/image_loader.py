# -*- coding: utf-8 -*-

from __future__ import print_function
import traceback
import sys
import os
import requests
import gazu
import tempfile

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

    def __init__(self, parent, preview_file):
        super(PreviewImageLoader, self).__init__(self, parent)

        self.parent = parent
        self.password = load_keyring('swing', 'password', 'Not A Password')
        self.server = load_settings('server', 'https://example.wildchildanimation.com')
        self.email = load_settings('user', 'user@example.com')            

        self.preview_file = preview_file

        self.callback = ImageLoaderSignal()

    def run(self):
        fp = tempfile.mkstemp(".{0}".format(self.preview_file["extension"]))
        target = fp[1]
        gazu.files.download_preview_file_thumbnail(self.preview_file, target)

        pixmap = QtGui.QPixmap(target)
        self.callback.results.emit(pixmap)

        return pixmap