import maya.cmds as mc
from wildchildanimation.gui.settings import SwingSettings

from wildchildanimation.maya.maya_shelf import _shelf

class SwingShelf(_shelf):

    _run_swing = '''
import wildchildanimation.studio_interface
import wildchildanimation.maya_handlers
handler = wildchildanimation.maya_handlers.StudioHandler()
wildchildanimation.SwingGUI.show_dialog(handler)
    '''

    _playblast = '''
import wildchildanimation.studio_interface
import wildchildanimation.maya_handlers
swing_playblast_dialog = wildchildanimation.gui.swing_playblast.SwingPlayblastUi()
swing_playblast_dialog.show()
    '''    

    def __init__(self, controller, name, iconPath):
        super().__init__(controller=controller, name=name, iconPath=iconPath)

    def build(self):
        self.addButon(label="Swing", icon = "swing_assets.png", command = SwingShelf._run_swing)
        self.addButon(label="PB", icon = "swing_pb.png", command = SwingShelf._playblast)

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