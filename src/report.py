# report.py
# Genera un report HTML leggibile nel browser a partire dai risultati dell'analisi.

from datetime import datetime


def status_badge(status: str) -> str:
    """
    Restituisce un badge colorato in base allo status dell'item.
    """
    if status == "found":
        return '<span class="badge found">✓ Found</span>'
    return '<span class="badge not-found">✗ Not Found</span>'


def pdpa_badge(pdpa_status: str) -> str:
    """
    Restituisce un badge colorato in base allo status PDPA.
    """
    colors = {
        "equivalent": "equivalent",
        "partial": "partial",
        "absent": "absent"
    }
    css_class = colors.get(pdpa_status, "partial")
    return f'<span class="badge {css_class}">{pdpa_status.capitalize()}</span>'


def severity_badge(severity: str) -> str:
    """
    Restituisce un badge colorato in base alla severity dell'item.
    """
    colors = {
        "critical": "critical",
        "major": "major",
        "minor": "minor"
    }
    css_class = colors.get(severity, "minor")
    return f'<span class="badge {css_class}">{severity.capitalize()}</span>'


def generate_html(results: list[dict], summary: dict, policy_source: str) -> str:
    """
    Genera il codice HTML completo del report.
    """

    # Raggruppa i risultati per area
    areas = {}
    for r in results:
        area_name = r["area_name"]
        if area_name not in areas:
            areas[area_name] = []
        areas[area_name].append(r)

    # Genera le righe della tabella per ogni area
    areas_html = ""
    for area_name, items in areas.items():
        areas_html += f"""
        <div class="area">
            <h2>{area_name}</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Question</th>
                        <th>GDPR Ref</th>
                        <th>Status</th>
                        <th>Keywords Found</th>
                        <th>Severity</th>
                        <th>PDPA Status</th>
                        <th>Context</th>
                    </tr>
                </thead>
                <tbody>
        """

        for item in items:
            keywords_found = ", ".join(
                item["found_keywords"]) if item["found_keywords"] else "—"
            gdpr_refs = ", ".join(item["gdpr_ref"])
            context = item["context"][:300] + \
                "..." if len(item["context"]) > 300 else item["context"]
            context = context if context else "—"

            areas_html += f"""
                    <tr class="{'row-found' if item['status'] == 'found' else 'row-not-found'}">
                        <td>{item['item_id']}</td>
                        <td>{item['question']}</td>
                        <td><small>{gdpr_refs}</small></td>
                        <td>{status_badge(item['status'])}</td>
                        <td><small>{keywords_found}</small></td>
                        <td>{severity_badge(item['severity'])}</td>
                        <td>{pdpa_badge(item['pdpa_status'])}</td>
                        <td><small class="context">{context}</small></td>
                    </tr>
            """

        areas_html += """
                </tbody>
            </table>
        </div>
        """

    # Genera la lista dei gap critici
    critical_gaps_html = ""
    if summary["critical_gaps"]:
        critical_gaps_html = "<ul>"
        for gap in summary["critical_gaps"]:
            critical_gaps_html += f"<li><strong>{gap['item_id']}</strong> — {gap['question']}</li>"
        critical_gaps_html += "</ul>"
    else:
        critical_gaps_html = "<p>No critical gaps found.</p>"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDPR x PDPA Gap Analysis Report</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: Arial, sans-serif; font-size: 14px; color: #1e293b; background: #f8fafc; padding: 40px; }}
        header {{ margin-bottom: 32px; }}
        header h1 {{ font-size: 24px; color: #1e293b; margin-bottom: 8px; }}
        header p {{ color: #64748b; font-size: 13px; }}
        .summary {{ display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }}
        .summary-card {{ background: white; border-radius: 8px; padding: 20px 24px; flex: 1; min-width: 150px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .summary-card .number {{ font-size: 32px; font-weight: bold; color: #2563eb; }}
        .summary-card .label {{ font-size: 12px; color: #64748b; margin-top: 4px; }}
        .critical-gaps {{ background: #fff1f2; border-left: 4px solid #9f1239; border-radius: 4px; padding: 16px 20px; margin-bottom: 32px; }}
        .critical-gaps h3 {{ color: #9f1239; margin-bottom: 8px; }}
        .critical-gaps ul {{ padding-left: 20px; }}
        .critical-gaps li {{ margin-bottom: 4px; color: #1e293b; }}
        .area {{ background: white; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .area h2 {{ font-size: 16px; margin-bottom: 16px; color: #1e3a5f; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; font-size: 12px; color: #64748b; padding: 8px 12px; border-bottom: 1px solid #e2e8f0; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #f1f5f9; vertical-align: top; font-size: 13px; }}
        .row-found {{ background: #f0fdf4; }}
        .row-not-found {{ background: #fff1f2; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; }}
        .badge.found {{ background: #dcfce7; color: #166534; }}
        .badge.not-found {{ background: #fee2e2; color: #991b1b; }}
        .badge.equivalent {{ background: #dcfce7; color: #166534; }}
        .badge.partial {{ background: #fef3c7; color: #b45309; }}
        .badge.absent {{ background: #fee2e2; color: #991b1b; }}
        .badge.critical {{ background: #fee2e2; color: #991b1b; }}
        .badge.major {{ background: #fef3c7; color: #b45309; }}
        .badge.minor {{ background: #e0f2fe; color: #0369a1; }}
        .context {{ color: #475569; font-style: italic; }}
        footer {{ margin-top: 40px; text-align: center; color: #94a3b8; font-size: 12px; }}
    </style>
</head>
<body>
    <header>
        <h1>GDPR x PDPA Gap Analysis Report</h1>
        <p>Source: {policy_source}</p>
        <p>Generated: {datetime.now().strftime("%d %B %Y, %H:%M")}</p>
    </header>

    <div class="summary">
        <div class="summary-card">
            <div class="number">{summary['total_items']}</div>
            <div class="label">Total Items</div>
        </div>
        <div class="summary-card">
            <div class="number">{summary['found']}</div>
            <div class="label">Found</div>
        </div>
        <div class="summary-card">
            <div class="number">{summary['not_found']}</div>
            <div class="label">Not Found</div>
        </div>
        <div class="summary-card">
            <div class="number">{summary['coverage_percent']}%</div>
            <div class="label">Coverage</div>
        </div>
        <div class="summary-card">
            <div class="number">{len(summary['critical_gaps'])}</div>
            <div class="label">Critical Gaps</div>
        </div>
    </div>

    <div class="critical-gaps">
        <h3>Critical Gaps</h3>
        {critical_gaps_html}
    </div>

    {areas_html}

    <footer>
        <p>This report is a structured working tool for a student research project. It does not constitute legal advice.</p>
    </footer>
</body>
</html>"""

    return html


def save_report(html: str, output_path: str = "output/report.html") -> None:
    """
    Salva il report HTML nel file di output.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Report salvato in: {output_path}")
