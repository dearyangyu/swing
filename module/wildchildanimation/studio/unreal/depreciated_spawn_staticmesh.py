import unreal

import json
import sys

from PyQt5 import QtWidgets

#localisation
#json_file_path = 'E:/sdmp/mayafiles/CabiMExtA/cache/SDMP_CabinMExtA_Mo_Publ_V05.json'
#asset_path = '/Game/pop/assets/environments/CabinMExtA/components/fbx/'

class UESpawnStatic():

    def load(self):
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(None, caption = "Select json file",  filter = "JSON (*.json);; All Files (*.*)")
        if not (q):
            return None

        return q[0]

    def create_actor_in_world(self, data, asset_path):
        print("UESpawnStatic::create_actor_in_world processing {}".format(asset_path))

        obj_str = ''
        name_str = data['name']
        tx = float(data['tx'])
        ty = float(data['ty'])
        tz = float(data['tz'])
        obj = unreal.load_asset((asset_path + str(data['name']) + '.' + str(data['name'])))
        actor_location = unreal.Vector((tx * 1),(tz * 1),(ty * 1))
        actor_rotation = unreal.Rotator(float(data['rx']),float(data['rz']),float(data['ry']))
        actor_scale = unreal.Vector(float(data['sx']),float(data['sz']),float(data['sy']))
        actor = unreal.EditorLevelLibrary.spawn_actor_from_object(obj, actor_location, actor_rotation)
        actor.set_actor_scale3d(actor_scale)
        actor.set_actor_label(data['fullname'])

        print("UESpawnStatic::create_actor_in_world {}".format(data['fullname']))

    def get_json_file(self):
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()    

        file_name = self.load()
        return(file_name)

    def spawn_static(self):
        json_file = self.get_json_file()
        with open(json_file, 'r') as open_file:
            json_object = json.load(open_file)

        print("UESpawnStatic::Loading {}".format(json_file))

        asset_path = ''
        count = 0
        for obj in json_object:
            if (count == 0):
                print("UESpawnStatic::Reading File Header")
                asset_path = obj['game_path']
            else:    
                self.create_actor_in_world(obj,asset_path)
            count = count + 1

        print("UESpawnStatic::Processed {} records".format(count))
    #open_json_file()