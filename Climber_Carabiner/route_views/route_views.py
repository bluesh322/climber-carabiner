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
from ..models import User, db, Route, Project, Send, Likes, Kudos, boulder_levels, sport_levels
from flask_login import login_required, current_user
from ..user_views.feed import generate_feed_from_users_and_routes, generate_feed_from_projects_sends
from sqlalchemy import and_, func, between, or_, asc

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
    is_project = Project.query.filter(and_((Project.user_id == current_user.id), (Project.route_id == route_id))).all()
    is_sent = Send.query.filter(and_((Send.user_id == current_user.id), (Send.route_id == route_id))).all()
    feed = generate_feed_from_projects_sends(recent_projects, recent_sends)
    likes = [like.project_id for like in Likes.query.filter(
                Likes.user_id == current_user.id).all()]
    kudos = [kudo.send_id for kudo in Kudos.query.filter(
                Kudos.user_id == current_user.id).all()]
    return render_template(
        'route_details.html',
        nearby_routes=nearby_routes,
        route=route,
        feed=feed,
        likes=likes,
        kudos=kudos,
        is_project=is_project,
        is_sent=is_sent,
        boulder_levels=boulder_levels,
        sport_levels=sport_levels
        )