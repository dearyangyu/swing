# -*- coding: utf-8 -*-
import os
import traceback
import subprocess

from datetime import datetime

UE_EDITOR = r"D:\Epic\UE_4.27\Engine\Binaries\Win64\UE4Editor-Cmd.exe"
UE_LEVEL = r"H:\UE\witw_render_only_v001\witw_proj_v001.uproject"

## BATCH_IMPORT_SCRIPT = r"D:\DEV\swing-ue-test\wildchildanimation\swing\unreal\batch_import.py"
BATCH_IMPORT_SCRIPT = r"Z:\env\wca\swing\swing-main\module\wildchildanimation\unreal\batch_import.py"

SOURCE_DIR = r"Z:\productions\wotw\wotw_edit\wip\editorial\110_nursetoad\shot_cache\110_nursetoad_sc020_sh020\shot_cache\cache\abc"

#    parser.add_argument('-p', '--project', help='Project', default='None')
#    parser.add_argument('-e', '--episode', help='Episode', default='None')
#    parser.add_argument('-d', '--dir', help='Source directory', default='None')
#    parser.add_argument('-l', '--loc', help='Localization', default='None')

class SwingUE:

    SUPPRESS_LINES = [
        r"LogInit",
        r"LogConfig",
        r"LogAudio",
        r"LogPakFile",
        r"LogWindows",
        r"LogMemory",
        r"LogSubstance",
        r"LogDerivedDataCache",
        r"LogSlate",
        r"LogModuleManager: Shutting down and abandoning module",
        r"LogDirectoryWatcher: Display: A directory notification failed",
        r"LogShaderLibrary: Display: ShaderCodeLibraryPakFileMountedCallback",
        r"LogPakFile: PakFile",
        r"LogD3D12RHI: Display: D3D12 ReleaseResources",
        r"LogPluginManager: Mounting plugin",
        r"LogDevObjectVersion",
        r"LogConfig: Setting CVar",
        r"LogD3D12RHI",
        r"LogTargetPlatformManager",
    ]    

    def __init__(self):
        self.log = []    

    def server_log(self, text):
        log = "{} swing: ".format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
        log += " {}".format(text)

        self.log.append(log.strip())          
        print(log)   

    def swing_ue_import(self, ue_editor = UE_EDITOR, project_path = UE_LEVEL, python_script = BATCH_IMPORT_SCRIPT, episode = None, dir = None, log_dir = None):
        self.log = []            
        time_start = datetime.now()
        suppress_count = 0        

        # run shot cache on the project file                                          
        LOG_STDOUT = "-stdout"
        LOG_OUTPUT = "-FullStdOutLogOutput"
        SCRIPT = '-ExecutePythonScript={} --episode={} --dir={}'.format(python_script, episode, dir)

        self.server_log("*** Popen({} {} {} {} {}".format(ue_editor, project_path, LOG_STDOUT, LOG_OUTPUT, SCRIPT))

        proc = subprocess.Popen([ue_editor, project_path, "-cmdline", "-unattended", LOG_STDOUT, LOG_OUTPUT, SCRIPT], shell = False, stdout=subprocess.PIPE)
        while True:
            #output = proc.stdout.read(1)
            output = proc.stdout.readline()
            try:
                show_line = True                
                log = output.decode('utf-8')
                if log == '' and proc.poll() != None:
                    break
                else:
                    if SwingUE.SUPPRESS_LINES: 
                        for item in SwingUE.SUPPRESS_LINES:
                            if item in log:
                                suppress_count += 1
                                show_line = False
                                break

                    if show_line:
                        # sys.stdout.write(log)
                        log = log.strip()
                        if log != '':
                            self.server_log(log)
            except:
                print(traceback.format_exc())
            # continue

        time_end = datetime.now()
        self.server_log("completed in {}".format(time_end - time_start))            

        log_out = os.path.join(os.path.dirname(log_dir), "logs", "ue_import.log")

        self.server_log("Writing log file {}".format(log_out))

        if not os.path.exists(os.path.dirname(log_out)):
            os.mkdir(os.path.dirname(log_out))

        with open(log_out, 'w') as f:
            try:
                for item in self.log:
                    f.write("%s\n" % item.strip())
            finally:
                f.close()    

        return True       
                

    #SCRIPT = r"C:\Program Files\Epic Games\UE_4.25\Engine\Binaries\Win64\UE4Editor-Cmd.exe" "C:\Path\To\Project.uproject" -stdout -FullStdOutLogOutput -ExecutePythonScript="C:\Path\To\do_import.py C:\Path\To\model.fbx /Game/MyProject/Level/Test"
    #-ExecutePythonScript="D:\DEV\swing-ue-test\wildchildanimation\swing\unreal\batch_import.py None None Z:\productions\wotw\wotw_edit\wip\editorial\110_nursetoad\shot_cache\110_nursetoad_sc020_sh020\shot_cache\cache\abc None"

if __name__ == "__main__":
    SwingUE().swing_ue_import(dir = SOURCE_DIR,  episode="110_nursetoad")