# GDPR × PDPA Privacy Policy Analyzer

A cross-jurisdictional compliance tool that analyzes privacy policies against EU GDPR and Singapore PDPA obligations — built as a collaboration between [Edoardo Pes](https://github.com/pesedo00) (EU/GDPR) and [Kairin Batrisyiah](https://github.com/kairinb) (SG/PDPA).

---

## Live Demo

| Version | Engine | Link |
|---|---|---|
| **v2.0** — current | AI semantic analysis (Claude) | [pesedo00.github.io/gdpr-pdpa-checker/v2](https://pesedo00.github.io/gdpr-pdpa-checker/v2) |
| v1.0 | Keyword matching | [pesedo00.github.io/gdpr-pdpa-checker](https://pesedo00.github.io/gdpr-pdpa-checker) |

Both versions are live. v1.0 is preserved to document the evolution of the tool.

---

## What It Does

Analyzes a privacy policy text against 5 compliance areas under GDPR (Regulation 2016/679) and PDPA (Singapore, as amended 2021):

1. **Purpose Limitation** — specificity of purposes, legal basis per Art. 6(1), legitimate interest balancing test
2. **Consent Language** — freely given/specific/informed/unambiguous consent, withdrawal mechanism, children's data
3. **Data Retention** — specific periods per data category, deletion and anonymisation procedures
4. **Third-Party Sharing** — recipient categories, processor vs. controller distinction, legal basis for transfers
5. **Cross-Border Transfers** — transfer mechanism (adequacy, SCCs, BCRs), PDPA comparable protection standard

---

## v2.0 — AI Engine

v2.0 replaces keyword matching with semantic analysis via the Anthropic API (Claude). Each of the 5 areas is analyzed by a dedicated legal prompt that reasons about the policy text rather than scanning for keywords.

**The key gap this closes:** a policy that says *"we retain data as long as necessary for business purposes"* matches keywords like `as long as necessary` — so v1.0 marks it as found. v2.0 recognizes this as PDPA-compliant under s.25 but a GDPR gap under Art. 5(1)(e), which requires either a specific period or explicit, assessable criteria. The AI catches the asymmetry. The keyword engine cannot.

**Output per area:**
- `verdict` — compliant / ambiguous / gap
- `confidence` — high / medium / low
- `excerpt` — relevant sentence extracted from the policy
- `reasoning` — 1-2 sentence legal rationale with article citations
- `framework` — GDPR / PDPA / both

**Fallback:** if an API call fails for any area, that area falls back to keyword matching automatically. The rest of the analysis is unaffected.

**How to use v2.0:**
1. Open [pesedo00.github.io/gdpr-pdpa-checker/v2](https://pesedo00.github.io/gdpr-pdpa-checker/v2)
2. Enter your Anthropic API key in the field at the top (never stored, never transmitted beyond your browser session)
3. Paste the full text of a privacy policy
4. Click **Analyze**

No account, no backend, no install required. Runs entirely in the browser.

---

## v1.0 — Keyword Engine

The original version. Runs keyword matching against 19 compliance checks across the 5 areas. No API key required — works fully offline.

**How to use v1.0:**
1. Open [pesedo00.github.io/gdpr-pdpa-checker](https://pesedo00.github.io/gdpr-pdpa-checker)
2. Paste the full text of a privacy policy
3. Click **Analyze**

Also available as a Python CLI tool (see [Installation](#installation) below).

---

## Real-World Validation

The tool has been tested on real privacy policies by a Cyber Security & Data Privacy Intern at SkillLab (Amsterdam), who confirmed it saves meaningful time in compliance review workflows.

> *"The tool can be really valuable in real-life scenarios, especially in startups or small businesses where the security/compliance team is wearing multiple hats."*

Primary use case: small compliance teams where one person covers security + privacy + GDPR, and needs to screen multiple policies quickly without a full legal review for each one.

**Test case — Grab privacy policy** (Singapore-based company operating in the EU, subject to both frameworks simultaneously):
- v1.0 result: 73.7% GDPR coverage, 2 critical gaps (retention periods, cross-border transfer mechanism)
- v2.0 result: AI-identified gaps in 4 of 5 areas with legal reasoning, including GDPR/PDPA asymmetries that keyword matching cannot detect

---

## Architecture

```
gdpr-pdpa-checker/
├── index.html              # v1.0 — keyword engine (browser)
├── v2/
│   └── index.html          # v2.0 — AI engine (browser)
├── checklist/
│   └── checklist.json      # 19 compliance checks, GDPR + PDPA mapped
│                           # versioned separately — update without touching code
├── prompts/
│   └── prompts.json        # AI prompts for 5 areas
│                           # versioned separately — update when EDPB guidelines change
├── src/
│   ├── fetcher.py          # fetches policy from URL or text (Python CLI)
│   ├── analyzer.py         # keyword matching engine (Python CLI)
│   └── report.py           # HTML report generator (Python CLI)
├── main.py                 # Python CLI entry point
├── requirements.txt
└── tests/
    └── grab_test.py        # test case with Grab
```

**Design decision — decoupled normative layer:**
`checklist.json` and `prompts.json` are loaded at runtime, not hardcoded. When EDPB publishes new guidelines or PDPA is amended, only these files need updating — no changes to application logic required. This keeps the tool maintainable as the regulatory landscape evolves.

---

## Installation (Python CLI)

```bash
git clone https://github.com/pesedo00/gdpr-pdpa-checker.git
cd gdpr-pdpa-checker
pip3 install -r requirements.txt
```

**Analyze from URL:**
```bash
python3 main.py --url https://www.grab.com/sg/terms-policies/privacy-notice/
```

**Analyze from pasted text:**
```bash
python3 main.py --text "paste your privacy policy text here"
```

**Custom output path:**
```bash
python3 main.py --url https://example.com/privacy --output output/myreport.html
```

---

## Roadmap

| Feature | Status |
|---|---|
| AI semantic engine (v2.0) | ✅ Complete |
| PDPA-specific ambiguity flags | 🔄 In progress (Kairin) |
| Batch analysis — up to 20 policies per session | 📋 Planned |
| CSV export for compliance reporting | 📋 Planned |
| Side-by-side GDPR vs. PDPA view | 📋 Planned |
| Historical policy comparison | 💡 Post-beta |

---

## Disclaimer

This tool is a student research project. It does not constitute legal advice and is not a substitute for a professional compliance audit.
