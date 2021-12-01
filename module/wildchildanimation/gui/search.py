# -*- coding: utf-8 -*-

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    import sip
    qtMode = 1

from wildchildanimation.gui.background_workers import SearchFn
from wildchildanimation.gui.search_files_dialog import Ui_SearchFilesDialog
from wildchildanimation.gui.settings import SwingSettings

class SearchFilesDialog(QtWidgets.QDialog, Ui_SearchFilesDialog):

    working_dir = None
    file_list = []

    def __init__(self, parent, text = '', entity = None, handler = None, project = None, task_types = None, status_types = None):
        super(SearchFilesDialog, self).__init__(parent) # Call the inherited classes __init__ method
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setModal(True)

        self.setMinimumWidth(640)

        self.swing_settings = SwingSettings.get_instance()

        self.handler = handler
        self.entity = entity
        self.project_id = project
        self.task_types = task_types
        self.status_types = status_types
        self.textEdit.setText(text)

        self.threadpool = QtCore.QThreadPool.globalInstance()

        self.pushButtonSearch.clicked.connect(self.process)
        self.pushButtonCancel.clicked.connect(self.cancel_dialog)

    def process(self):
        self.threadpool = QtCore.QThreadPool.globalInstance()

        file_list = []

        items = self.textEdit.toPlainText().split(",")
        for i in items:
            file_list.append(i)

        worker = SearchFn(self,file_list, self.project_id, show_hidden=False, task_types=self.task_types, status_types=self.status_types)
        worker.callback.results.connect(self.search_results)

        self.enable_ui(False)
        self.threadpool.start(worker)
        ##worker.run()
    # process        

    def enable_ui(self, enabled):
        self.pushButtonSearch.setEnabled(enabled)
        self.pushButtonCancel.setEnabled(enabled)

        if enabled:
            self.progressBar.setRange(0, 1)
        else:
            # set progressbar to busy
            self.progressBar.setRange(0, 0)

    def search_results(self, results):
        self.file_list = results
        self.enable_ui(True)

        if len(results) == 0:
            QtWidgets.QMessageBox.information(self, 'File Search', 'No files found, sorry', QtWidgets.QMessageBox.Ok)            
            return   
        else:
            self.close_dialog()

    def get_file_list(self):
        return self.file_list

    def close_dialog(self):
        self.accept()
        self.close()

    def cancel_dialog(self):
        self.reject()        
        self.close()

