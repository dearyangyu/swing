# -*- coding: utf-8 -*-

import os
try:
    import opentimelineio as otio
    OPEN_TIMELINE = True
except:
    print("Please install opentimeline")
    OPEN_TIMELINE = False
# check open timeline
from wildchildanimation.gui.swing_utils import friendly_string
from wildchildanimation.gui.swing_tables import CheckBoxDelegate

# ==== auto Qt load ====
try:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets
    qtMode = 1

import gazu

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.maya_sequence_shot_table_dialog import Ui_SequenceShotTableDialog
from wildchildanimation.gui.swing_utils import set_button_icon

CLEAN_NAME = [
    ".mp4", ".mov"
]

class SequencerShotTableModel(QtCore.QAbstractTableModel):    

    COL_SELECTED = 0
    COL_SHOT_NAME = 1
    COL_SHOT_IN = 2
    COL_SHOT_OUT = 3
    COL_SEQ_IN = 4
    COL_SEQ_OUT = 5
    COL_SHOT_PADDING = 6
    COL_CAMERA = 7
    COL_AUDIO = 8
    COL_IMAGE_PLANE = 9
    
    columns = [
        "",  "Shot", "Shot In", "Shot Out", "Seq In", "Seq Out", "Padding", "Camera", "Audio", "Image Plane"
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
            if col == SequencerShotTableModel.COL_SELECTED:
                return item["selected"]
            elif col == SequencerShotTableModel.COL_SHOT_NAME:
                return item["shotName"]
            elif col == SequencerShotTableModel.COL_SHOT_IN:
                return item["startTime"]
            elif col == SequencerShotTableModel.COL_SHOT_OUT:
                return item["endTime"]
            elif col == SequencerShotTableModel.COL_SEQ_IN:
                return item["sequencerStartTime"]
            elif col == SequencerShotTableModel.COL_SEQ_OUT:
                return item["sequencerEndTime"]                
            elif col == SequencerShotTableModel.COL_SHOT_PADDING:
                return item["padding"]
            elif col == SequencerShotTableModel.COL_CAMERA:
                return item["currentCamera"]                
            elif col == SequencerShotTableModel.COL_AUDIO:
                return item["audio"]                
            elif col == SequencerShotTableModel.COL_IMAGE_PLANE:
                return item["image_plane"]    

        return None   

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            item = self.shots[index.row()]
            col = index.column()

            if col == SequencerShotTableModel.COL_SELECTED:
                item["selected"] = bool(value)
            elif col == SequencerShotTableModel.COL_SHOT_NAME:
                item["shot"] = str(value)
            elif col == SequencerShotTableModel.COL_SHOT_IN:
                item["frame_in"] = int(value)
            elif col == SequencerShotTableModel.COL_SHOT_OUT:
                item["frame_out"] = int(value)
            elif col == SequencerShotTableModel.COL_SHOT_PADDING:
                item["padding"] = int(value)
            elif col == SequencerShotTableModel.COL_AUDIO:
                item["audio"] = str(value)                

            self.dataChanged.emit(index, index) 
            return True            
            
    def flags(self, index):
        col = index.column()

        if col in [ SequencerShotTableModel.COL_SELECTED,
            SequencerShotTableModel.COL_SHOT_NAME, 
            SequencerShotTableModel.COL_SHOT_IN, SequencerShotTableModel.COL_SHOT_OUT, 
            SequencerShotTableModel.COL_SHOT_PADDING, SequencerShotTableModel.COL_AUDIO ]:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled             
        return QtCore.Qt.ItemIsEnabled                   

    #def select_none(self):
    #    for row in range(self.tableView.model().rowCount()):
    #        index = self.tableView.model().index(row, 0)
    #        self.tableView.model().setData(index, False, QtCore.Qt.EditRole)
    #    self.tableView.update()        

class SequencerShotCreator(QtWidgets.QDialog, Ui_SequenceShotTableDialog):

    ALLOWED_MOVIE_EXTENSION = [
        ".avi",
        ".m4v",
        ".mkv",
        ".mov",
        ".mp4",
        ".webm",
        ".wmv",
    ]       

    def __init__(self, parent = None, shot_list = [], handler = None, task = None):
        super(SequencerShotCreator, self).__init__(parent) # Call the inherited classes __init__ method

        ##shot_list = list(filter(lambda x: ('witw_' in x["name"]), shot_list)) 
        self.setupUi(self)
        self.read_settings()
        self.groupBoxImagePlane.setChecked(False)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("swing: shot sequencer")
        self.setMinimumWidth(720)

        self.model = SequencerShotTableModel(self, shot_list)
        self.tableView.setModel(self.model)        

        self.handler = handler
        self.task = task
        self.fps = task["project"]["fps"]
        self.sequence = self.task["sequence"]
        self.episode = self.task["episode"]

        print("SequencerShotCreator::Task {}".format(self.task))
        print("SequencerShotCreator::Project {}".format(self.task["project"]))
        print("SequencerShotCreator::Episode {}".format(self.episode))
        print("SequencerShotCreator::Sequence {}".format(self.sequence))
        print("SequencerShotCreator::FPS {}".format(self.fps))

        prefix_sections = []
        if self.task["project"]["code"]:
            self.project_code = self.task["project"]["code"]
            # prefix_sections.append(self.task["project"]["code"])
        else:
            self.project_code = self.task["project"]["name"]
            # prefix_sections.append(self.task["project"]["name"])

        episode_name = self.episode["name"]

        if not self.project_code in episode_name:
            prefix_sections.append(self.project_code)

        prefix_sections.append(self.task["episode"]["name"])
        prefix_sections.append(self.task["sequence"]["name"])

        self.lineEditShotPrefix.setText(self.project_code)

        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SELECTED, 40)
        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SHOT_NAME, 175)
        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SHOT_IN, 100)
        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SHOT_OUT, 100)
        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SEQ_IN, 100)
        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SEQ_OUT, 100)

        self.tableView.setColumnWidth(SequencerShotTableModel.COL_SHOT_PADDING, 80)

        checkboxDelegate = CheckBoxDelegate()
        self.tableView.setItemDelegateForColumn(0, checkboxDelegate)  
        self.tableView.verticalHeader().setDefaultSectionSize(18)

        #tableViewPowerDegree->verticalHeader()->setDefaultSectionSize(tableViewPowerDegree->verticalHeader()->minimumSectionSize());

        self.status = 'OK'

        self.buttonClear.clicked.connect(self.select_none)
        self.buttonAll.clicked.connect(self.select_all)
        self.buttonCancel.clicked.connect(self.cancel_dialog)
        self.buttonCreateShots.clicked.connect(self.process)

        self.toolButtonXmlFile.clicked.connect(self.select_xml_file)
        set_button_icon(self.toolButtonXmlFile, "../resources/fa-free/solid/folder.svg")

        self.toolButtonExportDir.clicked.connect(self.select_export_dir)
        set_button_icon(self.toolButtonExportDir, "../resources/fa-free/solid/folder.svg")

        self.scan_breakout_folder()

    def scan_breakout_folder(self):
        self.shot = gazu.shot.get_shot_by_name(self.sequence, 'sh000')

        breakout_task_type = gazu.task.get_task_type_by_name("Breakout")
        if not breakout_task_type:
            print("Error loading breakout_task_type, aborting")
            return False
        
        self.breakout_task = gazu.task.get_task_by_entity(self.shot, breakout_task_type)
        if not self.breakout_task:
            print("Breakout Task for Shot {} not found, aborting".format(self.shot))
            return False

        self.shot_path = gazu.files.build_working_file_path(self.breakout_task)
        self.shot_path = os.path.normpath(self.shot_path.replace("/mnt/content/productions", SwingSettings.get_instance().shared_root()))

        self.lineEditExportDir.setText(os.path.dirname(self.shot_path))
        print(F"Loaded layout shot {self.shot} {self.shot_path}")
        ##edits = gazu.edit.all_edits_for_project(self.task["project"])

    def select_xml_file(self):
        q = QtWidgets.QFileDialog.getOpenFileName(self, "Open Editorial XML File", self.last_xml_file, "XML (*.xml);; All Files (*.*)")
        if (q and q[0] != ''):     
            self.last_xml_file = q[0]
            self.lineEditXmlFile.setText(q[0])

            export_dir = os.path.dirname(self.last_xml_file)
            export_dir = os.path.join(export_dir, "exports")
            if os.path.exists(export_dir):
                self.lineEditExportDir.setText(os.path.normpath(export_dir))

            self.read_xml()

    def select_export_dir(self):
        q = QtWidgets.QFileDialog.getExistingDirectory(self, "Select directory containing shots and audio", self.last_export_dir)
        if q:
            self.last_export_dir = q            
            self.lineEditExportDir.setText(q)

    def read_xml(self):
        if not OPEN_TIMELINE:
            print("Open Timeline not installed")
            return False

        file_parts = os.path.basename(self.lineEditXmlFile.text()).split("_")
        prefix = "{}_{}".format(file_parts[0], file_parts[1])
        self.lineEditShotPrefix.setText(prefix)

        timeline = otio.adapters.read_from_file(self.lineEditXmlFile.text())
        self.build_sequence(timeline)        

    def build_sequence(self, timeline):
        if not OPEN_TIMELINE:
            print("Open Timeline not installed")
            return False

        tracks = [
            track for track in timeline.tracks
            if track.kind == otio.schema.TrackKind.Video
        ]

        track_index = 1

        for track_no, track in enumerate(reversed(tracks)):
            if len(track) > 0:
                self.build_track(track, track_index)
                track_index += 1

    def build_track(self, track, track_no):
        if not OPEN_TIMELINE:
            print("Open Timeline not installed")
            return False

        shots = []

        ##prefix = self.lineEditShotPrefix.text()
        ## overriding prefix for SDMP for now
        ## prefix = ""

        target_dir = self.lineEditExportDir.text()

        start_frame = 0

        for n, item in enumerate(track):
            if not isinstance(item, otio.schema.Clip):
                continue

            name, extension = os.path.splitext(item.name)            

            if extension not in SequencerShotCreator.ALLOWED_MOVIE_EXTENSION:
                continue

            if not name.lower().startswith("sc"):
                continue             

            track_range = track.range_of_child_at_index(n)
            item_name = item.name

            for clip_item in CLEAN_NAME:
                if clip_item in item_name:
                    #print("Cleaning {} from {}".format(clip_item, item_name))
                    item_name = item_name.replace(clip_item, "")            

            shot_parts = item_name.split("_")

            if len(shot_parts) >= 3:
                sequence_name = shot_parts[1]
                shot_name = shot_parts[2]

                item_name = "{}_{}_{}".format(shot_parts[0], sequence_name, shot_name)
            else:
                sequence_name = shot_parts[0]
                shot_name = shot_parts[1]

                item_name = "{}_{}_{}".format(self.episode["name"], sequence_name, shot_name)              

            print(F"Scanning Shot {item_name} Sequence {self.sequence['name']}")                    

            if self.sequence and self.checkBoxFilterTask.isChecked():
                scene = "_{}_".format(self.sequence["name"].lower())
                print("Checking {} against {}".format(scene, item_name.lower()))
                if not scene in item_name.lower():
                    print("Skipping item {} not in sequence {}".format(item_name, self.sequence["name"]))
                    continue

            #item_name = "{}_{}".format(prefix, item_name.lower())
            ## V:\productions\HNL\hnl_work\shots\hnl_ep000\sc010\sh000\breakout\sc010_sh000_breakout
            master_scene = self.shot_path
            master_scene = self.shot_path.replace(self.sequence['name'], sequence_name)
            master_scene = self.shot_path.replace("sh000", shot_name)

            print(F"Checking {master_scene}")

            ## images_dir = os.path.join(target_dir, "{}".format(item_name), "images")
            images_dir = master_scene
            if not os.path.exists(images_dir):
                print("Skipping images_dir {} not found".format(images_dir))
                image_plane = None
            else:
                image_plane = os.path.normpath(os.path.join(images_dir, "{}.0000.jpg".format(item_name)))
                if not os.path.exists(image_plane):
                    print("build_track::image_plane missing {}".format(image_plane))
                    image_plane = None

            audio_file = None
            if self.checkBoxImportAudio.isChecked():   
                ## audio_dir = os.path.join(target_dir, "{}".format(item_name), "audio")
                audio_dir = master_scene
                if os.path.exists(audio_dir):
                    audio_file = os.path.normpath(os.path.join(audio_dir, "{}.wav".format(item_name)))
                    if not os.path.exists(audio_file):
                        print("build_track::audio_file missing {}".format(audio_file))      
                        audio_file = None

            #shot_parts = item_name.split("_")
            #shot = "{}_{}_{}".format(shot_parts[0], shot_parts[1], shot_parts[2])

            #shot = "{}".format(item_name).lower()
            camera = "{}_cam".format(item_name)

            frame_count = track_range.end_time_exclusive().value - track_range.start_time.value - 1

            shot = {
                "id": item_name,
                "e": False,
                "shotName": item_name,
                "track": track_no,
                "currentCamera": camera,
                #"startTime": track_range.start_time.value + 1,
                #"endTime": track_range.end_time_exclusive().value,
                #"sequencerStartTime": track_range.start_time.value + 1,
                #"sequencerEndTime": track_range.end_time_exclusive().value,
                "startTime": start_frame,
                "endTime": start_frame + frame_count,
                "sequencerStartTime": start_frame, 
                "sequencerEndTime": start_frame + frame_count,
                "audio": audio_file,
                "image_plane": image_plane,
                "padding": self.spinBoxPadShots.value()
            }                         

            shots.append(shot)
            start_frame = start_frame + frame_count + self.spinBoxPadShots.value()

        self.model = SequencerShotTableModel(self, shots)
        self.tableView.setModel(self.model)

    
    # save main dialog state
    def write_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)

        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

        self.settings.setValue("last_xml_file", self.last_xml_file)
        self.settings.setValue("last_export_dir", self.last_export_dir)

        if self.groupBoxImagePlane.isChecked():
            self.settings.setValue("image_plane", "True")
        else:
            self.settings.setValue("image_plane", "False")

        if self.checkBoxFilterTask.isChecked():
            self.settings.setValue("filter_task", "True")
        else:
            self.settings.setValue("filter_task", "False")

        if self.checkBoxImportAudio.isChecked():
            self.settings.setValue("import_audio", "True")
        else:
            self.settings.setValue("import_audio", "False")

        #self.settings.setValue("software", self.comboBoxSoftware.currentText())

        #self.settings.setValue("output_dir_path_le", self.output_dir_path_le.text())
        #self.settings.setValue("output_filename_le", self.output_filename_le.text())
        
        self.settings.endGroup()

    # load main dialog state
    def read_settings(self):
        self.settings = QtCore.QSettings()
        self.settings.beginGroup(self.__class__.__name__)
        
        self.resize(self.settings.value("size", QtCore.QSize(480, 520)))
        ##self.move(self.settings.value("pos", QtCore.QPoint(0, 200)))

        self.last_xml_file = self.settings.value("last_xml_file", os.path.expanduser("~"))
        self.last_export_dir = self.settings.value("last_export_dir", os.path.expanduser("~"))

        self.groupBoxImagePlane.setChecked(self.settings.value("image_plane", "True") == "True")
        self.checkBoxFilterTask.setChecked(self.settings.value("filter_task", "True") == "True")
        self.checkBoxImportAudio.setChecked(self.settings.value("import_audio", "True") == "True")

        self.settings.endGroup()            

    def is_all_selected(self):
        all_selected = True
        for i in range(len(self.model.shots)):
            all_selected = all_selected and self.model.shots[i]["selected"]
        return all_selected

    def select_none(self):
        for i in range(len(self.model.shots)):
            index = self.model.index(i, SequencerShotTableModel.COL_SELECTED)
            self.model.setData(index, False, QtCore.Qt.EditRole)

    def select_all(self):
        for i in range(len(self.model.shots)):
            index = self.model.index(i, SequencerShotTableModel.COL_SELECTED)
            self.model.setData(index, True, QtCore.Qt.EditRole)

    def get_selected(self):
        selected = []
        for i in range(len(self.model.shots)):
            if self.model.shots[i]["selected"]:
                selected.append(self.model.shots[i])
        return selected

    def process(self):
        self.write_settings()

        if self.groupBoxImagePlane.isChecked():
            image_plane = {
                "alphaGain": self.doubleSpinBoxAlphaGain.value(),
                "sizeX": self.doubleSpinBoxSizeX.value(),
                "offsetX": self.doubleSpinBoxOffsetX.value(),
                "offsetY": self.doubleSpinBoxOffsetY.value()
            }
        else:
            image_plane = None

        if self.groupBoxShotPadding.isChecked():
            padding = self.spinBoxPadShots.value()
        else:
            padding = None

        export_dir = self.lineEditExportDir.text()            

        self.handler.on_sequencer_create_shots(shot_list = self.model.shots, fps = self.fps, image_plane = image_plane, padding = padding, export_dir = export_dir)
        self.status = 'OK'

        self.close()        
        QtWidgets.QMessageBox.information(self, 'swing: shot sequencer', 'Shots created')               


    def cancel_dialog(self):
        self.status = 'Cancel'
        self.close()                    