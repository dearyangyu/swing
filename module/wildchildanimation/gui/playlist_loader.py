# -*- coding: utf-8 -*-

import requests
import gazu
from wildchildanimation.gui.settings import SwingSettings

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5.QtCore import pyqtSignal

class PlaylistLoaderSignal(QtCore.QObject):

    # setting up custom signal
    loaded = pyqtSignal(object)        

class PlaylistLoader(QtCore.QRunnable):

    def __init__(self, parent, project_id, episode_id):
        super(PlaylistLoader, self).__init__(self, parent)

        self.settings = SwingSettings.get_instance()
        self.request_url = "{}/edit/api/episode_shot_list".format(self.settings.swing_server())
        self.project_id = project_id
        self.episode_id = episode_id
        self.callback = PlaylistLoaderSignal()            

    def run(self):
        response = {}

        params = { 
            "username": self.settings.swing_user(),
            "password": self.settings.swing_password(),
            "project_id": self.project_id, 
            "episode_id": self.episode_id,
        }             

        results = []
        rq = requests.post(self.request_url, data = params)

        if rq.status_code == 200:
            results = rq.json()

        project = gazu.project.get_project(self.project_id)

        response["items"] = results
        response["project"] = project

        self.callback.loaded.emit(response)                        
        return results       

