# -*- coding: utf-8 -*-
#
# Author: P Niemandt
# Date: 2022-11-30
# Version: 1.0
#
# Allows for Project Shot Selection to pass to Sequence Creator

import sys
import traceback
import gazu

from wildchildanimation.gui.swing_utils import load_keyring

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.background_workers import ProjectLoaderThread, ProjectShotLoader
from wildchildanimation.gui.swing_utils import connect_to_server
from wildchildanimation.gui.shot_table import ShotTableModel
from wildchildanimation.gui.swing_tables import CheckBoxDelegate
from wildchildanimation.unreal.sequence_creator import SwingUESequencer

from wildchildanimation.unreal.gui.shot_selector_widget import Ui_ShotSelectorWidget

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2.QtCore import QThreadPool
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    from PyQt5.QtCore import QThreadPool
    qtMode = 1

class ShotSelectorDialog(QtWidgets.QDialog, Ui_ShotSelectorWidget):

    _status = { 
        "projects": False,
        "episodes": False,
        "sequences": False
    }    

    def __init__(self, parent = None):
        super(ShotSelectorDialog, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowTitle("Swing UE Shot Create")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.read_settings()
        self.threadpool = QThreadPool.globalInstance()

        self.comboBoxProject.currentIndexChanged.connect(self.project_changed)
        self.comboBoxEpisode.currentIndexChanged.connect(self.episode_changed)
        self.comboBoxSequence.currentIndexChanged.connect(self.sequence_changed)        

        if connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password()):
            self.load_open_projects()

        self.pushButtonSelectNone.clicked.connect(self.select_none)
        self.pushButtonSelectAll.clicked.connect(self.select_all)
        self.pushButtonCancel.clicked.connect(self.close_dialog)
        self.pushButtonOk.clicked.connect(self.process)        

    def get_project(self):
        return self.comboBoxProject.currentData()

    def set_project(self, index):
        self.comboBoxProject.setCurrentIndex(index)
        self.project_changed(index)

    def get_episode(self):
        return self.comboBoxEpisode.currentData()

    def set_episode(self, index):
        self.comboBoxEpisode.setCurrentIndex(index)
        self.episode_changed(index)

    def get_sequence(self):
        return self.comboBoxSequence.currentData()        

    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()

        self.settings.beginGroup(self.__class__.__name__)
        self.settings.setValue("pos", self.pos())
        #self.settings.setValue("working_dir", self.lineEditRenderPath.text())

        #self.settings.setValue("handles_in", self.spinBoxHandlesIn.value())
        #self.settings.setValue("handles_out", self.spinBoxHandlesOut.value())

        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        #self.working_dir = self.settings.value("working_dir", "~")

    def load_open_projects(self):
        self.comboBoxProject.clear()
        self.comboBoxEpisode.clear()        
        self.comboBoxSequence.clear()

        loader = ProjectLoaderThread(self)
        loader.callback.loaded.connect(self.projects_loaded)
        
        self.threadpool.start(loader)  

    def projects_loaded(self, results): 
        project_dict = {}
        for item in results["projects"]:
            project_id = item["project_id"]
            if not project_id in project_dict:
                project_dict[project_id] = { "project_id": project_id, "project": item["project"], "episodes": [] }

            project = project_dict[project_id]
            project["episodes"].append(item)

        self._projects = project_dict.values()

        self._status["projects"] = True
        self._status["episodes"] = True

        self.comboBoxProject.blockSignals(True)
        self.comboBoxProject.clear()

        for item in self._projects:
            self.comboBoxProject.addItem(item["project"], userData = item)
        self.comboBoxProject.blockSignals(False)

        self.comboBoxEpisode.clear()
        self.comboBoxSequence.clear()

        self.project_changed(self.comboBoxProject.currentIndex())

    def project_changed(self, index):
        project = self.comboBoxProject.itemData(index)

        self.comboBoxEpisode.clear()
        self.comboBoxSequence.clear()

        self.comboBoxEpisode.blockSignals(True)

        # Add Main Pack Episode placeholder for Asset Tasks
        self.comboBoxEpisode.addItem("MP", userData = {"episode": "all", "episode_id": "All"} )
        if "episodes" in project:
            episodes = project["episodes"]
            for item in episodes:
                self.comboBoxEpisode.addItem(item["episode"], userData = item)
            
        self.comboBoxEpisode.blockSignals(False)

        self.comboBoxEpisode.setCurrentIndex(0)   
        self.episode_changed(self.comboBoxProject.currentIndex())
        ## self.sequence_changed(self.comboBoxSequence.currentIndex())   
        #        

    def episode_changed(self, index):
        episode = self.get_episode()

        if episode is None:
            return

        loader = ProjectShotLoader(episode["episode_id"])
        loader.callback.loaded.connect(self.sequence_loaded)

        loader.run()

    def sequence_loaded(self, results):
        sequence_dict = {}

        for item in results:
            sequence_id = item["sequence_id"]

            if not sequence_id in sequence_dict:
                sequence_dict[sequence_id] = { "sequence_id": item["sequence_id"], "sequence": item["sequence"], "episode_id": item["episode_id"] }

            sequence = sequence_dict[sequence_id]
            if not "shots" in sequence:
                sequence["shots"] = []

            shots = sequence["shots"]
            shots.append(item)

        self.comboBoxSequence.blockSignals(True)
        self.comboBoxSequence.clear()
        self.comboBoxSequence.addItem("All", userData = {"sequence": "all", "sequence_id": "All"})
        for item in sequence_dict.values():
            self.comboBoxSequence.addItem(item["sequence"], userData = item)
        self.comboBoxSequence.blockSignals(False)                

        self._status["sequences"] = True

        self.comboBoxSequence.setCurrentIndex(0)
        self.sequence_changed(self.comboBoxSequence.currentIndex())    

    def sequence_changed(self, index):
        if index >= 0:
            sequence = self.get_sequence()

            if sequence["sequence"] == 'all':
                return False

            production_project = gazu.project.get_project_by_name(self.get_project()["project"])
            production_episode = gazu.shot.get_episode_by_name(production_project, self.get_episode()["episode"])
            production_sequence = gazu.shot.get_sequence_by_name(production_project, sequence["sequence"], production_episode)
            production_shots = gazu.shot.all_shots_for_sequence(production_sequence)

            shot_list = []
            for shot in production_shots:

                if shot["nb_frames"]:
                    nb_frames = int(shot["nb_frames"])
                else:
                    nb_frames = 0

                if nb_frames > 0:
                    shot["frame_in"] = 0
                    shot["frame_out"] = nb_frames - 1
                    shot["start"] = 0
                    shot["end"] = nb_frames - 1   

                    shot_list.append(shot)                 

            self.shotModel = ShotTableModel(self, shot_list)
            self.tableViewShots.setModel(self.shotModel)

            self.tableViewShots.setColumnWidth(ShotTableModel.COL_SELECTED, 40)
            self.tableViewShots.setColumnWidth(ShotTableModel.COL_SHOT_NAME, 175)
            self.tableViewShots.setColumnWidth(ShotTableModel.COL_SHOT_IN, 80)
            self.tableViewShots.setColumnWidth(ShotTableModel.COL_SHOT_OUT, 80)
            self.tableViewShots.setColumnWidth(ShotTableModel.COL_SHOT_START, 80)
            self.tableViewShots.setColumnWidth(ShotTableModel.COL_SHOT_END, 80)

            checkboxDelegate = CheckBoxDelegate()
            self.tableViewShots.setItemDelegateForColumn(0, checkboxDelegate)  
            self.tableViewShots.verticalHeader().setDefaultSectionSize(18)

            # create the sorter model
            sorterModel = QtCore.QSortFilterProxyModel()
            sorterModel.setSourceModel(self.shotModel)
            sorterModel.setFilterKeyColumn(0)

            # filter proxy model
            filter_proxy_model = QtCore.QSortFilterProxyModel()
            filter_proxy_model.setSourceModel(self.shotModel)
            filter_proxy_model.setFilterKeyColumn(ShotTableModel.COL_SHOT_NAME) # third column          

            self.tableViewShots.setModel(sorterModel)                
            self.tableViewShots.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

            self.tableViewShots.setSortingEnabled(True)
            self.tableViewShots.sortByColumn(ShotTableModel.COL_SHOT_IN, QtCore.Qt.AscendingOrder)              


    def select_none(self):
        for i in range(len(self.shotModel.shots)):
            index = self.shotModel.index(i, ShotTableModel.COL_SELECTED)
            self.shotModel.setData(index, False, QtCore.Qt.EditRole)     

    def select_all(self):
        for i in range(len(self.shotModel.shots)):
            index = self.shotModel.index(i, ShotTableModel.COL_SELECTED)
            self.shotModel.setData(index, True, QtCore.Qt.EditRole)

    def get_selected(self):
        selected = []
        for i in range(len(self.shotModel.shots)):
            if self.shotModel.shots[i]["selected"]:
                selected.append(self.shotModel.shots[i])
        return selected                           
      
    def close_dialog(self):
        self.write_settings()
        self.close()

    def process(self):
        shot_list = self.get_selected()
        if len(shot_list) > 0:
            production_project = gazu.project.get_project_by_name(self.get_project()["project"])
            production_episode = gazu.shot.get_episode_by_name(production_project, self.get_episode()["episode"])
            production_sequence = gazu.shot.get_sequence_by_name(production_project, self.get_sequence()["sequence"], production_episode)
            number_handles = self.spinBoxHandles.value()

            try:
                shots = []
                frames = []

                for shot in shot_list:
                    shots.append(shot["name"])
                    frames.append(shot["nb_frames"])

                print("{}: Ep {} Seq {}".format(self.__class__.__name__, production_episode["name"], production_sequence["name"]))
                SwingUESequencer().CreateMasterSequence(production_episode["name"], production_sequence["name"], len(shot_list), frames, shots, number_handles)   

                QtWidgets.QMessageBox.information(self, 'Swing UE Sequencer', 'Create sequence completed', QtWidgets.QMessageBox.Ok)             
            except:
                QtWidgets.QMessageBox.warning(self, 'Swing UE Sequencer', 'Error creating sequence', QtWidgets.QMessageBox.Ok)             
                traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    password = load_keyring('swing', 'password', 'Not A Password')
    
    app = QtWidgets.QApplication(sys.argv)

    dialog = ShotSelectorDialog()
    dialog.show()

    sys.exit(app.exec_())
    # wildchildanimation.unreal.gui.swing_sequencer_dialog 
