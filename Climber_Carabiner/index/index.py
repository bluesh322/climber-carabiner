from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from flask import current_app as app

from Climber_Carabiner.models import db, User, Route
from flask_login import login_required, login_user, logout_user, current_user

sess = db.session

# Blueprint configuration
index_bp = Blueprint(
    "index_bp", __name__, template_folder="templates", static_folder="static"
)


@index_bp.route("/")
def index():
    """Homepage. Currently Performs a log in."""
    return render_template("index.html", template="index-template")


@index_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@index_bp.route("/profile")
@login_required
def show_profile():
    return render_template("profile.html", name=current_user.username)
