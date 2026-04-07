# analyzer.py
# Analizza il testo di una privacy policy confrontandolo con la checklist.

import json
import re
from pathlib import Path


def load_checklist(path: str = "checklist/checklist.json") -> dict:
    """
    Carica la checklist dal file JSON.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_keywords(text: str, keywords: list[str]) -> list[str]:
    """
    Cerca le keywords nel testo in modo case-insensitive.
    Restituisce la lista delle keywords trovate.
    """
    text_lower = text.lower()
    found = []
    for keyword in keywords:
        if keyword.lower() in text_lower:
            found.append(keyword)
    return found


def get_context(text: str, keyword: str, window: int = 200) -> str:
    """
    Restituisce un frammento di testo intorno alla keyword trovata.
    Utile per capire in che contesto appare la keyword nel documento.
    """
    text_lower = text.lower()
    idx = text_lower.find(keyword.lower())
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(text), idx + len(keyword) + window)
    return text[start:end].strip()


def analyze(policy_text: str, checklist_path: str = "checklist/checklist.json") -> list[dict]:
    """
    Esegue l'analisi della policy contro tutti gli item della checklist.
    Restituisce una lista di risultati, uno per ogni item.
    """
    checklist = load_checklist(checklist_path)
    results = []

    for area in checklist["areas"]:
        for item in area["items"]:
            found_keywords = find_keywords(policy_text, item["keywords"])

            # Determina lo stato dell'item
            if found_keywords:
                status = "found"
                # Prende il contesto della prima keyword trovata
                context = get_context(policy_text, found_keywords[0])
            else:
                status = "not_found"
                context = ""

            results.append({
                "area_id": area["id"],
                "area_name": area["name"],
                "item_id": item["id"],
                "question": item["question"],
                "gdpr_ref": item["gdpr_ref"],
                "pdpa_ref": item["pdpa_ref"],
                "pdpa_status": item["pdpa_status"],
                "severity": item["severity"],
                "status": status,
                "found_keywords": found_keywords,
                "context": context
            })

    return results


def summary(results: list[dict]) -> dict:
    """
    Genera un riepilogo numerico dell'analisi.
    """
    total = len(results)
    found = sum(1 for r in results if r["status"] == "found")
    not_found = total - found
    critical_gaps = [
        r for r in results
        if r["status"] == "not_found" and r["severity"] == "critical"
    ]

    return {
        "total_items": total,
        "found": found,
        "not_found": not_found,
        "coverage_percent": round((found / total) * 100, 1),
        "critical_gaps": critical_gaps
    }
