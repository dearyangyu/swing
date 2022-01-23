# -*- coding: utf-8 -*-

from wildchildanimation.gui.swing_tables import CheckBoxDelegate

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

from wildchildanimation.gui.shot_table_dialog import Ui_ShotTableDialog

class ShotTableModel(QtCore.QAbstractTableModel):    

    COL_SELECTED = 0
    COL_SHOT_NAME = 1
    COL_SHOT_IN = 2
    COL_SHOT_OUT = 3
    COL_SHOT_START = 4
    COL_SHOT_END = 5

    columns = [
        "", "Shot", "Frame In", "Frame Out", "Start", "End"
    ]

    def __init__(self, parent = None, shots = []):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.shots = shots

        for item in self.shots:
            item["selected"] = True

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.shots)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

    def data(self, index, role):
        col = index.column()
        row = index.row()
        item = self.shots[row]

        if role == QtCore.Qt.UserRole:
            return item

        if role == QtCore.Qt.DisplayRole:
            if col == ShotTableModel.COL_SELECTED:
                return item["selected"]
            elif col == ShotTableModel.COL_SHOT_NAME:
                return item["name"]
            elif col == ShotTableModel.COL_SHOT_IN:
                return item["frame_in"]
            elif col == ShotTableModel.COL_SHOT_OUT:
                return item["frame_out"]
            elif col == ShotTableModel.COL_SHOT_START:
                return item["start"]
            elif col == ShotTableModel.COL_SHOT_END:
                return item["end"]

        return None   

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            item = self.shots[index.row()]
            col = index.column()

            if col == ShotTableModel.COL_SELECTED:
                item["selected"] = not item["selected"]
                return True
            elif col == ShotTableModel.COL_SHOT_NAME:
                item["name"] = str(value)
            elif col == ShotTableModel.COL_SHOT_IN:
                item["frame_in"] = int(value)
            elif col == ShotTableModel.COL_SHOT_OUT:
                item["frame_out"] = int(value)

            return False     

    def flags(self, index):
        col = index.column()

        if col == ShotTableModel.COL_SELECTED:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled            
        elif col == ShotTableModel.COL_SHOT_NAME:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled            
        elif col == ShotTableModel.COL_SHOT_IN:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled            
        elif col == ShotTableModel.COL_SHOT_OUT:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled            
        return QtCore.Qt.ItemIsEnabled                   

    #def select_none(self):
    #    for row in range(self.tableView.model().rowCount()):
    #        index = self.tableView.model().index(row, 0)
    #        self.tableView.model().setData(index, False, QtCore.Qt.EditRole)
    #    self.tableView.update()        

class ShotTableDialog(QtWidgets.QDialog, Ui_ShotTableDialog):

    def __init__(self, parent = None, shot_list = []):
        super(ShotTableDialog, self).__init__(parent) # Call the inherited classes __init__ method


        ##shot_list = list(filter(lambda x: ('witw_' in x["name"]), shot_list)) 
        self.setupUi(self)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("swing: select shots")
        self.model = ShotTableModel(self, shot_list)
        self.tableView.setModel(self.model)

        self.tableView.setColumnWidth(ShotTableModel.COL_SELECTED, 40)
        self.tableView.setColumnWidth(ShotTableModel.COL_SHOT_NAME, 175)
        self.tableView.setColumnWidth(ShotTableModel.COL_SHOT_IN, 80)
        self.tableView.setColumnWidth(ShotTableModel.COL_SHOT_OUT, 80)
        self.tableView.setColumnWidth(ShotTableModel.COL_SHOT_START, 80)
        self.tableView.setColumnWidth(ShotTableModel.COL_SHOT_END, 80)

        checkboxDelegate = CheckBoxDelegate()
        self.tableView.setItemDelegateForColumn(0, checkboxDelegate)  
        self.tableView.verticalHeader().setDefaultSectionSize(18)

        # create the sorter model
        sorterModel = QtCore.QSortFilterProxyModel()
        sorterModel.setSourceModel(self.model)
        sorterModel.setFilterKeyColumn(0)

        # filter proxy model
        filter_proxy_model = QtCore.QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        filter_proxy_model.setFilterKeyColumn(ShotTableModel.COL_SHOT_NAME) # third column          

        self.tableView.setModel(sorterModel)                
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.tableView.setSortingEnabled(True)
        self.tableView.sortByColumn(ShotTableModel.COL_SHOT_IN, QtCore.Qt.AscendingOrder)        
        # self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

#tableViewPowerDegree->verticalHeader()->setDefaultSectionSize(tableViewPowerDegree->verticalHeader()->minimumSectionSize());

        self.status = 'OK'

        self.buttonClear.clicked.connect(self.select_none)
        self.buttonAll.clicked.connect(self.select_all)
        self.buttonCancel.clicked.connect(self.cancel_dialog)
        self.buttonOk.clicked.connect(self.close_dialog)

    def is_all_selected(self):
        all_selected = True
        for i in range(len(self.model.shots)):
            all_selected = all_selected and self.model.shots[i]["selected"]
        return all_selected

    def select_none(self):
        for i in range(len(self.model.shots)):
            self.model.shots[i]["selected"] = False
        self.tableView.update()        

    def select_all(self):
        for i in range(len(self.model.shots)):
            self.model.shots[i]["selected"] = True
        self.tableView.update()        

    def get_selected(self):
        selected = []
        for i in range(len(self.model.shots)):
            if self.model.shots[i]["selected"]:
                selected.append(self.model.shots[i])
        return selected

    def close_dialog(self):
        self.status = 'OK'
        self.close()

    def cancel_dialog(self):
        self.status = 'Cancel'
        self.close()                    