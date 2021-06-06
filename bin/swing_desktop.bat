@ECHO OFF

set WORKING_PATH=%SWING_PATH%

if not defined WORKING_PATH (
    WORKING_PATH = "C:\WCA"
)

echo "Running Swing Desktop"
echo "cd %WORKING_PATH% && env\Scripts\activate && %WORKING_PATH%\Scripts\python %WORKING_PATH%/swing/swing-main/module/wildchildanimation/plugin/swing_desktop.py"
cd %WORKING_PATH% && env\Scripts\activate && %WORKING_PATH%\Scripts\python %WORKING_PATH%/swing/swing-main/module/wildchildanimation/plugin/swing_desktop.py