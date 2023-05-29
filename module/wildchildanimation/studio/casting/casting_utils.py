# -*- coding: utf-8 -*-
#
# Casting Manager
# Utility functions to retrieve and manage Casting and Breakdown information from Treehouse
#
# Author: P Niemandt
# Date: 2022-12-16
# Version: 1.00

import argparse
import gazu

from wildchildanimation.gui.settings import SwingSettings

class CastingManager:

    def __init__(self):
        self.swing_settings = SwingSettings.get_instance()        
        self.connected = False

    def connect_to_server(self): 
        if self.connected and self.gazu_client:
            self.gazu_client = None
            self.connected = False

        password = self.swing_settings.swing_password()
        server = self.swing_settings.swing_server()
        email = self.swing_settings.swing_user()

        gazu.set_host("{}/api".format(server))
        try:
            self.gazu_client = gazu.log_in(email, password)
            self.connected = True
        except:
            self.connected = False        

        return self.connected

    def get_casting(self, project_name, type, sequence_name = None, name = None):
        casting = None
        if self.connect_to_server():
            project = gazu.project.get_project_by_name(project_name)

            if type.lower() == 'asset':
                asset = gazu.asset.get_asset_by_name(project, name)
                casting = gazu.casting.get_asset_casting(asset)
            elif type.lower() == 'sequence':
                sequence = gazu.shot.get_sequence_by_name(project, sequence_name)
                casting = gazu.casting.get_sequence_casting(sequence)
            elif type.lower() == 'shot':
                sequence = gazu.shot.get_sequence_by_name(project, sequence_name)
                shot = gazu.shot.get_shot_by_name(sequence)
                casting = gazu.casting.get_shot_casting(shot)
        return casting

def process(project, type, sequence = None, name = None):
    manager = CastingManager()
    return manager.get_casting(project, type, sequence, name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--project', help='Project Code', default='None')
    parser.add_argument('-t', '--type', help='Asset or Shot casting', default='Asset')
    parser.add_argument('-s', '--seq', help='Sequence Name', default='None')    
    parser.add_argument('-n', '--name', help='Entity Name', default='None')

    args = parser.parse_args()
    process(args.project, args.seq, args.type, args.name)


