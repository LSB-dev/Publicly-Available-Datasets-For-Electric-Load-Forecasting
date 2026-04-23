## How To
You have a dataset that is not on the list yet, but you want to add it?

There are two options:
(1) *preferred*: if you're familiar with git, try to add it to the list yourself and open a pull request to merge. (see tutorial below)
(2) if you have no expertise: [create a new post](https://github.com/LSB-dev/Publicly-Available-Datasets-For-Electric-Load-Forecasting/issues) to let us know, and we add it

## For Developers & Contributors

### Repository Structure

```
.
├── README.md                  # Authoritative dataset table (this file)
├── Images/                    # Header and footer images
├── metadata/
│   ├── datasets.yaml          # Parser output (auto-generated, committed)
│   ├── datasets_full.yaml     # Merged output (consumed by Dashboard)
│   ├── overrides.yaml         # Manual overrides (license, preferred_citation, bibtex only)
│   ├── datasets_template.yaml # Template for reference
│   ├── schema.md              # Schema documentation
│   └── README_datasets_mapping.md  # Column mapping reference
├── scripts/
│   ├── parse_readme.py        # Parser: README table → datasets.yaml
│   ├── merge_datasets.py      # Merges datasets.yaml + overrides.yaml → datasets_full.yaml
│   └── validates_datasets.py  # Pydantic schema validation
└── tests/
  └── test_parse_readme.py   # Parser unit tests
```

### How the Pipeline Works

The README table above is the single source of truth (SSOT) for all dataset metadata. `scripts/parse_readme.py` parses the Markdown table and produces `metadata/datasets.yaml`. `scripts/merge_datasets.py` merges `datasets.yaml` with `metadata/overrides.yaml` to produce `metadata/datasets_full.yaml`; the overrides file is strictly scoped to three fields: `license`, `preferred_citation`, and `bibtex`, and no other fields may be added to overrides. `scripts/validates_datasets.py` validates `datasets_full.yaml` against a Pydantic schema. The CI pipeline (GitHub Actions) runs on every push to `main` and performs a drift-check that re-runs the parser and diffs the output against the committed `datasets.yaml`, and also performs Pydantic validation of `datasets_full.yaml`. The PADELF Dashboard (separate repo: https://github.com/LSB-dev/PADELF-Dashboard) consumes `datasets_full.yaml` as its sole data source.

```
README.md (table)
    │
    ▼
  parse_readme.py
    │
    ▼
  datasets.yaml ──► merge_datasets.py ◄── overrides.yaml
              │
              ▼
          datasets_full.yaml ──► validates_datasets.py
              │
              ▼
          PADELF Dashboard (separate repo)
```

### How to Add a New Dataset

1. Add a new row to the dataset table in this `README.md`, following the exact column format of existing rows. Assign the next available ID.
2. Run the parser locally to verify: `python scripts/parse_readme.py`
3. Check the output in `metadata/datasets.yaml` -- your new entry should appear.
4. Run the merge script: `python scripts/merge_datasets.py`
5. If you have license, citation, or BibTeX information for the dataset, add an entry to `metadata/overrides.yaml` using the dataset abbreviation as key. Only three fields are allowed: `license`, `preferred_citation`, `bibtex`.
6. Run validation: `python scripts/validates_datasets.py`
7. Commit all changed files (`README.md`, `metadata/datasets.yaml`, `metadata/datasets_full.yaml`, and optionally `metadata/overrides.yaml`).
8. Open a pull request. CI will re-run the pipeline and validate automatically.

### overrides.yaml Scope

`overrides.yaml` is strictly limited to three fields per dataset entry: `license`, `preferred_citation`, and `bibtex`. All other metadata must be parseable from the README table. This constraint ensures the README remains the single source of truth and overrides only supplement information that cannot be expressed in the table format.
