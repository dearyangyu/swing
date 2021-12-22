import json

import os
import maya.cmds as cmds

class SceneData(object):

    def __init__(self):
        super(SceneData, self).__init__()

        self.scene_descriptor = json.loads("{}")

    def get_scene_path(self):
        return os.path.dirname(self.get_scene_name())

    def get_scene_name(self):
        scene_name = cmds.file(q=True, sn=True)
        return scene_name

    def load_scene_descriptor(self):
        working_folder = self.get_scene_path()
        if os.path.exists(working_folder):
            file_name = os.path.basename(self.get_scene_name())
            fn, ext = os.path.splitext(file_name)

            scene_descriptor = os.path.join(working_folder, "{}-swing.json".format(fn))

            if os.path.exists(scene_descriptor):
                with open(scene_descriptor) as json_file:
                    try:
                        self.scene_descriptor = json.load(json_file)
                        print("Loaded Scene Descriptor {}".format(scene_descriptor))
                        return True

                    finally:
                        json_file.close()
            return False

    def save_scene_descriptor(self):
        working_folder = self.get_scene_path()
        if os.path.exists(working_folder):
            file_name = os.path.basename(self.get_scene_name())
            fn, ext = os.path.splitext(file_name)

            scene_descriptor = os.path.join(working_folder, "{}-swing.json".format(fn))
            with open(scene_descriptor, 'w') as json_file:
                try:
                    json.dump(self.scene_descriptor, json_file)
                    print("Saved Scene Descriptor {}".format(scene_descriptor))
                    return True

                finally:
                    json_file.close()
        return False

    def save_task_data(self, task):
        self.scene_descriptor["project_id"] = task["project_id"]
        
        if "episode" in task:
            self.scene_descriptor["episode_id"] = task["episode"]["id"]
        else:
            self.scene_descriptor["episode_id"] = "All"

        self.scene_descriptor["task_id"] = task["id"]

        self.save_scene_descriptor()

    def load_task_data(self):
        if not self.load_scene_descriptor():
            print("No scene data to load")
            return False

        project_id = self.scene_descriptor["project_id"]
        episode_id = self.scene_descriptor["episode_id"]
        task_id = self.scene_descriptor["task_id"]

        return project_id, episode_id, task_id

                

