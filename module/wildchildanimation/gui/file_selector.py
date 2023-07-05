# -*- coding: utf-8 -*-

import sys
import os

# ==== auto Qt load ====
try:
    from PySide2 import QtWidgets, QtCore
    from PySide2.QtCore import Signal as pyqtSignal
    qtMode = 0
except ImportError:
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtCore import pyqtSignal
    qtMode = 1

from wildchildanimation.gui.file_select_widget import Ui_FileSelectWidget
from wildchildanimation.gui.background_workers import SwingCompressor
from wildchildanimation.studio.studio_interface import StudioInterface

class WalkedSignal(QtCore.QObject):
    walked = pyqtSignal(object)  

class FileExcludeWalker(QtCore.QRunnable):

    def __init__(self, root = '', exclude = []):
        super(FileExcludeWalker, self).__init__(self)
        self.root = root
        self.exclude = exclude
        self.callback = WalkedSignal()    


    def run(self):
        results = []
        for root, dirs, files in os.walk(self.root, topdown=False):
            for name in files:
                if any(name.endswith(ext) for ext in self.exclude):
                    results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Unchecked, 'timestamp': os.path.getmtime(os.path.join(root, name))})
                else:
                    results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Checked, 'timestamp': os.path.getmtime(os.path.join(root, name))})

            for name in dirs:
                if any(name.endswith(ext) for ext in self.exclude):
                    results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Unchecked, 'timestamp': os.path.getmtime(os.path.join(root, name))})
                else:
                    results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Checked, 'timestamp': os.path.getmtime(os.path.join(root, name))})

        self.callback.walked.emit(results)                        
        return results    

class FileIncludeWalker(QtCore.QRunnable):

    def __init__(self, root = '', include = []):
        super(FileIncludeWalker, self).__init__(self)
        self.root = root
        self.include = include
        self.callback = WalkedSignal()    

    def run(self):
        results = []
        for root, dirs, files in os.walk(self.root, topdown=False):
            upload_dir = False            

            for name in dirs:
                if any(name.endswith(ext) for ext in self.include):
                    results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Checked, 'timestamp': os.path.getmtime(os.path.join(root, name))})
                    upload_dir = True
                else:
                    results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Unchecked, 'timestamp': os.path.getmtime(os.path.join(root, name))})

            if not upload_dir:
                for name in files:
                    if any(name.endswith(ext) for ext in self.include):
                        results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Checked, 'timestamp': os.path.getmtime(os.path.join(root, name))})

                    elif any(name in item for item in self.include):
                        results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Checked, 'timestamp': os.path.getmtime(os.path.join(root, name))})
                    else:
                        results.append({'path': os.path.normpath(os.path.join(root, name)), 'selected': QtCore.Qt.Unchecked, 'timestamp': os.path.getmtime(os.path.join(root, name))})
                    


        self.callback.walked.emit(results)                        
        return results             
 

