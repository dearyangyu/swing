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

class RefTableModel(QtCore.QAbstractTableModel):    

    COL_SELECTED = 0
    COL_REF_FILE = 1
    COL_UPDATE_FILE = 2
    COL_UPDATED_AT = 3
    COL_COMMENTS = 4

    refs = []

    columns = [
        "", "Reference File", "Update", "Updated At", "Comments"
    ]

    def __init__(self, parent = None, refs = []):
        QtCore.QAbstractTableModel.__init__(self, parent) 
        self.refs = refs
        for item in self.refs:
            item["selected"] = not item["update"] is None

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.refs)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self.columns[section])

    def data(self, index, role):
        col = index.column()
        row = index.row()
        item = self.refs[row]

        if role == QtCore.Qt.UserRole:
            return item

        if role == QtCore.Qt.DisplayRole:
            if col == RefTableModel.COL_SELECTED:
                return item["selected"]

            elif col == RefTableModel.COL_REF_FILE:
                return item["ref"].path
                
            elif col == RefTableModel.COL_UPDATE_FILE:
                if item["update"]:
                    return item["update"]["name"]
                else:
                    return None
            elif col == RefTableModel.COL_UPDATED_AT:
                if item["update"]:
                    return item["update"]["updated_at"]
                else:
                    return None

            elif col == RefTableModel.COL_UPDATED_AT:
                if item["update"]:
                    return item["update"]["comments"]
                else:
                    return None                    
        return None   

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            item = self.refs[index.row()]
            col = index.column()

            if col == RefTableModel.COL_SELECTED:
                item["selected"] = bool(value)

            self.dataChanged.emit(index, index)
            return True            

    def flags(self, index):
        col = index.column()

        if col == RefTableModel.COL_SELECTED:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled            

        return QtCore.Qt.ItemIsEnabled                   

class RefTableDialog(QtWidgets.QDialog, Ui_ShotTableDialog):

    def __init__(self, parent = None, ref_list = []):
        super(RefTableDialog, self).__init__(parent) # Call the inherited classes __init__ method

        ##shot_list = list(filter(lambda x: ('witw_' in x["name"]), shot_list)) 
        self.setupUi(self)
        self.setModal(True)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("swing::update references")

        self.model = RefTableModel(parent, ref_list)
        self.tableView.setModel(self.model)

        self.tableView.setColumnWidth(RefTableModel.COL_SELECTED, 40)
        self.tableView.setColumnWidth(RefTableModel.COL_REF_FILE, 275)
        self.tableView.setColumnWidth(RefTableModel.COL_UPDATE_FILE, 150)
        self.tableView.setColumnWidth(RefTableModel.COL_UPDATED_AT, 150)

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
        filter_proxy_model.setFilterKeyColumn(RefTableModel.COL_REF_FILE) # third column          

        self.tableView.setModel(sorterModel)                
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        ##self.tableView.setSortingEnabled(True)
        ## self.tableView.sortByColumn(RefTableModel.COL_SHOT_IN, QtCore.Qt.AscendingOrder)        
        # self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
#tableViewPowerDegree->verticalHeader()->setDefaultSectionSize(tableViewPowerDegree->verticalHeader()->minimumSectionSize());

        self.status = 'OK'

        self.buttonClear.clicked.connect(self.select_none)
        self.buttonAll.clicked.connect(self.select_all)
        self.buttonCancel.clicked.connect(self.cancel_dialog)
        self.buttonOk.clicked.connect(self.close_dialog)

    def is_all_selected(self):
        all_selected = True
        for i in range(len(self.model.refs)):
            all_selected = all_selected and self.model.refs[i]["selected"]
        return all_selected

    def select_none(self):
        for i in range(len(self.model.refs)):
            index = self.model.index(i, RefTableModel.COL_SELECTED)
            self.model.setData(index, False, QtCore.Qt.EditRole)     

    def select_all(self):
        for i in range(len(self.model.refs)):
            index = self.model.index(i, RefTableModel.COL_SELECTED)
            self.model.setData(index, True, QtCore.Qt.EditRole)

    def get_selected(self):
        selected = []
        for i in range(len(self.model.refs)):
            if self.model.refs[i]["selected"]:
                selected.append(self.model.refs[i])
        return selected

    def close_dialog(self):
        self.status = 'OK'
        self.close()

    def cancel_dialog(self):
        self.status = 'Cancel'
        self.close()                    