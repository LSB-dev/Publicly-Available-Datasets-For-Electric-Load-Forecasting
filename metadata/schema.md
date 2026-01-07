
# PADELF Metadata Schema 

## Purpose
This document defines the metadata schema for publicly available electric load forecasting datasets.
The schema is designed to support both human-readable curation (README table) and machine-readable consumption (generated YAML for dashboards/tools).

## Files
- `README.md` (SSOT, human-edited; dataset table is the canonical source)
- `metadata/overrides.yaml` (optional; manual overrides/completions for fields not reliably derivable from README)
- `metadata/datasets.yaml` (generated artifact; do not edit by hand)
- `metadata/schema.md` (this file)

## Generation rule
`metadata/datasets.yaml` is generated from the dataset table in `README.md` plus optional `metadata/overrides.yaml`.
Manual edits to `metadata/datasets.yaml` will be overwritten by the generator.

## General conventions
- `dataset_id` is stable and unique; allowed pattern: `^[a-z0-9_]+$`
- Dates are ISO strings:
  - `"YYYY-MM"` if only month is known
  - `"YYYY-MM-DD"` if exact date is known
- `null` is allowed where explicitly stated as nullable.
- Lists must be YAML sequences (e.g., `[load, weather]`).

## Top-level object
`datasets.yaml` is a YAML list. Each list item is one dataset object.

An empty list is valid:
```yaml
[]
````

---

## Dataset fields (v0.02)

### Required fields

* `dataset_id` (string)

  * unique identifier (slug), stable over time
* `name` (string)

  * full dataset name
* `abbreviation` (string | null)
* `type` (enum)
* `domain` (enum)
* `resolution_minutes` (int | null)
* `features` (list[string], can be empty if unknown)
* `time_coverage` (object)

  * `start_date` (string, ISO | null)
  * `end_date` (string, ISO | null)
* `duration_months` (int | null)
* `horizons` (list[enum], can be empty if unknown)
* `regions_multiple` (bool)
* `access` (object)

  * `url` (string)
  * `access_notes` (string)
* `license` (string)

  * use `"unknown"` if not known
* `citation` (object)

  * `preferred_citation` (string)
  * `bibtex` (string | null)
* `source_paper` (object)

  * `in_baur_2024` (bool)
  * `baur_2024_usage_count` (int | null)

### Optional fields (recommended for robust generation)

These fields preserve original values from README when normalization is ambiguous.

* `domain_raw` (string | null) — original domain cell (e.g., `S, R`, `?`)
* `resolution_raw` (string | null) — original resolution cell (e.g., `8sec`, `15-60`, `d,m,y`, `<1`)
* `features_raw` (string | null) — original features cell (e.g., `E, W, T, PV`, `Undef.`, `>25`)
* `duration_raw` (string | null) — original duration cell (e.g., `8-909`, `<=288`, `diff`, `?`)
* `time_coverage_raw` (string | null) — original spanned years cell (e.g., `till 2015`, `2013-now`, `unknown`)
* `regions_raw` (string | null) — original regions cell (e.g., `✔️ (386)`, `❌`)
* `links` (list[string] | null) — all extracted URLs from the README links cell (first URL should also be used as `access.url`)
* `tags` (list[string] | null)

### Optional fields (schema-ready, not required)

* `geo` (object)

  * `country` (string | null)
  * `continent` (string | null)
  * `tz` (string | null, e.g. `Europe/Berlin`)
* `granularity` (string | null) — e.g. `household`, `building`, `substation`, `national`
* `data_format` (list[string] | null) — e.g. `csv`, `xlsx`, `api`, `zip`

---

## Enums

### type

* `collection` — multiple files/sources grouped (often per region or per year)
* `file_archive` — downloadable archive(s), e.g. ZIP/CSV bundles
* `platform_api` — data accessed via API/platform endpoints

### domain

* `system`
* `residential`
* `industrial`
* `unknown`

### horizons

* `vst` — very short-term
* `st` — short-term
* `mt` — mid-term
* `lt` — long-term

---

## Minimal example (illustrative)

```yaml
- dataset_id: example_dataset
  name: Example Load Dataset
  abbreviation: null
  type: file_archive
  domain: system
  domain_raw: "S"
  resolution_minutes: 60
  resolution_raw: "60"
  features: [load]
  features_raw: "E"
  time_coverage:
    start_date: "2010-01"
    end_date: "2012-12"
  time_coverage_raw: "2010-2012"
  duration_months: 36
  duration_raw: "36"
  horizons: [st, mt]
  regions_multiple: false
  regions_raw: "❌"
  access:
    url: "https://example.org/dataset"
    access_notes: "Direct download"
  links: ["https://example.org/dataset"]
  license: unknown
  citation:
    preferred_citation: "Example Org, Example Load Dataset, accessed YYYY-MM-DD."
    bibtex: null
  source_paper:
    in_baur_2024: false
    baur_2024_usage_count: null
```

## Validation notes (recommended)

* If `end_date` is `null`, dataset is considered ongoing.
* If a value is ambiguous (resolution, duration, spanned years), set the normalized field to `null` and store the original value in the corresponding `*_raw` field.


