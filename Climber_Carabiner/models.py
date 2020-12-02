from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask import current_app as app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from geoalchemy2 import Geometry
from sqlalchemy import func, asc
import datetime, re
from flask import redirect
from better-profanity import profranity


bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()

boulder_levels = [ 'V', 'V0',
         'V1',
         'V2',
         'V3',
         'V4',
         'V5',
         'V6',
         'V7',
         'V8',
         'V9']

sport_levels = ['5.4','5.5',
        '5.6',
        '5.6+',
        '5.7-',
        '5.7',
        '5.7+',
        '5.8-',
        '5.8',
        '5.8+',
        '5.9-',
        '5.9',
        '5.9+',
        '5.10',
        '5.10a',
        '5.10b',
        '5.10c',
        '5.10d',
        '5.11',
        '5.11a',
        '5.11b',
        '5.11c',
        '5.11d',
        '5.12',
        '5.12a',
        '5.12b',
        '5.12c',
        '5.12d',
        '5.13',
        '5.13a',
        '5.13b',
        '5.13c',
        '5.13d',
        '5.14',
        '5.14a',
        '5.14b']

def connect_db(app):
    db.app = app
    db.init_app(app)

# Models go below

class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    def __repr__(self):
        """Show info about a Follow"""
        f = self
        return f"<Follow {f.user_being_followed_id} {f.user_following_id}>"

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    
class Send(db.Model):
    """Finish a route - ticks in Mountain Project Api"""

    __tablename__ = 'sends'

    def __repr__(self):
        """Show info about a Send"""
        s = self
        return f"<Send id: {s.id}, user_id: {s.user_id}, route_id: {s.route_id}, attempts: {s.attempts}>"

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'route_id': self.route_id,
            'attempts': self.attempts
        }

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        nullable=False
    )

    route_id = db.Column(
        db.Integer,
        db.ForeignKey('routes.id', ondelete="cascade"),
        nullable=False
    )

    attempts = db.Column(
        db.Text,
        nullable=True
    )

    sent_on = db.Column(
        db.DateTime, 
        nullable=True
    )

    user = db.relationship("User")

    kudo = db.relationship('Kudos')

    route = db.relationship('Route')



class Project(db.Model):
    """Project a route, a route you currently attempting to send."""

    __tablename__ = 'projects'

    def __repr__(self):
        """Show info about a Send"""
        s = self
        return f"<Project {s.user_id} {s.route_id}>"

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'route_id': self.route_id
        }

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        nullable=False
    )

    route_id = db.Column(
        db.Integer,
        db.ForeignKey('routes.id', ondelete="cascade"),
        nullable=False
    )

    projected_on = db.Column(
        db.DateTime, 
        nullable=True
    )

    user = db.relationship("User")

    like = db.relationship('Likes')

    route = db.relationship(
        'Route'
        )

class User(UserMixin, db.Model):
    """User - UserMixin gives access to is_active, is_authenticated, is_anonymous, and get_id"""
    def __repr__(self):
        """Show info about a user"""
        u = self
        return f"<User {u.id}, {u.username}, {u.email}>"

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.Text,
        #nullable=False
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    first_name = db.Column(
        db.Text,
        nullable=True
    )
    last_name = db.Column(
        db.Text,
        nullable=True
    )
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )
    b_skill_level = db.Column(
        db.Text,
        nullable=True,
    )
    tr_skill_level = db.Column(
        db.Text,
        nullable=True
    )
    ld_skill_level = db.Column(
        db.Text,
        nullable=True
    )
    #How will I process User location ? 
    location = db.Column(
        db.Text,
        nullable=True
    )
    geo = db.Column(
        Geometry(geometry_type="POINT")
    )
    lat = db.Column(
        db.Numeric,
        nullable=True
    )
    lon = db.Column(
        db.Numeric,
        nullable=True
    )
    #About me section - but labelled goals for climbing
    goals = db.Column(
        db.Text,
        nullable=True
    )

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )
    #Email confirmation
    confirmed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )
    confirmed_on = db.Column(
        db.DateTime, 
        nullable=True
    )

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_url': self.image_url,
            'b_skill_level': self.b_skill_level,
            'tr_skill_level': self.tr_skill_level,
            'ld_skill_level': self.ld_skill_level,
            'location': self.location,
            'lat': str(self.lat),
            'lon': str(self.lon),
            'goals': self.goals
        }

    #Is methods for checking information about a user
    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1
    def is_following(self, other_user):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1
    

    #Class Methods for Authenticating a User
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        if profanity.contains_profanity(username) or profanity.contains_profanity(email):
            return False


        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def change_password(cls, email, password):
        """Already found user will do one more check for email and change password"""
        user = cls.query.filter_by(email=email).first()

        if user:
            hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
            user.password = hashed_pwd
            sess.add(user)
            sess.commit()
        return user
        


