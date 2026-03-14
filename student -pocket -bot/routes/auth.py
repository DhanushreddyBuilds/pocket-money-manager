from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User
from database.db import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    d = request.json
    pw = generate_password_hash(d["password"])
    u = User(username=d["username"], password=pw)
    db.session.add(u)
    db.session.commit()
    return jsonify({"msg":"ok"})


@auth_bp.route("/login", methods=["POST"])
def login():
    d = request.json
    u = User.query.filter_by(username=d["username"]).first()

    if u and check_password_hash(u.password, d["password"]):
        session["uid"] = u.id
        return jsonify({"msg":"ok"})

    return jsonify({"msg":"fail"})
