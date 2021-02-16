import sys

import PySide2.QtWidgets
import PySide2.QtGui
from PySide2.QtWidgets import QApplication, QWidget

sys.path.append("C:\\DEV\\Github\\wca-maya\\module")
from wildchildanimation.swing_gui import SwingGUI

# studio specific import callbacks 
from maya_handlers import StudioHandler
handler = StudioHandler()    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = SwingGUI(handler)
    ex.show()
    sys.exit(app.exec_())
else:
    ex = SwingGUI(handler)
# entry point    
