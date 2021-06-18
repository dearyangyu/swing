# -*- coding: utf-8 -*-
_VERSION = "1.00"

import argparse
import sys

sys.path.append("./module")
from wildchildanimation.gui.swing_updater import update

import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help = "Target dir", default = None, action='store')

    args = parser.parse_args()
    update(args.dir)