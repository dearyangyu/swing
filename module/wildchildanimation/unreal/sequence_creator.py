# -*- coding: utf-8 -*-
#
# Author: Wian Jacobs
# Date: 2022-11-29
#
# Unreal Sequence Create script
# 
# Update: 2022-12-14
#

import unreal
import re

class SwingUESequencer:

    VERSION = "0.4"

    def __init__(self):
        # get asset tools
        self.asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        unreal.log("{}: Created".format(self.__class__.__name__,))

        self.num_handles = 0

    def split_episode_name(self, episode):
        episode_name = re.sub(r'\d_+', '', episode)
        episode_number = re.sub(r"([a-zA-Z_]+)", '', episode)

        return episode_name.strip(), int(episode_number.strip())

    def get_sequence_number(self, sequence):
        sequence_number = re.sub(r"([a-zA-Z_]+)", '', sequence)

        return int(sequence_number.strip())        

    def CreateMasterSequence(self, episode, sequence, shot_amount, total_frame_array, shot_names_array, handles):   # all parameters should come from Kitsu
        unreal.log("{}: Ep Nr [{}], Ep Name [{}], Scene [{}] Number of Shots: {}".format(self.__class__.__name__, "CreateMasterSequence", episode, sequence, shot_amount))

        self.num_handles = handles

        self.episode = episode.lower()
        self.sequence = sequence.lower()

        self.episode_name, self.episode_number = self.split_episode_name(self.episode)
        self.sequence_number = self.get_sequence_number(self.sequence)

        master_sequence_name = "sl_{}_{}".format(self.episode, self.sequence)
        # master_sequence_name = "sl_" + (str(episode_nr)) + "_" + (str(episode_name)) + "_sc0" + (str(scene_nr))

        ue_path = "/Game/cinematics/episodes/{}".format(self.episode)
        # ue_path = "/Game/cinematics/episodes/" + (str(episode_nr)) + "_" + (str(episode_name))

        master_sequence_length = 0
        for element in total_frame_array:   
            master_sequence_length += (element) + 1     # set master sequence length to sum of all shot lengths

        # creates the master sequence
        master_sequence = unreal.AssetTools.create_asset(self.asset_tools, asset_name = master_sequence_name, package_path = ue_path, asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())

        # add master track
        scene_track_01 = master_sequence.add_master_track(unreal.MovieSceneCinematicShotTrack)

        # set master sequence playback length
        master_sequence.set_playback_end(master_sequence_length)

        self.CreateShotSequences(self.episode, self.sequence, total_frame_array, shot_names_array, scene_track_01)

    def CreateShotSequences(self, episode, sequence, total_frame_array, shot_names_array, master_track_01):  # shot parameters should get from Kitsu
        shot_amount = len(shot_names_array)
        _, episode_number = self.split_episode_name(episode)        
        current_frame = 0
        shcount = 1

        while shcount <= shot_amount:   # for each shot
            shot = shot_names_array[shcount - 1]

            # ue_path = "/Game/cinematics/episodes/" + (str(episode_nr)) + "_" + (str(episode_name)) + "/" + sc_string + (str(scene_nr)) + "/" + sh_string
            ue_path = "/Game/cinematics/episodes/{}/{}/{}".format(episode, sequence, shot)

            unreal.log("{}: {} {} {} {}".format(self.__class__.__name__, "CreateShotSequences", "create_asset", shot, ue_path))

            shot_sequence = unreal.AssetTools.create_asset(self.asset_tools, asset_name = shot, package_path = ue_path, asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
            shot_total_frames = total_frame_array[shcount - 1] + self.num_handles - 1   # Add handle amount to shot lenths as a buffer on each shot

            # add shots to the master track(s)
            self.AddShotsToTrack(master_track_01, shot_sequence, current_frame, shot_total_frames)

            # create sub sequences for Lighting & Sky
            self.CreateSubSequences(ue_path, shot, shot_sequence, shot_total_frames)

            # spawn cine camera actor
            ##_, episode_number = self.split_episode_name(episode)
            ## sc_string = self.get_sequence_number(sequence)

            # camera_name = (str(episode_number)) + "_" + sc_string + (str(scene_nr)) + "_" + sh_string
            camera_name = "{}_{}_{}".format(episode_number, sequence, shot)

            self.CreateCamera(shot_sequence, camera_name, shot_total_frames)

            # update current_frame to end of this shot
            current_frame += shot_total_frames
            shcount += 1

    def AddShotsToTrack(self, master_track_01, shot_sequence, current_frame, shot_total_frames):
        # add section to the master sequence track
        section = master_track_01.add_section()
        # add shot sequence to the section
        section.set_editor_property('sub_sequence', shot_sequence)
        # set section start to end frame range
        section.set_range(current_frame, (current_frame + shot_total_frames))
        # set shot sequence playback end
        shot_sequence.set_playback_end(shot_total_frames)


    def CreateSubSequences(self, ue_path, sh_string, shot_sequence, shot_total_frames): #(Lighting & Sky)
        # add level sequences for lighting and sky sub systems
        lighting_shot_name = sh_string + "_lighting"
        shot_sequence_lighting = unreal.AssetTools.create_asset(self.asset_tools, asset_name = lighting_shot_name, package_path = ue_path, asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())
        sky_shot_name = sh_string + "_sky"
        shot_sequence_sky = unreal.AssetTools.create_asset(self.asset_tools, asset_name = sky_shot_name, package_path = ue_path, asset_class = unreal.LevelSequence, factory = unreal.LevelSequenceFactoryNew())

        # add subsequence tracks to sub sequences (lighting & sky)
        scene_track_ss02 = shot_sequence.add_master_track(unreal.MovieSceneSubTrack)    # Sky track
        section_ss02 = scene_track_ss02.add_section()
        section_ss02.set_editor_property('sub_sequence', shot_sequence_sky)
        section_ss02.set_range(0, shot_total_frames)
        shot_sequence_sky.set_playback_end(shot_total_frames)
        ###
        scene_track_ss01 = shot_sequence.add_master_track(unreal.MovieSceneSubTrack)    # Lightning track
        section_ss01 = scene_track_ss01.add_section()
        section_ss01.set_editor_property('sub_sequence', shot_sequence_lighting)
        section_ss01.set_range(0, shot_total_frames)
        shot_sequence_lighting.set_playback_end(shot_total_frames)

        self.CreateFolders(shot_sequence, shot_sequence_lighting, shot_sequence_sky)

    def CreateCamera(self, sequence, camera_name, total_frames):
        camera_cut_track = sequence.add_master_track(unreal.MovieSceneCameraCutTrack) 
        cam_binding = None
        for binding in [x for x in sequence.get_bindings()]:
            if binding.get_name() == camera_name:
                if not binding.get_tracks(): continue
                cam_binding = binding

        if not cam_binding:
            cam_binding = self.AddCameraToSequence(sequence, camera_cut_track, camera_name, total_frames)

    def AddCameraToSequence(self, sequence, camera_cut_track, camera_name, total_frames):
        camera_cut_section = camera_cut_track.add_section()
        camera_cut_section.set_range(0, total_frames)

        camera_actor = unreal.EditorLevelLibrary().spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector(0, 0, 0))
        camera_actor.set_actor_label(camera_name)
        camera_binding = sequence.add_spawnable_from_instance(camera_actor)

        camera_component = camera_actor.get_cine_camera_component()
        camera_component_binding = sequence.add_possessable(camera_component)
        camera_component_binding.set_parent(camera_binding)

        camera_component.set_filmback_preset_by_name("16:9 DSLR")
        
        camera_binding_id = unreal.MovieSceneObjectBindingID()
        camera_binding_id.set_editor_property('Guid', camera_binding.get_id())
        camera_cut_section.set_editor_property('CameraBindingID', camera_binding_id)

        # add binding to camera cut track
        camera_cut_track_binding = sequence.make_binding_id(camera_binding, unreal.MovieSceneObjectBindingSpace.LOCAL)
        camera_cut_section.set_camera_binding_id(camera_cut_track_binding)

        self.AddCameraTracks(camera_binding, camera_component_binding, total_frames)

        self.RemoveDuplicateBindings(sequence)
        
        camera_actor.destroy_actor()
        return camera_binding

    def AddCameraTracks(self, camera_binding, camera_component_binding, total_frames):
        focal_length_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
        focal_length_track.set_property_name_and_path('Current Focal Length', 'CurrentFocalLength')
        focal_length_section = focal_length_track.add_section()
        focal_length_section.set_start_frame_bounded(0)
        focal_length_section.set_end_frame_bounded(total_frames)
        focal_length_section.get_channels()[0].set_default(35.0)
        
        manual_focus_distance_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
        manual_focus_distance_track.set_property_name_and_path('Manual Focus Distance (focus settings)', 'FocusSettings.ManualFocusDistance')
        manual_focus_distance_section = manual_focus_distance_track.add_section()
        manual_focus_distance_section.set_start_frame_bounded(0)
        manual_focus_distance_section.set_end_frame_bounded(total_frames)
        manual_focus_distance_section.get_channels()[0].set_default(100000.0)
        
        current_aperture_track = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)
        current_aperture_track.set_property_name_and_path('Current Aperture', 'CurrentAperture')
        current_aperture_section = current_aperture_track.add_section()
        current_aperture_section.set_start_frame_bounded(0)
        current_aperture_section.set_end_frame_bounded(total_frames)
        current_aperture_section.get_channels()[0].set_default(2.8)

        transform_track = camera_binding.add_track(unreal.MovieScene3DTransformTrack)
        transform_section = transform_track.add_section()
        transform_section.set_start_frame_bounded(0)
        transform_section.set_end_frame_bounded(total_frames)

    def RemoveDuplicateBindings(self, sequence):
        bs = []
        bindings = sequence.get_bindings()
        for b in bindings:
            if (bs.__contains__(b.get_name())):
                b.remove()
            else:
                bs.append(b.get_name())


    def CreateFolders(self, shot_sequence, lighting_sequence, sky_sequence):
        '''
        # create folders
        folder_cache = shot_sequence.add_root_folder_to_sequence("cache")
        folder_geo = shot_sequence.add_root_folder_to_sequence("geo")

        # change folder colors
        folder_cache.set_folder_color(unreal.Color(255, 140, 0, 255))   # change cache folder color to blue
        folder_geo.set_folder_color(unreal.Color(0, 255, 0, 255))       # change geo folder color to green
        
        # create sub folders
        sub_folder_char = shot_sequence.add_root_folder_to_sequence("char")
        sub_folder_prop = shot_sequence.add_root_folder_to_sequence("prop")
        sub_folder_var = shot_sequence.add_root_folder_to_sequence("var")

        sub_folder_transform = shot_sequence.add_root_folder_to_sequence("transform")
        sub_folder_visibility = shot_sequence.add_root_folder_to_sequence("visibility")
        sub_folder_shader = shot_sequence.add_root_folder_to_sequence("shader")

        # add subfolders to folders
        sub_folder_char = folder_cache.add_child_folder(sub_folder_char)
        sub_folder_prop = folder_cache.add_child_folder(sub_folder_prop)
        sub_folder_var = folder_cache.add_child_folder(sub_folder_var)

        sub_folder_transform = folder_geo.add_child_folder(sub_folder_transform)
        sub_folder_visibility = folder_geo.add_child_folder(sub_folder_visibility)
        sub_folder_shader = folder_geo.add_child_folder(sub_folder_shader)
        '''
        # create subsequence folders
        lighting_sequence.add_root_folder_to_sequence("master")
        lighting_sequence.add_root_folder_to_sequence("char")

        sky_sequence.add_root_folder_to_sequence("color")
        sky_sequence.add_root_folder_to_sequence("cloud")
