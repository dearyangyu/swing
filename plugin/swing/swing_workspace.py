from functools import partial

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from PySide2.QtWidgets import QLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy, QPushButton, QSpacerItem, QLineEdit, QLabel, QSpacerItem, QCheckBox
from PySide2.QtCore import QSize

import maya.cmds as cmds

from workspace_control import WorkspaceControl, DockableUI

class SwingWorkspaceUI(DockableUI):

    WINDOW_TITLE = "Swing"
    UI_NAME = "SwingUI"

    def __init__(self):
        super(SwingWorkspaceUI, self).__init__()

        self.setMinimumWidth(300)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.create_actions()
        #self.create_widgets()
        #self.create_layout()
        #self.create_connections()
        #self.create_workspace_control()

    def setupUi(self, widget):
        self.verticalLayout_4 = QVBoxLayout(widget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.projectButton = QPushButton(widget)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectButton.sizePolicy().hasHeightForWidth())

        self.projectButton.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.projectButton)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer_4)
        self.labelSelection = QLabel(widget)
        self.horizontalLayout.addWidget(self.labelSelection)

        self.assetsButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.assetsButton.sizePolicy().hasHeightForWidth())
        self.assetsButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.assetsButton)
        self.shotsButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.shotsButton.sizePolicy().hasHeightForWidth())
        self.shotsButton.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.shotsButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QHBoxLayout()
        self.verticalLayout = QVBoxLayout()
        self.taskButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.taskButton.sizePolicy().hasHeightForWidth())
        self.taskButton.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.taskButton)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.gridLayout = QGridLayout()
        self.epLabel = QLabel(widget)
        self.gridLayout.addWidget(self.epLabel, 2, 0, 1, 1)
        self.shotLael = QLabel(widget)
        self.gridLayout.addWidget(self.shotLael, 5, 0, 1, 1)
        self.projectLabel = QLabel(widget)
        self.gridLayout.addWidget(self.projectLabel, 1, 0, 1, 1)
        self.seqLabel = QLabel(widget)
        self.gridLayout.addWidget(self.seqLabel, 2, 2, 1, 1)
        self.seqEdit = QLineEdit(widget)
        self.gridLayout.addWidget(self.seqEdit, 2, 3, 1, 1)
        self.epEdit = QLineEdit(widget)
        self.gridLayout.addWidget(self.epEdit, 2, 1, 1, 1)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer_3, 6, 0, 1, 1)
        self.assetLabel = QLabel(widget)
        self.gridLayout.addWidget(self.assetLabel, 3, 0, 1, 1)
        self.shotEdit = QLineEdit(widget)
        self.gridLayout.addWidget(self.shotEdit, 5, 1, 1, 3)
        self.assetEdit = QLineEdit(widget)
        self.gridLayout.addWidget(self.assetEdit, 3, 1, 1, 3)
        self.projectEdit = QLineEdit(widget)
        self.gridLayout.addWidget(self.projectEdit, 1, 1, 1, 3)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.playblastButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.playblastButton.sizePolicy().hasHeightForWidth())
        self.playblastButton.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.playblastButton)
        self.updateButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.updateButton.sizePolicy().hasHeightForWidth())
        self.updateButton.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.updateButton)
        self.publishButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.publishButton.sizePolicy().hasHeightForWidth())
        self.publishButton.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.publishButton)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.horizontalLayout_2 = QHBoxLayout()
        self.searchLabel = QLabel(widget)

        self.horizontalLayout_2.addWidget(self.searchLabel)

        self.searchText = QLineEdit(widget)
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.searchText.sizePolicy().hasHeightForWidth())
        self.searchText.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.searchText)

        self.searchButton = QPushButton(widget)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_2.addWidget(self.searchButton)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.label_6 = QLabel(widget)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.projectCheck = QCheckBox(widget)
        self.projectCheck.setChecked(True)

        self.horizontalLayout_3.addWidget(self.projectCheck)

        self.hiddenFilesCheck = QCheckBox(widget)
        self.hiddenFilesCheck.setChecked(True)

        self.horizontalLayout_3.addWidget(self.hiddenFilesCheck)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.projectButton.setText("Project")
        self.labelSelection.setText("No project selected")
        self.assetsButton.setText("Assets")
        self.shotsButton.setText("Shots")
        self.taskButton.setText("Task")
        self.epLabel.setText("Episode")
        self.shotLael.setText("Shot")
        self.projectLabel.setText("Project")
        self.seqLabel.setText("Sequence")
        self.assetLabel.setText("Asset")
        self.playblastButton.setText("Playblast")
        self.updateButton.setText("Update")
        self.publishButton.setText("Publish")
        self.searchLabel.setText("Search")
        self.searchButton.setText("...")
        self.label_6.setText("Filters:")
        self.projectCheck.setText("Project")
        self.hiddenFilesCheck.setText("Hidden Files")


    def create_actions(self):
        self.project_action = QtWidgets.QAction("Project", self)
        self.task_action = QtWidgets.QAction("Task", self)
        self.playblast_action = QtWidgets.QAction("Playblast", self)
        self.publish_action = QtWidgets.QAction("Publish", self)
        self.update_action = QtWidgets.QAction("Update", self)
        self.assets_action = QtWidgets.QAction("Assets", self)
        self.shots_action = QtWidgets.QAction("Shots", self)
        self.search_action = QtWidgets.QAction("Search", self)

    def create_widgets(self):
        self.setupUi(self)

    def create_connections(self):
        pass

if __name__ == "__main__":

    workspace_control_name = SwingWorkspaceUI.get_workspace_control_name()
    if cmds.window(workspace_control_name, exists=True):
        cmds.deleteUI(workspace_control_name)

    SwingWorkspaceUI.module_name_override = "SwingWorkspaceUI"
    control = SwingWorkspaceUI()


