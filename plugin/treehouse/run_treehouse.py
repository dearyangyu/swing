# -*- coding: utf-8 -*-
import traceback
import sys

'''
StudioControl Maya Plugin Interface
v1.0 2020.01.28
  - 

log
v0.0: 
  * 

usage in maya: 
import scatter
scatter.main()
'''
deskMode = 0
qtMode = 0 # 0: PySide2; 1 : PyQt5
try:
    import maya.OpenMayaUI as mui
    import maya.cmds as cmds
except ImportError:
    traceback.print_exc(file=sys.stdout)

    deskMode = 1

# ==== for PyQt5 ====
#from PyQt4 import QtGui,QtCore
#import sip

# ==== for pyside2 ====
#from PySide import QtGui,QtCore
#import shiboken

# ==== auto Qt load ====
try:
    from PySide2 import QtGui, QtCore, QtWidgets
    import QtGui.QMainWindow
    import shiboken
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

import os
parent_path = os.path.join(os.path.dirname(__file__), '..')

sys.path.append("C:\\DEV\\Github\\wca-maya\\module")
from wildchildanimation.treehouse_gui import TreehouseGUI


def main(args):
    parentWin = None
    app = None
    if deskMode == 0:
        if qtMode == 0:
            # ==== for pyside ====
            parentWin = shiboken.wrapInstance(long(mui.MQtUtil.mainWindow()), QtGui.QWidget)
        elif qtMode == 1:
            # ==== for PyQt====
            parentWin = sip.wrapinstance(long(mui.MQtUtil.mainWindow()), QtCore.QObject)
            
    if deskMode == 1:
        app = QtWidgets.QApplication(sys.argv)
    
    # single UI window code, so no more duplicate window instance when run this function
    win = TreehouseGUI(parentWin) # extra note: in Maya () for no parent; (parentWin,0) for extra mode input
    win.show()
    
    if deskMode == 1:
        sys.exit(app.exec_())
    
    return app

if __name__ == '__main__':
    executable = sys.argv[0]
    args = sys.argv[1:]
    main(args)
# entry point    