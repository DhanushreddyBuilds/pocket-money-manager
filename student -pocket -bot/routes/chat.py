from flask import Blueprint, request, jsonify, session
from engine.chatbot import bot_reply
from database.models import ChatLog
from database.db import db

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():

    if "uid" not in session:
        return jsonify({"reply":"login first"})

    msg = request.json["msg"]
    r = bot_reply(session["uid"], msg)

    log = ChatLog(user_id=session["uid"], message=msg, reply=r)
    db.session.add(log)
    db.session.commit()

    return jsonify({"reply":r})
