# <center>Wild Child Animation .EXRs to .Mov Conversion Module</center>

## INTRODUCTION:
#### This module converts EXRs files in .mov file. In process of conversion module first convert exrs file to png files and then uses ffmpeg to convert pngs into .mov file with Codec: MPEG-H Part2/HEVC(H.265)(hev1)<hr><br>

## How to use the class: class Convert():
### 1. Initialising class:
### <p style="margin:10">Initialise the class with 3 required parameters, (1) working directory, (2) directory where exrs are located and (3) directory where converted pngs can get stored. For smooth functionality make sure both exrs and pngs folders are inside your working directory given as first parameter. If Pngs folder is not created then it will get created. Audio file parameter is not required by default, if it is not provided then vidoe will be without audio. Please follow the example below.</P>
<code style="color:lightgreen">
<blockquote>
    
    working_dir = os.getcwd()
    
    exrs=r'C:\Users\username\Desktop\exr-to-png-to-mp4-v-001\exrs\sh010'
    pngs=r'C:\Users\username\Desktop\exr-to-png-to-mp4-v-001\pngs\sh010'
    audio=r'C:\Users\username\Desktop\exr-to-png-to-mp4-v-001\audio\witw_104lcd_sc090_sh020.wav'
    
    convert = Convert(working_dir, exrs, pngs, audio)
</blockquote>
</code>

<h3><b>Other parameters class can take and their default values:</b></h3>

1. Audio path where scene audio file is located. Default value is an empty string as <b>audio_path="",</b>.
2. Preset_speed it is the option between quality or time. Means more time better quality or less time lesser the quality. Default value is 'veryfast' <b>preset_speed="veryfast"</b>. Available options are ‘veryfast’ ‘faster’, ‘fast’, ‘medium’, ‘slow’, ‘slower’, ‘veryslow’.
3. Framerate(FPS) default value is 25, <b>framerate=25.</b>. This is an integer and can be set to the required integer value.
4. Last 3 parameters take information to write as metadata information on the file. <b>artist="wca-teams", album="wotw" genere="children-animation".</b>
<hr><br>

## Class Methods:
### 1. add_meta_information()
### 2. check_exr_files()
### 3. check_png_folder_is_empty()
### 4. rename_png_files()
### 5. exr_to_png_converter()
### 6. ffmpeg_convert_command()
### 7. exr_to_png_mp4_convert()
<br>
<h2><u>1. add_meta_information():</u></h2>
<p>The function runs the loop on array which contains all metadata information as string and returns part of ffmpeg command that updates metadata infomration on the video file. Return value will look like this <b>-metadata title='104_sc100' -metadata artist='WCA-Teams' -metadata album='WOTW' -metadata genre='children-animation' </b></p>

<br>
<h2><u>2. check_exr_files():</u></h2>
<p>The functions checks that if all files are proper exr files and there are no other files in the folder. It returns <b>True</b> or exits with <b>Error: with the file name</b> which is not correct exr file.</p>

<br>
<h2><u>3. check_png_folder_is_empty():</u></h2>
<p>The functions checks that folder provided to create png file is empty. To make sure image sequnces is not picking up files which are not part of png sequence. If folder is empty function returns <b>True</b> otherwise exit with the error that png folder is not empty.</p>

<br>
<h2><u>4. rename_png_files():</u></h2>
<p>The functions rename all pngs into the 4 digits 0's sequence. This is required to run regular epression that is part of ffmpeg command to pick up image sequence so they are added correctly with correct sequence in video file. Once the files are converted function returns <b>True</b>.</p>


<br>
<h2><u>5. exr_to_png_converter():</u></h2>
<p>The function uses numpy and Imath logics to convert exr files into high quality png files. Function takes exrs file path and pngs file path then converts exrs files to path given for png files. Once all files are converted funciton returns <b>True</b>.</p><br>

<br>
<h2><u>6. ffmpeg_convert_command():</u></h2>
<p>This function is taking different parts of ffmpeg command example audio part, metadata part etc and joins them into one ffmpeg convert command and returns the completed ffmpeg command.</p><br>

<br>
<h2>7. exr_to_png_mp4_convert():</h2>
<p>This function function takes the returned ffmpeg command from above function and runs it on the pngs folder to convert them into complete .mov video file. Function uses subprocess.Popen to run the final ffmpeg on operating system shell. Final output.mov file is created in working directory with the names taken from exrs files. <b>For example 104_sc100.mov</b></p><br><hr>

## Downloading and installing packages
## Deployment:-
### <u>To Download EXR for Python version 3.9.5:-</u>
##### 1. Visit the site https://www.lfd.uci.edu/~gohlke/pythonlibs/ search or look for OpenEXR binaries.
##### 2. Copy downloaded file inside your python scripts pip folder "C:\Program Files\Python39\Scripts".
##### 3. Type pip install and write the name of downloaded file to install OpenEXR package librairies. 
### <u>Other required python packages:-</u>
##### 1. pip install numpy
##### 2. pip install imath
##### 3. pip install pillow
