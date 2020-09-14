"""Seed Database"""

import sys 
sys.path.append('..')
from wsgi import app
from Climber_Carabiner.models import db, User

db.drop_all()
db.create_all()

blues = User(username='blues', email='b@b.com')

db.session.add(blues)

db.session.commit()