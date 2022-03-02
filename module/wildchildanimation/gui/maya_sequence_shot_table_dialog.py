# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sequence_shot_table_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_SequenceShotTableDialog(object):
    def setupUi(self, SequenceShotTableDialog):
        if not SequenceShotTableDialog.objectName():
            SequenceShotTableDialog.setObjectName(u"SequenceShotTableDialog")
        SequenceShotTableDialog.resize(699, 556)
        self.verticalLayout_5 = QVBoxLayout(SequenceShotTableDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableView = QTableView(SequenceShotTableDialog)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_5.addWidget(self.tableView)

        self.groupBox_2 = QGroupBox(SequenceShotTableDialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelXmlFile = QLabel(self.groupBox_2)
        self.labelXmlFile.setObjectName(u"labelXmlFile")
        self.labelXmlFile.setMinimumSize(QSize(100, 0))
        self.labelXmlFile.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_5.addWidget(self.labelXmlFile)

        self.lineEditXmlFile = QLineEdit(self.groupBox_2)
        self.lineEditXmlFile.setObjectName(u"lineEditXmlFile")

        self.horizontalLayout_5.addWidget(self.lineEditXmlFile)

        self.toolButtonXmlFile = QToolButton(self.groupBox_2)
        self.toolButtonXmlFile.setObjectName(u"toolButtonXmlFile")

        self.horizontalLayout_5.addWidget(self.toolButtonXmlFile)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.labelExportDir = QLabel(self.groupBox_2)
        self.labelExportDir.setObjectName(u"labelExportDir")
        self.labelExportDir.setMinimumSize(QSize(100, 0))
        self.labelExportDir.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_6.addWidget(self.labelExportDir)

        self.lineEditExportDir = QLineEdit(self.groupBox_2)
        self.lineEditExportDir.setObjectName(u"lineEditExportDir")

        self.horizontalLayout_6.addWidget(self.lineEditExportDir)

        self.toolButtonExportDir = QToolButton(self.groupBox_2)
        self.toolButtonExportDir.setObjectName(u"toolButtonExportDir")

        self.horizontalLayout_6.addWidget(self.toolButtonExportDir)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelShotPrefix = QLabel(self.groupBox_2)
        self.labelShotPrefix.setObjectName(u"labelShotPrefix")
        self.labelShotPrefix.setMinimumSize(QSize(100, 0))
        self.labelShotPrefix.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_3.addWidget(self.labelShotPrefix)

        self.lineEditShotPrefix = QLineEdit(self.groupBox_2)
        self.lineEditShotPrefix.setObjectName(u"lineEditShotPrefix")

        self.horizontalLayout_3.addWidget(self.lineEditShotPrefix)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.checkBoxFilterTask = QCheckBox(SequenceShotTableDialog)
        self.checkBoxFilterTask.setObjectName(u"checkBoxFilterTask")
        self.checkBoxFilterTask.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBoxFilterTask)

        self.checkBoxImportAudio = QCheckBox(SequenceShotTableDialog)
        self.checkBoxImportAudio.setObjectName(u"checkBoxImportAudio")
        self.checkBoxImportAudio.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBoxImportAudio)

        self.groupBoxImagePlane = QGroupBox(SequenceShotTableDialog)
        self.groupBoxImagePlane.setObjectName(u"groupBoxImagePlane")
        self.groupBoxImagePlane.setCheckable(True)
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxImagePlane)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.labeAlphaGain = QLabel(self.groupBoxImagePlane)
        self.labeAlphaGain.setObjectName(u"labeAlphaGain")

        self.horizontalLayout_4.addWidget(self.labeAlphaGain)

        self.doubleSpinBoxAlphaGain = QDoubleSpinBox(self.groupBoxImagePlane)
        self.doubleSpinBoxAlphaGain.setObjectName(u"doubleSpinBoxAlphaGain")
        self.doubleSpinBoxAlphaGain.setValue(0.500000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxAlphaGain)

        self.labelSizeX = QLabel(self.groupBoxImagePlane)
        self.labelSizeX.setObjectName(u"labelSizeX")

        self.horizontalLayout_4.addWidget(self.labelSizeX)

        self.doubleSpinBoxSizeX = QDoubleSpinBox(self.groupBoxImagePlane)
        self.doubleSpinBoxSizeX.setObjectName(u"doubleSpinBoxSizeX")
        self.doubleSpinBoxSizeX.setValue(0.500000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxSizeX)

        self.labelOffsetX = QLabel(self.groupBoxImagePlane)
        self.labelOffsetX.setObjectName(u"labelOffsetX")

        self.horizontalLayout_4.addWidget(self.labelOffsetX)

        self.doubleSpinBoxOffsetX = QDoubleSpinBox(self.groupBoxImagePlane)
        self.doubleSpinBoxOffsetX.setObjectName(u"doubleSpinBoxOffsetX")
        self.doubleSpinBoxOffsetX.setValue(0.460000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxOffsetX)

        self.labelOffsetY = QLabel(self.groupBoxImagePlane)
        self.labelOffsetY.setObjectName(u"labelOffsetY")

        self.horizontalLayout_4.addWidget(self.labelOffsetY)

        self.doubleSpinBoxOffsetY = QDoubleSpinBox(self.groupBoxImagePlane)
        self.doubleSpinBoxOffsetY.setObjectName(u"doubleSpinBoxOffsetY")
        self.doubleSpinBoxOffsetY.setValue(0.260000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBoxOffsetY)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_5.addWidget(self.groupBoxImagePlane)

        self.groupBoxShotPadding = QGroupBox(SequenceShotTableDialog)
        self.groupBoxShotPadding.setObjectName(u"groupBoxShotPadding")
        self.groupBoxShotPadding.setCheckable(True)
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxShotPadding)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelShotPadding = QLabel(self.groupBoxShotPadding)
        self.labelShotPadding.setObjectName(u"labelShotPadding")
        self.labelShotPadding.setMinimumSize(QSize(100, 0))
        self.labelShotPadding.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.labelShotPadding)

        self.spinBoxPadShots = QSpinBox(self.groupBoxShotPadding)
        self.spinBoxPadShots.setObjectName(u"spinBoxPadShots")
        self.spinBoxPadShots.setMaximum(999999)
        self.spinBoxPadShots.setValue(100)

        self.horizontalLayout_2.addWidget(self.spinBoxPadShots)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_5.addWidget(self.groupBoxShotPadding)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.buttonAll = QPushButton(SequenceShotTableDialog)
        self.buttonAll.setObjectName(u"buttonAll")

        self.horizontalLayout.addWidget(self.buttonAll)

        self.buttonClear = QPushButton(SequenceShotTableDialog)
        self.buttonClear.setObjectName(u"buttonClear")

        self.horizontalLayout.addWidget(self.buttonClear)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.buttonCancel = QPushButton(SequenceShotTableDialog)
        self.buttonCancel.setObjectName(u"buttonCancel")

        self.horizontalLayout.addWidget(self.buttonCancel)

        self.buttonCreateShots = QPushButton(SequenceShotTableDialog)
        self.buttonCreateShots.setObjectName(u"buttonCreateShots")
        self.buttonCreateShots.setMinimumSize(QSize(100, 0))
        self.buttonCreateShots.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.buttonCreateShots)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.retranslateUi(SequenceShotTableDialog)

        self.buttonCreateShots.setDefault(True)


        QMetaObject.connectSlotsByName(SequenceShotTableDialog)
    # setupUi

    def retranslateUi(self, SequenceShotTableDialog):
        SequenceShotTableDialog.setWindowTitle(fakestr(u"Dialog", None))
        self.groupBox_2.setTitle(fakestr(u"Editorial", None))
        self.labelXmlFile.setText(fakestr(u"XML File", None))
        self.toolButtonXmlFile.setText(fakestr(u"...", None))
        self.labelExportDir.setText(fakestr(u"Export Dir", None))
        self.toolButtonExportDir.setText(fakestr(u"...", None))
        self.labelShotPrefix.setText(fakestr(u"Shot Prefix", None))
        self.checkBoxFilterTask.setText(fakestr(u"Filter by Task", None))
        self.checkBoxImportAudio.setText(fakestr(u"Import Audio ", None))
        self.groupBoxImagePlane.setTitle(fakestr(u"Image Plane", None))
        self.labeAlphaGain.setText(fakestr(u"alphaGain", None))
        self.labelSizeX.setText(fakestr(u"sizeX", None))
        self.labelOffsetX.setText(fakestr(u"Offset X", None))
        self.labelOffsetY.setText(fakestr(u"Offset Y", None))
        self.groupBoxShotPadding.setTitle(fakestr(u"Shot Padding", None))
        self.labelShotPadding.setText(fakestr(u"Pad Shots", None))
        self.buttonAll.setText(fakestr(u"All", None))
        self.buttonClear.setText(fakestr(u"None", None))
        self.buttonCancel.setText(fakestr(u"Cancel", None))
        self.buttonCreateShots.setText(fakestr(u"Create Shots", None))
    # retranslateUi

