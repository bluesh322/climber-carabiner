"""Init Flask App"""
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_assets import Environment
from .assets import compile_assets
from .models import connect_db
import os

assets = Environment()

def create_app():
    """Create Flask Application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    #config app with things i'd normally put in app.py
    # if not set there, use development local db.
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        os.environ.get('DATABASE_URL', 'postgres:///carabiner'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
    toolbar = DebugToolbarExtension(app)

    assets.init_app(app)

    with app.app_context():
        #Import parts of our application
        from .index import index
        from .api_test import api_test

        # Register Blueprints
        app.register_blueprint(index.index_bp)
        app.register_blueprint(api_test.api_test_bp, url_prefix='/api')


        # Compile static assets
        compile_assets(assets)

        return app