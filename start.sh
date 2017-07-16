#!/bin/bash

PROJECT_HOME="/home/dance/savesoundcloud"
cd "${PROJECT_HOME}" || exit
python3.5 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# run the server
if [[ -n $DEBUG && $DEBUG == true ]]; then
    flask run -h 0.0.0.0
else
    gunicorn --config=config/gunicorn.py savesoundcloud:app
fi
