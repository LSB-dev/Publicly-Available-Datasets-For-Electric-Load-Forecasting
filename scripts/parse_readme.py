#!/usr/bin/env python3
"""
Deterministic parser for README.md table -> metadata/datasets.yaml

Design principles:
- 100% reproducible output
- Strict rule-based parsing (minimal intelligence)
- Header-based column mapping
- Preserve raw values, normalize only when unambiguous
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


# ============================================================================
# CONFIGURATION
# ============================================================================

# Icon mappings for Type column
TYPE_ICON_MAP = {
    "📦": "collection",
    "📁": "file_archive",
    "🌐": "platform_api",
}

# Domain mappings
DOMAIN_MAP = {
    "S": "system",
    "R": "residential",
    "I": "industrial",
    "?": "unknown",
}

# Feature code mappings
FEATURE_MAP = {
    "E": "load",
    "W": "weather",
    "xW": "extreme_weather",
    "T": "temperature",
    "PV": "pv",
    "H": "holiday",
    "P": "price",
}

# Horizon checkmark positions (VST, ST, MT, LT)
HORIZON_MAP = ["vst", "st", "mt", "lt"]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def slugify(text: str) -> str:
    """Convert text to valid dataset_id slug (lowercase, alphanumeric, underscores, hyphens)."""
    # Remove HTML tags like <sup>9</sup>
    text = re.sub(r"<[^>]+>", "", text)
    # Convert to lowercase
    text = text.lower().strip()
    # Replace spaces and special chars with underscore
    text = re.sub(r"[^a-z0-9_-]+", "_", text)
    # Remove leading/trailing underscores
    text = text.strip("_")
    return text


def extract_links(cell: str) -> List[str]:
    """Extract all URLs from markdown links in a cell."""
    # Pattern: [text](url)
    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, cell)
    return [url for _, url in matches]


def parse_checkmarks(cell: str) -> List[str]:
    """
    Parse checkmark sequence for horizons.
    Expected format: 4 checkmarks/crosses (✔️/❌) mapping to [vst, st, mt, lt]
    """
    # Remove VARIATION SELECTOR-16 to normalize emoji
    # ✔️ is actually ✔ (U+2714) + ️ (U+FE0F), but we want to treat it as a single character
    cell = cell.replace("\ufe0f", "")
    
    # Extract marks (should now be clean ✔ and ❌)
    marks = list(cell)
    # Filter to only checkmarks and crosses
    marks = [m for m in marks if m in ("✔", "❌")]
    
    if len(marks) != 4:
        # Non-standard format, cannot reliably parse
        return []
    
    horizons = []
    for i, mark in enumerate(marks):
        if mark == "✔":
            horizons.append(HORIZON_MAP[i])
    
    return horizons


def parse_domain(cell: str) -> tuple[Optional[str], str]:
    """
    Parse domain cell. Returns (normalized_domain, raw_domain).
    If multiple domains or ambiguous, return (None, raw).
    """
    raw = cell.strip()
    
    # Check if it's a single, clear domain
    if raw in DOMAIN_MAP:
        return DOMAIN_MAP[raw], raw
    
    # Multiple domains (e.g., "S, R") - cannot normalize uniquely
    if "," in raw:
        # Try to pick the first one as primary? No, user said be conservative.
        return None, raw
    
    # Ambiguous
    return DOMAIN_MAP.get(raw, None), raw


def parse_resolution(cell: str) -> tuple[Optional[int], str]:
    """
    Parse resolution cell. Returns (resolution_minutes, raw).
    Only normalize if it's a simple integer.
    """
    raw = cell.strip()
    
    # Try to parse as integer
    try:
        minutes = int(raw)
        return minutes, raw
    except ValueError:
        pass
    
    # Special cases that can be normalized
    if raw == "8sec":
        return None, raw  # Less than 1 minute, keep raw
    if raw == "15 hz":
        return None, raw  # Frequency, not minutes
    if raw == "<1":
        return None, raw
    
    # Complex format (e.g., "d,m,y", "1-15", "15-60")
    return None, raw


def parse_features(cell: str, dataset_id: str = "") -> tuple[List[str], str]:
    """
    Parse features cell. Returns (normalized_features, raw).
    Tokenize by comma and map known codes.
    """
    raw = cell.strip()

    if raw in ["Undef.", ">25", "?"]:
        return [], raw

    # Split by comma
    tokens = [t.strip() for t in raw.split(",")]

    normalized = []
    for token in tokens:
        if token in FEATURE_MAP:
            normalized.append(FEATURE_MAP[token])
        elif token:
            print(f"Warning: Unknown feature code '{token}' in dataset {dataset_id}", file=sys.stderr)

    return normalized, raw


def parse_duration(cell: str) -> tuple[Optional[int], str]:
    """
    Parse duration cell. Returns (duration_months, raw).
    Only normalize if it's a simple integer.
    """
    raw = cell.strip()
    
    # Try to parse as integer
    try:
        months = int(raw)
        return months, raw
    except ValueError:
        pass
    
    # Complex formats (e.g., "8-909", "<=288", "diff", "?")
    return None, raw


def parse_time_coverage(cell: str) -> tuple[Dict[str, Optional[str]], str]:
    """
    Parse time coverage (spanned years) cell.
    Returns (time_coverage_dict, raw).
    """
    raw = cell.strip()
    
    # Pattern: YYYY-YYYY
    match = re.match(r"^(\d{4})-(\d{4})$", raw)
    if match:
        start_year, end_year = match.groups()
        return {
            "start_date": f"{start_year}-01",
            "end_date": f"{end_year}-12",
        }, raw
    
    # Pattern: YYYY (single year)
    match = re.match(r"^(\d{4})$", raw)
    if match:
        year = match.group(1)
        return {
            "start_date": f"{year}-01",
            "end_date": f"{year}-12",
        }, raw
    
    # Pattern: "till YYYY"
    match = re.search(r"till (\d{4})", raw)
    if match:
        end_year = match.group(1)
        return {
            "start_date": None,
            "end_date": f"{end_year}-12",
        }, raw
    
    # Pattern: "YYYY-now" or "YYYY- now"
    match = re.match(r"^(\d{4})-\s*now$", raw)
    if match:
        start_year = match.group(1)
        return {
            "start_date": f"{start_year}-01",
            "end_date": None,
        }, raw
    
    # Ambiguous/unknown
    return {
        "start_date": None,
        "end_date": None,
    }, raw


def parse_regions(cell: str) -> tuple[bool, str]:
    """
    Parse regions cell. Returns (regions_multiple, raw).
    """
    raw = cell.strip()
    
    # Contains ✔️ = multiple regions
    if "✔️" in raw or "✔" in raw:
        return True, raw
    else:
        return False, raw


# ============================================================================
# TABLE PARSING
# ============================================================================

def parse_markdown_table(readme_content: str) -> List[Dict[str, Any]]:
    """
    Parse the markdown table from README.md and return list of dataset dicts.
    """
    lines = readme_content.splitlines()
    
    # Find table start
    table_start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("# The list"):
            table_start_idx = i
            break
    
    if table_start_idx is None:
        raise ValueError("Could not find '# The list' section in README.md")
    
    # Find header row (starts with | ID)
    header_idx = None
    for i in range(table_start_idx, len(lines)):
        if lines[i].strip().startswith("| ID"):
            header_idx = i
            break
    
    if header_idx is None:
        raise ValueError("Could not find table header")
    
    # Parse header to get column names
    header_line = lines[header_idx]
    # Skip separator line
    separator_idx = header_idx + 1
    
    # Extract column names from header
    # Expected: | ID | Abbrev | Name | Domain | Resolution | Features | Duration | Spanned years | Horizons | Regions | Type | Links | Access |
    header_cells = [cell.strip() for cell in header_line.split("|")]
    header_cells = [cell for cell in header_cells if cell]  # Remove empty
    
    # Remove superscript footnote markers (e.g., "Domain<sup>1</sup>" -> "Domain")
    header_cells = [re.sub(r"<sup>\d+</sup>", "", cell).strip() for cell in header_cells]

    
    # Start parsing data rows (after separator)
    datasets = []
    for i in range(separator_idx + 1, len(lines)):
        line = lines[i].strip()
        
        # Stop at empty line or next section
        if not line or line.startswith("#"):
            break
        
        # Skip if not a table row
        if not line.startswith("|"):
            continue
        
        # Parse row
        cells = [cell.strip() for cell in line.split("|")]
        cells = [cell for cell in cells if cell]  # Remove empty from edges
        
        # Verify column count (should match header)
        if len(cells) != len(header_cells):
            print(f"Warning: Row {i+1} has {len(cells)} cells, expected {len(header_cells)}. Skipping.", file=sys.stderr)
            continue
        
        # Map cells to a dict
        row = dict(zip(header_cells, cells))
        
        # Parse the row
        dataset = parse_row(row)
        datasets.append(dataset)

    # Check for duplicate dataset_ids
    seen_ids: Dict[str, int] = {}
    for dataset in datasets:
        did = dataset["dataset_id"]
        if did in seen_ids:
            print(f"Warning: Duplicate dataset_id '{did}' (rows {seen_ids[did]} and {dataset['name']})", file=sys.stderr)
        else:
            seen_ids[did] = dataset["name"]

    return datasets


def parse_row(row: Dict[str, str]) -> Dict[str, Any]:
    """
    Parse a single table row into a dataset dict.
    """
    # Extract basic fields
    id_raw = row["ID"]
    abbrev = row["Abbrev"]
    name = row["Name"]

    # Generate dataset_id
    if abbrev and abbrev.strip():
        dataset_id = slugify(abbrev)
    else:
        dataset_id = slugify(id_raw)

    # Derive in_baur_2024: datasets WITHOUT <sup>9</sup> are from the original paper
    in_baur_2024 = "<sup>9</sup>" not in id_raw

    # Type (from icon)
    type_icon = row["Type"]
    dataset_type = TYPE_ICON_MAP.get(type_icon.strip(), None)
    if dataset_type is None:
        print(f"Warning: Unknown type icon '{type_icon}' for dataset {dataset_id}", file=sys.stderr)
        dataset_type = "unknown"

    # Domain
    domain, domain_raw = parse_domain(row["Domain"])
    if domain is None:
        print(f"Warning: Unmapped domain code '{domain_raw}' for dataset {dataset_id}, using 'unknown'", file=sys.stderr)
        domain = "unknown"

    # Resolution
    resolution_minutes, resolution_raw = parse_resolution(row["Resolution"])

    # Features
    features, features_raw = parse_features(row["Features"], dataset_id=dataset_id)

    # Duration
    duration_months, duration_raw = parse_duration(row["Duration"])

    # Time coverage
    time_coverage, time_coverage_raw = parse_time_coverage(row["Spanned years"])

    # Horizons
    horizons = parse_checkmarks(row["Horizons"])

    # Regions
    regions_multiple, regions_raw = parse_regions(row["Regions"])

    # Links
    links = extract_links(row["Links"])

    # Access URL: always use first link if available
    access_url = links[0] if links else ""

    # Access notes
    access_notes_parts = []
    if len(links) > 1:
        access_notes_parts.append(f"{len(links)} links available, see links field")
    elif len(links) == 0:
        access_notes_parts.append("No direct link available")

    access_type_icon = row.get("Access", "").strip()
    if access_type_icon == "🔓":
        if not access_notes_parts:
            access_notes_parts.append("Open access")
    elif access_type_icon == "📧":
        access_notes_parts.append("Registration or request required")

    access_notes = "; ".join(access_notes_parts)

    # Abbreviation (nullable)
    abbreviation = abbrev.strip() if abbrev.strip() else None

    # Build dataset object
    dataset = {
        "dataset_id": dataset_id,
        "name": name.strip(),
        "abbreviation": abbreviation,
        "type": dataset_type,
        "domain": domain,
        "domain_raw": domain_raw,
        "resolution_minutes": resolution_minutes,
        "resolution_raw": resolution_raw,
        "features": features,
        "features_raw": features_raw,
        "time_coverage": time_coverage,
        "time_coverage_raw": time_coverage_raw,
        "duration_months": duration_months,
        "duration_raw": duration_raw,
        "horizons": horizons,
        "regions_multiple": regions_multiple,
        "regions_raw": regions_raw,
        "access": {
            "url": access_url,
            "access_notes": access_notes,
        },
        "links": links,
        "license": "unknown",
        "citation": {
            "preferred_citation": "",
            "bibtex": None,
        },
        "source_paper": {
            "in_baur_2024": in_baur_2024,
            "baur_2024_usage_count": None,
        },
    }

    return dataset


# ============================================================================
# YAML OUTPUT
# ============================================================================

class NoAliasDumper(yaml.SafeDumper):
    """Custom YAML dumper to disable aliases and preserve key order."""
    def ignore_aliases(self, data):
        return True


def write_yaml(datasets: List[Dict[str, Any]], output_path: Path) -> None:
    """
    Write datasets to YAML file with consistent formatting.
    """
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(
            datasets,
            f,
            Dumper=NoAliasDumper,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )


# ============================================================================
# MAIN
# ============================================================================

def apply_overrides(datasets: List[Dict[str, Any]], overrides_path: Path) -> List[Dict[str, Any]]:
    """
    Merge optional overrides into parsed datasets.
    Overrides are keyed by dataset_id and do a shallow dict update.
    """
    if not overrides_path.exists():
        return datasets

    with overrides_path.open(encoding="utf-8") as f:
        overrides = yaml.safe_load(f)

    if not overrides:
        return datasets

    # Build lookup by dataset_id
    overrides_by_id = {}
    for dataset_id, fields in overrides.items():
        if isinstance(fields, dict):
            overrides_by_id[dataset_id] = fields
        else:
            print(f"Warning: Override for '{dataset_id}' is not a dict, skipping.", file=sys.stderr)

    applied = 0
    for dataset in datasets:
        did = dataset["dataset_id"]
        if did in overrides_by_id:
            dataset.update(overrides_by_id[did])
            applied += 1

    unused = set(overrides_by_id) - {d["dataset_id"] for d in datasets}
    for uid in sorted(unused):
        print(f"Warning: Override for '{uid}' does not match any dataset_id.", file=sys.stderr)

    if applied:
        print(f"Applied overrides to {applied} dataset(s).")

    return datasets


def main():
    """Main entry point."""
    # Paths
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"
    overrides_path = repo_root / "metadata" / "overrides.yaml"
    output_path = repo_root / "metadata" / "datasets.yaml"

    # Read README
    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}", file=sys.stderr)
        sys.exit(1)

    readme_content = readme_path.read_text(encoding="utf-8")

    # Parse table
    print(f"Parsing README table from {readme_path}...")
    datasets = parse_markdown_table(readme_content)
    print(f"Parsed {len(datasets)} datasets.")

    # Apply overrides
    datasets = apply_overrides(datasets, overrides_path)

    # Write YAML
    print(f"Writing to {output_path}...")
    write_yaml(datasets, output_path)
    print("Done.")


if __name__ == "__main__":
    main()
