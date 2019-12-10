#!/bin/bash
DIRECTORY="ScatterTestApp"
CurrentDir=`echo "${PWD##*/}"`
if [ $CurrentDir = $DIRECTORY ] ; then
	if [ -f "venv" ]; then
		echo "environment already installed, use run.bat or delete venv folder and retry"
		exit 1
	else
		echo "Installing virtual environment"
		virtualenv venv
		echo "Completed - Installed virtual environment"
		source venv/bin/activate
		pip3 install -e .
		echo "Completed - Installed required packages"
		echo "Done install, use run.sh to start the server"
		exit 1
	fi
else
	echo "Could not install, Parent Directory isn't correctly named"
	echo "$DIRECTORY != $CurrentDir, please rename and rerun"
	exit 1
fi