'''
    Set to folder containing module/ and plugin/
'''
WCA_ROOT = "C:/WCA/wca-maya-main"

import sys
sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))

# Load Zurbrigg Playblaster
from wildchildanimation.gui.zurbrigg_playblast import ZurbriggPlayblastUi
ZurbriggPlayblastUi.show_dialog()

