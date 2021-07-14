# -*- coding: utf-8 -*-
# 
# Allows Artist to submit for approval
# - Task
# - Working file set
# - Output file set 
# - Task comments
# ==== auto Qt load ====
import sys
import traceback


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

class WorkPacket:

    task = None
    api = None
    threadpool = None
    workers = []
    comments = []

    def __init__(self, edit_api, task) -> None:
        self.api = edit_api
        self.task = task
        self.threadpool = QtCore.QThreadPool()

    def add_worker(self, worker):
        self.workers.append(worker)

    def add_output_files(self, files):
        self.output_files.append(files)




