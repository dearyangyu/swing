# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dcc_tools.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr


class Ui_DCCToolsDialog(object):
    def setupUi(self, DCCToolsDialog):
        if not DCCToolsDialog.objectName():
            DCCToolsDialog.setObjectName(u"DCCToolsDialog")
        DCCToolsDialog.resize(410, 248)
        self.verticalLayout = QVBoxLayout(DCCToolsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditEntityName = QLineEdit(DCCToolsDialog)
        self.lineEditEntityName.setObjectName(u"lineEditEntityName")
        self.lineEditEntityName.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEditEntityName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayoutFbx = QHBoxLayout()
        self.horizontalLayoutFbx.setObjectName(u"horizontalLayoutFbx")
        self.pushButtonFbxExport = QPushButton(DCCToolsDialog)
        self.pushButtonFbxExport.setObjectName(u"pushButtonFbxExport")
        self.pushButtonFbxExport.setMinimumSize(QSize(85, 0))

        self.horizontalLayoutFbx.addWidget(self.pushButtonFbxExport)

        self.labelFbxSelection = QLabel(DCCToolsDialog)
        self.labelFbxSelection.setObjectName(u"labelFbxSelection")
        self.labelFbxSelection.setMinimumSize(QSize(50, 0))
        self.labelFbxSelection.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayoutFbx.addWidget(self.labelFbxSelection)

        self.comboBoxFbxSelection = QComboBox(DCCToolsDialog)
        self.comboBoxFbxSelection.addItem("")
        self.comboBoxFbxSelection.addItem("")
        self.comboBoxFbxSelection.setObjectName(u"comboBoxFbxSelection")

        self.horizontalLayoutFbx.addWidget(self.comboBoxFbxSelection)

        self.horizontalSpacerFbx = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutFbx.addItem(self.horizontalSpacerFbx)


        self.verticalLayout.addLayout(self.horizontalLayoutFbx)

        self.horizontalLayoutAlembic = QHBoxLayout()
        self.horizontalLayoutAlembic.setObjectName(u"horizontalLayoutAlembic")
        self.pushButtonAlembicExport = QPushButton(DCCToolsDialog)
        self.pushButtonAlembicExport.setObjectName(u"pushButtonAlembicExport")
        self.pushButtonAlembicExport.setMinimumSize(QSize(85, 0))

        self.horizontalLayoutAlembic.addWidget(self.pushButtonAlembicExport)

        self.labelAlembicSelection = QLabel(DCCToolsDialog)
        self.labelAlembicSelection.setObjectName(u"labelAlembicSelection")
        self.labelAlembicSelection.setMinimumSize(QSize(50, 0))
        self.labelAlembicSelection.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayoutAlembic.addWidget(self.labelAlembicSelection)

        self.comboBoxAlembicSelection = QComboBox(DCCToolsDialog)
        self.comboBoxAlembicSelection.addItem("")
        self.comboBoxAlembicSelection.addItem("")
        self.comboBoxAlembicSelection.setObjectName(u"comboBoxAlembicSelection")

        self.horizontalLayoutAlembic.addWidget(self.comboBoxAlembicSelection)

        self.horizontalSpacerAlembic = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutAlembic.addItem(self.horizontalSpacerAlembic)


        self.verticalLayout.addLayout(self.horizontalLayoutAlembic)

        self.line = QFrame(DCCToolsDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(DCCToolsDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(80, 0))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.comboBoxFrameRange = QComboBox(DCCToolsDialog)
        self.comboBoxFrameRange.setObjectName(u"comboBoxFrameRange")

        self.horizontalLayout_2.addWidget(self.comboBoxFrameRange)

        self.horizontalSpacerFrameRange = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacerFrameRange)

        self.spinBoxStart = QSpinBox(DCCToolsDialog)
        self.spinBoxStart.setObjectName(u"spinBoxStart")
        self.spinBoxStart.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxStart.setMaximum(9999999)

        self.horizontalLayout_2.addWidget(self.spinBoxStart)

        self.labelFrameRangeX = QLabel(DCCToolsDialog)
        self.labelFrameRangeX.setObjectName(u"labelFrameRangeX")
        self.labelFrameRangeX.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.labelFrameRangeX)

        self.spinBoxEnd = QSpinBox(DCCToolsDialog)
        self.spinBoxEnd.setObjectName(u"spinBoxEnd")
        self.spinBoxEnd.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxEnd.setMaximum(9999999)

        self.horizontalLayout_2.addWidget(self.spinBoxEnd)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line_2 = QFrame(DCCToolsDialog)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayoutDialog = QHBoxLayout()
        self.horizontalLayoutDialog.setObjectName(u"horizontalLayoutDialog")
        self.horizontalSpacerDialog = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutDialog.addItem(self.horizontalSpacerDialog)

        self.pushButtonDialog = QPushButton(DCCToolsDialog)
        self.pushButtonDialog.setObjectName(u"pushButtonDialog")

        self.horizontalLayoutDialog.addWidget(self.pushButtonDialog)


        self.verticalLayout.addLayout(self.horizontalLayoutDialog)


        self.retranslateUi(DCCToolsDialog)

        QMetaObject.connectSlotsByName(DCCToolsDialog)
    # setupUi

    def retranslateUi(self, DCCToolsDialog):
        DCCToolsDialog.setWindowTitle(fakestr(u"Swing: Export", None))
        self.pushButtonFbxExport.setText(fakestr(u"Export FBX", None))
        self.labelFbxSelection.setText(fakestr(u"selection:", None))
        self.comboBoxFbxSelection.setItemText(0, fakestr(u"All", None))
        self.comboBoxFbxSelection.setItemText(1, fakestr(u"Selected", None))

        self.pushButtonAlembicExport.setText(fakestr(u"Export Alembic", None))
        self.labelAlembicSelection.setText(fakestr(u"selection:", None))
        self.comboBoxAlembicSelection.setItemText(0, fakestr(u"All", None))
        self.comboBoxAlembicSelection.setItemText(1, fakestr(u"Selected", None))

        self.label.setText(fakestr(u"Frame Range:", None))
        self.labelFrameRangeX.setText(fakestr(u" - ", None))
        self.pushButtonDialog.setText(fakestr(u"Close", None))
    # retranslateUi

