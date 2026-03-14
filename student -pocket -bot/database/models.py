from database.db import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    type = db.Column(db.String(10))  # income / expense
    created = db.Column(db.DateTime, default=datetime.utcnow)


class ChatLog(db.Model):
    __tablename__ = "chat_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)
    reply = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
