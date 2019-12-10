#!/bin/bash

source venv/bin/activate
export FLASK_APP=FlaskAPP
export FLASK_ENV=development

echo "`hostname -i`:5000"

flask run --host=0.0.0.0