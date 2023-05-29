# -- coding: utf-8 --
import sys
import os
import unreal
import json
import traceback

try:
    from PySide2 import QtCore, QtWidgets
    qtMode = 0
except ImportError:
    from PyQt5 import QtCore, QtWidgets

from wildchildanimation.unreal.gui.asset_manager_dialog import Ui_AssetManagerDialog

class UnrealAssetManager(QtWidgets.QDialog, Ui_AssetManagerDialog):

    VERSION = "0.2"

    def __init__(self, parent = None):
        super(UnrealAssetManager, self).__init__(parent) # Call the inherited classes __init__ method    
        self.setupUi(self)
        self.setWindowTitle("Unreal Asset Loader: Select json config file")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.selected_file = None
        self.toolButtonSelectFileName.clicked.connect(self.select_file)

        self.buttonBox.accepted.connect(self.process)
        self.buttonBox.rejected.connect(self.reject)

        unreal.log("{}: v{} Created".format(self.__class__.__name__, self.VERSION))    

    def select_file(self):
        #Get the file location
        q = QtWidgets.QFileDialog.getOpenFileName(None, caption = "Select json file",  filter = "JSON (*.json);; All Files (*.*)")
        if not (q):
            return None
        
        self.selected_file = q[0]
        self.lineEditFileName.setText(self.selected_file)

    def build_import_tasks(self,asset_path, fbx_folder_path, fbx_file):
        import_task = unreal.AssetImportTask()
        import_task.filename = (fbx_folder_path + fbx_file)
        import_task.destination_path = asset_path
        import_task.set_editor_property('automated', True)
        import_task.set_editor_property('save', True)
        import_task.replace_existing = True

        return import_task

    def build_staticmesh_fbx_import_options(self):
        # set the import options
        options = unreal.FbxImportUI()
        options.set_editor_property("import_mesh", True)
        options.set_editor_property("import_materials", False)
        options.set_editor_property("import_textures", False)
        options.set_editor_property('import_as_skeletal', False)
        # set the static_mesh_import_data options
        options.static_mesh_import_data.set_editor_property('combine_meshes', True)
        options.static_mesh_import_data.set_editor_property("import_translation", unreal.Vector(0, 0, 0))
        options.static_mesh_import_data.set_editor_property("import_rotation", unreal.Rotator(0, 0, 0))
        options.static_mesh_import_data.set_editor_property("import_uniform_scale", 1.0)
        options.static_mesh_import_data.set_editor_property("build_nanite", False)
        options.static_mesh_import_data.set_editor_property("auto_generate_collision", False)
        return options

    def build_skeletalmesh_fbx_import_options(self):
        # set the import options
        options = unreal.FbxImportUI()
        options.set_editor_property("import_mesh", True)
        options.set_editor_property("import_materials", False)
        options.set_editor_property("import_textures", False)
        options.set_editor_property('import_as_skeletal', True)
        #options.set_editor_property('skeleton', skeleton)
        # set the skeletal_mesh_import_data options
        # unreal.FbxMeshImportData
        options.skeletal_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
        options.skeletal_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
        options.skeletal_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
        # unreal.FbxSkeletalMeshImportData
        options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
        #options.skeletal_mesh_import_data.set_editor_property('import_meshes_in_bone_hierarchy ', True)
        options.skeletal_mesh_import_data.set_editor_property('import_morph_targets', True)
        options.skeletal_mesh_import_data.set_editor_property('update_skeleton_reference_pose', False)
        return options

    def import_fbx_static_mesh(self, obj, asset_path, sys_path):

        # set the folder path to search for FBX files
        fbx_folder_path = (sys_path + '/fbx/')

        # Get a list of all the FBX files in the folder
        fbx_files = [f for f in os.listdir(fbx_folder_path) if f.endswith('.fbx')]
        # iterate through the list of files and import FBX files
        for fbx_file in fbx_files:

            # create the import task
            import_task = self.build_import_tasks(asset_path, fbx_folder_path, fbx_file)
            options = self.build_staticmesh_fbx_import_options()
            
            import_task.options = options

            # execute the import task
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])

    def import_fbx_skeletal_mesh(self, obj, asset_path, sys_path):

        # set the folder path to search for FBX files
        fbx_folder_path = (sys_path + '/fbx/')

        # Get a list of all the FBX files in the folder
        fbx_files = [f for f in os.listdir(fbx_folder_path) if f.endswith('.fbx')]
        # iterate through the list of files and import FBX files
        for fbx_file in fbx_files:
            # create the import task
            import_task = self.build_import_tasks(asset_path, fbx_folder_path, fbx_file)
            options = self.build_skeletalmesh_fbx_import_options()
            
            import_task.options = options

            # execute the import task
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])

    def get_skeleton(self, skeleton_name, asset_path):
        asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
        skel_assets = asset_reg.get_assets_by_path(asset_path)
        
        for skel_asset in skel_assets:
            #you could use isinstance unreal.SkeletalMesh, but let's build on what we learned
            if skel_asset.asset_class_path.asset_name == 'Skeleton':
                if skeleton_name in str(skel_asset.asset_name):
                    skeleton = skel_asset
        return(skeleton)

    def create_actor_in_world(self, data, asset_path):
        unreal.log("{}: v{} create_actor_in_world {}]".format(self.__class__.__name__, self.VERSION, asset_path))    
        try:
            tx = float(data['tx'])
            ty = float(data['ty'])
            tz = float(data['tz'])
            
            asset_name = "{}{}.{}".format(asset_path, str(data['name']), str(data['name']))
            obj = unreal.load_asset(asset_name)

            if not obj:
                unreal.log("{}: v{} asset not found: {}]".format(self.__class__.__name__, self.VERSION, asset_name))            
                return False

            actor_location = unreal.Vector((tx * 1),(tz * 1),(ty * 1))
            actor_rotation = unreal.Rotator(float(data['rx']),float(data['rz']),float(data['ry']))
            actor_scale = unreal.Vector(float(data['sx']),float(data['sz']),float(data['sy']))

            actor = unreal.EditorLevelLibrary.spawn_actor_from_object(obj, actor_location, actor_rotation)

            actor.set_actor_scale3d(actor_scale)
            actor_name = data['fullname'].split(':')
            actor.set_actor_label(actor_name[-1])        

            return True
        except:            
            traceback.print_exc(file=sys.stdout)

    def get_json_file(self):
        file_name = self.load()
        return(file_name)

    def process(self):
        json_file = self.selected_file
        if not json_file:
            print("No file selected, aborting")
            return False
        
        unreal.log("{}: v{} Processing JSON {}]".format(self.__class__.__name__, self.VERSION, json_file))    
        
        with open(json_file, 'r') as open_file:
            json_object = json.load(open_file)

        self.lineEditStatus.setText("Processing {}".format(json_file))

        asset_path = ''
        count = 0
        for obj in json_object:
            if (count == 0):
                unreal.log("{}: v{} Processing {}]".format(self.__class__.__name__, self.VERSION, "File Header"))    
                asset_type = obj['asset_type']
                game_path = obj['game_path']
                local_path = obj['local_path']
                shared_path = obj['shared_path']

            else:    
                self.lineEditStatus.setText("Processing {}".format(obj["fullname"]))
                if asset_type == 'env':
                    
                    self.import_fbx_static_mesh(obj, game_path, shared_path)
                    self.create_actor_in_world(obj, game_path)
                if asset_type == 'rig':
                    #skeleton_name = obj['skeleton_name']
                    #skeleton = self.get_skeleton(skeleton_name, game_path)
                    self.import_fbx_skeletal_mesh(obj, game_path, shared_path)

            count = count + 1

        self.lineEditStatus.setText("Processing {}".format("Completed"))        
        unreal.log("{}: v{} Processing Completed]".format(self.__class__.__name__, self.VERSION))   
        self.accept() 
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    dialog = UnrealAssetManager()
    dialog.show()

    sys.exit(app.exec_())    