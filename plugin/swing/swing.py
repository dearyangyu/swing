import sys
sys.path.append('C:/Users/wildwrangler/Documents/maya/scripts')

import swing
import maya.cmds as cmds

#from swing import DockableOutliner
# python path
# C:/Users/wildwrangler/Documents/maya/scripts

if __name__ == "__main__":
    workspace_control_name = swing.SwingWorkspaceUI.get_workspace_control_name()
    print(workspace_control_name)
    if cmds.window(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name)
        
    try:
        control.setParent(None)
        control.deleteLater()
    except:
        pass                   
        
    swing.SwingWorkspaceUI.module_name_override = "swing"
    control = swing.SwingWorkspaceUI()
    
    
    
    
    
    