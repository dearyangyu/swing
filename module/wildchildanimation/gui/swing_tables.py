# -*- coding: utf-8 -*-
import traceback
import sys
import copy
import os

from PySide2.QtWidgets import QStyledItemDelegate

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

class CheckBoxDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent = None):
        QStyledItemDelegate.__init__(self, parent)
        self.optns = QtWidgets.QStyleOptionButton()

    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        checked = bool(index.model().data(index, QtCore.Qt.DisplayRole))
        optns = QtWidgets.QStyleOptionButton()
        optns.state |= QtWidgets.QStyle.State_Active

        if index.flags() & QtCore.Qt.ItemIsEditable:
            optns.state |= QtWidgets.QStyle.State_Enabled
        else:
            optns.state |= QtWidgets.QStyle.State_ReadOnly

        if checked:
            optns.state |= QtWidgets.QStyle.State_On
        else:
            optns.state |= QtWidgets.QStyle.State_Off
        
        optns.rect = self.getCheckBoxRect(option)
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_CheckBox, optns, painter)

    def editorEvent(self, event, model, option, index):
        if not (index.flags() & QtCore.Qt.ItemIsEditable):
            return False

        if event.button() == QtCore.Qt.LeftButton:
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if self.getCheckBoxRect(option).contains(event.pos()):
                    self.setModelData(None, model, index)
                    return True
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                if self.getCheckBoxRect(option).contains(event.pos()):
                    return True

        return False

    def setModelData(self, editor, model, index):
        col = index.column()
        row = index.row()
        checked = not index.model().data(index, QtCore.Qt.DisplayRole)
        model.setData(index, checked, QtCore.Qt.EditRole)

    def getCheckBoxRect(self, option):
        checkBoxRect = QtWidgets.QApplication.style().subElementRect(QtWidgets.QStyle.SE_CheckBoxIndicator, self.optns, None)

        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()

        checkBoxTopLeftCorner = QtCore.QPoint(x + w / 2 - checkBoxRect.width() / 2, y + h / 2 - checkBoxRect.height() / 2)
        return QtCore.QRect(checkBoxTopLeftCorner, checkBoxRect.size())


       
class FileTableModel(QtCore.QAbstractTableModel):    

    _COL_SELECT = 0
    _COL_FILE_NAME = 1
    _COL_VERSION = 2
    _COL_TASK = 3
    _COL_UPDATED = 4
    _COL_SIZE = 5
    _COL_COMMENT = 6
    _COL_DESCRIPTION = 7
    _COL_PATH = 8

    columns = [
        "", 
        "File Name", 
        "v", 
        "Task",
        "Updated", 
        "Size", 
        "Comment", 
        "Description", 
        "Path"
    ]
    files = []
    selection = []

    def __init__(self, parent, working_dir, files = [], entity = None):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.items = files
        self.entity = entity
        self.working_dir = working_dir

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.items)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)

    def flags(self, index):
        if index.column() == FileTableModel._COL_SELECT:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled        

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            col = index.column()
            row = index.row()
            item = self.items[row]   

            if FileTableModel._COL_SELECT == col:
                if type(value) is bool:
                    if value and not item in FileTableModel.selection:
                        FileTableModel.selection.append(item)
                    elif not value and item in FileTableModel.selection:
                        FileTableModel.selection.remove(item)
                    return True

            if FileTableModel._COL_SIZE == col:
                item["download_status"] = value
                return True                    
        return False

    def data(self, index, role):
        #if role == QtCore.Qt.TextAlignmentRole:
        #    col = index.column()
        #    if col == 1 or col == 3:
        #        return QtCore.Qt.AlignLeft | QtCore.AlignTop
        #    else:
        #        return QtCore.Qt.AlignRight | QtCore.AlignBottom

        col = index.column()
        row = index.row()
        item = self.items[row]        

        if role == QtCore.Qt.UserRole:
            return item        

        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list

            if col == FileTableModel._COL_SELECT:
                return item in FileTableModel.selection
            elif col == FileTableModel._COL_FILE_NAME:
                return item["file_name"]
            elif col == FileTableModel._COL_SIZE:
                if "download_status" in item:
                    text = item["download_status"]["message"]
                    return text

                if item["file_size"]:
                    size = int(item["file_size"])
                    if (size):
                        return human_size(size)
                #return item["size"]
            elif col == FileTableModel._COL_VERSION:
                return item["file_revision"]
            elif col == FileTableModel._COL_UPDATED:
                return my_date_format(item["file_updated_at"])
            elif col == FileTableModel._COL_TASK:
                if "task_type" in item and item["task_type"]:
                    return item["task_type"]["name"]
                else:
                    if "type" in item:
                        return item["type"]
                    return ""
            elif col == FileTableModel._COL_COMMENT:
                return item["file_comment"]                
            elif col == FileTableModel._COL_DESCRIPTION:
                return item["file_description"]
            elif col == FileTableModel._COL_PATH:
                test = "/mnt/content/productions"
                if test in item["file_path"]:
                    return item["file_path"].replace(test, self.working_dir)

                test = "/productions"
                if test in item["file_path"]:
                    return item["file_path"].replace(test, self.working_dir)

                return item["file_path"]

        if role == QtCore.Qt.BackgroundRole:
            col = index.column()
            row = index.row()

            if col == FileTableModel._COL_TASK:
                item = self.items[row]
                if "task_type" in item and item["task_type"]:
                        return QtGui.QColor(item["task_type"]["color"])

            elif col == FileTableModel._COL_SIZE:
                if "download_status" in item and item["download_status"] != 2:
                    if "color" in item["download_status"]:
                        return item["download_status"]["color"]

        return None
