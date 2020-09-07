from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask import current_app as app
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Models go below

class User(db.Model):
    """User"""
    def __repr__(self):
        """Show info about a user"""
        u = self
        return f"<User {u.id} {u.name}>"

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.Text,
        nullable=False
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
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

class Route(db.Model):
    """Route"""
    def __repr__(self):
        """Show informatoin about a route"""
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
    description = db.Column(
        db.Text,
        nullable=True
    )
    route_type = db.Column(
        db.Text,
        nullable=False
    )

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
        db.ForeignKey('routes.id', ondelete="cascade"),
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