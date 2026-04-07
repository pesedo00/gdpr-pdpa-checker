# main.py
# Punto di ingresso del tool. Esegui con:
# python3 main.py --url https://grab.com/sg/terms/privacy/
# python3 main.py --text "testo della policy"

import argparse
import sys
from src.fetcher import fetch_policy
from src.analyzer import analyze, summary
from src.report import generate_html, save_report


def main():
    parser = argparse.ArgumentParser(
        description="GDPR x PDPA Privacy Policy Analyzer"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="URL della privacy policy da analizzare"
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Testo della privacy policy incollato direttamente"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/report.html",
        help="Percorso del file HTML di output (default: output/report.html)"
    )

    args = parser.parse_args()

    # Controlla che sia stato fornito almeno un input
    if not args.url and not args.text:
        print("Errore: devi fornire un URL (--url) o un testo (--text)")
        sys.exit(1)

    # Recupera il testo della policy
    if args.url:
        print(f"Scarico la policy da: {args.url}")
        policy_text = fetch_policy(args.url, mode="url")
        source = args.url
    else:
        print("Uso il testo fornito direttamente.")
        policy_text = fetch_policy(args.text, mode="text")
        source = "Testo diretto"

    print(f"Testo recuperato: {len(policy_text)} caratteri")

    # Analizza la policy
    print("Analizzo la policy...")
    results = analyze(policy_text)
    report_summary = summary(results)

    # Mostra il riepilogo nel terminale
    print(f"\nRiepilogo:")
    print(f"  Item totali:     {report_summary['total_items']}")
    print(f"  Trovati:         {report_summary['found']}")
    print(f"  Non trovati:     {report_summary['not_found']}")
    print(f"  Copertura:       {report_summary['coverage_percent']}%")
    print(f"  Gap critici:     {len(report_summary['critical_gaps'])}")

    if report_summary["critical_gaps"]:
        print("\nGap critici:")
        for gap in report_summary["critical_gaps"]:
            print(f"  {gap['item_id']} — {gap['question']}")

    # Genera e salva il report HTML
    html = generate_html(results, report_summary, source)
    save_report(html, args.output)
    print(f"\nApri il report con: open {args.output}")


if __name__ == "__main__":
    main()
