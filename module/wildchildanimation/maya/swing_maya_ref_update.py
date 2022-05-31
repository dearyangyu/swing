# -*- coding: utf-8 -*-
import traceback
import sys
import os
import gazu
import ntpath

from wildchildanimation.maya.swing_maya_ref_table import RefTableDialog
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.background_workers import WorkingFileGetLatestLoader
from wildchildanimation.maya.swing_maya import SwingMaya

try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om
    import maya.OpenMayaUI as omui
    _stand_alone = False
    _log_to_maya = True
except:
    _stand_alone = True
    _log_to_maya = False   

class MayaReferenceUpdater(SwingMaya):

    NAME = "MayaReferenceUpdater"
    VERSION = "0.0.3"

    def __init__(self):
        super(MayaReferenceUpdater, self).__init__()

        self.log_output("{} v{}".format(self.NAME, self.VERSION))   

        self.connected = False
        self.gazu_client = None        
        self.swing_settings = SwingSettings.get_instance()

    def connect_to_server(self): 
        if self.connected or self.gazu_client:
            self.gazu_client = None
            self.connected = False

        password = self.swing_settings.swing_password()
        server = self.swing_settings.swing_server()
        email = self.swing_settings.swing_user()

        gazu.set_host("{}/api".format(server))
        try:
            self.gazu_client = gazu.log_in(email, password)    
        except:
            traceback.print_exc(file=sys.stdout)                     

    def load_maya_references(self):
        refs = []
        for ref in pm.listReferences(recursive=False):

            # returns a list of FileReferences
            refs.append(ref) 

        return refs

    def list_reference_updates(self):
        file_list = []
        ref_updates = []

        self.connect_to_server()
        for ref in self.load_maya_references():
            try:
                filename = ntpath.basename(ref.path)
                if not filename in file_list:
                    loader = WorkingFileGetLatestLoader(filename)
                    check_ref = loader.run()

                    if check_ref is None or len(check_ref) == 0:
                        reference = {
                            "ref": ref,
                            "update": None
                        }

                    else:
                        working_file = gazu.files.get_working_file(check_ref[0])
                        reference = {
                            "ref": ref,
                            "update": working_file
                        }

                    if not reference in ref_updates:
                        ref_updates.append(reference)

                    file_list.append(filename)

            except:
                traceback.print_exc(file=sys.stdout)    

        return ref_updates

    def update_references(self, show_gui = True):
        log_file = os.path.join(self.get_scene_path(), "swing_update.log")

        if os.path.exists(log_file) and os.path.isfile(log_file):
            logger = open(log_file, 'a') 
        else:
            logger = open(log_file, 'w')

        try:
            self.log_output("update_references")  

            ref_list = self.list_reference_updates()
            self.log_output("update_references {} refs".format(len(ref_list)))  

            if show_gui:
                self.log_output("update_references: show_gui")  

                # def __init__(self, parent = None, ref_list = []):
                dialog = RefTableDialog(ref_list = ref_list)
                dialog.exec()

                if dialog.status == 'OK':
                    self.log_output("update_references: updating references")  
                    ref_list = dialog.get_selected()
                else:
                    self.log_output("update_references: cancel")  
                    return False

            ## check and update references
            self.log_output("list_reference_updates: open Undo")  
            cmds.undoInfo(state=True, infinity=True)
            try:
                for item in ref_list:
                    if item["update"]:
                        ref_update = os.path.join(item["update"]["path"], item["update"]["name"])
                        ref_update = ref_update.replace("/mnt/content/productions", "Z://productions")

                        ref_target = item["ref"].path

                        self.log_output("Updating {} to {}".format(ref_target, ref_update))

                        try:
                            item["ref"].replaceWith(ref_update)
                            logger.write("{} updated with {}\n".format(ref_target, ref_update))
                        except:
                            traceback.print_exc(file=sys.stdout)                        
                            logger.write("ERROR: Could not update updated {}\n".format(ref_target))
                        
            finally:
                cmds.undoInfo(closeChunk=True)
                self.log_output("update_refs: close Undo")  

            self.log_output("update_refs: done")                  

        finally:
            logger.flush()
            logger.close()

        return True
