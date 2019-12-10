@echo off
title run script
echo Activating virtual environment
CALL venv\Scripts\activate.bat

set FLASK_APP=FlaskAPP

set FLASK_ENV=development

ECHO set environment variables

ECHO Starting Webserver
FOR /F "delims=: tokens=2" %%a in ('ipconfig ^| find "IPv4"') do set _IPAddress=%%a
ECHO %_IPAddress%:5000

flask run --host=0.0.0.0

PAUSE