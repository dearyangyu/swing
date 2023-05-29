from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_Name_Validator(object):

    def setupUI(self, Name_Validator):
        if not Name_Validator.objectName():
            Name_Validator.setObjectName(u"Name Validator")
        Name_Validator.setWindowModality(Qt.WindowModal)
        Name_Validator.resize(680, 460)

        self.verticalLayout_2 = QVBoxLayout(Name_Validator)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        '''
        self.labelMatNoPrefx = QLabel(Name_Validator)
        self.labelMatNoPrefx.setObjectName(u"labelMatNoPrefx")
        self.verticalLayout.addWidget(self.labelMatNoPrefx)

        self.listMatNoPrefx = QListWidget()
        self.listMatNoPrefx.setObjectName(u"listMatNoPrefx")
        self.verticalLayout.addWidget(self.listMatNoPrefx)
        self.listMatNoPrefx.setSortingEnabled(True)
        self.listMatNoPrefx.installEventFilter(self)
        self.listMatNoPrefx.sortItems(Qt.SortOrder.AscendingOrder)
        '''
        self.labelTex = QLabel(Name_Validator)
        self.labelTex.setObjectName(u"labelTex")
        self.verticalLayout.addWidget(self.labelTex)

        self.listTex = QListWidget()
        self.listTex.setObjectName(u"listTex")
        self.verticalLayout.addWidget(self.listTex)
        self.listTex.setSortingEnabled(True)
        self.listTex.installEventFilter(self)
        self.listTex.sortItems(Qt.SortOrder.AscendingOrder)

        self.labelMatNoTex = QLabel(Name_Validator)
        self.labelMatNoTex.setObjectName(u"labelMatNoTex")
        self.verticalLayout.addWidget(self.labelMatNoTex)

        self.listMatIncorrect = QListWidget()
        self.listMatIncorrect.setObjectName(u"listMatIncorrect")
        self.listMatIncorrect.setSortingEnabled(True)
        self.listMatIncorrect.sortItems(Qt.SortOrder.AscendingOrder)
        self.listMatIncorrect.installEventFilter(self)
        self.verticalLayout.addWidget(self.listMatIncorrect)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(self.verticalSpacer)
        self.verticalLayout_2.addLayout(self.verticalLayout)
    
        self.search_btn = QPushButton()
        self.search_btn.setObjectName(u"search_btn")
        self.verticalLayout_2.addWidget(self.search_btn)

        self.add_prefix_btn = QPushButton()
        self.add_prefix_btn.setObjectName(u"add_prefix_btn")
        self.verticalLayout_2.addWidget(self.add_prefix_btn)

        self.rename_btn = QPushButton()
        self.rename_btn.setObjectName(u"rename_btn")
        self.verticalLayout_2.addWidget(self.rename_btn)

        self.retranslateUi(Name_Validator)
        
        QMetaObject.connectSlotsByName(Name_Validator)


    def retranslateUi(self, Name_Validator):
        Name_Validator.setWindowTitle(fakestr(u"Name Validator", None))
        #self.labelMatNoPrefx.setText(fakestr(u"Materials on geo without 'mi_'prefix:", None))
        self.labelTex.setText(fakestr(u"Textures without Materials in selection:", None))
        self.labelMatNoTex.setText(fakestr(u"Materials without textures or named incorrectly in selection:", None))
        self.search_btn.setText("Search")
        self.add_prefix_btn.setText("Rename: add mi_ prefix")
        self.rename_btn.setText("Rename: material on texture selection")

    
