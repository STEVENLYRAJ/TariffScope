from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/risk")
def get_risk(country: str = "India", sector: str = "Electronics", tariff: float = 25):
    score = min(100, int(tariff * 1.8 + 20))
    return {
        "risk_score": score,
        "country": country,
        "sector": sector,
        "chart_data": [
            {"name": "Steel", "value": 40},
            {"name": "Tech", "value": 80},
            {"name": "Agri", "value": 30}
        ]
    }

@app.get("/simulate")
def simulate(tariff: float = 10):
    price_increase = round(tariff * 1.5, 1)
    risk = "LOW" if tariff < 15 else "HIGH" if tariff > 30 else "MEDIUM"
    return {
        "tariff": tariff,
        "price_increase": price_increase,
        "top_affected": ["China", "India"],
        "risk": risk
    }

@app.get("/")
def home():
    return {"message": "TariffScope API Running "}

@app.get("/dashboard")
def dashboard():
    return {
        "global_exposure_index": 72,
        "exposure_label": "High",
        "most_affected": "China",
        "highest_risk_sector": "Electronics",
        "trade_volume": [100, 88, 82, 95, 108, 120, 112, 90]
    }

from nlp import analyze_article

@app.get("/analyze")
def analyze(text: str):
    return analyze_article(text)