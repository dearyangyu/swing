import subprocess
import sys
import traceback
import glob

from wildchildanimation.gui.swing_utils import write_log
from wildchildanimation.studio.maya_studio_handlers import MayaStudioHandler

_maya_loaded = False    
try:
    import maya.mel as mel
    _maya_loaded = True
except:
    pass

class SwingScriptRunner():

    NAME = "SwingScriptRunner"
    VERSION = "0.0.9"

    SCRIPT_PATH = "Z:/env/wca/swing/swing-main/scripts"

    def __init__(self):
        super(SwingScriptRunner, self).__init__()
        write_log("{} v{}".format(self.NAME, self.VERSION))  

        if not _maya_loaded:
            write_log("{} v{} - ERROR !!! Maya not found".format(self.NAME, self.VERSION))  

        self.episode_name = None
        self.task_name = None

    def set_episode_name(self, ep_name):
        self.episode_name = ep_name

    def set_task_name(self, task_name):
        self.task_name = task_name

    def anim_update(self):
        script_name = 'anim_updateRefs_v0_5.mel'
        write_log("script_runner '{}' ".format(script_name))

        script_uri = "{}/{}".format(SwingScriptRunner.SCRIPT_PATH, script_name)
        mel_command = 'source "{}"'.format(script_uri)
        
        try:
            write_log("Sourcing mel script: {}".format(mel_command))
            mel.eval(mel_command)

            return True
        except:
            write_log("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False           

    def anim_export(self):
        script_name = 'server_export_v0_1.mel'
        method = 'animExport'

        write_log("script_runner '{}' '{}'".format(script_name, method))

        script_uri = "{}/{}".format(SwingScriptRunner.SCRIPT_PATH, script_name)
        try:
            mel_command = 'source "{}"'.format(script_uri)
            write_log("Sourcing mel script: {}".format(mel_command))
            mel.eval(mel_command)

            #mel_command = 'animExport("{}", "{}")'.format(self.episode_name, self.task_name)
            #write_log("Exec mel method: {}".format(mel_command))
            #mel.eval(mel_command)

            return True
        except:
            write_log("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False  

    def layout_breakout(self):
        write_log("script_runner 'layout_breakout'")
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
            write_log("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False  

    def run_script(self, script_name, method = None):
        write_log("script_runner '{}' '{}'".format(script_name, method))

        script_uri = "{}/{}".format(SwingScriptRunner.SCRIPT_PATH, script_name)
        mel_command = 'source "{}"'.format(script_uri)
        
        try:
            write_log("Sourcing mel script: {}".format(mel_command))
            mel.eval(mel_command)

            if method:
                if len(self.params) > 0:
                    param_str = ''
                    for p in self.params:
                        param_str += "'{}'".format(p) + ' '

                    mel_command = '{} {}'.format(method, param_str)
                else:
                    mel_command = '{}'.format(method)
                    
                write_log("Exec mel method: {}".format(mel_command))
                mel.eval(mel_command)
            else:
                write_log('Execution method not found')
            return True
        except:
            write_log("Exception during script")
            traceback.print_exc(file=sys.stdout)
        return False
