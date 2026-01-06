Gut. Dann ist **Schritt 1** jetzt: im Data-Repo die **Metadaten-Felder (v0.01) verbindlich festschreiben**. Das machen Sie am saubersten mit `metadata/schema.md` als kleiner Folge-PR.

Unten ist eine fertige Version zum Copy/Paste.

````md
# PADELF Metadata Schema (v0.01)

## Purpose
This document defines the minimal, reviewable metadata schema (v0.01) for publicly available electric load forecasting datasets.
The canonical metadata source is `metadata/datasets.yaml`.

## Files
- `metadata/datasets.yaml` (SSOT, human-edited)
- `metadata/schema.md` (this file)

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

## Dataset fields (v0.01)

### Required fields

* `dataset_id` (string)

  * unique identifier (slug), stable over time
* `name` (string)

  * full dataset name
* `abbreviation` (string | null)
* `type` (enum)
* `domain` (enum)
* `resolution_minutes` (int | null)
* `features` (list[enum_or_string], non-empty recommended)
* `time_coverage` (object)

  * `start_date` (string, ISO)
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

### Optional fields (schema-ready, not required in v0.01)

* `geo` (object)

  * `country` (string | null)
  * `continent` (string | null)
  * `tz` (string | null, e.g. `Europe/Berlin`)
* `granularity` (string | null) — e.g. `household`, `building`, `substation`, `national`
* `data_format` (list[string] | null) — e.g. `csv`, `xlsx`, `api`, `zip`
* `tags` (list[string] | null)

---

## Enums (v0.01)

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
  resolution_minutes: 60
  features: [load]
  time_coverage:
    start_date: "2010-01"
    end_date: "2012-12"
  duration_months: 36
  horizons: [st, mt]
  regions_multiple: false
  access:
    url: "https://example.org/dataset"
    access_notes: "Direct download"
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
* If `resolution_minutes` is unknown, set it to `null` and explain in `access.access_notes` or future `notes` field.
