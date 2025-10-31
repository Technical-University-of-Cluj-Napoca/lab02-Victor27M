#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://dexonline.ro/definitie/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_definitions(word: str) -> list[str]:
    """Scrape definitions for a Romanian word from dexonline.ro."""
    url = BASE_URL + word
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Eroare la conectare: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    defs = []

    for tag in soup.select("span.def, span.tree-def"):
        text = tag.get_text(strip=True)
        if text and text not in defs:
            defs.append(text)

    return defs[:3]  

def main():
    if len(sys.argv) < 2:
        print("Utilizare: python define.py <cuvânt>")
        sys.exit(1)

    word = sys.argv[1].strip().lower()
    if not word:
        print("Te rog introdu un cuvânt valid.")
        sys.exit(1)

    defs = get_definitions(word)

    if defs:
        print(f"Definiții pentru „{word}”:")
        for d in defs:
            print("-", d)
    else:
        print(f"Nu am găsit nicio definiție pentru „{word}”.")

if __name__ == "__main__":
    main()
