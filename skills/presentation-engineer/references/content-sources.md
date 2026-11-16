# Content sources — public data and standards that supplement the user's material

Open this only when the brief needs public context that the user didn't provide. The user's own
material is always the primary source. Every external fact gets its own `sources[]` entry with an
`accessedAt` date. Search with public topic terms only. Never put names, internal numbers or other
sensitive strings from private documents into a search query.

Verification status (2026-11-16):
- **read**: the licence text itself was read (usually its copy on GitHub).
- **search**: the official page was seen only in search results. Open it before relying on it.

---

## Our World in Data — ourworldindata.org
- **Has:** Long-run global series on health, education, energy, economy, and many other topics, as
  charts with downloadable data.
- **Licence (search):**
  - Charts, articles and data that OWID produces are **CC BY**, "unless stated otherwise".
  - Data that OWID republishes from third parties keeps **those authors' terms**.
  - Older charts may be labelled CC BY-SA; the FAQ says to treat them as CC BY.
- **Extract:** On a chart, use *Download → data (CSV)*. Keep the chart URL and note the indicator
  name, unit, years and the underlying source shown under the chart.
- **Cite both** OWID and the original producer:
  ```json
  { "id": "owid_literacy", "title": "Literacy rate (OWID, based on UNESCO)", "kind": "dataset",
    "url": "https://ourworldindata.org/grapher/…", "creator": "Our World in Data; UNESCO",
    "accessedAt": "2026-11-16", "license": "CC BY 4.0 (OWID); third-party terms apply to source data" }
  ```
  Citation on the slide: `{"sourceId": "owid_literacy", "locator": "Israel, 2000–2022"}`.

## Israel Central Bureau of Statistics (הלמ"ס) — cbs.gov.il
- **Has:** Official Israeli statistics: population, education, labour, prices and more. Includes
  tables, press releases and the Statistical Abstract.
- **Licence:**
  - The site publishes an open-use licence page: "רישיון פתוח למידע באתר האינטרנט של הלשכה המרכזית
    לסטטיסטיקה" (cbs.gov.il/he/Pages/רישיון-שימוש.aspx).
  - Only the page title was seen in search. The **attribution clause and conditions were not
    verified**. Read the page before reuse and quote its required credit line.
- **Extract:**
  - Download the table as Excel or CSV.
  - Keep the table number and title, the publication date, the unit (thousands? percent?), and the
    exact cell range you used as the locator, for example `לוח 2.1!B4:F9`.
  - Hebrew tables often carry footnotes that change the definition. Copy them into `notes`.
- **Cite as:** `הלמ"ס, {table title}, {publication}, {year}`. Include the URL and `accessedAt`.

## MITRE ATT&CK — attack.mitre.org
- **Has:**
  - A knowledge base of adversary tactics and techniques, each with an ID.
  - Example technique: **T1566 Phishing**, https://attack.mitre.org/techniques/T1566/ (search).
    Sub-technique: `T1566.002`.
- **Data (read):**
  - STIX 2.1 bundles in github.com/mitre-attack/attack-stix-data, split into `enterprise-attack/`,
    `mobile-attack/` and `ics-attack/`. The unversioned file is always the latest release.
  - STIX 2.0 bundles in github.com/mitre/cti.
  - The ATT&CK Navigator is for layer views. The "Data & Tools" page URL is unverified:
    attack.mitre.org/resources/attack-data-and-tools/.
- **Licence (read, the repo's LICENSE.txt):**
  - Royalty-free use, including commercial.
  - Copies must keep MITRE's copyright notice, for example "© 2026 The MITRE Corporation. This work is
    reproduced and distributed with the permission of The MITRE Corporation."
  - ATT&CK® is a registered trademark.
  - Terms of use: attack.mitre.org/resources/legal-and-branding/terms-of-use/ (search).
- **Extract:**
  - Record the technique ID, name, tactic(s) and the ATT&CK version or date.
  - Put the ID on the slide (e.g. `T1566 · Phishing`), monospaced and LTR inside RTL text.
- **In a cyber deck, map a technique only where your evidence shows it.**
  - Cite the finding itself, e.g. an email header in the incident report (`sourceId: ir_report,
    locator: "p.7"`).
  - Cite the ATT&CK technique as a second citation, with `kind: "derived"` for the mapping.
  - If the mapping is a guess, mark it `disputed` and say so in the notes.
  - Don't decorate a slide with a matrix of techniques you didn't observe.

## Standards and primary documents (pattern)
- Use the document itself rather than a blog about it. Examples: RFCs (rfc-editor.org), W3C or WHATWG
  specs, legislation, papers (DOI), vendor documentation.
- The locator is a section (`§4.1.1`), figure, or page.
- Keep the version or date: specs change.

## Before using any public number
- [ ] the unit, period and population match the claim on the slide
- [ ] the licence allows reuse, and the required credit is in the `sources[]` record
- [ ] the number is the latest release, or the slide says which release it uses
- [ ] if it disagrees with the user's material, both are kept and the gap is explained (source-intake.md §5)
