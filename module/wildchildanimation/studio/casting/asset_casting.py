# -*- coding: utf-8 -*-
#
# Casting Manager: Asset Casting
# Utility functions to retrieve and manage Casting and Breakdown information from Treehouse
#
# Author: P Niemandt
# Date: 2022-12-16
# Version: 1.00

from wildchildanimation.studio.casting.casting_utils import CastingManager

if __name__ == "__main__":
    mgr = CastingManager()
    casting = mgr.get_casting(project_name = "SDMP", type = "Asset", name = "MainLodgeGreatHallIntA")

    for item in casting:
        print(item)

    casting = mgr.get_casting(project_name = "SDMP", type = "Asset", name = "MainLodgeExtA")
    for item in casting:
        print(item)        
    