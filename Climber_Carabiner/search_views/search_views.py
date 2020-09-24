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

search_views = Blueprint(
    "search_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@search_views.route('/search')
def show_search_form():
    return render_template('search.html')

@search_views.route('/search/list_users')
def list_users():
    return render_template('list_users.html')

@search_views.route('/search/list_routes')
def list_routes():
    return render_template('list_routes.html')