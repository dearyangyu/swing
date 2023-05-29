@ECHO OFF

set WORKING_PATH=%SWING_PATH%

IF NOT DEFINED WORKING_PATH (SET WORKING_PATH=Z:\env\wca)

echo "Running Swing Desktop"
cd %WORKING_PATH% && %WORKING_PATH%\env\Scripts\activate && %WORKING_PATH%\env\Scripts\python.exe %WORKING_PATH%\swing\swing-main\module\wildchildanimation\plugin\swing_desktop.py
