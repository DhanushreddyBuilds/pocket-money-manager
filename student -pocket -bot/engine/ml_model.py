import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from database.models import ChatLog
from database.db import db

vectorizer = CountVectorizer()
model = MultinomialNB()

trained = False


BASE_FILE = "data/training_data.json"


def load_base_data():

    with open(BASE_FILE) as f:
        return json.load(f)


def load_chatlog_data():

    rows = ChatLog.query.all()

    data = {
        "expense": [],
        "income": [],
        "balance": [],
        "summary": []
    }

    for r in rows:

        text = r.message.lower()

        if "spent" in text or "expense" in text:
            data["expense"].append(text)

        elif "received" in text or "income" in text:
            data["income"].append(text)

        elif "balance" in text:
            data["balance"].append(text)

        elif "summary" in text or "report" in text:
            data["summary"].append(text)

    return data


def merge_datasets(base, learned):

    merged = base.copy()

    for k in merged:
        merged[k].extend(learned.get(k, []))

    return merged


def train_model():

    global trained

    base = load_base_data()
    learned = load_chatlog_data()

    data = merge_datasets(base, learned)

    X = []
    y = []

    for intent, phrases in data.items():
        for p in phrases:
            X.append(p)
            y.append(intent)

    if not X:
        return

    Xv = vectorizer.fit_transform(X)
    model.fit(Xv, y)

    trained = True


def predict_intent(text):

    if not trained:
        train_model()

    Xv = vectorizer.transform([text])
    pred = model.predict(Xv)[0]
    prob = max(model.predict_proba(Xv)[0])

    return pred, prob


def retrain_from_logs():
    train_model()
