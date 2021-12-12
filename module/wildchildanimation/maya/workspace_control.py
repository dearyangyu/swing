# -*- coding: utf-8 -*-
# Maya Widget control for Treehouse: Swing
#
import sys

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import getCppPointer

    qtMode = 0
except ImportError:

    from PyQt5 import QtCore, QtWidgets
    import sip
    qtMode = 1

class WorkspaceControl(object):

    def log_output(self, text):
        om.MGlobal.displayInfo(text)

    def __init__(self, name):
        self.name = name
        self.widget = None

    def create(self, label, widget, ui_script):
        cmds.workspaceControl(self.name, label = label)
        if ui_script:
            cmds.workspaceControl(self.name, e=True, uiScript=ui_script)

        self.add_widget_to_layout(widget)
        self.set_visible(True)

    def restore(self, widget):
        self.add_widget_to_layout(widget)

    def exists(self):
        return cmds.workspaceControl(self.name, q=True, exists=True)

    def is_visible(self):
        return cmds.workspaceControl(self.name, q=True, visible=True)

    def set_visible(self, visible):
        if visible:
            cmds.workspaceControl(self.name, e=True, restore=True)
        else:
            cmds.workspaceControl(self.name, e=True, visible=True)

    def set_label(self, label):
        cmds.workspaceControl(self.name, label=label)

    def is_floating(self):
        return cmds.workspaceControl(self.name, q=True, floating=True)

    def is_collapsed(self):
        return cmds.workspaceControl(self.name, q=True, collapse=True)

    def add_widget_to_layout(self, widget):
        print("Add_widget_to_layout")
        if widget:
            print("Add_widget_to_layout: widget found")
            self.widget = widget
            self.widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)

            # python 3
            workspace_control_ptr = int(omui.MQtUtil.findControl(self.name))
            print("Add_widget_to_layout: widget found: {}".format(self.name))

            widget_ptr = int(getCppPointer(self.widget)[0])
            print("Add_widget_to_layout: widget found: {}".format(widget_ptr))

            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)
            print("Add_widget_to_layout: Added widget to maya layout")

    def add_widget_to_layout1(self, widget):
        if widget:
            self.widget = widget
            self.widget.setAttribute(QtCore.Qt.WA_DontCreateNativeAncestors)

            # python 3
            if sys.version_info.major >= 3:
                workspace_control_ptr = int(omui.MQtUtil.findControl(self.name))
                widget_ptr = int(getCppPointer(self.widget)[0])
            else:
                workspace_control_ptr = long(omui.MQtUtil.findControl(self.name))
                widget_ptr = long(getCppPointer(self.widget)[0])

            omui.MQtUtil.addWidgetToMayaLayout(widget_ptr, workspace_control_ptr)


if __name__ == "__main__":
    workspace_control_name = "SwingWorkspaceControl"
    if cmds.window(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name)

    # Create the main window
    workspace_control = WorkspaceControl(workspace_control_name)
    workspace_control.create(workspace_control_name, QtWidgets.QPushButton("Swing!"))
    workspace_control.set_label("SwingWorkspaceControl")