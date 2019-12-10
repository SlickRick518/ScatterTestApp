@echo off
:: Auto install script for fast and easy deployment.
color 03
title Build Environment
set directory= ScatterTestApp
for %%a in ("%~dp0\.") do set "parent=%%~nxa"
if %parent% == %directory% goto :install
if not %parent% == %directory% goto :fail
:install
if EXIST venv (
color 04
echo environment already installed, use run.bat or delete venv folder and retry
pause
exit
) ELSE (
goto :virtualenv
)
:virtualenv
echo Installing virtual environment
CALL virtualenv venv
echo Completed - Installed virtual environment
CALL venv\Scripts\activate
PING localhost -n 2 >NUL
CALL pip install -e .
echo Completed - Installed required packages
echo Done install, use run.bat to start the server
pause
exit

:fail
color 04
echo Could not install, Parent Directory isn't correctly named
echo %parent% != ScatterTestApplication, please rename and rerun
pause
exit