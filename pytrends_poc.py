"""
POC - Google Trends via Pytrends
Hackathon avec Emmanuel
"""

from pytrends.request import TrendReq
import pandas as pd
import json
import time
from datetime import datetime

# ─── Init ───────────────────────────────────────────────────────────────────
# retries + backoff pour éviter les 429/400 de Google
pytrends = TrendReq(hl='fr-FR', tz=60, timeout=(10, 25))


def get_interest_over_time(keywords: list[str], timeframe: str = "today 3-m") -> pd.DataFrame:
    """
    Récupère l'évolution de l'intérêt dans le temps pour une liste de mots-clés.

    timeframe exemples:
      - 'now 1-H'     : dernière heure
      - 'now 4-H'     : 4 dernières heures
      - 'now 1-d'     : dernier jour
      - 'now 7-d'     : 7 derniers jours
      - 'today 1-m'   : dernier mois
      - 'today 3-m'   : 3 derniers mois (défaut)
      - 'today 12-m'  : 12 derniers mois
      - 'today 5-y'   : 5 dernières années
      - '2024-01-01 2024-12-31' : plage de dates custom
    """
    pytrends.build_payload(keywords, timeframe=timeframe)
    df = pytrends.interest_over_time()
    if df.empty:
        print(f"[!] Aucune donnée pour: {keywords}")
        return df
    df = df.drop(columns=["isPartial"], errors="ignore")
    return df


def get_related_queries(keywords: list[str], timeframe: str = "today 3-m") -> dict:
    """Requêtes associées (top + rising) pour chaque mot-clé."""
    pytrends.build_payload(keywords, timeframe=timeframe)
    return pytrends.related_queries()


def get_related_topics(keywords: list[str], timeframe: str = "today 3-m") -> dict:
    """Sujets associés (top + rising) pour chaque mot-clé."""
    pytrends.build_payload(keywords, timeframe=timeframe)
    return pytrends.related_topics()


def get_trending_searches(country: str = "france") -> pd.DataFrame:
    """Recherches tendances du jour pour un pays (daily trending searches)."""
    return pytrends.trending_searches(pn=country)


def get_realtime_trending(country: str = "FR", category: str = "all") -> pd.DataFrame:
    """
    Tendances en temps réel.
    country: code ISO 2 lettres (FR, US, GB...)
    category: 'all', 'b' (business), 'e' (entertainment), 'h' (health), etc.
    """
    return pytrends.realtime_trending_searches(pn=country, cat=category, count=20)


def get_interest_by_region(keywords: list[str], resolution: str = "COUNTRY", timeframe: str = "today 12-m") -> pd.DataFrame:
    """
    Intérêt par région géographique.
    resolution: 'COUNTRY', 'REGION', 'CITY', 'DMA'
    """
    pytrends.build_payload(keywords, timeframe=timeframe)
    return pytrends.interest_by_region(resolution=resolution, inc_low_vol=True)


def get_suggestions(keyword: str) -> list[dict]:
    """Auto-complétion Google pour un mot-clé (utile pour trouver des variantes)."""
    return pytrends.suggestions(keyword)


# ─── Demo ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("POC Pytrends — Hackathon")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # 1. Évolution temporelle
    keywords = ["intelligence artificielle", "ChatGPT", "LLM"]
    print(f"\n[1] Intérêt dans le temps — {keywords}")
    df_time = get_interest_over_time(keywords, timeframe="today 12-m")
    if not df_time.empty:
        print(df_time.tail(5).to_string())
    time.sleep(2)

    # 2. Comparaison de 2 termes
    print("\n[2] Comparaison rapide — 6 derniers mois")
    df_cmp = get_interest_over_time(["Python", "JavaScript"], timeframe="today 3-m")
    if not df_cmp.empty:
        print(df_cmp.describe().to_string())
    time.sleep(2)

    # 3. Requêtes associées
    print("\n[3] Requêtes associées — 'intelligence artificielle'")
    related = get_related_queries(["intelligence artificielle"], timeframe="today 3-m")
    for kw, data in related.items():
        if data and data.get("top") is not None:
            print(f"  TOP pour '{kw}':")
            print(data["top"].head(5).to_string(index=False))
        if data and data.get("rising") is not None:
            print(f"  RISING pour '{kw}':")
            print(data["rising"].head(5).to_string(index=False))
    time.sleep(2)

    # 4. Tendances en temps réel — France
    print("\n[4] Tendances en temps réel — France")
    try:
        trending = get_realtime_trending(country="FR")
        print(trending[["title", "entityNames"]].head(10).to_string(index=False))
    except Exception as e:
        print(f"  [!] {e}")
    time.sleep(2)

    # 5. Intérêt par région (France)
    print("\n[5] Intérêt par région — 'intelligence artificielle'")
    df_region = get_interest_by_region(
        ["intelligence artificielle"],
        resolution="COUNTRY",
        timeframe="today 12-m"
    )
    if not df_region.empty:
        top_countries = df_region.sort_values("intelligence artificielle", ascending=False).head(10)
        print(top_countries.to_string())
    time.sleep(2)

    # 6. Suggestions / autocomplete
    print("\n[6] Suggestions Google — 'hackathon'")
    suggestions = get_suggestions("hackathon")
    for s in suggestions:
        print(f"  - {s.get('title')} ({s.get('type')})")

    print("\n[OK] POC terminé.")
