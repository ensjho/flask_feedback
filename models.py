"""Models for USER"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site user."""

    __tablename__ = "users"


    username = db.Column(db.String(20), 
                         nullable=False, 
                         unique=True,)

    password = db.Column(db.Text, 
                         nullable=False,)

    email = db.Column(db.String(50),
                         unique=True, 
                         nullable=False,)

    first_name = db.Column(db.String(30), 
                         nullable=False,)

    last_name = db.Column(db.String(30), 
                         nullable=False,)
