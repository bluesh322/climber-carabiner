"""Class-based Flask app configuration"""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    """Configuration from environment variables"""

    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'wsgi.py'

    # Flask-Assets
    LESS_BIN = '/usr/local/bin/lessc'
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = 'True'

    # API - Mountain Project