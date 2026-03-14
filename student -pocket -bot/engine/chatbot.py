from engine.ml_model import predict_intent, retrain_from_logs
from engine.nlp import detect_intent, extract_amount, detect_category
from engine.finance import (
    add_transaction,
    get_balance,
    get_summary,
    get_today_spend,
    get_top_category,
    clear_user_transactions
)
from engine.predictor import predict_next_days, average_daily_spend
from engine.anomaly import detect_expense_anomaly

LAST_ACTION = {}
CHAT_COUNTER = 0

import random

def human_ack():
    return random.choice([
        "Got it 👍",
        "Okay — noted.",
        "Saved that for you.",
        "Done — recorded.",
        "All set ✅"
    ])


def smart_spending_suggestion(user):

    avg = average_daily_spend(user)
    today = get_today_spend(user)
    top = get_top_category(user)

    tips = []

    if avg > 0 and today > avg * 1.4:
        tips.append("Today’s spending is higher than your usual pattern.")

    if top:
        tips.append(f"You spend most on {top[0]}. Try setting a weekly limit.")

    tips.append("Try the 50-30-20 saving rule.")

    return " 💡 " + random.choice(tips)

def maybe_retrain():
    global CHAT_COUNTER
    CHAT_COUNTER += 1
    if CHAT_COUNTER % 10 == 0:
        retrain_from_logs()


# ---------- FINANCIAL HEALTH SCORE ----------
def financial_health_score(user):

    bal = get_balance(user)
    avg = average_daily_spend(user)
    today = get_today_spend(user)
    summary = get_summary(user)

    if avg == 0:
        return 50, "No history", "Start tracking to compute score"

    score = 100

    # burn rate risk
    if today > avg * 1.5:
        score -= 15

    # low balance buffer
    if bal < avg * 3:
        score -= 20

    # concentration risk
    if summary:
        top_amt = summary[0][1]
        total = sum(a for _, a in summary)
        if total > 0 and top_amt / total > 0.5:
            score -= 10

    # high avg spend
    if avg > 700:
        score -= 15

    if score >= 80:
        status = "Excellent"
        risk = "Low"
    elif score >= 60:
        status = "Stable"
        risk = "Medium"
    else:
        status = "Risky"
        risk = "High"

    advice = coach_advice(user)

    return max(score, 10), status, risk + "\n" + advice


# ---------- COACH ENGINE ----------
def coach_advice(user):

    bal = get_balance(user)
    avg = average_daily_spend(user)
    today = get_today_spend(user)
    top = get_top_category(user)

    tips = []

    if avg == 0:
        return "Start tracking expenses."

    if today > avg * 1.5:
        tips.append("Reduce today's discretionary spending.")

    if bal < avg * 3:
        tips.append("Your balance buffer is low.")

    if top:
        tips.append(f"Cap spending on {top[0]} category.")

    tips.append("Save at least 20% of each income.")

    return " | ".join(tips)


# ---------- INSIGHTS ----------
def insight_block(user):

    avg = average_daily_spend(user)
    today = get_today_spend(user)
    top = get_top_category(user)

    msg = ""

    if avg > 0 and today > avg * 1.5:
        msg += "\n📈 Today spending above pattern"

    if top:
        msg += f"\n🏷 Top category: {top[0]}"

    return msg
import re

def generate_budget_plan(user, text):

    nums = list(map(int, re.findall(r'\d+', text)))

    if len(nums) < 2:
        return None

    amount = nums[0]
    days = nums[1]

    if days == 0:
        return None

    daily = round(amount / days, 2)

    top = get_top_category(user)

    # base split
    food = 0.30 * amount
    travel = 0.15 * amount
    education = 0.20 * amount
    personal = 0.15 * amount
    savings = 0.20 * amount

    # adjust if user has heavy category history
    if top and top[0] == "food":
        food += 0.05 * amount
        savings -= 0.05 * amount

    return f"""
📅 Smart Spending Plan — {days} Days

💰 Total Budget: ₹{amount}
📆 Daily Safe Spend: ₹{daily}

Suggested Allocation:
🍽 Food: ₹{round(food,2)}
🚌 Travel: ₹{round(travel,2)}
📚 Education: ₹{round(education,2)}
🎯 Personal: ₹{round(personal,2)}
💰 Savings Target: ₹{round(savings,2)}

Tip: Try not to exceed ₹{daily} per day.
"""



