
# Copyright Epic Games, Inc. All Rights Reserved

"""
This is a commandline script that can be used to execute local and remote renders from Unreal.
This script can be executed in Editor or via commandline.

This script has several modes:
    

    sequence:
        This mode allows you to specify a specific level sequence, map and movie render queue preset to render.
        Command:
            ` py mrq_cli.py sequence my_level_sequence_name my_map_name my_mrq_preset_name `

    

    --user: This options sets the author on the render job. If None is provided, the current logged-in user is used.


Editor CMD window:
    py mrq_cli.py <--remote> sequence sequence_name map mrq_preset_name

Editor Commandline:
    UnrealEditor.exe uproject_name/path <startup-args> -ExecCmds="py mrq_cli.py sequence sequence_name map mrq_preset_name --cmdline"

In a commandline interface, it is very important to append `--cmdline` to the script args as this will tell the editor
to shut down after a render is complete. Currently, this is the only method to keep the editor open till a render is
complete due to the default python commandlet assuming when a python script ends, the editor needs to shut down.
This behavior is not ideal as PIE is an asynchronous process we need to wait for during rendering.
"""

import argparse
import traceback
import subprocess

UNREAL_EXE = "C:\\Program Files\\Epic Games\\UE_4.27\\Engine\\Binaries\\Win64\\UE4Editor-Cmd.exe"
U_PROJECT = "Y:\\productions\\witw\\witw_render_only_v001\\witw_proj_v001.uproject" 

from wildchildanimation.unreal.mrq.swing_mrq_cli_modes.render_sequence import *

def process_render2(args):
    print("MRQ::process_render")

    render_map = args.map    
    render_seq = args.sequence
    render_preset = args.preset
    render_target = args.output_dir
    render_x = args.resx
    render_y = args.resy
    render_cmdline = args.cmdline

    print(f"MRQ::process_render: render_map = {render_map}")
    print(f"MRQ::process_render: render_seq = {render_seq}")
    print(f"MRQ::process_render: render_preset = {render_preset}")
    print(f"MRQ::process_render: render_target = {render_target}")
    print(f"MRQ::process_render: render_x = {render_x}")
    print(f"MRQ::process_render: render_y = {render_y}")
    print(f"MRQ::process_render: render_cmdline = {render_cmdline}")

    movie_queue_render(render_map, render_seq, render_preset)

def movie_queue_render(u_level_file, u_level_seq_file, u_preset_file):
    command = [
        UNREAL_EXE,
        U_PROJECT,
        u_level_file,

        # required
        "-LevelSequence=%s" % u_level_seq_file,  # The sequence to render
        "-MoviePipelineConfig=\"%s\"" % u_preset_file,
        "-game",

        # options
        "-NoLoadingScreen",
        "-log",

        # window size not resolution
        "-Windowed",
        "-ResX=800",
        "-ResY=600",
        "--cmdline"
    ]
    #proc = subprocess.Popen(command)
    #return proc.communicate()
    print(command)

    proc = subprocess.Popen(command, shell = False, stdout=subprocess.PIPE)
    while True:
        #output = proc.stdout.read(1)
        output = proc.stdout.readline()
        try:
            log = output.decode('utf-8')
            if log == '' and proc.poll() != None:
                break
            else:
                print(log)
        except:
            print(traceback.format_exc())
        # continue

if __name__ == "__main__":
    print("Swing.MRQ.cli::main")

    parser = argparse.ArgumentParser(
        description="Swing UE Command Line Render"
    )

    parser.add_argument("-m", "--map", help="Unreal Map", action="store")
    parser.add_argument("-s", "--sequence", help="Unreal Sequence", action="store")
    parser.add_argument("-p", "--preset", help="Render Preset", action="store")
    parser.add_argument("-o", "--output_dir", help="Output Directory", action="store")

    parser.add_argument("-x", "--resx", help="X Resolution", action="store", default=1920)
    parser.add_argument("-y", "--resy", help="Y Resolution", action="store", default=1080)

    parser.add_argument("-e", "--episode", help="Episode", action="store", default=None)

    parser.add_argument("--frame_in", help="Frame In", action="store", default=None)
    parser.add_argument("--frame_out", help="Frame Out", action="store", default=None)

    parser.add_argument("-c", "--cmdline", help="Execute from Command Line", action="store_true")

    args = parser.parse_args()

    # Add arguments for the sequence parser
    try:
        process_render(args)
    except:
        traceback.print_exc()
    # Process the args using the argument execution functions

