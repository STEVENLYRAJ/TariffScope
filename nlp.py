from transformers import pipeline
import spacy

nlp_spacy = spacy.load("en_core_web_sm")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

LABELS = ["tariff escalation", "trade tension", "trade relief", "neutral"]

def analyze_article(text: str) -> dict:
    result = classifier(text, LABELS)
    top_label = result["labels"][0]
    top_score = result["scores"][0]
    
    doc = nlp_spacy(text)
    countries = [e.text for e in doc.ents if e.label_ == "GPE"]
    orgs = [e.text for e in doc.ents if e.label_ == "ORG"]
    
    tension_score = int(top_score * 100) if "tension" in top_label or "escalation" in top_label else 20
    
    return {
        "label": top_label,
        "confidence": round(top_score, 2),
        "tension_score": tension_score,
        "countries_mentioned": list(set(countries)),
        "orgs_mentioned": list(set(orgs))
    }