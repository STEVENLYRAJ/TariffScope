import re

LABELS = ["tariff escalation", "trade tension", "trade relief", "neutral"]
KEYWORD_MAP = {
    "tariff escalation": ["escalation", "escalating", "spike", "sharp increase", "sharp rise", "tariff hike", "higher tariffs"],
    "trade tension": ["tension", "trade tension", "dispute", "standoff", "friction", "sanction", "trade war"],
    "trade relief": ["relief", "easing", "rollback", "reduction", "lower tariffs", "deal", "agreement"]
}
COUNTRIES = [
    "India", "China", "USA", "Germany", "Japan", "Brazil", "UK", "France", "Canada",
    "Australia", "South Korea", "Mexico", "Indonesia", "Turkey", "Saudi Arabia"
]

def analyze_article(text: str) -> dict:
    normalized = text.lower()
    best_label = "neutral"
    best_score = 0

    for label, keywords in KEYWORD_MAP.items():
        score = sum(1 for keyword in keywords if keyword in normalized)
        if score > best_score:
            best_score = score
            best_label = label

    confidence = min(0.99, 0.3 + best_score * 0.15)
    tension_score = 85 if best_label == "tariff escalation" else 65 if best_label == "trade tension" else 40 if best_label == "trade relief" else 20
    countries_mentioned = sorted({country for country in COUNTRIES if country.lower() in normalized})
    orgs_mentioned = sorted(set(re.findall(r"\b[A-Z][A-Za-z0-9&\.]{2,}(?:\s+[A-Z][A-Za-z0-9&\.]{2,})*\b", text)))[:5]

    return {
        "label": best_label,
        "confidence": round(confidence, 2),
        "tension_score": tension_score,
        "countries_mentioned": countries_mentioned,
        "orgs_mentioned": orgs_mentioned
    }
