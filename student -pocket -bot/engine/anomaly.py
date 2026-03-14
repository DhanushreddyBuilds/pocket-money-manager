from database.models import Transaction
from database.db import db
from sklearn.ensemble import IsolationForest
import numpy as np


def get_expense_amounts(user):

    rows = Transaction.query.filter_by(
        user_id=user,
        type="expense"
    ).all()

    if not rows:
        return None

    return np.array([[r.amount] for r in rows])


def detect_expense_anomaly(user, new_amount):

    data = get_expense_amounts(user)

    if data is None or len(data) < 5:
        return False, "Not enough history for anomaly detection"

    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(data)

    pred = model.predict([[new_amount]])

    if pred[0] == -1:
        avg = float(np.mean(data))
        return True, f"⚠️ Unusual expense detected (avg ₹{round(avg,2)})"

    return False, ""
