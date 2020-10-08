"""Class-based Flask app configuration"""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    """Configuration from environment variables"""

    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = "wsgi.py"

    # Flask-Assets
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = "True"

    # API - Mountain Project

    # Mail Server
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_USERNAME = "bluesh322@gmail.com"
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_PORT = 465
    MAIL_USE_SSL = True