class CheckableFileSystemModel(QtWidgets.QFileSystemModel):

    checkStateChanged = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()
        self.threadpool = QtCore.QThreadPool.globalInstance()        
        self.checkStates = {}
        self.rowsInserted.connect(self.checkAdded)
        self.rowsRemoved.connect(self.checkParent)
        self.rowsAboutToBeRemoved.connect(self.checkRemoved)

    def checkState(self, index):
        return self.checkStates.get(self.filePath(index), QtCore.Qt.Unchecked)

    def setCheckState(self, index, state, emitStateChange = True):
        path = self.filePath(index)
        if self.checkStates.get(path) == state:
            return

        self.checkStates[path] = state
        if emitStateChange:
            self.checkStateChanged.emit(path, bool(state))

    def checkAdded(self, parent, start, end):
        if not parent.isValid():
            return

        if self.filePath(parent) in self.checkStates:
            state = self.checkState(parent)
            for row in range(start, end + 1):
                index = self.index(row, 0, parent)
                path = self.filePath(index)
                if path not in self.checkStates:
                    self.checkStates[path] = state
        self.checkParent(parent)

    def checkRemoved(self, parent, first, last):
        for row in range(first, last + 1):
            path = self.filePath(self.index(row, 0, parent))
            if path in self.checkStates:
                self.checkStates.pop(path)

    def checkParent(self, parent):
        if not parent.isValid():
            return

        childStates = [self.checkState(self.index(r, 0, parent)) for r in range(self.rowCount(parent))]
        newState = QtCore.Qt.Checked if all(childStates) else QtCore.Qt.Unchecked
        oldState = self.checkState(parent)

        if newState != oldState:
            self.setCheckState(parent, newState)
            self.dataChanged.emit(parent, parent)
        self.checkParent(parent.parent())

    def flags(self, index):
        return super().flags(index) | QtCore.Qt.ItemIsUserCheckable
        #if index.column() < 2:
        #    return super().flags(index) | QtCore.Qt.ItemIsUserCheckable
        #else:
        #    return super().flags(index)

    def data(self, index, role= QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            #if index.row() == 0:
            #    return False
            #print("{} {} {}".format(index.column(), index.row(), index.parent()))
            return self.checkState(index)
        return super().data(index, role)

    def setData(self, index, value, role, checkParent = True, emitStateChange = True):
        if role == QtCore.Qt.CheckStateRole and index.column() == 0:
            self.setCheckState(index, value, emitStateChange)

            for row in range(self.rowCount(index)):
                self.setData(index.child(row, 0), value, QtCore.Qt.CheckStateRole, checkParent = False, emitStateChange = False)

            if emitStateChange:
                self.dataChanged.emit(index, index)

            if checkParent:
                self.checkParent(index.parent())

            return True

        return super().setData(index, value, role)

    def scan_working_files(self, callback = None, excluded =  [] ):
        walker = FileExcludeWalker(self.rootPath(), excluded)
        if callback is not None:
            walker.callback.walked.connect(callback)

        self.threadpool.start(walker)
        #walker.run()


    # scans directory for output files
    # if specified only include files in included and select count 
    def scan_output_files(self, callback = None, included = []):  
        walker = FileIncludeWalker(self.rootPath(), included)
        if callback is not None:
            walker.callback.walked.connect(callback)

        self.threadpool.start(walker)        
        #walker.run()


'''
    FileSelectDialog class
    ################################################################################
'''

class FileSelectDialog(QtWidgets.QDialog, Ui_FileSelectWidget):        

    root = ''

    def __init__(self, parent = None, root_path = ""):
        super(FileSelectDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.pushButtonOK.clicked.connect(self.close_dialog)
        self.pushButtonCancel.clicked.connect(self.cancel)   

        self.pushButtonWorkingFiles.clicked.connect(self.scan_working_files)
        self.pushButtonOutputFiles.clicked.connect(self.scan_output_files)
        self.pushButtonZip.clicked.connect(self.zip_selection)

        self.pushButtonWorkingFiles.setVisible(False)
        self.pushButtonOutputFiles.setVisible(False)
        self.pushButtonZip.setVisible(False)

        self.set_root(root_path)
        self.include_count = 0
        self.threadpool = QtCore.QThreadPool.globalInstance()


    def set_root(self, root):
        self.root = root

        self.treeView.blockSignals(True)

        root_dir = QtCore.QDir(root)

        model = CheckableFileSystemModel()
        model.setRootPath(root_dir.path())

        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(root_dir.path()))
        self.treeView.setSortingEnabled(True)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setUniformRowHeights(True)
        #self.treeView.expand(model.index(root_dir.path()))
        #self.treeView.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.treeView.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.treeView.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.treeView.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)        

        self.treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.treeView.blockSignals(False)

        #self.treeView.expandToDepth(10)
        #QtCore.QTimer.singleShot(0, lambda: self.treeView.expandToDepth(0))

    def item_count(self):
        count = 0
        model = self.treeView.model()
        selection = model.checkStates

        for item in selection:
            index = model.index(item)
            selected = model.checkState(index)
            if selected == QtCore.Qt.Checked:
                count += 1
        return count

    def set_enabled(self, enabled):
        self.treeView.blockSignals(not enabled)

        self.treeView.setEnabled(enabled)
        self.pushButtonOutputFiles.setEnabled(enabled)
        self.pushButtonCancel.setEnabled(enabled)
        self.pushButtonOK.setEnabled(enabled)
        self.pushButtonWorkingFiles.setEnabled(enabled)
        self.pushButtonZip.setEnabled(enabled)

    def close_dialog(self):
        self.accept()
        self.close()

    def cancel(self):
        self.reject()
        self.close() 

    def scan_working_files(self):
        print("scan_working_files::")
        self.set_enabled(False)

        excluded = StudioInterface.WF_DEFAULT_EXCLUDE
        self.working_files = []
        self.labelMessage.setText("Scanning working files...")

        self.treeView.model().scan_working_files(self.select_working_files, excluded)

    def scan_output_files(self, to_include  = None):
        self.set_enabled(False)

        if to_include is None:
            included = StudioInterface.OF_DEFAULT_INCLUDE
        else:
            included = to_include

        self.include_count = len(included)

        print("FileSelectDialog::Selecting up to {} files".format(self.include_count))
        self.output_files = []
        self.set_enabled(False)
        self.labelMessage.setText("Scanning output files...")

        self.treeView.model().scan_output_files(self.select_output_files, included)

    def select_working_files(self, data):
        print("select_working_files::")

        self.labelMessage.setText("Selecting files...")
        model = self.treeView.model()
        index = model.index(model.rootPath())

        model.setData(index, QtCore.Qt.Checked, QtCore.Qt.CheckStateRole, checkParent = True, emitStateChange = True)
        for item in data:
            if not item["selected"]:
                # print("Unselecting {}".format(item["path"]))
                if os.path.isdir(item["path"]):
                    model.setData(model.index(item["path"]), QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole, checkParent = False, emitStateChange = True)
                else:
                    model.setData(model.index(item["path"]), QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole, checkParent = False, emitStateChange = True)

        self.set_enabled(True)
        self.labelMessage.setText("")

    def select_output_files(self, data):
        print("file_selector::file list {} select length {}".format(str(self.output_files), self.include_count))

        self.labelMessage.setText("Selecting files...")
        self.output_files = []
        model = self.treeView.model()

        index = model.index(model.rootPath())
        model.setData(index, QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole, checkParent = True, emitStateChange = True)
        for item in data:
            if item["selected"]:            
                index = model.index(item['path'], 0)
                model.setData(index, QtCore.Qt.Checked, QtCore.Qt.CheckStateRole, checkParent = True, emitStateChange = True)
                self.output_files.append(item)                
            

        # check for output directories
        # if we find an export directory, select that, and unselect everything else
        found = False
        selected = sorted(self.output_files, key = lambda x: x['timestamp'], reverse=True)
        for item in selected:
            if not found and os.path.isdir(item['path']):
                # print("Found first output dir {}, skipping any other media files".format(item['path']))
                found = True
            else:
                model.setCheckState(model.index(item['path']), QtCore.Qt.Unchecked, False)     

        # select the most recent file (only if we didn't get a shot_list to select)
        if not found and self.include_count == 1:
            print("Selecting newest file only")
            if len(selected) > 0:
                model.setCheckState(model.index(selected[0]['path']), QtCore.Qt.Checked, False)

            for x in range(1, len(selected)):
                print("Unselecting the rest")
                model.setCheckState(model.index(selected[x]['path']), QtCore.Qt.Unchecked, False)
        else:
            # otherwise select everything from of_include
            ## ToDo: check and confirm
            #for x in range(0, self.include_count):
            for x in range(0, len(selected)):
                model.setCheckState(model.index(selected[x]['path']), QtCore.Qt.Checked, False)

        self.set_enabled(True)
        self.labelMessage.setText("")        

    def zip_callback(self, data):    
        self.labelMessage.setText("{}".format(data))

    def zip_selection(self, target = 'outputfiles.zip'):
        if not target:
            target = 'outputfiles.zip'

        self.set_enabled(False)
        self.labelMessage.setText("Zipping selection ...")

        model = self.treeView.model()
        directory = model.rootPath()

        zipper = SwingCompressor(directory, model, target=target)
        zipper.callback.progress.connect(self.on_zip_message)

        zipper.run()
        #self.threadpool.start(zipper)
        self.labelMessage.setText("")
        self.set_enabled(True)        

    def on_zip_message(self, data):
        self.labelMessage.setText("{}".format(data))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test = FileSelectDialog(None, "E:/Work/WCA/content/tg201_080_020/TG201clr_080_020_ani_08")
    #test = FileSelectDialog(None, "E:/productions/Tom_Gates_Sky_S02/tg_2d_main/tg_2d_build/tg_2d_ep206/shots/sc100/sh010/anim_block/sc100_sh010_anim_block/")

    test.pushButtonWorkingFiles.setVisible(True)
    test.pushButtonOutputFiles.setVisible(True)
    test.pushButtonZip.setVisible(True)


    test.show()
    sys.exit(app.exec_())