###########################################################################
def setup_file_table(tableModelFiles, tableView):

    # create the sorter model
    sorterModel = QtCore.QSortFilterProxyModel()
    sorterModel.setSourceModel(tableModelFiles)
    sorterModel.setFilterKeyColumn(0)

     # filter proxy model
    filter_proxy_model = QtCore.QSortFilterProxyModel()
    filter_proxy_model.setSourceModel(tableModelFiles)
    filter_proxy_model.setFilterKeyColumn(FileTableModel._COL_FILE_NAME) # third column          

    tableView.setModel(sorterModel)                
    tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

    tableView.setSortingEnabled(True)
    tableView.sortByColumn(FileTableModel._COL_UPDATED, QtCore.Qt.DescendingOrder)

    tableView.setColumnWidth(FileTableModel._COL_SELECT, 10)
    tableView.setColumnWidth(FileTableModel._COL_FILE_NAME, 300)
    tableView.setColumnWidth(FileTableModel._COL_VERSION, 20)
    tableView.setColumnWidth(FileTableModel._COL_TASK, 100)
    tableView.setColumnWidth(FileTableModel._COL_UPDATED, 160)
    tableView.setColumnWidth(FileTableModel._COL_SIZE, 80)
    tableView.setColumnWidth(FileTableModel._COL_COMMENT, 200)
    tableView.setColumnWidth(FileTableModel._COL_DESCRIPTION, 150)
    tableView.setColumnWidth(FileTableModel._COL_PATH, 100)

    #tableView.horizontalHeader().setSectionResizeMode(FileTableModel._COL_PATH, QtWidgets.QHeaderView.Stretch)

    tableView.resizeRowsToContents()
    tableView.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)        

    tableView.verticalHeader().setDefaultSectionSize(tableView.verticalHeader().minimumSectionSize())        
    tableView.horizontalHeader().setSectionResizeMode(FileTableModel._COL_PATH, QtWidgets.QHeaderView.Stretch)

    checkboxDelegate = CheckBoxDelegate()
    tableView.setItemDelegateForColumn(FileTableModel._COL_SELECT, checkboxDelegate)        

    ## self.tableView.verticalHeader().setDefaultSectionSize(self.tableView.verticalHeader().minimumSectionSize())        
    tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)        
    ## self.tableView.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)

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

        if role == QtCore.Qt.UserRole:
            return item

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

                if item["entity_type_name"]:
                    text = "{} {}".format(text, item["entity_type_name"])

                return text.strip()
            elif col == 3:
                text = item["entity_name"]
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
                if item["entity_description"]:
                    return item["entity_description"].strip()
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

def load_file_table_widget(tableWidget, model, working_dir = "{ROOT}/"):
    headers = [ "File Name", "Size", "Revision", "Task", "Updated", "Status", "Path" ]
    #tableWidget.setColumnCount(len(headers))

    tableWidget.clear()
    tableWidget.setRowCount(len(model))

    font = QtGui.QFont()
    font.setPointSize(8)
    tableWidget.setFont(font)
    tableWidget.setProperty("showDropIndicator", False)
    tableWidget.setAlternatingRowColors(True)
    tableWidget.horizontalHeader().setStretchLastSection(True)    
    tableWidget.setHorizontalHeaderLabels(headers)

    row = 0
    for file_item in model:
        item = copy.deepcopy(file_item)

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

        cell = QtWidgets.QTableWidgetItem(item["task_type"]["name"])
        cell.setBackgroundColor(QtGui.QColor(item["task_type"]["color"]))

        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 3, cell)

        cell = QtWidgets.QTableWidgetItem(my_date_format(item["updated_at"]))
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 4, cell)                                        

        cell = QtWidgets.QTableWidgetItem(str(""))
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 5, cell)

        file_path = item["path"].replace("/mnt/content/productions", working_dir)
        cell = QtWidgets.QTableWidgetItem(file_path)
        cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
        tableWidget.setItem(row, 6, cell)

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
