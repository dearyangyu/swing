# -*- coding: utf-8 -*-
import sys

# ==== auto Qt load ====
try:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtGui, QtCore, QtWidgets
    qtMode = 1

import gazu    

from wildchildanimation.gui.upload_monitor_dialog import Ui_UploadMonitorDialog    

'''
    UploadListModel class
    ################################################################################
'''

class UploadListModel(QtCore.QAbstractListModel):

    def __init__(self, parent, files = None):
        super(UploadListModel, self).__init__(parent)
        self.files = files or []
        self.status = {}

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the data structure.
            item = self.files[index.row()]
            text = self.status[item]

            # Return the todo text only.
            return "{} {}".format(item, text)

    def rowCount(self, index):
        return len(self.files)   

    def add_item(self, item, text):
        self.files.append(item)
        self.status[item] = text
        self.layoutChanged.emit()

    def set_item_text(self, item, text):
        self.status[item] = text
        self.layoutChanged.emit()

'''
    UploadMonitorDialog class
    ################################################################################
'''


class UploadMonitorDialog(QtWidgets.QDialog, Ui_UploadMonitorDialog):

    def __init__(self, parent = None):
        super(UploadMonitorDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setMinimumWidth(640)

        self.model = UploadListModel(self.listView)
        self.listView.setModel(self.model)
        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.queue = []
        self.task = None
        #self.progressBar.setRange(0, len(self.model.files))

    def set_queue(self, queue):
        self.queue = []
        
        index = 0
        for item in queue:
            print("{}: {}".format(index, item))            

            self.queue.append(item)
            self.add_item(item.source, 'Pending')
            index += 1

        self.reset_progressbar()            

    def reset(self):
        self.queue = []

    def close_dialog(self):
        self.hide()

    def set_task(self, task):
        self.task = task

    def file_loading(self, results):
        ## print("file loading: {}".format(results))

        message = results["message"]
        source = results["source"]     
        status = results["status"]

        if not source in self.model.files:
            self.model.add_item(source, message)
        else:
            self.model.set_item_text(source, message)

    def file_loaded(self, results):
        upload_index = self.progressBar.value()
        ## print("file_loaded {}: {} {} {} {}".format(len(self.queue), results['status'], upload_index, results['source'], results['message']))

        status = results["status"]

        message = results["message"]
        source = results["source"]     

        self.model.set_item_text(source, message)        

        if "upload complete" in message:
            if upload_index == len(self.queue) - 1:
                self.pushButtonCancel.setText("Close")
                # QtWidgets.QMessageBox.question(self, 'Publishing complete', 'All files uploaded, thank you', QtWidgets.QMessageBox.Ok)
                try:
                    self.reset()
                    url = gazu.task.get_task_url(self.task)
                    self.open_url(url)
                except:
                    print("Error loading url {0}".format(url))
                    pass   

            self.progressBar.setValue(upload_index + 1)
         

    def add_item(self, source, text):
        self.model.add_item(source, text)         

    def reset_progressbar(self):
        self.progressBar.setRange(0, len(self.queue))      
        self.progressBar.setValue(0)

    def open_url(self, url):
        link = QtCore.QUrl(url)
        if not QtGui.QDesktopServices.openUrl(link):
            QtWidgets.QMessageBox.warning(self, 'Open Url', 'Could not open url')           


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test = UploadMonitorDialog(None)
    test.show()
    sys.exit(app.exec_())