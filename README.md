# Scatter-Like Test
Rowan University Senior Project: Scatter-like Test App

Team Members:

Richard Gonzalez: https://github.com/SlickRick518/SeniorProjectIndividual.git

Tom Auriemma: https://github.com/KartoffelMann/SeniorProj

Rostyslav Hnatyshyn: https://github.com/rostyhn/seniorproject

Michael Zacierka: https://github.com/mzacierka/SeniorProj

Tom Lentz: https://github.com/tlentz98/Senior-Project

Hiral Shah: https://github.com/hiralshah5172/senior_project

## Workspace Installation Guide

## Install [Python](https://www.python.org/), [pip](https://pip.pypa.io/en/stable/installing/), and [Virtualenv](https://virtualenv.pypa.io/en/latest/)
Once installed, run the following commands to verify that the installations were successful.
```
python --version
> Python 3.7.2

pip --version
> pip 19.3.1

virtualenv --version
> 16.7.5
```
## Set up the virtual environment 
First, run the following command to create a new virtual environment.
```
virtualenv venv
```
Wait for it to complete, then start the environment by running 
```
.\venv\Scripts\activate
```
Afterwards, install the required packages by running
```
pip install -e .
```

Next, set the environment variables by running
```
# Powershell
$env:FLASK_APP="FlaskAPP"
$env:FLASK_ENV="development"

# Windows command-line
set FLASK_APP=FlaskAPP
set FLASK_ENV=development

# GNU/LINUX
export FLASK_APP=FlaskAPP
export FLASK_ENV=development
```
Create a config file using the config_example.py file located in the FlaskAPP directory 
and modify the following values accordingly.
```
DB_USER = "[YOUR DATABASE'S USER NAME]"
DB_PASS = "[YOUR DATABASE'S PASSWORD]"

SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASS + '[YOUR DATABASE'S URL]'
```
Finally, run the Flask server with
```
flask run
```
## License Information

Copyright 2019 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
