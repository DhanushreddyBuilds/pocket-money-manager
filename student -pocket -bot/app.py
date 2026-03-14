from flask import Flask, render_template, jsonify
from config import Config
from database.db import db

# blueprints
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.dashboard import dash_bp

# AI warmup
from engine.ml_model import train_model

import logging


# -----------------------------
# App Setup
# -----------------------------
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------
# Database Init
# -----------------------------
with app.app_context():
    db.create_all()
    logger.info("Database initialized")


# -----------------------------
# AI Model Warmup
# -----------------------------
with app.app_context():
    try:
        train_model()
        logger.info("ML model trained on startup")
    except Exception as e:
        logger.warning(f"ML warmup skipped: {e}")


# -----------------------------
# Blueprint Registration
# -----------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(dash_bp)   # ✅ added — not replacing


# -----------------------------
# UI Routes
# -----------------------------
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/chatpage")
def chatpage():
    return render_template("chat.html")


@app.route("/registerpage")
def registerpage():
    return render_template("register.html")


# -----------------------------
# System API Endpoints
# -----------------------------
@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Student Pocket AI",
        "ai_layers": [
            "rule_nlp",
            "ml_intent",
            "prediction",
            "anomaly_detection",
            "auto_learning",
            "dashboard",
            "report_export"
        ]
    })


@app.route("/api/model-status")
def model_status():
    return jsonify({
        "ml_intent": "loaded",
        "prediction_model": "enabled",
        "anomaly_detector": "enabled",
        "online_learning": "enabled"
    })


# -----------------------------
# Global Error Handler
# -----------------------------
@app.errorhandler(Exception)
def handle_error(e):
    logger.error(str(e))
    return jsonify({
        "error": "Internal server error",
        "detail": str(e)
    }), 500


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    logger.info("Starting Student Pocket AI Server")
    app.run(debug=True)
