#!/bin/bash
pipenv run pybabel extract -F babel.cfg -k _l -o messages.pot .;
pipenv run pybabel update -i messages.pot -d app/translations;
pipenv run pybabel compile -d app/translations;
