import re
from difflib import SequenceMatcher

INTENT_PATTERNS = {
    "expense": ["spent", "pay", "paid", "expense", "buy", "bought"],
    "income": ["income", "received", "got", "salary", "pocket", "have", "deposit", "credit"],
    "balance": ["balance", "left", "remain"],
    "summary": ["summary", "report", "total"]
}

CATEGORIES = [
    "food","travel","bus","book","movie",
    "shopping","mobile","data","fees","rent"
]


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def fuzzy_contains(text, word_list):
    words = text.lower().split()
    for w in words:
        for key in word_list:
            if similarity(w, key) > 0.75:
                return True
    return False


def detect_intent(text):

    t = text.lower()

    for intent, words in INTENT_PATTERNS.items():
        if fuzzy_contains(t, words):
            return intent, 0.9

    return "unknown", 0.3


def extract_amount(text):
    nums = re.findall(r"\d+", text)
    return float(nums[0]) if nums else 0


def detect_category(text):

    t = text.lower()

    for c in CATEGORIES:
        if c in t:
            return c

    return "general"
