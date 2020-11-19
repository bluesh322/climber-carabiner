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
from ..models import User, db, Route, Project, Send
from flask_login import login_required, current_user
from ..user_views.feed import generate_feed_from_users_and_routes

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
    nearby_routes = Route.get_routes_within_radius_count(route.lat, route.lon, 5, 10)
    recent_projects = Project.query.filter(Project.route_id == route_id).order_by(Project.projected_on.desc()).all()
    recent_sends = Send.query.filter(Send.route_id == route_id).order_by(Send.sent_on.desc()).all()
    feed = generate_feed_from_users_and_routes(recent_projects, recent_sends)
    print("***********************")
    print(recent_sends)
    print(feed)
    return render_template(
        'route_details.html',
        nearby_routes=nearby_routes,
        route=route,
        feed=feed
        )