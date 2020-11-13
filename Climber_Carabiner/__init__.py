"""Init Flask App"""
from flask import Flask, url_for
from flask_debugtoolbar import DebugToolbarExtension
from flask_assets import Environment
from flask_login import LoginManager
from flask_mail import Mail
from .assets import compile_assets
from .models import connect_db, User
import os

assets = Environment()


def create_app():
    """Create Flask Application"""
    app = Flask(__name__, instance_relative_config=False)

    # config app with things i'd normally put in app.py
    app.config.from_object("config.Config")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgres:///carabiner"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    toolbar = DebugToolbarExtension(app)

    # Flask-Login init
    login_manager = LoginManager()

    # Mail init
    mail = Mail()
    

    # Assets init
    assets = Environment()
    

    # DB init
    connect_db(app)
    mail.init_app(app)
    login_manager.init_app(app)
    assets.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .index import index
        from .api_test import api_test
        from .auth import auth
        from .user_views import user_views
        from .search_views import search_views
        from .route_views import route_views

        # Register Blueprints
        app.register_blueprint(index.index_bp)
        app.register_blueprint(api_test.api_test_bp, url_prefix="/api")
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(user_views.user_views)
        app.register_blueprint(search_views.search_views)
        app.register_blueprint(route_views.route_views)

        # Compile static assets
        compile_assets(assets)

        return app

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html")