@ECHO OFF

set WORKING_PATH=%SWING_PATH%

IF NOT DEFINED WORKING_PATH (SET WORKING_PATH=C:\WCA)

echo "Running Swing Update"
python ..\module\wildchildanimation\gui\swing_updater.py --force

