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
from .search_forms import SearchForm
import os
from sqlalchemy import and_, or_, func, asc, between
from ..user_views.user_forms import boulder_levels, sport_levels

sess = db.session

search_views = Blueprint(
    "search_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@current_app.login_manager.user_loader
def load_user(id):
    return User.query.get_or_404(int(id))

@search_views.route('/search', methods=["GET"])
@login_required
def show_search_form():
    return render_template('search.html')

@search_views.route('/search', methods=["POST"])
@login_required
def submit_search():
    """Submit search to database for routes or users"""
    search = request.json.get('q')
    option1 = request.json.get('option1')
    advanced = request.json.get('advanced')
    route_type = request.json.get('route_type')
    r_distance = int(request.json.get('r_distance'))
    u_distance = int(request.json.get('u_distance'))
    if route_type == "Boulder": 
        low = boulder_levels.index(request.json.get('low'))
        high = boulder_levels.index(request.json.get('high'))
    else:
        low = sport_levels.index(request.json.get('low'))
        high = sport_levels.index(request.json.get('high'))
    geo = func.ST_GeomFromText('POINT({} {})'.format(current_user.lon, current_user.lat))

    if option1:
        if advanced:
            if not search:
                routes = Route.query.filter(and_((Route.route_type == route_type),
                    (func.ST_DistanceSphere(Route.geo, geo) < (r_distance*1609.344)), (Route.difficulty.between(int(low),int(high))))).order_by(func.ST_DistanceSphere(Route.geo, geo)).limit(30).all()
                
            else:
                routes = Route.query.filter(and_(Route.name.ilike(f"%{search}%"), (Route.route_type == route_type),
                    (func.ST_DistanceSphere(Route.geo, geo) < (r_distance*1609.344)), (Route.difficulty.between(int(low),int(high))))).order_by(func.ST_DistanceSphere(Route.geo, geo)).limit(30).all()
            all_routes = [route.serialize() for route in routes]
            return jsonify(routes=all_routes)
        else: 
            if not search:
                routes = Route.query.all()
            else:
                routes = Route.query.filter((Route.name.ilike(f"%{search}%"))).all()
            all_routes = [route.serialize() for route in routes]
            return jsonify(routes=all_routes)
    else:
        if advanced:
            if not search:
                users = User.query.filter(and_((func.ST_DistanceSphere(User.geo, geo) < (u_distance*1609.344)), (User.geo != null), (User.confirmed == True))).order_by(func.ST_DistanceSphere(User.geo, geo)).limit(30).all()
            else:
                users = User.query.filter(and_((User.username.ilike(f"%{search}%")), (User.confirmed == True), (User.geo != null), (func.ST_DistanceSphere(User.geo, geo) < (u_distance*1609.344))).limit(30).all()
            all_users = [user.serialize() for user in users]
            return jsonify(users=all_users)
        else:
            if not search:
                users = User.query.filter(and_((User.confirmed == True), (User.geo != null)).limit(50).all()
            else:
                users = User.query.filter(and_((User.username.ilike(f"%{search}%")), (User.confirmed == True), (User.geo != null))).order_by(func.ST_DistanceSphere(User.geo, geo)).all()
            all_users = [user.serialize() for user in users]
            return jsonify(users=all_users)

@search_views.route('/location')
@login_required
def get_user_location():
    return jsonify(user=current_user.serialize())

@search_views.route('/update_map')
@login_required
def update_map():
    lat = current_user.lat
    lon = current_user.lon
    routes = Route.get_routes_within_radius(lat, lon, 50)
    all_routes = [route.serialize() for route in routes]
    return jsonify(routes=all_routes)

@search_views.route('/update_map', methods=["POST"])
@login_required
def update_map_on_bounds_change():
    center = request.json['center']
    lat = center['lat']
    lon = center['lng']
    routes = Route.get_routes_within_radius(lat, lon, 50)
    all_routes =  [route.serialize() for route in routes]
    return jsonify(routes=all_routes)

@search_views.route('/mapskey')
@login_required
def maps():
    MP_KEY = os.environ.get('GOOGLE_KEY') #Also should not put this on github
    return MP_KEY