import subprocess
import sys
import traceback
import glob
import os
import json

from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler

_maya_loaded = False    
try:
    import maya.mel as mel
    import maya.cmds as cmds
    _maya_loaded = True
except:
    pass

class SwingScriptRunner():

    NAME = "SwingScriptRunner"
    VERSION = "0.0.10"

    SCRIPT_PATH = "Z:/env/wca/swing/swing-main/scripts"

    def __init__(self):
        super(SwingScriptRunner, self).__init__()
        print("{} v{}".format(self.NAME, self.VERSION))  

        if not _maya_loaded:
            print("{} v{} - ERROR !!! Maya not found".format(self.NAME, self.VERSION))  

        self.episode_name = None
        self.task_name = None

    def set_episode_name(self, ep_name):
        self.episode_name = ep_name

        print("{}: Episode Name: {}".format(self.NAME, ep_name))  

    def set_task_name(self, task_name):
        self.task_name = task_name

        print("{}:  Task Name:{}".format(self.NAME, task_name))  

    # suggested example of anim fbx file naming: hnl_char_alan_ava_0000_ep001_sc010_sh010.fbx ?
    # Alan example:
    # Swing generated namespace :     char_hnl_char_alan_ava_0000
    # extracted name:                 alan_ava_0000
    def get_references(self):
        fbx_sets = []
        objList = cmds.ls(type='objectSet')
        for obj in objList:
            if '_fbx_set' in obj:
                fbx_sets.append(obj)
        return fbx_sets
    
    def create_name_from_namespace(self, fbx_sets):
        output = []
        anim_file_name = cmds.file(query=True, sceneName=True, shortName=True)

        for set in fbx_sets:
            # check if current object set is referenced into the scene file
            if cmds.referenceQuery(set, isNodeReferenced=True):
                # get file name of referenced in node
                reference_file_name = cmds.referenceQuery(set, filename=True, shortName=True)

                # get first namespace

                if ':' in set:
                    obj_namespace = set.split(':')[0]
                else:
                    obj_namespace = set.trim()

                # split into parts to naming convention (production_assettype_name_variant_number)
                list = obj_namespace.split('_')

                print("extract_naming: set: {} reference_file_name: {} anim_file_name: {}".format(set, reference_file_name, anim_file_name))
                print("extract_naming: {}:{}".format(list, len(list)))
                try:
                    if len(list) >= 6:
                        name = '{}_{}_{}'.format(list[3], list[4], list[5])
                        dict = {
                            'item': set,
                            'namespace_name': name,
                            'reference_file_name': reference_file_name,
                            'anim_file_name': anim_file_name
                        }                        
                    else:
                        dict = {
                            'item': set,
                            'error': 'namespace naming incorrect'
                        }

                    output.append(dict)
                    print("Swing: namespace: {} reference_file_name: {} anim_file_name: {}".format(name, reference_file_name, anim_file_name))
                except:
                    print('Error: namespace naming incorrect: {}'.format(obj_namespace))

            else:
                print('Error: object set not referenced: {}'.format(set))

        return output

    def anim_update(self):
        script_name = 'anim_updateRefs_v0_5.mel'
        print("script_runner '{}' ".format(script_name))

        script_uri = "{}/{}".format(SwingScriptRunner.SCRIPT_PATH, script_name)
        mel_command = 'source "{}"'.format(script_uri)
        
        try:
            print("Sourcing mel script: {}".format(mel_command))
            mel.eval(mel_command)

            return True
        except:
            print("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False           

    def anim_export(self):
        script_name = 'server_export_v0_1.mel'
        method = 'animExport'

        print("script_runner '{}' '{}'".format(script_name, method))

        # write json metadata for export naming
        try:
            fbx_sets = self.get_references()
            naming = self.create_name_from_namespace(fbx_sets)      

            print("\n")
            for row in naming:
                print("\t{}".format(row))      
            print("\n")   

            anim_file_name = cmds.file(q=True, sn=True)
            export_file_name = os.path.join(os.path.dirname(anim_file_name), "cache", "swing_export.json")

            with open(export_file_name, 'w') as outfile:
                json.dump(naming, outfile, indent=4)

            print("*** Exported namespace to file: {}".format(export_file_name))
        except:
            traceback.print_exc(file=sys.stdout)            
            print("script_runner error running naming & references")                
            pass

        script_uri = "{}/{}".format(SwingScriptRunner.SCRIPT_PATH, script_name)
        try:
            mel_command = 'source "{}"'.format(script_uri)
            print("Sourcing mel script: {}".format(mel_command))
            mel.eval(mel_command)

            #mel_command = 'animExport("{}", "{}")'.format(self.episode_name, self.task_name)
            #print("Exec mel method: {}".format(mel_command))
            #mel.eval(mel_command)

            return True
        except:
            print("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False  

    def layout_breakout(self):
        print("script_runner 'layout_breakout'")
        try:
            swingMaya = MayaStudioHandler()

            ## swingMaya.cleanup_scene()
            breakout_path = swingMaya.chainsaw_panel('breakout.csv')

            for item in glob.glob("{}/*.ma".format(breakout_path)):
                cmds = [ "Z:\\env\\wca\\swing\\swing-main\\bin\\anim_prep.bat", item ] 

                print("Running command: {}".format(str(cmds)))
                #proc = s
                subprocess.run(cmds, shell = False, stderr=subprocess.PIPE)
                print("Completed command: {}".format(str(cmds)))                

            return True
        except:
            print("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False  

    def run_script(self, script_name, method = None):
        print("script_runner '{}' '{}'".format(script_name, method))

        script_uri = "{}/{}".format(SwingScriptRunner.SCRIPT_PATH, script_name)
        mel_command = 'source "{}"'.format(script_uri)
        
        try:
            print("Sourcing mel script: {}".format(mel_command))
            mel.eval(mel_command)

            if method:
                if len(self.params) > 0:
                    param_str = ''
                    for p in self.params:
                        param_str += "'{}'".format(p) + ' '

                    mel_command = '{} {}'.format(method, param_str)
                else:
                    mel_command = '{}'.format(method)
                    
                print("Exec mel method: {}".format(mel_command))
                mel.eval(mel_command)
            else:
                print('Execution method not found')
            return True
        except:
            print("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False
