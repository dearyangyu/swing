# -*- coding: utf-8 -*-
# Asset Library utility functions
# 

from wildchildanimation.gui.swing_utils import *
from wildchildanimation.gui.settings import SwingSettings

import gspread

def get_task_status(task_list, task_type_name):
    for task in task_list:
        if task["task_type_name"].lower() == task_type_name.lower():
            return task["task_status_name"]
    return None
        

def sync_asset_index(project_name, spreadsheet_name, worksheet_name = "Asset_Index"):
    connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password())

    project = gazu.project.get_project_by_name(project_name)
    if not project:
        print(F"Error loading project: {project_name}")
        return False
    
    gc = gspread.service_account(filename='./treehouse-gsuite-dcad9a674b8c.json')     
    sh = gc.open(spreadsheet_name)    

    if not sh:
        print(F"Error loading Google Spreadsheet {spreadsheet_name}")
        return False
    
    asset_data = []
    asset_types = gazu.asset.all_asset_types_for_project(project)

    assembly_task_type = gazu.task.get_task_type_by_name("Assembly")
    rigging_task_type = gazu.task.get_task_type_by_name("Rig")

    for asset_type in asset_types:
        assets = gazu.asset.all_assets_for_project_and_type(project, asset_type)

        for asset in assets:
            working_files = gazu.files.get_all_working_files_for_entity(asset)
            working_files = sorted(working_files, key=lambda x: x["updated_at"], reverse=True) 

            asset_tasks = gazu.task.all_tasks_for_asset(asset)   

            assembly_status = get_task_status(asset_tasks, assembly_task_type["name"])
            rigging_status = get_task_status(asset_tasks, rigging_task_type["name"])

            updated_at = ""
            working_file = ""

            if len(working_files) > 0:
                working_file = working_files[0]["name"]
                updated_at = working_files[0]["updated_at"]

            row_data = {
                "Asset_Type": asset_type["name"],
                "Asset": asset["name"],
                "Assembly": assembly_status,
                "Rig": rigging_status,
                "Link": gazu.asset.get_asset_url(asset),
                "Working_File": working_file,
                "Updated": updated_at,
                "Deleted": asset["canceled"]
            }
            asset_data.append(row_data)
            print(F"+ {row_data['Asset_Type']} - {row_data['Asset']}, {row_data['Working_File']}")

            ##TESTING
            ##if len(asset_data) > 10:
            ##    break

    print(F"Loaded {len(asset_data)} assets")            

    row_count = len(asset_data) + 100
    worksheet_list = sh.worksheets()

    worksheet = None
    for item in worksheet_list:
        if item.title == worksheet_name:
            worksheet = item
            break    

    if row_count < 500:
        row_count = 500

    if not worksheet:
        worksheet = sh.add_worksheet(worksheet_name, rows=row_count, cols=10)    
    else:
        rows_in_sheet = worksheet.row_count

        if rows_in_sheet < row_count:
            rows_to_add = row_count - rows_in_sheet
            worksheet.add_rows(rows_to_add)
            print(F"Increased {spreadsheet_name} rowcount to {row_count}")

    
    batch_update = [] # batch list update

    ## Add / Update Header
    row = 1
    cell_range = "A{}:H{}".format(1, row)

    batch = {
        "range": cell_range,
        "values": [ [
            "Type", 
            "Name", 
            "Assembly",
            "Rig",
            "Link",
            "File",
            "Deleted", 
            'Updated: {}'.format(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))
            ] 
        ]
    }
    batch_update.append(batch)
    row += 1       

    for item in asset_data:
        cell_range = "A{}:$H{}".format(row, row)

        batch = {
            "range": cell_range,
            "values": [ [item['Asset_Type'], item['Asset'], item["Assembly"], item["Rig"], item["Link"], item["Working_File"], item["Deleted"]] ],
        }

        batch_update.append(batch)
        row += 1

    try:
        worksheet.batch_update(batch_update)
        print(F"Updated {spreadsheet_name} with {len(asset_data)} assets in {worksheet_name}")
    except:
        print(traceback.format_exc())    

def asset_in_casting(asset, asset_list):
    for item in asset_list:
        if item["asset_id"] == asset["id"]:
            return True
    return False

