import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'should-be-changed'    # config item against CSFR attacks
    # config item to change the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False                              # Connect to the following signals to get notified before and after changes are committed to the database. These changes are only tracked if SQLALCHEMY_TRACK_MODIFICATIONS is enabled in the config.
    POSTS_PER_PAGE = 5                                                  # config item to that determines how many items will be displayer per page
