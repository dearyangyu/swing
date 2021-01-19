import sys
import pprint

from pyside2uic import compileUi

import os 


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))

    pyfile = open(dir_path + "/src/wcamaya/wcamaya-gui.py", 'w')
    compileUi(dir_path + "/gui/forms/wca-tools/form.ui", pyfile, False, 4, False)
    pyfile.close()

