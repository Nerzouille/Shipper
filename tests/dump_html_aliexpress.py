"""
Aliexpress HTML Dumper
==================
Dump N pages de résultats Aliexpress en fichiers HTML bruts.
Usage :
  python dump_html.py --query "abris de jardin" --pages 50 --apikey TA_CLE
"""
import os
import time
import random
import argparse
import requests

SCRAPERAPI_URL = "http://api.scraperapi.com"
BASE_URL       = "https://www.aliexpress.com"


def fetch(url: str, api_key: str) -> str:
    for attempt in range(3):
        try:
            resp = requests.get(
                SCRAPERAPI_URL,
                params={
                    "api_key":      api_key,
                    "url":          url,
                    "country_code": "fr",
                    "render":       "true",   # JS rendering — essentiel pour Aliexpress
                },
                timeout=90,  # Aliexpress est plus lent qu'Amazon
            )
            if resp.status_code == 200:
                return resp.text
            print(f"  ⚠️ HTTP {resp.status_code} (tentative {attempt+1}/3)")
            time.sleep(5)
        except Exception as e:
            print(f"  ❌ Erreur: {e} (tentative {attempt+1}/3)")
            time.sleep(5)
    return ""


def build_url(query: str, page_num: int) -> str:
    """
    URL de recherche Aliexpress.
    - /wholesale est le endpoint de recherche standard
    - SearchText = mot-clé
    - page       = numéro de page (commence à 1)
    - SortType   = default (pertinence), SALE_PRICE_ASC / DESC, NEWEST
    """
    slug = query.strip().replace(" ", "-")
    encoded = query.strip().replace(" ", "+")
    return (
        f"{BASE_URL}/wholesale"
        f"?SearchText={encoded}"
        f"&page={page_num}"
        f"&SortType=default"
    )


def main():
    parser = argparse.ArgumentParser(description="Aliexpress HTML Dumper via ScraperAPI")
    parser.add_argument("--query",  "-q", required=True,        help="Mot-clé de recherche")
    parser.add_argument("--pages",  "-p", type=int, default=50, help="Nombre de pages (défaut: 50)")
    parser.add_argument("--apikey", "-k", required=True,        help="Clé API ScraperAPI")
    parser.add_argument("--outdir", "-o", default="html_dump",  help="Dossier de sortie (défaut: html_dump)")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    print(f"\n🚀 Dump HTML Aliexpress — '{args.query}' — {args.pages} pages → ./{args.outdir}/\n")

    ok, fail = 0, 0

    for page_num in range(1, args.pages + 1):
        url = build_url(args.query, page_num)
        print(f"[{page_num:02d}/{args.pages}] {url} ... ", end="", flush=True)

        html = fetch(url, args.apikey)

        if not html:
            print("❌ vide")
            fail += 1
            continue

        # Vérification basique : Aliexpress charge parfois une page anti-bot vide
        if len(html) < 5_000:
            print(f"⚠️  Contenu suspect ({len(html):,} chars) — probable page anti-bot")
            fail += 1
            # On sauvegarde quand même pour diagnostic
            filename = os.path.join(args.outdir, f"page_{page_num:02d}_SUSPECT.html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            time.sleep(random.uniform(3, 6))
            continue

        filename = os.path.join(args.outdir, f"page_{page_num:02d}.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ {len(html):,} chars → {filename}")
        ok += 1

        # Délai plus long que pour Amazon (site plus agressif anti-scraping)
        time.sleep(random.uniform(2, 4))

    print(f"\n{'='*50}")
    print(f"✅ {ok} pages sauvegardées | ❌ {fail} échecs")
    print(f"📁 Dossier : ./{args.outdir}/")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()