from flask import (
    current_app,
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)
from ..models import User, db

sess = db.session

user_views = Blueprint(
    "user_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@user_views.route('/user-feed')
def show_user_feed():
    return render_template('user_feed.html')

@user_views.route('/user/view-profile')
def show_user_profile():
    return render_template('view_profile.html')

@user_views.route('/user/edit-profile', methods=["GET", "POST"])
def edit_user_profile():
    return render_template('edit_profile.html')

@user_views.route('/user/list-connections', methods=["GET", "POST"])
def list_user_connections():
    return render_template('list_connections.html')