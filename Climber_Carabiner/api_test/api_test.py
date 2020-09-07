from flask import Blueprint, render_template, request, redirect, flash, jsonify, session
from flask import current_app as app
import requests, json
import os

# Blueprint configuration
api_test_bp = Blueprint(
    'api_test_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

BASE_URL = 'https://www.mountainproject.com/data/'
SECRET_KEY = '' #Also should not put this on github

# --------------------------- User Routes ----------------------------------------

@api_test_bp.route('/getUsers')
def list_user():
    """email or userId return the user and some info"""
    email = 'bluesh322@gmail.com' #using constants atm not for github
    user = requests.get(f'{BASE_URL}get-user?email={email}&key={SECRET_KEY}')
    user_res = json.loads(user.text)

    res = {}

    res.update({"name": user_res['name']})

    return render_template(
        'api_test.html',
        title='api test',
        subtitle='getUser',
        template='index-template', 
        res = res)

@api_test_bp.route('/users',  methods=['POST'])
def create_user():
    return render_template('index.html')

@api_test_bp.route('/users', methods=['DELETE'])
def delete_user():
    return jsonify(message="Deleted")

@api_test_bp.route('/getTicks')
def list_ticks():
    """email or userId return most recent ticks from user, optional - start pos"""
    email = 'bluesh322@gmail.com'
    tick = requests.get(f'{BASE_URL}get-ticks?email={email}&key={SECRET_KEY}')
    tick_res = json.loads(tick.text)
    res = {}
    res.update({"hardest": tick_res['hardest']})

    return render_template(
    'api_test.html',
    title='api test',
    subtitle='getTicks',
    template='index-template',
    res=res)

@api_test_bp.route('/getTodos')
def list_todos():
    """email or userId return most recent todos from user, optional - start pos"""
    email = 'bluesh322@gmail.com'
    todos = requests.get(f'{BASE_URL}get-to-dos?email={email}&key={SECRET_KEY}')
    todos_res = json.loads(todos.text)
    res = {}
    res.update({"todos": todos_res['toDos']})
    return render_template(
    'api_test.html',
    title='api test',
    subtitle='getUser',
    template='index-template',
    res=res)

# --------------------------- Route Routes ----------------------------------------

@api_test_bp.route('/getRoutes')
def list_routes():
    """routeId,... key: return routes based on id"""
    routes = requests.get(f'{BASE_URL}get-routes?routeIds=105748391,105750454,105749956&key={SECRET_KEY}')
    routes_res = json.loads(routes.text)
    res = {}
    k = []
    routes = routes_res['routes']
    for route in routes:
        k.append(route['name'])
    res.update({'name': k})

    return render_template(
    'api_test.html',
    title='api test',
    subtitle='getUser',
    template='index-template',
    res=res)

@api_test_bp.route('/getRoutesForLatLon')
def list_routes_lat_lon():
    """"""
    #coordinates for Denton TX
    lat = '33.2148'
    lon = '-97.1331'
    maxDist = '200'
    maxresults = '50'
    mindifficulty = 'V3'
    maxdifficulty = 'V8'
    routes_res = requests.get(f'{BASE_URL}get-routes-for-lat-lon?lat={lat}&lon={lon}&maxDistance={maxDist}&maxResults={maxresults}&minDiff={mindifficulty}&maxDiff={maxdifficulty}&key={SECRET_KEY}')
    routes = json.loads(routes_res.text)
    routes_t = routes['routes']
    k = []
    for route in routes_t:
        k.append(route['name'])
    print(k)
    res = {}
    res.update({'name': k})

    return render_template(
    'api_test.html',
    title='api test',
    subtitle='getRouteforlatlon',
    template='index-template',
    res=res)