import unreal

def list_level_sequences(class_names = ["LevelSequence"], package_paths=["/Game/cinematics"]):
    return search_assets(class_names = class_names, package_paths=package_paths)

def list_maps(class_names = ["World"], package_paths = ["/Game/"]):
    return search_assets(class_names=class_names, package_paths=package_paths)

def get_level_asset(class_names = ["World"], asset_paths = ["/Game/"]):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    filter = unreal.ARFilter(
        class_names=class_names,
        package_paths=asset_paths,
        recursive_paths=False)
    
    levels = asset_registry.get_assets(filter)
    for lvl in levels:
        return lvl
    
    return None

def get_sub_levels(level):
    sublevels = unreal.EditorLevelUtils.get_levels(level)    
    return sublevels

def search_assets(class_names = ["World"], package_paths=["/Game/"], recursive_paths=True):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

    filter = unreal.ARFilter(
        class_names=class_names,
        package_paths=package_paths,
        recursive_paths=recursive_paths)
    
    return asset_registry.get_assets(filter)

def get_asset_path_level(asset_path):
    level = get_level_asset(asset_path)

    if not level:
        print(F"Level not found: {asset_path}")
        return False

    print(F"Level: {level.package_name}.{level.asset_name}")
    sublevels = get_sub_levels(level)
    if not sublevels:
        print(F"Level has no sublevels: {asset_path}")
        return False

    if sublevels:
        for i, sublevel in enumerate(sublevels):
            print(F"Sublevel {i}: {sublevel.package_name}.{sublevel.asset_name}")    


#if __name__ == "__main__":
#    #get_asset_path_level("/Game/assets/iceberg_ava/")
#    get_asset_path_level("/Game/cinematics/ep000/sc010/ms_ep000_sc010/")

##get_asset_path_level("/Game/cinematics/ep000/sc010/ms_ep000_sc010/")    

#print("Found Levels: ***************")
#for lv in search_assets():
#    print(lv)
#print("Found Levels: ***************")    

#print("Testing Level Sequences: ***************")
#for item in list_level_sequences():
#    print(item)

#print("Testing Maps: ***************")
#for item in list_maps():
#    print(item)

# Z:\env\wca\swing\swing-main\module\wildchildanimation\unreal\unreal_utils.py 