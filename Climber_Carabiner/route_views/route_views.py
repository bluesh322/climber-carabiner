from flask import (
    current_app,
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify
)
from ..models import User, db, Route
from flask_login import login_required, current_user

sess = db.session

route_views = Blueprint(
    "route_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@current_app.login_manager.user_loader
def load_user(id):
    return User.query.get_or_404(int(id))

@route_views.route('/route/<int:route_id>')
@login_required
def show_user_feed(route_id):
    route = Route.query.get_or_404(route_id)
    nearby_routes = Route.get_routes_within_radius_count(route.lat, route.lon, 5, 5)
    return render_template(
        'route_details.html',
        route=route,
        nearby_routes=nearby_routes)