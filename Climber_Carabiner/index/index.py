from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from flask import current_app

from Climber_Carabiner.models import db, User, Route
from flask_login import login_required, login_user, logout_user, current_user

sess = db.session

# Blueprint configuration
index_bp = Blueprint(
    "index_bp", __name__, template_folder="templates", static_folder="static"
)


@index_bp.route("/")
def index():
    """Homepage"""
    return render_template("index.html")

@current_app.login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    return redirect(url_for('index_bp.index'))