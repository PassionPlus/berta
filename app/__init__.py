# all Flask extentions are needed to be initialized here
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from logging.handlers import RotatingFileHandler
import os
import logging
import pyaudio
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .berta_deepspeech import berta_factory

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)            # database
migrate = Migrate(app, db)      # for easy upgrading and downgrading database
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)      # styling
moment = Moment(app)            # libary for different formating options for date and time 
berta= berta_factory('bumblebee')
pa = pyaudio.PyAudio()

# if the app is not in debug mode write the messages in a log file 
# size of logfile 10KB, keeping last 10 log files as backup.
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/berta.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Berta voice assistant')


# bottom import for workaround to circular imports
from app import routes, models, errors      # error handler registered with Flask, import new module after application instance is created

