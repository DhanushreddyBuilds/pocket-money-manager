from flask import Blueprint, render_template, session, send_file
from engine.finance import get_balance, get_summary
from engine.predictor import predict_next_days, average_daily_spend
from engine.report import generate_pdf
import os

dash_bp = Blueprint("dash", __name__)


@dash_bp.route("/dashboard")
def dashboard():

    if "uid" not in session:
        return "login first"

    uid = session["uid"]

    bal = get_balance(uid)
    summary = get_summary(uid)
    avg = average_daily_spend(uid)
    pred = predict_next_days(uid)

    pred_total = pred[1] if pred else 0

    return render_template(
        "dashboard.html",
        balance=bal,
        summary=summary,
        avg=avg,
        pred_total=pred_total
    )


@dash_bp.route("/export-report")
def export_report():

    if "uid" not in session:
        return "login first"

    path = "report.pdf"
    generate_pdf(session["uid"], path)

    return send_file(path, as_attachment=True)
