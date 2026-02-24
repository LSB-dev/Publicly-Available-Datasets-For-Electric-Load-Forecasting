# README: datasets.yaml Mapping
## Scope
This document specifies how the dataset table in `README.md` is converted into `metadata/datasets.yaml`.
The generator must follow these rules. Ambiguous values are preserved via `*_raw` fields.

## Input location
- Source table: README section `# The list` (first markdown table under this heading)

## Table columns (as in README)
ID | Abbrev | Name | Domain | Resolution | Features | Duration | Spanned years | Horizons | Regions | Type | Links | Access

---

## Field mapping

### Identity
- `abbreviation` ← `Abbrev` (as-is, string)
- `dataset_id` ← normalized `Abbrev`
  - normalization:
    - lowercase
    - replace `-` with `_`
    - replace whitespace with `_`
    - remove all characters except `a-z0-9_`
    - collapse multiple `_` into one
  - examples:
    - `ISO-NE` → `iso_ne`
    - `BDG-Proj2` → `bdg_proj2`

- `name` ← `Name`

### Domain
- `domain_raw` ← `Domain` (as-is, trimmed)
- `domain` normalization:
  - single value:
    - `S` → `system`
    - `R` → `residential`
    - `I` → `industrial`
    - `?` → `unknown`
  - multiple values (e.g. `S, R` or `R, I`):
    - set `domain = unknown`
    - keep `domain_raw` (must contain original multi-value)

### Type
- `type` ← `Type` icon
  - `📦` → `collection`
  - `📁` → `file_archive`
  - `🌐` → `platform_api`

### Access
- access icon is preserved via notes:
  - `🔓` → `access.access_notes = ""` (or "direct access")
  - `📧` → `access.access_notes = "request required"`
- `access.url` is determined from links (see Links section)

### Links
- Extract all URLs from the `Links` cell (one or more markdown links).
- `links` ← list of extracted URLs (order preserved)
- `access.url` ← first URL in `links`

If no link is present:
- `links = null`
- `access.url` must be set to an empty string or the entry must be rejected (decision: reject)

### Resolution
- `resolution_raw` ← `Resolution` (as-is, trimmed)
- `resolution_minutes` normalization:
  - if cell is a single integer (e.g. `60`, `30`, `15`): parse as minutes
  - otherwise: set `resolution_minutes = null`

Examples treated as ambiguous (→ minutes null, raw preserved):
- `<1`
- `15-60`
- `8sec`, `1-12sec`
- `1Hz`, `15 hz`
- `d,m,y`

### Features
- `features_raw` ← `Features` (as-is, trimmed)
- `features` normalization:
  - split by comma, trim tokens
  - map tokens:
    - `E` → `load`
    - `W` → `weather`
    - `T` → `temperature`
    - `PV` → `pv`
    - `H` → `holiday`
    - `P` → `price`
    - `xW` → `extreme_weather`
  - tokens like `Undef.`, `>25`:
    - do not map; result can be empty
    - raw must be preserved

### Duration
- `duration_raw` ← `Duration` (as-is, trimmed)
- `duration_months` normalization:
  - if cell is a single integer: parse as months
  - otherwise: set `duration_months = null`

Examples treated as ambiguous:
- `<=288`
- `8-909`
- `11-23`
- `diff`
- `?`
- `20+`
- `<1`

### Time coverage
- `time_coverage_raw` ← `Spanned years` (as-is, trimmed)
- `time_coverage.start_date`, `time_coverage.end_date` normalization:
  - `YYYY-YYYY`:
    - start_date = `YYYY-01`
    - end_date = `YYYY-12`
  - `YYYY-now` / `YYYY- now`:
    - start_date = `YYYY-01`
    - end_date = null
  - `till YYYY`:
    - start_date = null
    - end_date = `YYYY-12`
  - `unknown`:
    - start_date = null
    - end_date = null
  - other formats:
    - set both to null, preserve raw

### Horizons
- Horizons cell encodes four positions: `VST ST MT LT`
- Parse icons left-to-right:
  - if position has ✔️ → include respective enum
  - if position has ❌ → do not include
- `horizons` ← list of enums (`vst`, `st`, `mt`, `lt`) in fixed order

### Regions
- `regions_raw` ← `Regions` (as-is, trimmed)
- `regions_multiple`:
  - if cell contains `✔️` → true
  - if cell contains `❌` → false
- Optional: extract count from `(N)` if present (future field `regions_count`)

### Paper linkage
- `source_paper.in_baur_2024`:
  - default false unless determined elsewhere (e.g. via override)
- `source_paper.baur_2024_usage_count`:
  - default null unless determined elsewhere (e.g. via override)

### License and citation
- Since README does not provide license/citation per dataset:
  - `license = "unknown"`
  - `citation.preferred_citation`:
    - default minimal format: `<Name>, accessed YYYY-MM-DD.`
  - `citation.bibtex = null`
- Prefer completing these via `metadata/overrides.yaml`.

---

## Overrides (recommended)
After parsing README, apply `metadata/overrides.yaml` by `dataset_id`:
- Any provided fields overwrite generated values.
- Overrides may add: `license`, full `citation`, `source_paper` flags/counts, normalized resolution/time coverage, tags, etc.
