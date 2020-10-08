from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask import current_app as app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from geoalchemy2 import Geometry
from sqlalchemy import func


bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Models go below

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
        nullable=False
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

    #Class Methods for Authenticating a User
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

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
    name = db.Column(
        db.Text,
        nullable=False
    )
    difficulty = db.Column(
        db.Text,
        nullable=False
    )
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
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

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'image_url': self.image_url,
            'lat': str(self.lat),
            'lon': str(self.lon),
            'route_type': self.route_type
        }

    def get_routes_within_radius(lat, lon, radius):
        """Return all routes within a given radius (in meters) of this point."""
        geo = func.ST_GeomFromText('POINT({} {})'.format(lon, lat))
        return Route.query.filter(func.ST_DistanceSphere(Route.geo, geo) < radius*1609.344).all()
    
    @classmethod
    def add_route(cls, name, difficulty, image_url, lat, lon, route_type):
        """Add a route to db."""
        geo = 'POINT({} {})'.format(lon, lat)
        new_route = Route(name = name, difficulty =difficulty, image_url=image_url, lat=lat, lon=lon, route_type=route_type, geo=geo)
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

class Sends(db.Model):
    """Finish a route - ticks in Mountain Project Api"""

    def __repr__(self):
        """Show info about a Send"""
        s = self
        return f"<Send {s.user_being_followed_id} {s.user_following_id}>"

    __tablename__ = 'sends'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade")
    )

    route_id = db.Column(
        db.Integer,
        db.ForeignKey('routes.id', ondelete="cascade")
    )

    attempts = db.Column(
        db.Integer,
        nullable=True
    )

class Messages(db.Model):
    """Comment on a route or message to a user profile"""
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    text = db.Column(
        db.Text,
        nullable=False
    )
    from_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    route_id = db.Column(
        db.Integer,
        db.ForeignKey('routes.id', ondelete='CASCADE'),
        nullable=False
    )
    to_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )