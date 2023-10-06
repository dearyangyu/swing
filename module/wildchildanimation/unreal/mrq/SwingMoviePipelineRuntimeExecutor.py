# Copyright Epic Games, Inc. All Rights Reserved.
import unreal

# This example is an implementation of an "executor" which is responsible for
# deciding how a queue is rendered, giving you complete control over the before,
# during, and after of each render. 
#
# This class is an example of how to make an executor which processes a job in a standalone executable launched with "-game".
# You can follow this example to either do a simple integration (read arguments from the command line as suggested here),
# or it can used to implement an advanced plugin which opens a socket or makes REST requests to a server to find out what
# work it should do, such as for a render farm implementation.
#
# We're building a UClass implementation in Python. This allows the Python to
# integrate into the system in a much more intuitive way but comes with some 
# restrictions: 
# Python classes cannot be serialized. This is okay for executors because they are
#   created for each run and are not saved into assets, but means that you cannot
#   implement a settings class as those do need to get saved into preset assets.
# All class properties must be UProperties. This means you cannot use native
#   Python sockets.
#
# This class must inherit from unreal.MoviePipelinePythonHostExecutor. This class also
# provides some basic socket and async http request functionality as a workaround for no
# native Python member variables.
#
# If you are trying to write your own executor based on this example, you will need to create
# a /Content/Python folder and place the custom python file within that folder. Then you will need
# to create an "init_unreal.py" file within that folder and add "import <YourPyModuleName>" to it
# so that Unreal will attempt to parse the class on engine load and it can be spawned by MRQ.
# If your Python file is named MyExecutorWithExtraFeatures.py, then you would add
#
# import MyExecutorWithExtraFeatures
#
# to your init_unreal.py file. 
#
# REQUIREMENTS:
#    Requires the "Python Editor Script Plugin" to be enabled in your project.
#
# USAGE:
#   Use the following command line argument to launch this:
#   UnrealEditor-Cmd.exe <path_to_uproject> <map_name> -game -MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor -ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor -LevelSequence=<path_to_level_sequence> -windowed -resx=1280 -resy=720 -log
#   ie:
#   UnrealEditor-Cmd.exe "E:\SubwaySequencer\SubwaySequencer.uproject" subwaySequencer_P -game -MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor -ExecutorPythonClass=/Engine/PythonTypes.SwingMoviePipelineRuntimeExecutor -LevelSequence="/Game/Sequencer/SubwaySequencerMASTER.SubwaySequencerMASTER" -windowed -resx=1280 -resy=720 -log
#
# If you are looking for how to render in-editor using Python, see the MoviePipelineEditorExample.py script instead.
@unreal.uclass()
class SwingMoviePipelineRuntimeExecutor(unreal.MoviePipelinePythonHostExecutor):

    VERSION = "0.0.0.1"
    
    # Declare the properties of the class here. You can use basic
    # Python types (int, str, bool) as well as unreal properties.
    # You can use Arrays and Maps (Dictionaries) as well
    activeMoviePipeline = unreal.uproperty(unreal.MoviePipeline)
    exampleArray = unreal.Array(str) # An array of strings
    exampleDict = unreal.Map(str, bool) # A dictionary of strings to bools.
    
    # Constructor that gets called when created either via C++ or Python
    # Note that this is different than the standard __init__ function of Python
    def _post_init(self):
        # Assign default values to properties in the constructor
        self.activeMoviePipeline = None
        
        self.exampleArray.append("Example String")
        self.exampleDict["ExampleKey"] = True

    # We can override specific UFunctions declared on the base class with
    # this markup.
    @unreal.ufunction(override=True)
    def execute_delayed(self, inPipelineQueue):
        unreal.log("{}: v{} execute_delayed]".format(self.__class__.__name__, self.VERSION))    
        
        # Here's how we can scan the command line for any additional args such as the path to a level sequence.
        (cmdTokens, cmdSwitches, cmdParameters) = unreal.SystemLibrary.parse_command_line(unreal.SystemLibrary.get_command_line())
        levelSequencePath = None
        try:
            levelSequencePath = cmdParameters['LevelSequence']
            unreal.log(F"Render Level: {levelSequencePath}")
        except:
            unreal.log_error("Missing '-LevelSequence=/Game/Foo/MySequence.MySequence' argument")
            self.on_executor_errored()
            return
        
        outputDir = None
        try:
            outputDir = cmdParameters['OutputDir']
            unreal.log(F"Render Output: {outputDir}")            
        except:
            unreal.log_error("Missing '-OutputDir=D:\Videos\Li\wca_ep000\sc000\sh000\v1' argument")
            self.on_executor_errored()
            return
        
        renderPreset = None
        try:
            renderPreset = cmdParameters['RenderPreset']
            unreal.log(F"Render Preset: {renderPreset}")            
        except:
            unreal.log_error("Missing '-renderPreset=D:\Videos\Li\wca_ep000\sc000\sh000\v1' argument")
            self.on_executor_errored()
            return   

        setFrames = None
        try:
            setFrames = str(cmdParameters['SetFrames']).lower() == 'true' 
            if setFrames:
                unreal.log("Setting Frame Range")            
            else:
                unreal.log("Using Preset FrameRange")            
        except:
            unreal.log_error("Missing '-SetFrames={true/false}' argument")
            self.on_executor_errored()
            return                       
        
        if setFrames:
            frameIn = None
            try:
                frameIn = cmdParameters['FrameIn']
                unreal.log(F"Frame In: {frameIn}")            
            except:
                unreal.log_error("Missing '-FrameIn=xxxx' argument")
                self.on_executor_errored()
                return                       
            
            frameOut = None
            try:
                frameOut = cmdParameters['FrameOut']
                unreal.log(F"Frame Out: {frameOut}")            
            except:
                unreal.log_error("Missing '-FrameOut=xxxx' argument")
                self.on_executor_errored()
                return    

        shotPrefix = None
        try:
            shotPrefix = cmdParameters['ShotPrefix']
            unreal.log(F"ShotPrefix: {shotPrefix}")            
        except:
            unreal.log_error("Missing '-ShotPrefix=proj_seq_shot_task' argument")
            self.on_executor_errored()
            return                              

        # get render settings
        mrq_preset_asset = unreal.load_asset(renderPreset)
        mrq_preset_data_asset = unreal.AssetRegistryHelpers.create_asset_data(mrq_preset_asset)        

        # A movie pipeline needs to be initialized with a job, and a job
        # should be owned by a Queue so we will construct a queue, make one job
        # and then configure the settings on the job. If you want inPipelineQueue to be
        # valid, then you must pass a path to a queue asset via -MoviePipelineConfig. Here
        # we just make one from scratch with the one level sequence as we didn't implement
        # multi-job handling.
        self.pipelineQueue = unreal.new_object(unreal.MoviePipelineQueue, outer=self)
        unreal.log("Building Queue...")
        
        # Allocate a job. Jobs hold which sequence to render and what settings to render with.
        newJob = self.pipelineQueue.allocate_new_job(unreal.MoviePipelineExecutorJob)

        newJob.set_configuration(mrq_preset_data_asset.get_asset())
        newJob.sequence = unreal.SoftObjectPath(levelSequencePath)
        
        # Now we can configure the job. Calling find_or_add_setting_by_class is how you add new settings.
        outputSetting = newJob.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)
        
        ## outputSetting.output_resolution = unreal.IntPoint(1280, 720)

        '''
A list of {format_strings} and example values that are valid to use in the File Name Format:

level_name => Main
sequence_name => ls_ep000_sc010_sh010
job_name => ls_ep000_sc010_sh010
frame_rate => 25.0
date => 2023.10.03
time => 09.54.00
year => 2023
month => 10
day => 03
version => v00x
job_author => pniemandt
frame_number => 0000
frame_number_shot => 0000
frame_number_rel => 0000
frame_number_shot_rel => 0000
camera_name => CameraName
shot_name => ShotName
render_pass => RenderPassName
project_dir => D:/Productions/hnl/hnl_ue/hnl_build_v001_5.3/
output_resolution => 1920_1080
output_width => 1920
output_height => 1080        
        '''

        outputSetting.output_directory.set_editor_property("path", outputDir)
        #outputSetting.file_name_format = "{sequence_name}_{shot_name}.{frame_number}"
        outputSetting.file_name_format = ""
        outputSetting.file_name_format += F"{shotPrefix}_"
        outputSetting.file_name_format += "{frame_number}"

        if setFrames:
            outputSetting.use_custom_playback_range = True
            outputSetting.custom_start_frame = int(frameIn)
            outputSetting.custom_end_frame = int(frameOut)
        
        combinedPath = unreal.Paths.combine([outputSetting.output_directory.path, outputSetting.file_name_format])        

        # Create the params struct
        params = unreal.MoviePipelineFilenameResolveParams()

        #params.frame_number = 55
        #params.frame_number_shot = 23
        #params.frame_number_rel = 12
        #params.frame_number_shot_rel = 3
        params.camera_name_override = newJob.shot_info[0].inner_name
        params.shot_name_override = newJob.shot_info[0].outer_name
        params.zero_pad_frame_number_count = 3
        params.force_relative_frame_numbers = False
        #params.file_name_format_overrides["ext"] = "jpg"
        params.initialization_time = unreal.MathLibrary.utc_now()
        params.initialization_version = 3

        params.job = newJob
        params.shot_override = newJob.shot_info[0]
        
        (resolvedPath, mergedFormatArgs) = unreal.MoviePipelineLibrary.resolve_filename_format_arguments(combinedPath, params)
        
        unreal.log("Resolved Path: " + resolvedPath)        
        
        # Ensure there is something to render
        ## newJob.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)

        # Ensure there's a file output.
        ## newJob.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)
        
        # This is important. There are several settings that need to be
        # initialized (just so their default values kick in) and instead
        # of requiring you to add every one individually, you can initialize
        # them all in one go at the end.
        newJob.get_configuration().initialize_transient_settings()
        
        # Now that we've set up the minimum requirements on the job we can created
        # a movie render pipeline to run our job. Construct the new object
        self.activeMoviePipeline = unreal.new_object(self.target_pipeline_class, outer=self.get_last_loaded_world(), base_type=unreal.MoviePipeline)
        
        # Register to any callbacks we want
        self.activeMoviePipeline.on_movie_pipeline_finished_delegate.add_function_unique(self, "on_movie_pipeline_finished")
        
        # And finally tell it to start working. It will continue working
        # and then call the on_movie_pipeline_finished_delegate function at the end.
        self.activeMoviePipeline.initialize(newJob)
   
    # This function is called every frame and can be used to do simple countdowns, checks
    # for more work, etc. Can be entirely omitted if you don't need it.
    @unreal.ufunction(override=True)
    def on_begin_frame(self):
        # It is important that we call the super so that async socket messages get processed.
        super(SwingMoviePipelineRuntimeExecutor, self).on_begin_frame()        
        
        if self.activeMoviePipeline:
            unreal.log("Progress: %f" % unreal.MoviePipelineLibrary.get_completion_percentage(self.activeMoviePipeline))
           
   
    # This is NOT called for the very first map load (as that is done before Execute is called).
    # This means you can assume this is the resulting callback for the last open_level call.
    @unreal.ufunction(override=True)
    def on_map_load(self, inWorld):

        unreal.log("on_map_load: ")       
        # We don't do anything here, but if you were processing a queue and needed to load a map
        # to render a job, you could call:
        # 
        # unreal.GameplayStatics.open_level(self.get_last_loaded_world(), mapPackagePath, True, gameOverrideClassPath)
        # 
        # And then know you can continue execution once this function is called. The Executor
        # lives outside of a map so it can persist state across map loads.
        # Don't call open_level from this function as it will lead to an infinite loop.
        pass
        
        
    # This needs to be overriden. Doens't have any meaning in runtime executors, only
    # controls whether or not the Render (Local) / Render (Remote) buttons are locked
    # in Editor executors.
    @unreal.ufunction(override=True)
    def is_rendering(self):
        return False
        
    # This declares a new UFunction and specifies the return type and the parameter types
    # callbacks for delegates need to be marked as UFunctions.
    @unreal.ufunction(ret=None, params=[unreal.MoviePipeline, bool])
    def on_movie_pipeline_finished(self, inMoviePipeline, bSuccess):
        # We're not processing a whole queue, only a single job so we can
        # just assume we've reached the end. If your queue had more than 
        # one job, now would be the time to increment the index of which
        # job you are working on, and start the next one (instead of calling
        # on_executor_finished_impl which should be the end of the whole queue)
        unreal.log("Finished rendering movie! Success: " + str(bSuccess))
        self.activeMoviePipeline = None
        self.on_executor_finished_impl()
        
    @unreal.ufunction(ret=None, params=[str])
    def on_socket_message(self, message):
        # Message is a UTF8 encoded string. The system expects
        # messages to be sent over a socket with a uint32 to describe
        # the message size (not including the size bytes) so
        # if you wanted to send "Hello" you would send 
        # uint32 - 5
        # uint8 - 'H'
        # uint8 - 'e' 
        # etc.
        # Socket messages sent from the Executor will also be prefixed with a size.
        pass
        
    @unreal.ufunction(ret=None, params=[int, int, str])
    def on_http_response_recieved(self, inRequestIndex, inResponseCode, inMessage):
        # This is called when an http response is returned from a request.
        # the request index will match the value returned when you made the original 
        # call, so you can determine the original intent this response is for.
        pass