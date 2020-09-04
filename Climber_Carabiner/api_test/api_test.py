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
SECRET_KEY = 'SECRET' #Also should not put this on github

# --------------------------- User Routes ----------------------------------------

@api_test_bp.route('/api/users')
def list_user():
    """email or userId return the user and some info"""
    email = '' #using constants atm not for github
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

@api_test_bp.route('/api/users',  methods=['POST'])
def create_user():
    return render_template('index.html')

@api_test_bp.route('/api/users', methods=['DELETE'])
def delete_user():
    return jsonify(message="Deleted")

@api_test_bp.route('/api/ticks')
def list_ticks():
    """email or userId return most recent ticks from user, optional - start pos"""
    return render_template(
    'index.html',
    title='api test',
    subtitle='getUser',
    template='index-template')

@api_test_bp.route('/api/todos')
def list_todos():
    """email or userId return most recent todos from user, optional - start pos"""
    return render_template(
    'index.html',
    title='api test',
    subtitle='getUser',
    template='index-template')

# --------------------------- Route Routes ----------------------------------------

@api_test_bp.route('/api/routes')
def list_routes():
    """routeId - """
    return render_template(
    'index.html',
    title='api test',
    subtitle='getUser',
    template='index-template')

@api_test_bp.route('/api/routes/<int:lat>&<int:lon>')
def list_routes_lat_lon(lat, lon):
    """email or userId return most recent ticks from user, optional - start pos"""
    return render_template(
    'index.html',
    title='api test',
    subtitle='getUser',
    template='index-template')