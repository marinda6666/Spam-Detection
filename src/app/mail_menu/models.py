from extensions import db
from sqlalchemy import Identity
from datetime import datetime

class Message(db.Model):
    __tablename__='message'
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    from_name = db.Column(db.String(150), unique=True, nullable=False)
    to_name = db.Column(db.String(150), unique=True, nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.now())

class Spam(db.Model):
    __tablename__='spam'
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    from_name = db.Column(db.String(150), unique=True, nullable=False)
    to_name = db.Column(db.String(150), unique=True, nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.now())