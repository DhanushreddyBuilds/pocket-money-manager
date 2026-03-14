from database.models import Transaction
from database.db import db
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
from sqlalchemy import func


def get_daily_expense_series(user):

    rows = db.session.query(
        func.date(Transaction.created),
        func.sum(Transaction.amount)
    ).filter_by(user_id=user, type="expense")\
     .group_by(func.date(Transaction.created))\
     .order_by(func.date(Transaction.created)).all()

    if not rows:
        return None

    X = []
    y = []

    for i, row in enumerate(rows):
        X.append([i])
        y.append(row[1])

    return np.array(X), np.array(y)


def predict_next_days(user, days=7):

    data = get_daily_expense_series(user)

    if data is None:
        return None

    X, y = data

    if len(X) < 1:
        return None  # not enough data

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.array([[len(X)+i] for i in range(days)])
    preds = model.predict(future_X)

    preds = [round(float(p), 2) for p in preds]

    total = round(sum(preds), 2)

    return preds, total


def average_daily_spend(user):

    data = get_daily_expense_series(user)
    if data is None:
        return 0

    _, y = data
    return round(float(np.mean(y)), 2)
