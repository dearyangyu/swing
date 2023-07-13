import zipfile

import os
import sys
import subprocess
import re


from datetime import datetime

import traceback

from wildchildanimation.gui.settings import SwingSettings
from wildchildanimation.gui.swing_utils import extract_archive, scan_archive, fcount

## list the contents of the archive, checking for sub directories
## default to listing all sub directories, if none found, assume content is in top level of archive
## returns a line item: '2023-07-05 11:23:20           83119208     79872331  60 files'
def check_archive_files(archive_name):
    program = SwingSettings.get_instance().bin_7z()
    extract_mode = 'l'
    output_contents = r"*\*"

    print(F"swing::list archive -> {program} {extract_mode} {archive_name}")

    proc = subprocess.Popen([program, extract_mode, archive_name, output_contents], shell = False, stdout=subprocess.PIPE)
    while True:
        output = proc.stdout.readline()
        try:
            log = output.decode('utf-8')
            if log == '' and proc.poll() != None:
                break
            else:
                line = log.strip()
                if "files" in line.lower():
                    return line

        except:
            print(traceback.format_exc())
        # continue

    return None


def extract_zip_contents(archive, directory):
    try:
        #drive_name = directory[:1]
        #os.chdir("{}:".format(drive_name))
        if not os.path.exists(directory):
            os.makedirs(directory)

        os.chdir(directory)

        program = SwingSettings.get_instance().bin_7z()
        extract_mode = 'e'

        time_start = datetime.now()   

        #
        # Extract first folder in .tpl to top level directory
        # this is to cater for the directory being zipped as top level, vs. the content of the directory being zipped
        # 7zip
        # -- working_folder.tpl
        # ---- folder_contents
        #

        if "0 files" in check_archive_files(archive):
            ## if no files found in sub directory, extract root content
            output_contents = r"*"
        else:
            ## if no files found in sub directory, extract sub dir content
            output_contents = r"*\*"

        print(F"Swing::Extracting -> {program} {extract_mode} -y {archive} {output_contents}")

        proc = subprocess.Popen([program, extract_mode, "-y", archive, output_contents], shell = False, stdout=subprocess.PIPE)
        while True:
            output = proc.stdout.readline()
            try:
                log = output.decode('utf-8')
                if log == '' and proc.poll() != None:
                    break
                else:
                    print(log.strip())
            except:
                print(traceback.format_exc())
            # continue

        time_end = datetime.now()
        try:
            print(r"swing: extracting {} completed in {}".format(directory, (time_end - time_start)))
            print(r"")
        except:
            print(traceback.format_exc())

        return True
    except:
        traceback.print_exc(file=sys.stdout)
        return False            


    # if extract_archive(SwingSettings.get_instance().bin_7z(), source, target_dir, extract_mode = extract_mode):


if __name__ == '__main__':    
    source = r"D:\Productions\tg3\tg_301_020_010_export.zip"
    target = r"D:\Productions\editorial\tg\tg_2d_ep301\tg_301_020_010"
    extract_zip_contents(source, target)

    source = r"D:\Productions\tg3\tg_301_090_020_export.7z"
    target = r"D:\Productions\editorial\tg\tg_2d_ep301\tg_301_090_020"
    extract_zip_contents(source, target)