def bot_reply(user, msg):

    maybe_retrain()
    text = msg.lower()
        # ---------- DYNAMIC BUDGET PLANNER ----------
    if ("for" in text and "day" in text) or "budget" in text or "plan" in text:
        plan = generate_budget_plan(user, text)
        if plan:
            return plan

        # ---------- DYNAMIC BUDGET PLANNER ----------
    # ---------- DYNAMIC BUDGET PLANNER ----------



        # ---------- HUMAN STYLE SUPPORT ----------
    if any(k in text for k in [
        "i am spending too much",
        "i overspend",
        "help me save",
        "how to save",
        "control my spending"
    ]):
        return coach_advice(user)


    # ---------- RESET ----------
    if "reset data" in text:
        clear_user_transactions(user)
        return "✅ All your transaction data cleared."

    # ---------- HEALTH SCORE ----------
    if any(k in text for k in ["health", "score", "behavior"]):
        s, status, advice = financial_health_score(user)
        return f"""📊 Financial Health Score: {s}/100
Status: {status}

{advice}"""

    # ---------- COACH ----------
    if any(k in text for k in [
        "coach", "save", "saving", "budget advice",
        "improve spending"
    ]):
        return "🧠 Coach:\n" + coach_advice(user)

    # ---------- ANALYSIS ----------
    if "analyze" in text:
        rows = get_summary(user)
        if not rows:
            return "No data yet"
        total = sum(a for _, a in rows)
        return f"Total spend ₹{total} | Top: {rows[0][0]}"

    # ---------- PREDICT ----------
    if "predict" in text:
        result = predict_next_days(user)
        if result is None:
            return "Not enough data yet."
        preds, total = result
        return f"🔮 Next week forecast total ₹{total}"

    # ---------- INTENT ----------
    ml_intent, ml_conf = predict_intent(msg)
    rule_intent, _ = detect_intent(msg)
    intent = ml_intent if ml_conf > 0.60 else rule_intent

    # ---------- EXPENSE ----------
    if intent == "expense":

        amt = extract_amount(msg)
        if amt == 0:
            LAST_ACTION[user] = "await_expense_amount"
            return "How much did you spend?"

        cat = detect_category(msg)
        is_anom, note = detect_expense_anomaly(user, amt)
        add_transaction(user, amt, cat, "expense")

        warn = ""
        if amt > 1000:
            warn += "\n⚠️ High expense"
        if is_anom:
            warn += f"\n{note}"

        return human_ack() + f" Expense ₹{amt} under {cat}" + warn + insight_block(user) + smart_spending_suggestion(user)


    # ---------- INCOME ----------
    if intent == "income":
        amt = extract_amount(msg)
        add_transaction(user, amt, "income", "income")
        return f"💰 Income ₹{amt} recorded"

    # ---------- BALANCE ----------
    if intent == "balance":
        return f"📊 Balance ₹{get_balance(user)}"

    # ---------- SUMMARY ----------
    if intent == "summary":
        rows = get_summary(user)
        if not rows:
            return "No expenses yet"
        return "\n".join([f"{c}: ₹{a}" for c, a in rows])

    # ---------- CONTEXT ----------
    if user in LAST_ACTION:
        if LAST_ACTION[user] == "await_expense_amount":
            amt = extract_amount(msg)
            add_transaction(user, amt, "general", "expense")
            LAST_ACTION.pop(user)
            return f"Expense ₹{amt} saved"

    return "🤖 Try: spent 200 food | balance | predict | coach | health score"

