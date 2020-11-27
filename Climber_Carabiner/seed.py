"""Seed Database"""

import sys 
sys.path.append('..')
from wsgi import app
from Climber_Carabiner.models import db, User, Route, Project, Follows, Send, Likes, Kudos
import datetime, requests, json, os
from sqlalchemy import func

BASE_URL = 'https://www.mountainproject.com/data/'
MP_KEY = os.environ.get('MP_KEY') 

db.drop_all()
db.create_all()

blues = User.signup('blues', 'bluesh322@gmail.com', 'testpass')

blues.confirmed = True
blues.confirmed_on = datetime.datetime.now()
blues.goals = "HCR Shrimp Scampi"
blues.b_skill_level = "6"
blues.tr_skill_level = "5"
blues.ld_skill_level = "4"
blues.location = "Denton, Texas"
blues.lat = "33.2148"
blues.lon = "-97.1331"
blues.geo = func.ST_GeomFromText('POINT({} {})'.format(blues.lon, blues.lat))

db.session.add(blues)
db.session.commit()

# dist = '200'
# results = '500'


# lat = ['32.7767', '30.2672', '31.7619', '31.3113', '34.7465', '32.2988', '28.5309', '33.7984', '35.2026', '36.1627', '35.4676', '35.0844', '33.4484', '36.1699',
#     '34.0522', '38.5816', '39.7392', '40.7608', '39.1911', '37.8651', '45.5051', '47.6062']
# lon = ['-96.7970', '-97.7431', '-106.4850', '-92.4451', '-92.2896', '-90.1848', '-81.3776', '-89.1476', '-80.8341', '-86.7816', '-97.5164', '-106.6504', '-112.0740', '-115.1398'
#     '-118.2437', '-121.4944', '-104.9903', '-111.8910', '-106.8175', '-119.5383', '-122.6750', '-122.3321']

# i = 0
# for l in lat:

#     routes_res = requests.get(f'{BASE_URL}get-routes-for-lat-lon?lat={l}&lon={lon[i]}&maxDistance={dist}&maxResults={results}&key={MP_KEY}')
#     routes = json.loads(routes_res.text)
#     print("**************************************")
#     print(routes)
#     routes_t = routes['routes']
#     for route in routes_t:
#         Route.add_route(mp_id = route['id'], name=route['name'], difficulty=route['rating'], image_url=route['imgMedium'], stars=route['stars'], location=route['location'][0], location2=route['location'][1] or None, lat=route['latitude'], lon=route['longitude'], route_type=route['type'])
#     i += 1
