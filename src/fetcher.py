# fetcher.py
# Recupera il testo di una privacy policy da URL o testo incollato direttamente.

import requests
from bs4 import BeautifulSoup


def fetch_from_url(url: str) -> str:
    """
    Scarica il contenuto testuale di una pagina web dall'URL fornito.
    Rimuove tag HTML, script e stili per restituire solo il testo leggibile.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Impossibile raggiungere l'URL: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Rimuove script e stili che non contengono testo utile
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    return text


def fetch_from_text(text: str) -> str:
    """
    Accetta testo incollato direttamente dall'utente.
    Pulisce spazi e righe vuote in eccesso.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)


def fetch_policy(source: str, mode: str = "url") -> str:
    """
    Punto di ingresso principale.
    mode='url'  -> scarica da URL
    mode='text' -> accetta testo diretto
    """
    if mode == "url":
        return fetch_from_url(source)
    elif mode == "text":
        return fetch_from_text(source)
    else:
        raise ValueError("mode deve essere 'url' oppure 'text'")
