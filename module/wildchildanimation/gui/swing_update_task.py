# -*- coding: utf-8 -*-
import traceback
import sys
import os
import datetime

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


from wildchildanimation.gui.background_workers import FileDownloader
from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import human_size, resolve_content_path
from wildchildanimation.gui.swing_update_task_dialog import Ui_SwingUpdateTask

'''
    Ui_SwingUpdateTaskDialog class
    ################################################################################
'''


class UpdateTaskTableModel(QtCore.QAbstractTableModel):    

    _COL_NAME = 0
    _COL_STATUS = 1
    _COL_UPDATED = 2
    _COL_SIZE = 3
    ## _COL_PATH = 4  

    columns = [
        "Name", "Status", "Updated", "Size", "Path"
    ]
    items = []

    def __init__(self, parent = None, items = []):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.items = items
        for item in self.items:
            item["selected"] = True

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.items)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            col = index.column()
            row = index.row()
            item = self.items[row]   

            if UpdateTaskTableModel._COL_SIZE == col:
                item["download_status"] = value
                return True                    
        return False                

    def data(self, index, role):
        col = index.column()
        row = index.row()

        item = self.items[row]

        if role == QtCore.Qt.UserRole:
            return item                    

        if role == QtCore.Qt.BackgroundRole:
            col = index.column()
            row = index.row()

            if col == UpdateTaskTableModel._COL_SIZE:
                if "download_status" in item:
                    if "color" in item["download_status"]:
                        return item["download_status"]["color"]            

        if role == QtCore.Qt.DisplayRole:

            if col == UpdateTaskTableModel._COL_NAME:
                return item["name"]

            elif col == UpdateTaskTableModel._COL_SIZE:
                if "download_status" in item:
                    if "message" in item["download_status"]:
                        return item["download_status"]["message"]            

                return item["size"]

            elif col == UpdateTaskTableModel._COL_STATUS:
                return item["local_status"]                

            elif col == UpdateTaskTableModel._COL_UPDATED:
                return item["updated_at"]

        return None

class SwingUpdateTaskDialog(QtWidgets.QDialog, Ui_SwingUpdateTask):

    def __init__(self, parent, task_info):
        super(SwingUpdateTaskDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Swing: Update Task")

        self.pushButtonCancel.clicked.connect(self.cancel_dialog)
        self.pushButtonOk.clicked.connect(self.accept_dialog)        

        self.threadpool = QtCore.QThreadPool.globalInstance()
        self.downloads = 0
        self.task_info = task_info

    def accept_dialog(self):
        self.process()
        #self.write_settings()
        ##self.accept()
        ##self.close()

    def cancel_dialog(self):
        #self.write_settings()
        self.reject()        
        self.close()        


    def file_loading(self, result):
        #message = result["message"]
        size = result["size"]
        #target = result["target"]
        file_id = result["file_id"]

        for row in range(self.tableView.model().rowCount()):
            index = self.tableView.model().index(row, 0)
            item = self.tableView.model().data(index, QtCore.Qt.UserRole)
            if file_id == item['id']:
                index = self.tableView.model().index(row, UpdateTaskTableModel._COL_SIZE)

                download_status = {}
                download_status["message"] = "{}".format(human_size(size))
                download_status["color"] = QtGui.QColor('darkCyan')

                self.tableView.model().setData(index, download_status, QtCore.Qt.EditRole) 
                self.tableView.model().dataChanged.emit(index, index, QtCore.Qt.DisplayRole)           
                self.tableView.viewport().update()      
        #print("{} {} {}".format(message, size, target))

    #
    # we have a file or an archive now, let's see what needs to be done
    #
    def file_loaded(self, results):
        status = results["status"]
        message = results["message"]
        file_name = results["target"]
        working_dir = results["working_dir"]

        self.scan_files()

        print("{} {} {}".format(message, status, file_name, working_dir))

    def process(self):
        edit_api = "{}/edit".format(SwingSettings.get_instance().swing_server())
        working_dir = SwingSettings.get_instance().swing_root()

        items = self.tableView.model().items
        self.downloads = 0
        for item in items:
            if item["local_status"] != "Up to date":
                print("Downloading {}".format(item["name"]))

                url = "{}/api/working_file/{}".format(edit_api, item["id"])

                worker = FileDownloader(self, item["id"], url, item["target_path"], skip_existing = False, extract_zips = True)

                worker.callback.progress.connect(self.file_loading)
                worker.callback.done.connect(self.file_loaded)
                
                self.threadpool.start(worker)
                self.downloads += 1                          

    def scan_files(self):
        count = 0
        file_list = []
        working_root = SwingSettings.get_instance().swing_root()

        if "working_files" in self.task_info:
            working_files = self.task_info["working_files"]

            for id in working_files:
                wf = working_files[id]
                
                fp = resolve_content_path(wf["path"], working_root)
                fn = os.path.normpath(os.path.join(fp, wf["name"]))

                wf["target_path"] = fn
                wf["local_date"] = ""
                wf["local_status"] = ""

                download_status = {}
                download_status["message"] = ""

                wf["download_status"] = download_status

                if os.path.exists(fn):
                    local_ts = None
                    if os.path.isfile(fn):

                        # time: The return value is a floating point number giving the number of seconds since the epoch 
                        # ld = os.path.getmtime(fn)

                        mtime = os.stat(fn).st_mtime
                        local_ts = datetime.datetime.fromtimestamp(mtime)

                        timestamp_str = local_ts.strftime('%Y-%m-%d-%H:%M')
                        wf["local_date"] = timestamp_str
                        wf["local_status"] = "Found"

                        if "updated_at" in wf:
                            ud = wf["updated_at"]
                            server_ts = datetime.datetime.strptime(ud, '%Y-%m-%dT%H:%M:%S')

                            if server_ts > local_ts:
                                wf["local_status"] = "Outdated"
                            else:
                                wf["local_status"] = "Up to date"
                                count += 1

                else:
                    wf["local_status"] = "Missing"                    

                file_list.append(wf)
            # scan all working files
        
        self.load_files(file_list)
        
        # return num out of date files
        return len(file_list) - count

    def load_files(self, file_list):
        model = UpdateTaskTableModel(self, list(file_list))
        self.tableView.setModel(model)

        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableView.setSortingEnabled(True)
        self.tableView.sortByColumn(UpdateTaskTableModel._COL_NAME, QtCore.Qt.DescendingOrder)

        self.tableView.setColumnWidth(UpdateTaskTableModel._COL_NAME, 200)
        self.tableView.setColumnWidth(UpdateTaskTableModel._COL_SIZE, 100)
        self.tableView.setColumnWidth(UpdateTaskTableModel._COL_STATUS, 100)
        self.tableView.setColumnWidth(UpdateTaskTableModel._COL_UPDATED, 180)

        self.tableView.resizeRowsToContents()
        self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())        
        self.tableView.horizontalHeader().setSectionResizeMode(UpdateTaskTableModel._COL_NAME, QtWidgets.QHeaderView.Stretch)

        ## self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())        
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)        
        ## self.tableView.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)        

