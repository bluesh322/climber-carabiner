"""Init Flask App"""
from flask import Flask
from flask_assets import Environment
from .assets import compile_assets

assets = Environment()

def create_app():
    """Create Flask Application"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    assets.init_app(app)

    with app.app_context():
        #Import parts of our application
        from .index import index
        from .api_test import api_test

        # Register Blueprints
        app.register_blueprint(index.index_bp)
        app.register_blueprint(api_test.api_test_bp)


        # Compile static assets
        compile_assets(assets)

        return app