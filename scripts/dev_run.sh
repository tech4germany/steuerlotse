#!/bin/bash
source venv/bin/activate;
export FLASK_APP=app;
export FLASK_ENV=dev;
flask run;