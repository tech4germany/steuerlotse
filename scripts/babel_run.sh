#!/bin/bash
source venv/bin/activate;
pybabel extract -F babel.cfg -k _l -o messages.pot .;
pybabel update -i messages.pot -d app/translations;
pybabel compile -d app/translations;
