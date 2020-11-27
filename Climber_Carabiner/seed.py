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

