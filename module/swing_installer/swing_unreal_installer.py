# -- coding: utf-8 --
import unreal
import pip

from wildchildanimation.unreal.mrq.SwingMoviePipelineRuntimeExecutor import *


# install PyQt5 in the current UE5 instance
DEPENDENCIES = [
    "pip",
    "PyQt5",
    "gazu",
    "sip",
    "keyring",
    "PySide2",
    "requests_toolbelt",
    "six",
    "opentimelineio",
    "imath==0.0.2",
    "numpy==1.22.3",
    "OpenEXR @ file:///Z:/env/wca/env/Scripts/OpenEXR-1.3.8-cp39-cp39-win_amd64.whl",
    "Pillow==9.1.0",
]

MENU_OWNER = "SwingUE-Tools"
SCRIPT_VERSION = "0.0.2"
tool_menus = unreal.ToolMenus.get()   

def install():
    print("Installing Swing dependencies ...")
    for lib in DEPENDENCIES:
        print("Install start {}".format(lib))
        pip.main(['install', lib])
        print("Install finished {}".format(lib))

def create_main_menu_section():
    # Get a reference to the Main Menu (The top bar)
    main_menu = tool_menus.extend_menu("LevelEditor.MainMenu")

    try:
        name = "LevelEditor.MainMenu.SwingTools"
        tool_menus.unregister_owner_by_name(name)
        tool_menus.remove_menu(name)        
    except:
        pass

    # Add a new category to the top bar, called a subMenu
    main_menu.add_sub_menu(MENU_OWNER, "", "SwingTools", "Swing Tools", "Tooltip")

    # Register a new menu on the My Tools subMenu we just made
    custom_menu = tool_menus.register_menu("LevelEditor.MainMenu.SwingTools", "", unreal.MultiBoxType.MENU, True)

    # Add a new vertical section.  Sections are the visual splitting of different parts of the menu with a label at the top
    custom_menu.add_section("Assets", "Assets")

    entry = unreal.ToolMenuEntryExtensions.init_menu_entry(
        MENU_OWNER, #owner
        "SwingAssetLoaderMenu", #name - used to reference this entry
        "Asset Loader", #label - Display Name on the button
        "", #tooltip
        unreal.ToolMenuStringCommandType.PYTHON, #command type - COMMAND, PYTHON, CUSTOM - Determines what sort of command to run.  CUSTOM is for supporting future languages.
        "", #custom command type - Only used is commandType is CUSTOM
        "from wildchildanimation.unreal.editor_utility.run_asset_loader import main; main()") #command string - Run this command
    custom_menu.add_menu_entry("Assets", entry) #Add the new entry to our menu

    # Add a new vertical section.  Sections are the visual splitting of different parts of the menu with a label at the top
    custom_menu.add_section("Shots", "Shots")

    entry = unreal.ToolMenuEntryExtensions.init_menu_entry(
        MENU_OWNER, #owner
        "SwingShotCreatorMenu", #name - used to reference this entry
        "Shot Creator", #label - Display Name on the button
        "", #tooltip
        unreal.ToolMenuStringCommandType.PYTHON, #command type - COMMAND, PYTHON, CUSTOM - Determines what sort of command to run.  CUSTOM is for supporting future languages.
        "", #custom command type - Only used is commandType is CUSTOM
        "from wildchildanimation.unreal.editor_utility.run_shot_creator import main; main()") #command string - Run this command
    custom_menu.add_menu_entry("Shots", entry) #Add the new entry to our menu   


    entry = unreal.ToolMenuEntryExtensions.init_menu_entry(
        MENU_OWNER, #owner
        "SwingRenderSubmit", #name - used to reference this entry
        "Render Submit", #label - Display Name on the button
        "", #tooltip
        unreal.ToolMenuStringCommandType.PYTHON, #command type - COMMAND, PYTHON, CUSTOM - Determines what sort of command to run.  CUSTOM is for supporting future languages.
        "", #custom command type - Only used is commandType is CUSTOM
        "from wildchildanimation.unreal.editor_utility.run_render_submit import main; main()") #command string - Run this command
    custom_menu.add_menu_entry("Render Submit", entry) #Add the new entry to our menu         

    # Add a new vertical section.  Sections are the visual splitting of different parts of the menu with a label at the top
    custom_menu.add_section("Swing", "Swing")

    entry = unreal.ToolMenuEntryExtensions.init_menu_entry(
        MENU_OWNER, #owner
        "SwingGUIMenu", #name - used to reference this entry
        "Swing UE", #label - Display Name on the button
        "", #tooltip
        unreal.ToolMenuStringCommandType.PYTHON, #command type - COMMAND, PYTHON, CUSTOM - Determines what sort of command to run.  CUSTOM is for supporting future languages.
        "", #custom command type - Only used is commandType is CUSTOM
        "from wildchildanimation.unreal.editor_utility.run_swing_gui import main; main()") #command string - Run this command
    custom_menu.add_menu_entry("Swing", entry) #Add the new entry to our menu         


def setup_menu():
    print(F"Setting up Menu")    

    tool_menus.unregister_owner_by_name(MENU_OWNER)
    create_main_menu_section()

    tool_menus.refresh_all_widgets()    


if __name__ == "__main__":
    print(F"Running Swing Unreal Installer v{SCRIPT_VERSION}")

    install_dependencies = False
    try:
        import PyQt5
        import PySide2
        import gazu
        import opentimelineio
    except:
        install_dependencies = True

    if install_dependencies:
        print("Installing dependencies ...")
        install()

    setup_menu()

    ## Z:\env\wca\swing\swing-main\module\swing_installer\swing_unreal_installer.py