from extensions import db
from sqlalchemy import Identity

class User(db.Model):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)