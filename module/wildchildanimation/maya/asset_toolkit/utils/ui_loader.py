import traceback
import sys

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

import shiboken2 as shiboken     

import maya.OpenMayaUI as apiUI
from io import StringIO 
import pysideuic
import xml.etree.ElementTree as xml


def get_maya_window():
    
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(int(ptr), QtGui.QMainWindow)
    
    
def load_ui_type(ui_file):
    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}
        
        pysideuic.compileUi(f, o, indent = 0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec(pyc, frame)
        
        #Fetch the base_class and form_class based on their type in the xml form design
        form_class = frame['Ui_{0}'.format(form_class)]
        base_class = eval('QtGui.{0}'.format(widget_class))
        
    return form_class, base_class