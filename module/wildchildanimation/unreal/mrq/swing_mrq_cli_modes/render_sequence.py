# Copyright Epic Games, Inc. All Rights Reserved

"""
This script handles processing jobs for a specific sequence
"""

import unreal

from getpass import getuser

import unreal
import os

from getpass import getuser

# Get a render queue
pipeline_subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)

# Get the project settings
project_settings = unreal.get_default_object(unreal.MovieRenderPipelineProjectSettings)

# Get the pipeline queue
render_queue = pipeline_subsystem.get_queue()

pipeline_executor = None

def get_executor_instance():
    """
    Method to return an instance of a render executor
    :return: Executor instance
    """

    # Convert the SoftClassPath into a SoftClassReference.
    # local executor class from the project settings
    soft_class_ref = unreal.MoviePipelinePIEExecutor
    # Get the executor class as this is required to get an instance of the executor
    executor_class = unreal.SystemLibrary.load_class_asset_blocking(soft_class_ref)
    global pipeline_executor
    pipeline_executor = unreal.new_object(executor_class)

    return pipeline_executor


def execute_render( executor_instance=None, is_cmdline=False):
    """
    Starts a render
    :param executor_instance: Executor instance used for rendering
    :param is_cmdline: Flag to determine if the render was executed from a commandline.
    """

    if not executor_instance:
        executor_instance = get_executor_instance()

    if is_cmdline:
        setup_editor_exit_callback(executor_instance)

    # Start the Render
    unreal.log("MRQ job started...")

    pipeline_subsystem.render_queue_with_executor_instance(executor_instance)

def setup_editor_exit_callback(executor_instance):
    """
    Setup callbacks for when you need to close the editor after a render
    :param executor_instance: Movie Pipeline executor instance
    """

    unreal.log("Executed job from commandline, setting up shutdown callback..")

    # add a callable to the executor to be executed when the pipeline is done rendering
    executor_instance.on_executor_finished_delegate.add_callable(
        shutdown_editor
    )
    # add a callable to the executor to be executed when the pipeline fails to render
    executor_instance.on_executor_errored_delegate.add_callable(
        executor_failed_callback
    )

def shutdown_editor(movie_pipeline=None, results=None):
    """
    This method shutdown the editor
    """
    unreal.log("Rendering is complete! Exiting...")
    unreal.SystemLibrary.quit_editor()


def executor_failed_callback(executor, pipeline, is_fatal, error):
    """
    Callback executed when a job fails in the editor
    """
    unreal.log_error(
        f"An error occurred while executing a render.\n\tError: {error}"
    )

    unreal.SystemLibrary.quit_editor()


def get_asset_data(name_or_path, asset_class):
    """
    Get the asset data for the asset name or path based on its class.
    :param name_or_path: asset name or package name
    :param asset_class: Asset class filter to use when looking for assets in registry
    :raises RuntimeError
    :return: Asset package if it exists
    """
    # Get all the specified asset class assets in the project. This is the only mechanism
    # we can think of at the moment to allow shorter path names in the
    # commandline interface. This will allow users to only provide the
    # asset name or the package path in the commandline interface
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_registry.get_assets_by_class(asset_class, True)

    # This lookup could potentially be very slow
    for asset in assets:
        # If a package name is provided lookup the package path
        if name_or_path.startswith("/Game"):
            if asset.package_name == name_or_path:
                return asset
        else:
            if asset.asset_name == name_or_path:
                return asset
    else:
        raise RuntimeError(f"`{name_or_path}` could not be found!")    


def process_render(args):
    unreal.log("MRQ::process_render")

    render_map = args.map    
    render_seq = args.sequence
    render_preset = args.preset
    render_target = args.output_dir
    render_x = args.resx
    render_y = args.resy
    render_cmdline = args.cmdline

    unreal.log_warning(f"MRQ::process_render: render_map = {render_map}")
    unreal.log_warning(f"MRQ::process_render: render_seq = {render_seq}")
    unreal.log_warning(f"MRQ::process_render: render_preset = {render_preset}")
    unreal.log_warning(f"MRQ::process_render: render_target = {render_target}")
    unreal.log_warning(f"MRQ::process_render: render_x = {render_x}")
    unreal.log_warning(f"MRQ::process_render: render_y = {render_y}")
    unreal.log_warning(f"MRQ::process_render: render_cmdline = {render_cmdline}")

    process_render(render_map, render_seq, render_preset)

