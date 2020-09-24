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

route_views = Blueprint(
    "route_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@route_views.route('/route-details')
def show_user_feed():
    return render_template('route_details.html')