'''
    Set to folder containing module/ and plugin/
'''

#WCA_ROOT = "Z:/env/maya/treehouse/wca-maya/"
#WCA_ROOT = "C:/DEV/github/wca-maya/"
WCA_ROOT = "C:/WCA/wca-maya/"

import sys
import argparse
import pprint

#sys.path.append("{0}/{1}".format(WCA_ROOT, "/module"))
#from wildchildanimation.swing_gui import SwingGUI

# studio specific import callbacks 
sys.path.append("{0}/{1}".format(WCA_ROOT, "/plugin/treehouse"))

def _main(args):
    if args.dir is None:
        print("scanning for {}".format(WCA_ROOT))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default = None, action='store_true')
    args  = parser.parse_args()
    _main(parser.parse_args())
# entry point    
