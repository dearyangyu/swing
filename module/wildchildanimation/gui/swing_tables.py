# -*- coding: utf-8 -*-
import traceback
import sys
import copy
import os

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance 
    import PySide2.QtUiTools as QtUiTools
    qtMode = 0
except ImportError:
    traceback.print_exc(file=sys.stdout)

    from PyQt5 import QtGui, QtCore, QtWidgets
    import sip
    qtMode = 1

from datetime import datetime

from wildchildanimation.gui.swing_utils import human_size, my_date_format
 

class FileTableModel(QtCore.QAbstractTableModel):    

    columns = [
        "File Name", "Size", "v", "Task", "Comment", "Description", "Updated"
    ]
    files = []

    def __init__(self, parent = None, files = [], entity = None):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.items = files
        self.entity = entity

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.items)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

    def data(self, index, role):
        #if role == QtCore.Qt.TextAlignmentRole:
        #    col = index.column()
        #    if col == 1 or col == 3:
        #        return QtCore.Qt.AlignLeft | QtCore.AlignTop
        #    else:
        #        return QtCore.Qt.AlignRight | QtCore.AlignBottom

        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            col = index.column()
            row = index.row()
            item = self.items[row]

            if col == 0:
                return item["name"]
            elif col == 1:
                if item["size"]:
                    size = int(item["size"])
                    if (size):
                        return human_size(size)
                #return item["size"]
            elif col == 2:
                return item["revision"]
            elif col == 3:
                if "task_type" in item and item["task_type"]:
                    return item["task_type"]["name"]
                return ""
            elif col == 4:
                return item["comment"]                
            elif col == 5:
                return item["description"]
            elif col == 6:
                return my_date_format(item["updated_at"])

        if role == QtCore.Qt.BackgroundRole:
            col = index.column()
            row = index.row()

            if col == 3:
                item = self.items[row]
                if "status" in item:
                    col = index.column()
                    row = index.row()
                    if "task_type" in item and item["task_type"]:
                        return QtGui.QColor(item["task_type"]["color"])

        return None
###########################################################################

class TaskTableModel(QtCore.QAbstractTableModel):    

    columns = [
        "Project", "Type", "For", "Entity", "Due", "Status", "Description"
    ]
    tasks = []

    def __init__(self, parent = None, tasks = [], entity = None):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.items = tasks
        self.entity = entity


    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.items)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

    def data(self, index, role):
        #if role == QtCore.Qt.TextAlignmentRole:
        #    col = index.column()
        #    if col == 1 or col == 3:
        #        return QtCore.Qt.AlignLeft | QtCore.AlignTop
        #    else:
        #        return QtCore.Qt.AlignRight | QtCore.AlignBottom
        if not index.isValid():
            return

        col = index.column()
        row = index.row()
        item = self.items[row]

        ### -----------------------------------------------------------------------------------
        if role == QtCore.Qt.ForegroundRole:
            if col == 4:
                if item["due_date"]:
                    text = item["due_date"]
                    if text and len(text) == 19:
                        my_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
                        if my_date < datetime.now():
                            return QtGui.QColor('red')        

        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list

            if col == 0:
                return item["project_name"].strip()
            elif col == 1:
                return item["task_type_name"].strip()
            elif col == 2:
                text = ""
                if "episode_name" in item and item["episode_name"]:
                    text = item["episode_name"]

                if "sequence_name" in item and item["sequence_name"]:
                    text = "{} {}".format(text, item["sequence_name"])

                return text.strip()
            elif col == 3:
                text = "{} / {}".format(item["entity_description"], item["entity_name"])
                return text.strip()
            elif col == 4:
                if item["due_date"]:
                    text = item["due_date"]
                    if text and len(text) == 19:
                        my_date = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S")
                        return my_date.strftime("%Y-%m-%d")
                return None
            elif col == 5:
                return item["task_status_name"].strip()
            elif col == 6:
                if item["description"]:
                    return item["description"].strip()
                if item["last_comment"]:
                    return item["last_comment"]["text"].strip()

        if role == QtCore.Qt.BackgroundRole:
            col = index.column()
            row = index.row()
            item = self.items[row]

            if col == 1:
                if "task_type_color" in item:
                    return QtGui.QColor(item["task_type_color"])      
            elif col == 5:
                if "task_status_color" in item:
                    return QtGui.QColor(item["task_status_color"])      

        return None
###########################################################################

class CastingTableModel(QtCore.QAbstractTableModel):    

    columns = [
        "Name", "Type"
    ]
    items = []

    def __init__(self, parent = None, items = [], entity = None):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.items = items
        self.entity = entity

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

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            col = index.column()
            row = index.row()
            item = self.items[row]

            if col == 0:
                return item["asset_type_name"]
            elif col == 1:
                return item["asset_name"]

        return None
###########################################################################

def load_file_table_widget(tableWidget, model):
    #headers = [ "File Name", "Size", "Revision", "Task", "Updated", "Status" ]
    #tableWidget.setColumnCount(len(headers))

    tableWidget.clear()
    tableWidget.setRowCount(len(model))

    row = 0
    for file_item in model:
        item = copy.copy(file_item)

        cell = QtWidgets.QTableWidgetItem(item["name"])
        cell.setData(QtCore.Qt.UserRole, item)

        cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        cell.setCheckState(QtCore.Qt.Checked)  
        tableWidget.setItem(row, 0, cell)

        if item["size"]:
            size = int(item["size"])
            if (size):
                cell = QtWidgets.QTableWidgetItem("{0}".format(size))
            else:
                cell = QtWidgets.QTableWidgetItem("")
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 1, cell)

        cell = QtWidgets.QTableWidgetItem("{}".format(item["revision"]))
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 2, cell)

        if "task_type" in item and item["task_type"]:
            cell = QtWidgets.QTableWidgetItem(item["task_type"]["name"])
            cell.setBackgroundColor(QtGui.QColor(item["task_type"]["color"]))
        else:
            cell = QtWidgets.QTableWidgetItem("")

        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 3, cell)

        cell = QtWidgets.QTableWidgetItem(my_date_format(item["updated_at"]))
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 4, cell)                                        

        cell = QtWidgets.QTableWidgetItem(str(""))
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 5, cell)

        row += 1

    #tableWidget.setColumnWidth(0, 350)
    #tableWidget.setColumnWidth(1, 100)
    #tableWidget.setColumnWidth(2, 50)        
    #tableWidget.setColumnWidth(3, 200)        
    #tableWidget.setColumnWidth(4, 200)       
    #tableWidget.setColumnWidth(5, 100)   

    hh = tableWidget.horizontalHeader()
    hh.setMinimumSectionSize(100)
    hh.setDefaultSectionSize(hh.minimumSectionSize())
    hh.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)     

    tableWidget.verticalHeader().setDefaultSectionSize(tableWidget.verticalHeader().minimumSectionSize())       
    #tableWidget.verticalHeader().setDefaultSectionSize(tableWidget.verticalHeader().minimumSectionSize())    
    return tableWidget
###########################################################################    
