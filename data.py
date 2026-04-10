
# ─────────────────────────────────────────────
#  data.py  —  TariffScope static/fallback data
#  Used by main.py when NLP is loading or fails
# ─────────────────────────────────────────────
 
# ── Country list (shown in frontend dropdown) ──────────────────────────────
COUNTRIES = [
    "India", "China", "USA", "Germany", "Japan",
    "Brazil", "UK", "France", "Canada", "Australia",
    "South Korea", "Mexico", "Indonesia", "Turkey", "Saudi Arabia"
]
 
# ── Sector list (shown in frontend dropdown) ───────────────────────────────
SECTORS = [
    "Electronics", "Steel", "Agriculture", "Automobiles",
    "Pharmaceuticals", "Textiles", "Semiconductors",
    "Energy", "Chemicals", "Defense"
]
 
# ── Base tariff risk weights per sector ────────────────────────────────────
# Higher = more sensitive to tariff changes
SECTOR_RISK_WEIGHT = {
    "Electronics":     0.90,
    "Semiconductors":  0.95,
    "Steel":           0.75,
    "Automobiles":     0.80,
    "Agriculture":     0.60,
    "Pharmaceuticals": 0.55,
    "Textiles":        0.65,
    "Energy":          0.70,
    "Chemicals":       0.68,
    "Defense":         0.50,
}
 
# ── Base country exposure scores (0–100) ───────────────────────────────────
# Represents how exposed a country is to global tariff tensions
COUNTRY_EXPOSURE = {
    "China":        92,
    "USA":          85,
    "India":        72,
    "Germany":      68,
    "Japan":        65,
    "South Korea":  70,
    "Brazil":       58,
    "UK":           55,
    "France":       52,
    "Canada":       60,
    "Australia":    48,
    "Mexico":       63,
    "Indonesia":    55,
    "Turkey":       60,
    "Saudi Arabia": 45,
}
 
# ── Chart data: sector tariff levels shown on Analyzer bar chart ────────────
# These are the default values before any user slider interaction
DEFAULT_SECTOR_CHART = [
    {"name": "Steel",          "value": 40, "color": "#FF6B6B"},
    {"name": "Tech",           "value": 80, "color": "#FFD93D"},
    {"name": "Agri",           "value": 30, "color": "#6BCB77"},
    {"name": "Auto",           "value": 55, "color": "#4D96FF"},
    {"name": "Pharma",         "value": 25, "color": "#C77DFF"},
]
 
# ── Trade volume timeline (8 data points = last 8 months) ──────────────────
# Used in the GeoTrade dashboard line chart
TRADE_VOLUME_TIMELINE = [
    {"month": "Sep", "value": 100},
    {"month": "Oct", "value": 88},
    {"month": "Nov", "value": 82},
    {"month": "Dec", "value": 91},
    {"month": "Jan", "value": 105},
    {"month": "Feb", "value": 115},
    {"month": "Mar", "value": 120},
    {"month": "Apr", "value": 90},
]
 
# ── Dashboard summary stats (fallback if NLP pipeline is unavailable) ───────
DASHBOARD_DEFAULTS = {
    "global_exposure_index": 72,
    "exposure_label":        "High",
    "most_affected_country": "China",
    "highest_risk_sector":   "Electronics",
    "active_trade_disputes": 14,
    "countries_monitored":   len(COUNTRIES),
}
 
# ── Simulation risk thresholds ──────────────────────────────────────────────
# Used by /simulate endpoint to decide risk label
SIMULATION_THRESHOLDS = {
    "LOW":    (0,  15),   # tariff 0–15%  → LOW
    "MEDIUM": (15, 30),   # tariff 15–30% → MEDIUM
    "HIGH":   (30, 100),  # tariff 30%+   → HIGH
}
 
# Countries most affected when tariffs spike (used in simulation response)
SIMULATION_TOP_AFFECTED = {
    "Electronics":     ["China", "South Korea", "Japan"],
    "Steel":           ["China", "India", "Brazil"],
    "Agriculture":     ["India", "Brazil", "USA"],
    "Automobiles":     ["Germany", "Japan", "Mexico"],
    "Pharmaceuticals": ["India", "Germany", "China"],
    "Semiconductors":  ["China", "South Korea", "Taiwan"],
    "Textiles":        ["India", "Bangladesh", "China"],
    "Energy":          ["Saudi Arabia", "Russia", "USA"],
    "Chemicals":       ["Germany", "China", "USA"],
    "Defense":         ["USA", "Russia", "France"],
}
 
# ── Sample news headlines (fallback when live API is unavailable) ───────────
SAMPLE_HEADLINES = [
    {
        "title": "US imposes 25% tariff on Chinese electronics imports",
        "source": "Reuters",
        "country": "China",
        "sector": "Electronics",
        "sentiment": "negative",
        "tension_score": 85,
    },
    {
        "title": "India and EU reach preliminary trade agreement on steel",
        "source": "Bloomberg",
        "country": "India",
        "sector": "Steel",
        "sentiment": "positive",
        "tension_score": 20,
    },
    {
        "title": "WTO flags rising agricultural tariff disputes between USA and Brazil",
        "source": "WTO",
        "country": "Brazil",
        "sector": "Agriculture",
        "sentiment": "negative",
        "tension_score": 65,
    },
    {
        "title": "Japan reduces auto tariffs as part of new bilateral deal",
        "source": "AP",
        "country": "Japan",
        "sector": "Automobiles",
        "sentiment": "positive",
        "tension_score": 15,
    },
    {
        "title": "Semiconductor export restrictions tighten between US and China",
        "source": "FT",
        "country": "China",
        "sector": "Semiconductors",
        "sentiment": "negative",
        "tension_score": 92,
    },
]
 
# ── Helper functions ────────────────────────────────────────────────────────
 
def get_risk_label(score: int) -> str:
    """Convert a numeric risk score to a display label."""
    if score >= 70:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"
 
 
def get_simulation_risk(tariff: float) -> str:
    """Return risk label for a given tariff percentage."""
    for label, (low, high) in SIMULATION_THRESHOLDS.items():
        if low <= tariff < high:
            return label
    return "HIGH"
 
 
def get_top_affected(sector: str) -> list:
    """Return top affected countries for a given sector."""
    return SIMULATION_TOP_AFFECTED.get(sector, ["China", "India", "USA"])
 
 
def calculate_risk_score(tariff: float, sector: str, country: str, tension_score: int = 50) -> int:
    """
    Core risk formula combining three signals:
      40% tariff level
      40% NLP tension score (default 50 if NLP unavailable)
      20% country base exposure
    Returns integer 0–100.
    """
    sector_weight  = SECTOR_RISK_WEIGHT.get(sector, 0.70)
    country_base   = COUNTRY_EXPOSURE.get(country, 60)
    tariff_signal  = min(tariff, 100)
 
    score = (
        (tariff_signal  * sector_weight * 0.40) +
        (tension_score               * 0.40) +
        (country_base                * 0.20)
    )
    return min(100, round(score))
 