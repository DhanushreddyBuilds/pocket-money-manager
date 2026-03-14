from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from engine.finance import get_balance, get_summary
from engine.predictor import predict_next_days


def generate_pdf(user, path):

    c = canvas.Canvas(path, pagesize=A4)

    c.setFont("Helvetica", 16)
    c.drawString(50, 800, "Student Pocket AI Report")

    bal = get_balance(user)
    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Current Balance: ₹{bal}")

    rows = get_summary(user)

    y = 720
    c.drawString(50, y, "Category Expenses:")
    y -= 20

    for cat, amt in rows:
        c.drawString(70, y, f"{cat} : ₹{amt}")
        y -= 18

    pred = predict_next_days(user)

    if pred:
        _, total = pred
        y -= 20
        c.drawString(50, y, f"Predicted next 7-day spend: ₹{total}")

    c.save()