def cast_episode(spreadsheet_name, worksheet_name, project_name, episode_name):
    connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password())

    project = gazu.project.get_project_by_name(project_name)
    if not project:
        print(F"Error loading project: {project_name}")
        return False

    episode = gazu.shot.get_episode_by_name(project, episode_name)    
    if not episode:
        print(F"Error loading episode: {episode_name}")
        return False

    print(F"Reading Google Sheet {spreadsheet_name} Tab {worksheet_name} to populate {project_name} episode {episode_name}")
    gc = gspread.service_account(filename='./treehouse-gsuite-dcad9a674b8c.json')     
    sh = gc.open(spreadsheet_name)    

    if not sh:
        print(F"Error loading Google Spreadsheet {spreadsheet_name}")
        return False
    
    worksheet_list = sh.worksheets()

    worksheet = None
    for item in worksheet_list:
        if item.title == worksheet_name:
            worksheet = item
            break  

    if not worksheet:
        print(F"Error loading Worksheet {worksheet_name}")
        return False
    
    rows_in_sheet = worksheet.row_count

    row_start = 13
    row_end = rows_in_sheet

    cell_range = [ "C{}:$H".format(row_start, row_end) ]
    row_data = worksheet.batch_get(cell_range)

    if len(row_data) == 0:
        print("No data loaded, aborting")
        return False
    
    asset_types = [ "Character", "Environment", "Prop"]

    # load casting for episode
    ##path = F"/data/projects/{project['id']}/entities/{episode['id']}/casting"
    #      `/api/data/projects/${episode.project_id}/entities/` + `${episode.id}/casting`
    ##episode_casting = gazu.client.get(path)    
    ##print(episode_casting)
    asset_casting = []    

    for row in row_data[0]:
        if len(row) >= 2:
            asset_type = row[0]
            asset_name = row[1]

            should_import = True
            if len(row) >= 4:
                status = row[3].lower()
                should_import = status != "omit"

            if len(row) >= 6:
                exists = row[5].lower()
                should_import = exists == "yes"

            if not should_import:
                continue

            if asset_type in asset_types:
                ## print(F"Checking {asset_type}: {asset_name}")

                asset = gazu.asset.get_asset_by_name(project, asset_name)
                if not asset:
                    print(F"{asset_name} - Asset not found")
                    continue

                data = {"asset_id": asset["id"], "nb_occurences": 1 }
                asset_casting.append(data)

    if len(asset_casting) > 0:
        path = F"/data/projects/{project['id']}/entities/{episode['id']}/casting"
        gazu.client.put(path, asset_casting)

                # if not asset["id"] in 
                # gazu.shot

def check_asset_casting(asset_name, project_name, episode_name):
    connect_to_server(SwingSettings.get_instance().swing_user(), SwingSettings.get_instance().swing_password())

    project = gazu.project.get_project_by_name(project_name)
    if not project:
        print(F"Error loading project: {project_name}")
        return False

    episode = gazu.shot.get_episode_by_name(project, episode_name)    
    if not episode:
        print(F"Error loading episode: {episode_name}")
        return False                
    
    asset = gazu.asset.get_asset_by_name(project, asset_name)
#    casting = gazu.casting.get_asset_casting(asset)
#    print("get_asset_casting: {}".format(casting))

#    casting = gazu.casting.get_asset_cast_in(asset)
#    print("get_asset_cast_in: {}".format(casting))

    # "/data/projects/<project_id>/episodes/casting",

    path = F"/data/projects/{project['id']}/episodes/casting"
    path = F"/data/projects/{project['id']}/entities/{episode['id']}/casting"
    #      `/api/data/projects/${episode.project_id}/entities/` + `${episode.id}/casting`
    data = gazu.client.get(path)
    _ = '''
        new_casting = [
            {"asset_id": self.asset_id, "nb_occurences": 1},
            {"asset_id": self.asset_character_id, "nb_occurences": 3},
        ]    
    
        self.put(
            "/data/projects/%s/entities/%s/casting"
            % (self.project_id, self.episode_id),
            new_casting,
        )    

    gazu.client.put()
'''
    print(data)

if __name__ == '__main__':
    # sync_asset_index("Tom Gates S3", "TG | Frame Ranges")

    #for i in range(307, 321):
    #    worksheet_name = F"{i}_Assets"
    #    episode_name = F"tg_2d_ep{i}"

    #    print(F"Processing {worksheet_name} for {episode_name}")
    #    cast_episode(spreadsheet_name="TG3_Bid&Estimate_Doc", worksheet_name=worksheet_name, project_name="Tom Gates S3", episode_name=episode_name)

    ## check_asset_casting(asset_name = "tg_char_tom_apron", project_name="Tom Gates S3", episode_name="tg_2d_ep307")

    i = 315
    worksheet_name = F"{i}_Assets"
    episode_name = F"tg_2d_ep{i}"

    print(F"Processing {worksheet_name} for {episode_name}")
    cast_episode(spreadsheet_name="TG3_Bid&Estimate_Doc", worksheet_name=worksheet_name, project_name="Tom Gates S3", episode_name=episode_name)


