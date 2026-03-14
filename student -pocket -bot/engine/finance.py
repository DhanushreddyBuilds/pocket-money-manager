from database.models import Transaction
from database.db import db
from sqlalchemy import func
from datetime import datetime, timedelta


def add_transaction(user, amt, cat, ttype):

    tx = Transaction(
        user_id=user,
        amount=amt,
        category=cat,
        type=ttype
    )

    db.session.add(tx)
    db.session.commit()


def get_balance(user):

    inc = db.session.query(func.sum(Transaction.amount))\
        .filter_by(user_id=user, type="income").scalar() or 0

    exp = db.session.query(func.sum(Transaction.amount))\
        .filter_by(user_id=user, type="expense").scalar() or 0

    return inc - exp


def get_summary(user):

    rows = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).filter_by(user_id=user, type="expense")\
     .group_by(Transaction.category).all()

    return rows


def get_today_spend(user):

    today = datetime.utcnow() - timedelta(days=1)

    total = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.user_id==user,
                Transaction.type=="expense",
                Transaction.created>=today)\
        .scalar() or 0

    return total


def get_top_category(user):

    row = db.session.query(
        Transaction.category,
        func.sum(Transaction.amount).label("s")
    ).filter_by(user_id=user, type="expense")\
     .group_by(Transaction.category)\
     .order_by(func.sum(Transaction.amount).desc())\
     .first()

    return row
def clear_user_transactions(user):
    from database.models import Transaction
    Transaction.query.filter_by(user_id=user).delete()
    db.session.commit()
