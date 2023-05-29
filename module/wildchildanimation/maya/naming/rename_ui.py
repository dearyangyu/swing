from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from wildchildanimation.gui.swing_utils import fakestr

class Ui_Rename(QDialog):

    def setupUI(self):
        self.setWindowTitle("Rename File")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(380, 360)

        self.verticalLayout_2 = QVBoxLayout(self)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        self.labelMat = QLabel(self)
        self.labelMat.setObjectName(u"labelMat")
        self.verticalLayout.addWidget(self.labelMat)

        self.listMaterial = QListWidget()
        self.listMaterial.setObjectName(u"listMaterial")
        self.verticalLayout.addWidget(self.listMaterial)
        self.listMaterial.setSortingEnabled(True)
        self.listMaterial.installEventFilter(self)
        self.listMaterial.sortItems(Qt.SortOrder.AscendingOrder)
        QListWidgetItem("Rename ME", self.listMaterial)

        self.labelTexNoMat = QLabel(self)
        self.labelTexNoMat.setObjectName(u"labelPreset")
        self.verticalLayout.addWidget(self.labelTexNoMat)

        self.listMatTexIncorrect = QListWidget()
        self.listMatTexIncorrect.setObjectName(u"listMatTexIncorrect")
        self.listMatTexIncorrect.setSortingEnabled(True)
        self.listMatTexIncorrect.sortItems(Qt.SortOrder.AscendingOrder)
        self.listMatTexIncorrect.installEventFilter(self)
        self.verticalLayout.addWidget(self.listMatTexIncorrect)
        QListWidgetItem("t_Texture_List", self.listMatTexIncorrect)
        
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout)
        
        # This might not be needed but left it here just incase
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.rename_btn = QPushButton()
        self.rename_btn.setObjectName(u"rename_btn")
        self.buttonBox.addButton(self.rename_btn, QDialogButtonBox.AcceptRole)
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
  

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)
        
 
    def retranslateUi(self):
        self.setWindowTitle(fakestr(u"Rename File", None))
        self.labelMat.setText(fakestr(u"Textures without Materials in selection:", None))
        self.labelTexNoMat.setText(fakestr(u"Materials without textures or named incorrectly in selection:", None))
        self.rename_btn.setText("Rename")

    
