"""Seed Database"""

import sys 
sys.path.append('..')
from wsgi import app
from Climber_Carabiner.models import db, User, Route, Send, Project, Follows, Likes, Kudo
import datetime
from sqlalchemy import func

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

jerry = User.signup('jerry', 'jerbear@gmail.com', 'testpass')

jerry.confirmed = True
jerry.confirmed_on = datetime.datetime.now()
jerry.goals = "Reimer's Ranch"
jerry.b_skill_level = "5"
jerry.tr_skill_level = "7"
jerry.ld_skill_level = "6"
jerry.location = "Austin, Texas"
jerry.lat = "30.2672"
jerry.lon = "-97.7431"
jerry.geo = func.ST_GeomFromText('POINT({} {})'.format(jerry.lon, jerry.lat))

sarah = User.signup('sarah', 'sarah@gmail.com', 'testpass')

sarah.confirmed = True
sarah.confirmed_on = datetime.datetime.now()
sarah.goals = "Huecos Tanks"
sarah.b_skill_level = "0"
sarah.tr_skill_level = "8"
sarah.ld_skill_level = "7"
sarah.location = "Dallas, Texas"
sarah.lat = "32.7767"
sarah.lon = "-96.7970"
sarah.geo = func.ST_GeomFromText('POINT({} {})'.format(sarah.lon, sarah.lat))


josh = User.signup('josh', 'josh@gmail.com', 'testpass')

josh.confirmed = True
josh.confirmed_on = datetime.datetime.now()
josh.goals = "The pink one in the corner"
josh.b_skill_level = "8"
josh.tr_skill_level = "7"
josh.ld_skill_level = "0"
josh.location = "Fort Worth, Texas"
josh.lat = "32.7555"
josh.lon = "-97.3308"
josh.geo = func.ST_GeomFromText('POINT({} {})'.format(josh.lon, josh.lat))


ben = User.signup('ben', 'ben@gmail.com', 'testpass')

ben.confirmed = True
ben.confirmed_on = datetime.datetime.now()
ben.goals = "Wichita Mountains"
ben.b_skill_level = "5"
ben.tr_skill_level = "3"
ben.ld_skill_level = "0"
ben.location = "Plano, Texas"
ben.lat = "33.0198"
ben.lon = "-96.6989"
ben.geo = func.ST_GeomFromText('POINT({} {})'.format(ben.lon, ben.lat))

users = [blues, jerry, sarah, josh, ben]

db.session.add_all(users)

db.session.commit()

route1 = Route(name="Big Theif", difficulty="V3", image_url="http://placehold.it/200x200&text=Route", stars="2", location="Dallas", location2="Texas", lat="32.7767", lon="-96.7970", route_type="Boulder")
route2 = Route(name="Not My Momma", difficulty="V4", image_url="http://placehold.it/200x200&text=Route", stars="3", location="Plano", location2="Texas", lat="33.0198", lon="-96.6989", route_type="Lead")
route1.geo = func.ST_GeomFromText('POINT({} {})'.format(route1.lon, route1.lat))
route2.geo = func.ST_GeomFromText('POINT({} {})'.format(route2.lon, route2.lat))

db.session.add(route1)
db.session.add(route2)
db.session.commit()

p1 = Project()
p1.user_id = 1
p1.route_id = 1
p1.projected_on = datetime.datetime.now()

p2 = Project()
p2.user_id = 2
p2.route_id = 2
p2.projected_on = datetime.datetime.now()

db.session.add(p1)
db.session.add(p2)
db.session.commit()

s = Send()
s.user_id = 1
s.route_id = 2
s.sent_on = datetime.datetime.now()

db.session.add(s)
db.session.commit()

f1 = Follows()
f1.user_being_followed_id = 2
f1.user_following_id = 1
db.session.add(f1)

f2 = Follows()
f2.user_being_followed_id = 3
f2.user_following_id = 1
db.session.add(f2)

f3 = Follows()
f3.user_being_followed_id = 1
f3.user_following_id = 2
db.session.add(f3)

db.session.commit()

l = Likes()
l.user_id = 1
l.route_id = 1
db.session.add(l)

k = Kudo()
k.route_id = 2
k.user_id = 2
db.session.add(k)