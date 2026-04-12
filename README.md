# GDPR × PDPA Privacy Policy Analyzer

## Live Demo

[Live Demo](https://pesedo00.github.io/gdpr-pdpa-checker)

### How to use the web tool

1. Open the URL above in your browser.
2. Paste the full text of a privacy policy into the text area.
3. Click **Analyze** to run the gap analysis.

The tool will instantly show you coverage percentage, a per-area breakdown table, and a list of critical gaps — no account or install required.

---

A Python tool that analyzes a privacy policy against a structured checklist
of obligations from both GDPR (EU) and PDPA (Singapore), and generates a
side-by-side gap analysis report.

Built as part of a cross-jurisdictional legal-tech collaboration between
Edoardo Pes (EU/GDPR side) and Kairin Batrisyiah (SG/PDPA side).

---

## What it does

- Fetches a privacy policy from a URL or accepts pasted text
- Runs keyword matching against 19 compliance checks across 5 areas
- Flags critical gaps under GDPR
- Shows the PDPA equivalent status for each item
- Generates a readable HTML report

## The 5 areas

1. Purpose Limitation
2. Consent Language
3. Data Retention
4. Third-Party Sharing
5. Cross-Border Transfers

## Test case

Grab privacy policy — a Singapore-based company operating in the EU,
making it subject to both frameworks simultaneously.

Result: 73.7% GDPR coverage, 2 critical gaps (retention periods and
cross-border transfer mechanism).

---

## Installation
```bash
git clone https://github.com/pesedo00/gdpr-pdpa-checker.git
cd gdpr-pdpa-checker
pip3 install -r requirements.txt
```

## Usage

Analyze from URL:
```bash
python3 main.py --url https://www.grab.com/sg/terms-policies/privacy-notice/
```

Analyze from pasted text:
```bash
python3 main.py --text "paste your privacy policy text here"
```

Custom output path:
```bash
python3 main.py --url https://example.com/privacy --output output/myreport.html
```

---

## Project structure
```
gdpr-pdpa-checker/
├── main.py                  # entry point
├── requirements.txt
├── checklist/
│   └── checklist.json       # 19 compliance checks, GDPR + PDPA mapped
├── src/
│   ├── fetcher.py           # fetches policy from URL or text
│   ├── analyzer.py          # keyword matching engine
│   └── report.py            # HTML report generator
├── output/
│   └── report.html          # generated report
└── tests/
    └── grab_test.py         # test case with Grab
```

---

## Disclaimer

This tool is a structured working instrument for a student research project.
It does not constitute legal advice and is not a substitute for a
professional compliance audit.