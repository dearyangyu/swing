# -*- coding: utf-8 -*-

import requests
import gazu
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import connect_to_server

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5.QtCore import pyqtSignal

class PlaylistEpisodeLoaderSignal(QtCore.QObject):

    # setting up custom signal
    loaded = pyqtSignal(object)        

class PlaylistEpisodeLoader(QtCore.QRunnable):

    def __init__(self, parent, project_id, episode_id):
        super(PlaylistEpisodeLoader, self).__init__(self, parent)

        self.settings = SwingSettings.get_instance()
        self.request_url = "{}/edit/api/episode_shot_list".format(self.settings.swing_server())
        self.project_id = project_id
        self.episode_id = episode_id
        self.callback = PlaylistEpisodeLoaderSignal()            

    def run(self):
        response = {}

        connect_to_server(self.settings.swing_user(), self.settings.swing_password())

        project = gazu.project.get_project(self.project_id)
        episode = gazu.shot.get_episode(self.episode_id)

        task_types = {}
        for t in gazu.task.all_task_types_for_project(self.project_id):
            task_types[t["id"]] = t

        results = gazu.files.all_output_files_for_entity(episode["id"])
        for item in results:
            item["entity"] = episode
            item["task_type"] = task_types[item["task_type_id"]]
            item["output_file_name"] = item["name"]

        response["items"] = results
        response["project"] = project
        response["episode"] = episode

        self.callback.loaded.emit(response)                        
        return response       
    

if __name__ == "__main__":
    worker =  PlaylistEpisodeLoader(None, "21b6284a-729a-4d40-b032-8fb28265a515", "5c88c458-53f5-4459-a83a-5210a71d150a")
    worker.run()

