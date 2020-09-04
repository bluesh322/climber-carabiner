from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app)
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