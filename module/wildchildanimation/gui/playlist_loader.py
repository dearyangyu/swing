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

class PlaylistLoaderSignal(QtCore.QObject):

    # setting up custom signal
    results = pyqtSignal(object)        

class PlaylistLoader(QtCore.QRunnable):

    def __init__(self, parent, project, episode):
        super(PlaylistLoader, self).__init__(self, parent)

        self.parent = parent
        self.password = load_keyring('swing', 'password', 'Not A Password')
        self.server = load_settings('server', 'https://production.wildchildanimation.com')
        self.email = load_settings('user', 'user@example.com')            

        self.project = project
        self.episode = episode

        self.callback = PlaylistLoaderSignal()

    def run(self):
        playlists = gazu.playlist.all_playlists_for_project(self.project)

        self.callback.results.emit(playlists)
        return True