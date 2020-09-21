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