def process_render(args):
    unreal.log("MRQ::process_render")

    ### Process Args
    #parser.add_argument("-m", "--map", description="Unreal Map", action="store")
    #parser.add_argument("-s", "--sequence", description="Unreal Sequence", action="store")
    #parser.add_argument("-p", "--preset", "MRQ Preset", action="true")
    #parser.add_argument("-o", "--output_dir", "Output Directory", action="true")
    #parser.add_argument("-x", "--resx", description="X Resolution", action="true", default=1920)
    #parser.add_argument("-y", "--resy", description="Y Resolution", action="true", default=1080)
    #parser.add_argument("-c", "--cmdline", desription="Execute from Command Line", action="store_true")

    render_map = args.map    
    render_seq = args.sequence
    render_preset = args.preset
    render_target = args.output_dir
    render_x = args.resx
    render_y = args.resy
    render_cmdline = args.cmdline

    unreal.log_warning(f"MRQ::process_render: render_map = {render_map}")
    unreal.log_warning(f"MRQ::process_render: render_seq = {render_seq}")
    unreal.log_warning(f"MRQ::process_render: render_preset = {render_preset}")
    unreal.log_warning(f"MRQ::process_render: render_target = {render_target}")
    unreal.log_warning(f"MRQ::process_render: render_x = {render_x}")
    unreal.log_warning(f"MRQ::process_render: render_y = {render_y}")
    unreal.log_warning(f"MRQ::process_render: render_cmdline = {render_cmdline}")

    # The queue subsystem behaves like a singleton so
    # clear all the jobs in the current queue.
    try:
        render_queue.delete_all_jobs()
    except:
        unreal.log_error("MRQ::process_render: Error clearing old jobs")

    render_job = render_queue.allocate_new_job(unreal.MoviePipelineExecutorJob)

    # Set the author on the job
    render_job.author = getuser()

    render_job.author = getuser()

    sequence_data_asset = get_asset_data(args.sequence, "LevelSequence")

    # Create a job in the queue
    unreal.log(f"Creating render job for `{sequence_data_asset.asset_name}`")
    render_job.job_name = sequence_data_asset.asset_name

    unreal.log(f"Setting the job sequence to `{sequence_data_asset.asset_name}`")
    render_job.sequence = sequence_data_asset.to_soft_object_path()

    map_data_asset = get_asset_data(args.map, "World")
    unreal.log(f"Setting the job map to `{map_data_asset.asset_name}`")
    render_job.map = map_data_asset.to_soft_object_path()

    mrq_preset_data_asset = get_asset_data(args.mrq_preset, "MoviePipelineMasterConfig")
    unreal.log(f"Setting the movie pipeline preset to `{mrq_preset_data_asset.asset_name}`")
    render_job.set_configuration(mrq_preset_data_asset.get_asset())

    # output settings
    outputSetting = render_job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    outputSetting.output_directory.set_editor_property("path", "W:/Renders/SDMP/"+ "{}".format(args.render_out_dir))
    unreal.Paths.combine([outputSetting.output_directory.path, args.render_out_dir, outputSetting.file_name_format])

    unreal.log_warning("These are the project settings {}".format(outputSetting.output_directory.path))

    # MRQ added the ability to enable and disable jobs. Check to see is a job is disabled and enable it.
    # The assumption is we want to render this particular job.
    # Note this try/except block is for backwards compatibility
    try:
        if not render_job.enabled:
            render_job.enabled = True
    except AttributeError:
        pass

    try:
        # Execute the render. This will execute the render based on whether its remote or local
        execute_render( is_cmdline=args.cmdline)

    except Exception as err:
        unreal.log_error(f"An error occurred executing the render.\n\tError: {err}")
        raise

    return True    


    pipelineQueue = unreal.new_object(unreal.MoviePipelineQueue)
    unreal.log_warning(f"MRQ::process_render: created {pipelineQueue}")
    
    # Allocate a job. Jobs hold which sequence to render and what settings to render with.
    newJob = pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)
    unreal.log_warning(f"MRQ::process_render: created {newJob}")
    
    newJob.sequence = unreal.SoftObjectPath(render_seq)  
    unreal.log_warning(f"MRQ::process_render: newJob {newJob}")  

    # Now we can configure the job. Calling find_or_add_setting_by_class is how you add new settings.
    outputSetting = newJob.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    outputSetting.output_resolution = unreal.IntPoint(render_x, render_y)
    unreal.log_warning(f"MRQ::process_render: set resolution {render_x},{render_y}") 

    outputSetting.file_name_format = "{sequence_name}.{frame_number}"  
    unreal.log_warning("MRQ::process_render: set filename format {sequence_name}.{frame_number}")     

    # Ensure there is something to render
    newJob.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)
    unreal.log_warning("MRQ::process_render: Ensure there is something to render")    

    # Ensure there's a file output.
    newJob.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
    unreal.log_warning("MRQ::process_render: Ensure there's a file output")        

    # This is important. There are several settings that need to be
    # initialized (just so their default values kick in) and instead
    # of requiring you to add every one individually, you can initialize
    # them all in one go at the end.
    newJob.get_configuration().initialize_transient_settings()    
    unreal.log_warning("MRQ::process_render: initialize_transient_settings")   

    target_pipeline_class = None
    activeMoviePipeline = unreal.new_object(target_pipeline_class, base_type=unreal.MoviePipeline);             

    activeMoviePipeline.initialize(newJob)

    return False

    # Set the author on the job
    render_job.author = getuser()

    sequence_data_asset = get_asset_data(render_seq, "LevelSequence")
    if sequence_data_asset:
        unreal.log_warning(f"MRQ::process_render: Loaded sequence {render_seq}")
    else:
        unreal.log_error(f"MRQ::process_render: Error loading sequence {render_seq}")
        return False
    
    # Create a job in the queue
    unreal.log(f"MRQ::process_render: Creating render job for `{sequence_data_asset.asset_name}`")
    render_job.job_name = sequence_data_asset.asset_name

    unreal.log(f"MRQ::process_render: Setting the job sequence to `{sequence_data_asset.asset_name}`")
    render_job.sequence = sequence_data_asset.to_soft_object_path()

    map_data_asset = get_asset_data(render_map, "World")
    if map_data_asset:
        unreal.log_warning(f"MRQ::process_render: Loaded map {render_map}")
    else:
        unreal.log_error(f"MRQ::process_render: Error loading map {render_map}")
        return False

    unreal.log(f"Setting the job map to `{map_data_asset.asset_name}`")
    render_job.map = map_data_asset.to_soft_object_path()

    mrq_preset_data_asset = get_asset_data(render_preset, "MoviePipelineMasterConfig")
    if map_data_asset:
        unreal.log_warning(f"MRQ::process_render: Loaded render preset {render_preset}")
    else:
        unreal.log_error(f"MRQ::process_render: Error loading render preset {render_preset}")
        return False

    unreal.log(f"Setting the movie pipeline preset to `{mrq_preset_data_asset.asset_name}`")
    render_job.set_configuration(mrq_preset_data_asset.get_asset())

    # output settings
    outputSetting = render_job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
    if outputSetting:
        unreal.log_warning("MRQ::process_render: Loaded outputsettings")
    else:
        unreal.log_error("MRQ::process_render: Error loading outputsettings")
        return False    

    outputSetting.output_directory.set_editor_property("path", render_target)

    unreal.Paths.combine([outputSetting.output_directory.path, render_target, outputSetting.file_name_format])
    unreal.log_warning(f"MRQ::process_render: Render Target {outputSetting.output_directory.path}")

    # MRQ added the ability to enable and disable jobs. Check to see is a job is disabled and enable it.
    # The assumption is we want to render this particular job.
    # Note this try/except block is for backwards compatibility
    try:
        if not render_job.enabled:
            render_job.enabled = True
    except AttributeError:
        pass

    try:
        # Execute the render. This will execute the render based on whether its remote or local
        ###UE 5 Maybe ? 
        execute_render(is_cmdline=args.cmdline)

    except Exception as err:
        unreal.log_error(f"An error occurred executing the render.\n\tError: {err}")
        raise
