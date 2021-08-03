# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'swing_export.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from wildchildanimation.gui.swing_utils import fakestr

class Ui_SwingExport(object):
    def setupUi(self, SwingExport):
        if not SwingExport.objectName():
            SwingExport.setObjectName(u"SwingExport")
        SwingExport.resize(503, 357)
        self.verticalLayout = QVBoxLayout(SwingExport)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelTask = QLabel(SwingExport)
        self.labelTask.setObjectName(u"labelTask")
        self.labelTask.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.labelTask)

        self.lineEditEntityName = QLineEdit(SwingExport)
        self.lineEditEntityName.setObjectName(u"lineEditEntityName")
        self.lineEditEntityName.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEditEntityName)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(SwingExport)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.lineEditPath = QLineEdit(SwingExport)
        self.lineEditPath.setObjectName(u"lineEditPath")

        self.horizontalLayout_3.addWidget(self.lineEditPath)

        self.output_dir_path_select_btn = QToolButton(SwingExport)
        self.output_dir_path_select_btn.setObjectName(u"output_dir_path_select_btn")

        self.horizontalLayout_3.addWidget(self.output_dir_path_select_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayoutAlembic = QHBoxLayout()
        self.horizontalLayoutAlembic.setObjectName(u"horizontalLayoutAlembic")
        self.label_3 = QLabel(SwingExport)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))

        self.horizontalLayoutAlembic.addWidget(self.label_3)

        self.comboBoxAlembicSelection = QComboBox(SwingExport)
        self.comboBoxAlembicSelection.addItem("")
        self.comboBoxAlembicSelection.addItem("")
        self.comboBoxAlembicSelection.setObjectName(u"comboBoxAlembicSelection")
        self.comboBoxAlembicSelection.setMinimumSize(QSize(150, 0))

        self.horizontalLayoutAlembic.addWidget(self.comboBoxAlembicSelection)

        self.horizontalSpacerAlembic = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutAlembic.addItem(self.horizontalSpacerAlembic)


        self.verticalLayout.addLayout(self.horizontalLayoutAlembic)

        self.line = QFrame(SwingExport)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(SwingExport)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.frame_range_cmb = QComboBox(SwingExport)
        self.frame_range_cmb.setObjectName(u"frame_range_cmb")
        self.frame_range_cmb.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.frame_range_cmb)

        self.frame_range_start_sb = QSpinBox(SwingExport)
        self.frame_range_start_sb.setObjectName(u"frame_range_start_sb")
        self.frame_range_start_sb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.frame_range_start_sb.setMaximum(9999999)

        self.horizontalLayout_2.addWidget(self.frame_range_start_sb)

        self.labelFrameRangeX = QLabel(SwingExport)
        self.labelFrameRangeX.setObjectName(u"labelFrameRangeX")
        self.labelFrameRangeX.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.labelFrameRangeX)

        self.frame_range_end_sb = QSpinBox(SwingExport)
        self.frame_range_end_sb.setObjectName(u"frame_range_end_sb")
        self.frame_range_end_sb.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.frame_range_end_sb.setMaximum(9999999)

        self.horizontalLayout_2.addWidget(self.frame_range_end_sb)

        self.horizontalSpacerFrameRange = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacerFrameRange)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line_2 = QFrame(SwingExport)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.treeWidget = QTreeWidget(SwingExport)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout.addWidget(self.treeWidget)

        self.horizontalLayoutDialog = QHBoxLayout()
        self.horizontalLayoutDialog.setObjectName(u"horizontalLayoutDialog")
        self.horizontalSpacerDialog = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayoutDialog.addItem(self.horizontalSpacerDialog)

        self.pushButtonExport = QPushButton(SwingExport)
        self.pushButtonExport.setObjectName(u"pushButtonExport")
        self.pushButtonExport.setMinimumSize(QSize(85, 0))

        self.horizontalLayoutDialog.addWidget(self.pushButtonExport)

        self.pushButtonClose = QPushButton(SwingExport)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayoutDialog.addWidget(self.pushButtonClose)


        self.verticalLayout.addLayout(self.horizontalLayoutDialog)


        self.retranslateUi(SwingExport)

        QMetaObject.connectSlotsByName(SwingExport)
    # setupUi

    def retranslateUi(self, SwingExport):
        SwingExport.setWindowTitle(fakestr(u"Swing: Export", None))
        self.labelTask.setText(fakestr(u"Task", None))
        self.label_2.setText(fakestr(u"Path:", None))
        self.output_dir_path_select_btn.setText(fakestr(u"...", None))
        self.label_3.setText(fakestr(u"Select:", None))
        self.comboBoxAlembicSelection.setItemText(0, fakestr(u"All", None))
        self.comboBoxAlembicSelection.setItemText(1, fakestr(u"Selected", None))

        self.label.setText(fakestr(u"Time Range", None))
        self.labelFrameRangeX.setText(fakestr(u" - ", None))
        self.pushButtonExport.setText(fakestr(u"Export", None))
        self.pushButtonClose.setText(fakestr(u"Close", None))
    # retranslateUi

