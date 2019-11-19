# Scatter-Like Test
Rowan University Senior Project: Scatter-like Test App

Team Members:

Richard Gonzalez: https://github.com/SlickRick518/SeniorProjectIndividual.git

Tom Auriemma: https://github.com/KartoffelMann/SeniorProj

Rostyslav Hnatyshyn: https://github.com/rostyhn/seniorproject

Michael Zacierka: https://github.com/mzacierka/SeniorProj

Tom Lentz: https://github.com/tlentz98/Senior-Project

Hiral Shah: https://github.com/hiralshah5172/senior_project

#### The basic necessities to run it

## Install [Python](https://www.python.org/), [pip](https://pip.pypa.io/en/stable/installing/), and [Virtualenv](https://virtualenv.pypa.io/en/latest/)
###### Once they're downloaded verify installation:
```
python --version
Python 3.7.2

pip --version
pip 19.3.1

virtualenv --version
16.7.5
```
## Get Environment Started
Create virtual environment
```
virtualenv venv
```

Wait for it to complete then start the environment. Afterwards, install required packages
```
.\venv\Scripts\activate
pip install -e .
```

Set the environment variables so flask knows what to run
```
# For Powershell users
$env:FLASK_APP="FlaskAPP"
$env:FLASK_ENV="development"

# For cmd shell users
set FLASK_APP=FlaskAPP
set FLASK_ENV=development
```

Create a config file using the config_example.py file located in FlaskAPP and set the values.
Then run the flask app!
```
flask run
```

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
