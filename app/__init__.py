""" Startup file for this app.
Print POS system made by jackjrz.
This webapp runs using Flask python web framework.
GitHub: https://github.com/jackjereza08
Twitter: https://twitter.com/jackjrz8
Instagram: https://instagram.com/jackjrz8

Started development: Nov 08 2022
Status: In development.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

with app.app_context():
    # Configuration outside app package.
    app.config.from_object('config')
    # Configuration inside instance folder.
    app.config.from_pyfile('config.py')
    db = SQLAlchemy(app)
    from . import models
    from . import routes