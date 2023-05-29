# -*- coding: utf-8 -*-
#
# Asset Utility file functions
#

from pathlib import Path

from wildchildanimation.gui.settings import SwingSettings

def get_server_path(path_name):
    '''
        Replace the local path prefix with the shared project path
    '''

    # norm path by converting to Path and returning posix
    root_path = Path(SwingSettings.get_instance().swing_root()).as_posix()
    shared_path = Path(SwingSettings.get_instance().shared_root()).as_posix()
    local_path = Path(path_name).as_posix()

    return local_path.replace(root_path, shared_path)


if __name__ == "__main__":
    print("Test:")

    local_path = r"D:\Productions\sdmp\sdmp_work\assets\env\mainlodgeexta\cl\mainlodgeexta"
    print("{} -> {}".format(local_path, get_server_path(local_path)))