class Route(db.Model):
    """Route"""
    def __repr__(self):
        """Show information about a route"""
        r = self
        return f'<Route {r.id}, {r.name}>'

    __tablename__ = "routes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    mp_id = db.Column(
        db.Text,
        nullable=False
    )
    name = db.Column(
        db.Text,
        nullable=False
    )
    difficulty = db.Column(
        db.Integer,
        nullable=False
    )
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )
    stars = db.Column(
        db.Integer,
        nullable=False
    )
    location = db.Column(
        db.Text
    )
    location2 = db.Column(
        db.Text
    )
    lat = db.Column(
        db.Numeric,
        nullable=False
    )
    lon = db.Column(
        db.Numeric,
        nullable=False
    )
    geo = db.Column(
        Geometry(geometry_type="POINT")
    )
    description = db.Column(
        db.Text,
        nullable=True
    )
    route_type = db.Column(
        db.Text,
        nullable=False
    )

    project = db.relationship(
        "Project",
        primaryjoin=(Project.route_id == id)
    )

    send = db.relationship(
        "Send",
        primaryjoin=(Send.route_id == id),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'image_url': self.image_url,
            'stars': self.stars,
            'location': self.location,
            'location2': self.location2,
            'lat': str(self.lat),
            'lon': str(self.lon),
            'route_type': self.route_type
        }

    def get_routes_within_radius(lat, lon, radius):
        """Return all routes within a given radius (in meters) of this point."""
        geo = func.ST_GeomFromText('POINT({} {})'.format(lon, lat))
        return Route.query.filter(func.ST_DistanceSphere(Route.geo, geo) < radius*1609.344).all()
    
    def get_routes_within_radius_count(lat, lon, radius, count):
        """Return all routes within a given radius (in meters) of this point."""
        geo = func.ST_GeomFromText('POINT({} {})'.format(lon, lat))
        return Route.query.filter(func.ST_DistanceSphere(Route.geo, geo) < radius*1609.344).order_by(func.ST_DistanceSphere(Route.geo, geo)).limit(count).offset(1).all()
        # Route.query.filter(func.ST_DistanceSphere(Route.geo, geo) < radius*1609.344).order_by(func.ST_DistanceSphere(Route.geo, geo)).offset(1).limit(count).all()

    def get_routes_within_radius_count_for_feed(lat, lon, radius, count):
        """Return all routes within a given radius (in meters) of this point."""
        geo = func.ST_GeomFromText('POINT({} {})'.format(lon, lat))
        return Route.query.filter(func.ST_DistanceSphere(Route.geo, geo) < radius*1609.344).order_by(func.ST_DistanceSphere(Route.geo, geo)).limit(count).all()

    def get_routes_search_all():
        """Return all routes"""
    
    @classmethod
    def add_route(cls, mp_id, name, difficulty, image_url, stars, location, location2, lat, lon, route_type):
        """Add a route to db."""
        geo = 'POINT({} {})'.format(lon, lat)
        new_route = Route(mp_id=mp_id, name = name, image_url=image_url, stars=stars, location=location, location2=location2, lat=lat, lon=lon, route_type=route_type, geo=geo)
        if route_type == 'Boulder' or difficulty[0] == "V":
            if difficulty in boulder_levels:
                new_route.difficulty = boulder_levels.index(difficulty)
            else:
                difficulty = difficulty[0:1]
                difficulty = difficulty.strip()
                if difficulty in boulder_levels:
                    new_route.difficulty = boulder_levels.index(difficulty)
                else: 
                    new_route.difficulty = 0
        else:
            if difficulty in sport_levels:
                new_route.difficulty = sport_levels.index(difficulty)
            else:
                difficulty = difficulty[0:4]
                difficulty = difficulty.strip()
                if difficulty in sport_levels:
                    new_route.difficulty = sport_levels.index(difficulty)
                else:
                    new_route.difficulty = 0
        db.session.add(new_route)
        db.session.commit()
    
    @classmethod
    def update_geometries(cls):
        """Using each route lon and lat, add a geometry data to db."""
        routes = Route.query.all()
        for route in routes:
            point = 'POINT({} {})'.format(route.lon, route.lat)
            route.geo = point
        db.session.commit()

class Likes(db.Model):
    """Mapping user likes to projects."""

    __tablename__ = 'likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id', ondelete='cascade'),
        unique=False
    )

class Message(db.Model):
    """Comment on a route or message to a user profile"""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    text = db.Column(
        db.Text,
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')

class Kudos(db.Model):
    """Mapping user kudos to sends."""

    __tablename__ = 'kudos'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    send_id = db.Column(
        db.Integer,
        db.ForeignKey('sends.id', ondelete='cascade'),
        unique=False
    )