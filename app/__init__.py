from decimal import Decimal, ROUND_UP
from flask import Flask
from flask_babel import Babel
from flask_navigation import Navigation
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_pyfile('config_dev.py')
if app.env == 'production': # overwrites
    app.config.from_pyfile('config_prod.py')

babel = Babel(app)
nav = Navigation(app)
mongo = PyMongo(app)

@babel.localeselector
def get_locale():
    return 'de'

@app.context_processor
def utility_processor():
    def EUR(decimal):
        return u"%s€" % decimal.quantize(Decimal('1.00'), rounding=ROUND_UP)
    return dict(EUR=EUR)

from app import routes