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

sess = db.session

search_views = Blueprint(
    "search_views",
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

@search_views.route('/search', methods=["GET", "POST"])
def show_search_form():
    return render_template('search.html')

@search_views.route('/update_map')
def update_map():
    lat = 30.2672
    lon = -97.7431
    routes = Route.get_routes_within_radius(lat, lon, 5)
    all_routes = [route.serialize() for route in routes]
    return jsonify(routes=all_routes)

@search_views.route('/update_map', methods=["POST"])
def update_map_on_bounds_change():
    center = request.json['center']
    lat = center['lat']
    lon = center['lng']
    routes = Route.get_routes_within_radius(lat, lon, 5)
    all_routes =  [route.serialize() for route in routes]
    return jsonify(routes=all_routes)


@search_views.route('/search/list_users')
def list_users():
    return render_template('list_users.html')

@search_views.route('/search/list_routes')
def list_routes():
    return render_template('list_routes.html')