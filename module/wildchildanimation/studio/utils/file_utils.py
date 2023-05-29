# -*- coding: utf-8 -*-
#
# File Utility functions
#
# Author: P Niemandt
# Date: 2023-02-13
# Version: 1.00

import argparse
import os
import glob
from pathlib import Path
import csv

def process(args):
    start_dir = args.dir
    file_types = args.type

    glob_str = "{}/**/{}".format(start_dir, "*.tpl")
    print("Glob: {}".format(glob_str))    

    with open('D:/dev/file_list.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for fn in Path(start_dir).rglob("*.tpl"):
            writer.writerow([fn.name, fn.parent])
            print(fn)


    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='Source directory', default='None')
    parser.add_argument('-t', '--type', help="Type of directories to search for: Toonboom => *.tpl")

    args = parser.parse_args()
    process(args)



