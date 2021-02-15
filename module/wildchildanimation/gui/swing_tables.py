# -*- coding: utf-8 -*-
import traceback
import sys
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

def my_date_format(date):
    if isinstance(date, str):
        return date

    if len(date) == 19: # YYYY-MM-DDTHH:MM:SS
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    return date.strftime("%Y-%m-%d %H:%M:%S")    

class FileTableModel(QtCore.QAbstractTableModel):    

    columns = [
        "File Name", "Size", "Revision", "Task", "Comment", "Description", "Updated", "Status"
    ]
    files = []

    def __init__(self, parent = None, files = [], entity = None):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.files = files
        self.entity = entity

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.files)

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
            item = self.files[row]

            if col == 0:
                return item["name"]
            elif col == 1:
                return item["size"]
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
            elif col == 7:
                if "task_type" in item and item["task_type"]:
                    return item["task_type"]["name"]


        if role == QtCore.Qt.BackgroundRole:
            col = index.column()
            row = index.row()

            if col == 7:
                item = self.files[row]
                if "status" in item:
                    col = index.column()
                    row = index.row()
                    item = self.files[row]
                    if "task_type" in item and item["task_type"]:
                        return QtGui.QColor(item["task_type"]["color"])

        return None
###########################################################################

class TaskTableModel(QtCore.QAbstractTableModel):    

    columns = [
        "Project", "Type", "Entity", "Status"
    ]
    tasks = []

    def __init__(self, parent = None, tasks = []):
        QtCore.QAbstractTableModel.__init__(self, parent, entity = None) 
        self.tasks = tasks
        self.entity = entity

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.tasks)

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
            item = self.tasks[row]

            if col == 0:
                return item["project_name"]
            elif col == 1:
                return item["entity_type_name"]
            elif col == 2:
                return my_date_format(item["entity_name"])
            elif col == 3:
                return item["task_type_name"]

        return None
###########################################################################
