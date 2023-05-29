# Copyright Epic Games, Inc. All Rights Reserved
import unreal

project_settings = None
pipeline_subsystem = None
pipeline_executor = None
render_queue = None

def get_executor_instance():
    unreal.log_warning("MRQ::get_executor_instance")

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

def execute_render(executor_instance=None, is_cmdline=False):
    unreal.log_warning("MRQ::execute_render")
    """
    Starts a render
    :param executor_instance: Executor instance used for rendering
    :param is_cmdline: Flag to determine if the render was executed from a commandline.
    """

    if not executor_instance:
        executor_instance = get_executor_instance()

    if is_cmdline:
        setup_editor_exit_callback(executor_instance)


    # Get a render queue
    pipeline_subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    if not pipeline_subsystem:
        unreal.log_error("MRQ::execute_render - Error loading pipeline subsystem")
        return False

    # Get the project settings
    project_settings = unreal.get_default_object(unreal.MovieRenderPipelineProjectSettings)
    if not project_settings:
        unreal.log_error("MRQ::execute_render - Error loading project settings")
        return False

    # Get the pipeline queue
    render_queue = pipeline_subsystem.get_queue()        
    if not render_queue:
        unreal.log_error("MRQ::execute_render - Error loading render queue")
        return False

    # Start the Render
    unreal.log("MRQ job started...")
    pipeline_subsystem.render_queue_with_executor_instance(executor_instance)

def setup_editor_exit_callback(executor_instance):
    unreal.log_warning("MRQ::setup_editor_exit_callback")

    """
    Setup callbacks for when you need to close the editor after a render
    :param executor_instance: Movie Pipeline executor instance
    """

    unreal.log_warning("Executed job from commandline, setting up shutdown callback..")

    # add a callable to the executor to be executed when the pipeline is done rendering
    executor_instance.on_executor_finished_delegate.add_callable(
        shutdown_editor
    )
    # add a callable to the executor to be executed when the pipeline fails to render
    executor_instance.on_executor_errored_delegate.add_callable(
        executor_failed_callback
    )


def shutdown_editor(movie_pipeline=None, results=None):
    unreal.log_warning("MRQ::shutdown_editor")

    """
    This method shutdown the editor
    """
    unreal.log_warning("Rendering is complete! Exiting...")
    unreal.SystemLibrary.quit_editor()


def executor_failed_callback(executor, pipeline, is_fatal, error):
    unreal.log_warning("MRQ::executor_failed_callback")

    """
    Callback executed when a job fails in the editor
    """
    unreal.log_error(
        f"An error occurred while executing a render.\n\tError: {error}"
    )

    unreal.SystemLibrary.quit_editor()


def get_asset_data(name_or_path, asset_class):
    unreal.log_warning(f"MRQ::get_asset_data Path {name_or_path} Class {asset_class}")

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


# Set the output folder directory

# def set_output_folder(selected_dir):
