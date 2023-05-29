import maya.cmds as mc
import maya.OpenMaya as om

from wildchildanimation.maya.util.abstract_shelf import _shelf

class MayaSwingShelf(_shelf):

    NAME = "MayaSwingShelf"
    VERSION = "1.0.1"

    SHELF_NAME = 'WCA'
    SHELF_ICON_PATH = r'Z:/env/wca/swing/swing-main/module/wildchildanimation/resources'

    COMMAND_PALETTE = [
        {
            "name": "Assets Toolkit",
            "annotation": 'Open Assets Toolkit',
            "type": "python",
            "icon": "toolbar/tools.png",
            "command": '''from wildchildanimation.maya.asset_toolkit.asset_toolkit import AssetToolkitDialog
AssetToolkitDialog().show()'''
        },

        {
            "name": "Playblaster",
            "annotation": 'Open Swing Playblaster',            
            "type": "python",
            "icon": "toolbar/video-outline.png",            
            "command": '''swing_playblast_dialog = wildchildanimation.gui.swing_playblast.SwingPlayblastUi()
swing_playblast_dialog.show()'''
        },

       {
            "name": "SurfnTurf: Clean Rigs",
            "annotation": 'Run SurfnTurf cleaning script on a rig',            
            "type": "python",
            "icon": "toolbar/housekeeping-icon.png",            
            "command": '''from wildchildanimation.scripts.surfnturf_rigging_v006 import SurfnTurf
SurfnTurf().clean_scene()'''
        },

       {
            "name": "SurfnTurf: Clean Model",
            "annotation": 'Run SurfnTurf cleaning script on a model',                        
            "type": "python",
            "icon": "toolbar/sweeper-cleaning-icon.png",                    
            "command": '''from wildchildanimation.scripts.surfnturf_modeling_v006 import SurfnTurf
SurfnTurf().clean_scene()'''
        },     

       {
            "name": "Bulk Rename",
            "annotation": 'Open bulk renamer',             
            "type": "mel",
            "icon": "toolbar/rename.png",                    
            "command": '''source "Z:/env/wca/swing/swing-main/scripts/quick_rename_tool.mel";
Quick_rename_tool();'''
        }, 

       {
            "name": "Export Environment",
            "annotation": 'Package and Export Environment, create JSON and FBX',             
            "type": "python",
            "icon": "toolbar/export.png",                    
            "command": '''
from wildchildanimation.maya.util.maya_asset_export import *
import maya.cmds as cmds

cmds.undoInfo(openChunk = True,undoName = 'prep_scene_for_export')  
      
MayaAssetHandler().export_selected_staticmesh_env()

cmds.undoInfo(closeChunk = True)
cmds.undo('prep_scene_for_export')            
'''
        },  

       {
            "name": "Name Validator",
            "annotation": 'Check naming on textures',                        
            "type": "python",
            "icon": "toolbar/name_validator.png",                    
            "command": '''from wildchildanimation.maya.naming.name_validator import Name_Validator
dialog = Name_Validator()
dialog.exec_()            
'''
        },  

       {
            "name": "Model Checker",
            "annotation": 'Model Checker',                        
            "type": "python",
            "icon": "toolbar/modelChecker.png",                    
            "command": '''from wildchildanimation.maya.modelChecker import modelChecker_UI
modelChecker_UI.UI.show_UI()           
'''
        },          



    ]

    def __init__(self):
        super(MayaSwingShelf, self).__init__(name= self.SHELF_NAME, iconPath=self.SHELF_ICON_PATH)
#        self.log_output("Loading {}".format(self.name))
#        self.build()

    def build(self):
        self.log_output("Build Shelf {}".format(self.name))
        for item in self.COMMAND_PALETTE:
            # self.addButon(label = "label", icon= None, command='', doubleCommand='', width=30, height=30)
            self.addButton(label = item["name"].strip(), icon = item["icon"], command = item["command"].strip(), style="iconOnly", annotation=item["annotation"], type = item["type"])
            self.log_output("Created button: {}".format(item))            

    def log_output(self, text):
        om.MGlobal.displayInfo(text)
        print("[info] {}".format(text))        


# ###################################################################################
# '''This is an example shelf.'''
# # class customShelf(_shelf):
# #     def build(self):
# #         self.addButon(label="button1")
# #         self.addButon("button2")
# #         self.addButon("popup")
# #         p = mc.popupMenu(b=1)
# #         self.addMenuItem(p, "popupMenuItem1")
# #         self.addMenuItem(p, "popupMenuItem2")
# #         sub = self.addSubMenu(p, "subMenuLevel1")
# #         self.addMenuItem(sub, "subMenuLevel1Item1")
# #         sub2 = self.addSubMenu(sub, "subMenuLevel2")
# #         self.addMenuItem(sub2, "subMenuLevel2Item1")
# #         self.addMenuItem(sub2, "subMenuLevel2Item2")
# #         self.addMenuItem(sub, "subMenuLevel1Item2")
# #         self.addMenuItem(p, "popupMenuItem3")
# #         self.addButon("button3")
# # customShelf()
# ###################################################################################