from wildchildanimation.gui.settings import SwingSettings

import sys

def load_unreal():
    try:
        #
        # add module root to sys path
        module_path = SwingSettings.get_instance().bin_ue_editor()
        module_path = module_path.replace("Engine/Binaries/Win64/UE4Editor.exe", r"Engine/Binaries/ThirdParty/Python3/Win64/Lib")

        if not module_path in sys.path:
            sys.path.append(module_path)

        import unreal
        return True
    except:
        print("Error loading Unreal libraries")
        return False
print(sys.path)