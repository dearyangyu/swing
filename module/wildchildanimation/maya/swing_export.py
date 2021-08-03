# -*- coding: utf-8 -*-
import json
import traceback
import sys
import os

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance    
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtCore, QtWidgets
    from shiboken2 import wrapInstance    
    qtMode = 1

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om
    import maya.OpenMayaUI as omui
    _stand_alone = False
    _log_to_maya = True
except:
    _stand_alone = True
    _log_to_maya = False    

from wildchildanimation.gui.background_workers import EntityTagLoader, TaskFileInfoThread
from wildchildanimation.gui.swing_utils import friendly_string, load_settings, save_settings
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.maya.swing_maya import SwingMaya
from wildchildanimation.maya.swing_export_dialog import Ui_SwingExport

import maya.cmds as cmds

'''
    SwingExport: Exports selection using Swing Tags
    ################################################################################
'''

class SwingExportDialog(QtWidgets.QDialog, Ui_SwingExport):

    working_dir = None

    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = SwingExportDialog()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()


    def __init__(self, parent = None, handler = None, task = None, working_dir = None):
        try:
            if sys.version_info.major < 3:
                maya_main_window = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
            else:
                maya_main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)

            super(SwingExportDialog, self).__init__(maya_main_window)
        except:
            super(SwingExportDialog, self).__init__(parent) # Call the inherited classes __init__ method  

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.create_connections()
        self.read_settings()

        self._swing_export = SwingExport(log_to_maya=_log_to_maya)

        self.handler = handler
        self.task = task
        self.working_dir = working_dir
        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.treeWidget.clear()
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabels(["Option Set"])   

        self.pushButtonExport.clicked.connect(self.process)
        self.pushButtonClose.clicked.connect(self.close_dialog)
        self.load_frame_ranges()

        if self.task:
            task_loader = TaskFileInfoThread(self, self.task, SwingSettings.get_instance().swing_root())
            task_loader.callback.loaded.connect(self.task_loaded)
            self.threadpool.start(task_loader)    

    def set_enabled(self, enabled):
        self.lineEditEntityName.setEnabled(enabled)
        self.lineEditPath.setEnabled(enabled)      
        self.output_dir_path_select_btn.setEnabled(enabled)      
        self.comboBoxAlembicSelection.setEnabled(enabled)      
        self.frame_range_cmb.setEnabled(enabled)      
        self.frame_range_start_sb.setEnabled(enabled)      
        self.frame_range_end_sb.setEnabled(enabled)      
        self.pushButtonExport.setEnabled(enabled)      

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))

        self.settings.endGroup()           
                     
    def log_output(self, text):
        self._swing_export.log_output(text)

    def log_error(self, text):
        self._swing_export.log_error(text)        
        
    def task_loaded(self, results):
        self.task = results["task"]
        self.working_dir = results["project_dir"]

        name = ""
        if "entity_type" in self.task:
            name = '{} {}'.format(name, self.task["entity_type"]["name"])
        else:
            name = '{} {}'.format(name, self.task["entity_type_name"])

        if "entity" in self.task:
            name = '{} {}'.format(name, self.task["entity"]["name"])
        else:
            name = '{} {}'.format(name, self.task["entity_name"])

        if "task_type" in self.task:
            task_type = self.task["task_type"]["name"]
            name = '{} {}'.format(name, self.task["task_type"]["name"])   
        else:
            task_type = self.task["task_type_name"]

        name = '{} {}'.format(name, task_type)   

        self.setWindowTitle("swing: export - {}".format(name))
        self.lineEditEntityName.setText(name)        
        self.lineEditPath.setText(self.working_dir) 
        self.log_output("{}: Loaded".format(name))

        self.load_tags()

    def load_tags(self):
        tag_loader = EntityTagLoader(project_id = self.task["project"]["id"], entity_id = self.task["task_type"]["id"])
        tag_loader.callback.loaded.connect(self.tags_loaded)
        self.threadpool.start(tag_loader)

    def tags_loaded(self, results):
        ## self.log_output("{}: tags_loaded".format(results))

        if len(results) < len("[]"):
            return False

        '''
            tags = json.loads(TAG)
            if "sets" in tags:
                for export_set in tags["sets"]:
                    for export in export_set.keys():
                        for export_param in export_set[export]:
                            for export_option in export_set[export][export_param]:
                                print("Adding {}: {} {}".format(export, export_option, export_param))
        '''            

        root = QtWidgets.QTreeWidgetItem(self.treeWidget)
        tags = json.loads(results)

        if "sets" in tags:
            for export_set in tags["sets"]:
                for export in export_set.keys():

                    item = QtWidgets.QTreeWidgetItem(root)
                    item.setText(0, export)

                    for export_param in export_set[export]:
                        for export_option in export_set[export][export_param]:                
                            opt_item = QtWidgets.QTreeWidgetItem(item)
                            opt_item.setText(0, export_option)
                            opt_item.setCheckState(0, QtCore.Qt.Checked)

                item.setExpanded(True)
                item.setCheckState(0, QtCore.Qt.Checked)
                
        self.treeWidget.addTopLevelItem(root)
        root.setExpanded(True)        
        self.set_enabled(True)  
        ### All Done

    def create_connections(self):
        self.output_dir_path_select_btn.clicked.connect(self.select_output_directory)
        #self.output_dir_path_show_folder_btn.clicked.connect(self.open_output_directory)

        #self.output_filename_select_btn.clicked.connect(self.select_output_filename)

        #self.camera_select_cmb.currentTextChanged.connect(self.on_camera_changed)
        #self.camera_select_hide_defaults_cb.toggled.connect(self.refresh_cameras)

        self.frame_range_cmb.currentTextChanged.connect(self.refresh_frame_range)
        self.frame_range_start_sb.editingFinished.connect(self.on_frame_range_changed)
        self.frame_range_end_sb.editingFinished.connect(self.on_frame_range_changed)    

    def refresh_frame_range(self):
        frame_range_preset = self.frame_range_cmb.currentText()
        if frame_range_preset != "Custom":
            frame_range = self.preset_to_frame_range(frame_range_preset)

            self.frame_range_start_sb.setValue(frame_range[0])
            self.frame_range_end_sb.setValue(frame_range[1])

    def load_frame_ranges(self):
        self.frame_range_cmb.clear()

        for item in self._swing_export.FRAME_RANGE_PRESETS:
            self.frame_range_cmb.addItem(item)
        self.frame_range_cmb.addItem("Custom")

        self.frame_range_cmb.currentIndexChanged.connect(self.frame_range_change)

    def frame_range_change(self, index):
        frame_range = self.frame_range_cmb.currentText()
        self.set_frame_range(frame_range)

    def close_dialog(self):
        self.write_settings()
        self.close()

    def select_output_directory(self):
        current_dir_path = self.lineEditPath.text()
        if not current_dir_path:
            current_dir_path = self.working_dir

        new_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", current_dir_path)
        if new_dir_path:
            self.working_dir = new_dir_path
            self.lineEditPath.setText(new_dir_path)

    def on_frame_range_changed(self):
        self.frame_range_cmb.setCurrentText("Custom")

        frame_range = (self.frame_range_start_sb.value(), self.frame_range_end_sb.value())
        self.set_frame_range(frame_range)        

    def set_frame_range(self, frame_range):
        resolved_frame_range = self.resolve_frame_range(frame_range)
        if not resolved_frame_range:
            return

        self._frame_range_preset = None
        if frame_range in self._swing_export.FRAME_RANGE_PRESETS:
            self._frame_range_preset = frame_range

        self._start_frame = resolved_frame_range[0]
        self.frame_range_start_sb.setValue(self._start_frame)

        self._end_frame = resolved_frame_range[1]
        self.frame_range_end_sb.setValue(self._start_frame)

    def get_start_end_frame(self):
        if self._frame_range_preset:
            return self.preset_to_frame_range(self._frame_range_preset)

        return (self._start_frame, self._end_frame)

    def resolve_frame_range(self, frame_range):
        try:
            if type(frame_range) in [list, tuple]:
                start_frame = frame_range[0]
                end_frame = frame_range[1]
            else:
                start_frame, end_frame = self.preset_to_frame_range(frame_range)

            return (start_frame, end_frame)

        except:
            presets = []
            for preset in self._swing_export.FRAME_RANGE_PRESETS:
                presets.append("'{0}'".format(preset))
            ## self.log_error('Invalid frame range. Expected one of (start_frame, end_frame), {0}'.format(", ".join(presets)))

        return None

    def preset_to_frame_range(self, frame_range_preset):
        if "Custom" in frame_range_preset:
            return (self.frame_range_start_sb.value(), self.frame_range_end_sb.value())

        if not self.handler:
            return False        

        return self.handler.get_param("frame_range", frame_range_preset)

    def process(self):
        if not self.handler:
            return False
        try:
            root = self.treeWidget.invisibleRootItem()
            for i in range(root.childCount()):
                for j in range(root.child(i).childCount()):
                    export_set = root.child(i).child(j)
                    if export_set.checkState(0) == QtCore.Qt.Checked:
                        options = []
                        for j in range(export_set.childCount()):
                            child = export_set.child(j)
                            if child.checkState(0) == QtCore.Qt.Checked:
                                options.append(child.text(0))
                        self.export_set(export_set.text(0), options)
        except:
            traceback.print_exc(file=sys.stdout)    

    def getSceneName(self):
        fileName = cmds.file(q=True,sn=True)
        fileNameArray = fileName.split('/')
        sceneName = fileNameArray[-1]
        return sceneName            

    def getSetContents(self, geoSet):
        setContents = cmds.listConnections(geoSet + '.dagSetMembers')
        return setContents                   

    def getExportSets(self, exportGeoType):
        allSets = cmds.ls (sn = True, set = True)
        exportSets = [s for s in allSets if any(xs in s for xs in exportGeoType)]
        return exportSets

    def getABCExportSets(self):
        exportAbcSets = self.getExportSets(['abc_set']) 
        return exportAbcSets            

    def export_set(self, export_set, export_options):
        self.log_output("Exporting {} using {}".format(export_set, export_options))            

        if "abc" in export_set:
            #sceneInfo = getSceneInfo()
            #scenePath = getScenePath()
            sceneName = self.getSceneName()
            sceneNameOnly = sceneName.split('.')

            # checkFilePath((scenePath + 'alembic'))
            for abcSet in self.getABCExportSets():
                objName = abcSet.split('_')
                abcContent = self.getSetContents(abcSet)

                if abcContent:
                    version = 1
                    version_string = "{}".format(version).zfill(3)
                    file_target = "{}/cache/{}_{}_v{}.abc".format(self.lineEditPath.text(), sceneNameOnly[0], objName[0], version_string)

                    if not os.path.exists(os.path.dirname(file_target)):
                        os.makedirs(os.path.dirname(file_target))

                    while os.path.exists(file_target):
                        version += 1
                        version_string = "{}".format(version).zfill(3)
                        file_target = "{}/cache/{}_{}_v{}.abc".format(self.lineEditPath.text(), sceneNameOnly[0], objName[0], version_string)

                    command = ""
                    command += "-framerange {} {}".format(self.frame_range_start_sb.value(), self.frame_range_end_sb.value())

                    for option in export_options:
                        command += " {}".format(option)

                    command += " -root {}".format(abcContent[0])
                    command += " -file {}".format(file_target)

                    self.log_output("Caching to alembic")
                    #self.log_output("abc::directory {}".format(self.lineEditPath.text()))
                    #self.log_output("abc::frame range {} {}".format(self.frame_range_start_sb.value(), self.frame_range_end_sb.value()))
                    #self.log_output("abc::frame range:: {}".format(command))
                    try:
                        cmds.loadPlugin('AbcExport.mil')
                        cmds.AbcExport(j = command)                      
                        
                        QtWidgets.QMessageBox.question(self, 'Swing: Export', 'Scene {}\r\nExport completed'.format(sceneNameOnly), QtWidgets.QMessageBox.Ok)
                        self.pushButtonCancel.setEnabled(True)

                    except:
                        self.log_error("Error exporting alembic")
                        traceback.print_exc(file=sys.stdout)

                    # abcCommand = ('-framerange ' + str(sceneInfo[0]) + ' ' + str(sceneInfo[1]) + ' -uvWrite -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root ' + abcContent[0] + ' -file ' + scenePath + 'alembic/' + sceneNameOnly[0] + '_' + objName[0] + '.abc')
                    #cmds.AbcExport(j = abcCommand)
                else:
                    print (abcSet + ' contains nothing.')
                


class SwingExport(SwingMaya):

    DEFAULT_CONTAINER = "mp4"
    DEFAULT_ENCODER = "h264"
    DEFAULT_H264_QUALITY = "High"
    DEFAULT_H264_PRESET = "fast"
    DEFAULT_IMAGE_QUALITY = 100

    def __init__(self, log_to_maya=_log_to_maya):
        super(SwingExport, self).__init__()

        self.set_maya_logging_enabled(log_to_maya)

