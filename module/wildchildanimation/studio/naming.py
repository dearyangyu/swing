# -*- coding: utf-8 -*-
import sys
import os, pathlib
import traceback

# Need Qt for Settings
# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)
    from PyQt5 import QtCore
    qtMode = 1

# gazu for lookups
import gazu

# Utils
from wildchildanimation.swing_gui import _APP_NAME
from wildchildanimation.gui.swing_utils import connect_to_server, load_settings, load_keyring

class StudioNaming:

    def __init__(self) -> None:
        QtCore.QCoreApplication.setOrganizationName("Wild Child Animation")
        QtCore.QCoreApplication.setOrganizationDomain("wildchildanimation.com")
        QtCore.QCoreApplication.setApplicationName(_APP_NAME)

        self.email = load_settings('user', 'user@example.com')
        self.password = load_keyring('swing', 'password', 'Not A Password')        
        self.g = None

    def get_gazu(self):
        if self.g == None:
            connect_to_server(self.email, self.password)
            self.g = gazu
        return self.g

    def resolve_path(self, resource_name):
        resource_path = pathlib.Path(resource_name)
        file_name = resource_path.name
        types = file_name.split("_")

        if len(types) < 4:        
            print("Error: could not split filename {} into at least 4 parts using '_'".format(file_name))
            return None

        if len(types) >= 4:
            pro = types[0]
            typ = types[1]
            ent = types[2]
            dep = types[3]

            entity = self.get_gazu().entity.get_entity_by_name(ent)

            if not entity:
                print("Error: Entity {} not found".format(ent))
                return None

            files = self.get_gazu().files.get_all_working_files_for_entity(entity)
            for f in files:
                if f["name"] == file_name:
                    return pathlib.Path("{}/{}".format(f["path"], f['name'])).as_posix()

        return None

if __name__ == '__main__':
    _TEST_DATA = [
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/dillydally_teddy/render/hby_chr_dillyteddy_assembly_v000.ma",
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/dillydally/render/hby_chr_dillydally_assembly_render_v000.ma",
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/rocket/hby_prp_rocket_assembly_v000.ma", 
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/moon/hby_chr_moon_assembly_v000.ma", 
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/stars/render/hby_chr_star1_assembly_v000.ma", 
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/stars/render/hby_chr_star2_assembly_v000.ma", 
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/stars/render/hby_chr_star3_assembly_v000.ma", 
        "Z:/productions/hushabye_s02/hsb2_build/assets/assembly/dillydally_teddy/render/hby_chr_dillyteddy_assembly_v000.ma"         
    ]

    naming = StudioNaming()
    for ref_item in _TEST_DATA:
        item = pathlib.Path(ref_item)
        path = naming.resolve_path(item.name)
        if path:
            print("{} points to {}".format(item.name, path)) 
        else:
            print("Error: File not found {}".format(item.name))
