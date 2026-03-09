#!/usr/bin/env python3
"""
Pytest tests for the README parser.

Tests verify:
- Parser runs without errors
- Generated dataset IDs are valid
- Horizons are correctly mapped from checkmark sequences
- Schema compliance with Dashboard's Pydantic model
"""

import sys
from pathlib import Path

import pytest
import yaml

# Add scripts directory to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from parse_readme import (
    parse_checkmarks,
    parse_domain,
    parse_features,
    parse_markdown_table,
    parse_resolution,
    parse_time_coverage,
    slugify,
)


# ============================================================================
# UNIT TESTS FOR UTILITY FUNCTIONS
# ============================================================================

def test_slugify():
    """Test slugify function."""
    assert slugify("ISO-NE") == "iso-ne"
    assert slugify("NYISO") == "nyiso"
    assert slugify("PJM") == "pjm"
    assert slugify("BDG-Proj2") == "bdg-proj2"


def test_parse_checkmarks():
    """Test horizon checkmark parsing."""
    # VST, ST, MT, LT = ✔, ✔, ✔, ✔ = 4 checks
    assert parse_checkmarks("✔️✔️✔️✔️") == ["vst", "st", "mt", "lt"]
    
    # ST, MT = ❌, ✔, ✔, ❌
    assert parse_checkmarks("❌✔️✔️❌") == ["st", "mt"]
    
    # All crosses
    assert parse_checkmarks("❌❌❌❌") == []
    
    # Invalid length (not 4)
    assert parse_checkmarks("✔️✔️") == []


def test_parse_domain():
    """Test domain parsing."""
    assert parse_domain("S") == ("system", "S")
    assert parse_domain("R") == ("residential", "R")
    assert parse_domain("I") == ("industrial", "I")
    assert parse_domain("?") == ("unknown", "?")
    
    # Multiple domains - cannot normalize
    assert parse_domain("S, R") == (None, "S, R")


def test_parse_resolution():
    """Test resolution parsing."""
    assert parse_resolution("60") == (60, "60")
    assert parse_resolution("30") == (30, "30")
    assert parse_resolution("5") == (5, "5")
    
    # Complex formats - cannot normalize
    assert parse_resolution("d,m,y") == (None, "d,m,y")
    assert parse_resolution("15-60") == (None, "15-60")
    assert parse_resolution("<1") == (None, "<1")


def test_parse_features():
    """Test feature parsing."""
    features, raw = parse_features("E")
    assert features == ["load"]
    assert raw == "E"
    
    features, raw = parse_features("E, W, T, PV")
    assert set(features) == {"load", "weather", "temperature", "pv"}
    
    features, raw = parse_features("Undef.")
    assert features == []
    assert raw == "Undef."


def test_parse_time_coverage():
    """Test time coverage parsing."""
    # Year range
    tc, raw = parse_time_coverage("2003-2014")
    assert tc["start_date"] == "2003-01"
    assert tc["end_date"] == "2014-12"
    
    # Single year
    tc, raw = parse_time_coverage("2021")
    assert tc["start_date"] == "2021-01"
    assert tc["end_date"] == "2021-12"
    
    # Till year
    tc, raw = parse_time_coverage("till 2015")
    assert tc["start_date"] is None
    assert tc["end_date"] == "2015-12"
    
    # Ongoing (YYYY-now)
    tc, raw = parse_time_coverage("2003-now")
    assert tc["start_date"] == "2003-01"
    assert tc["end_date"] is None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.fixture
def readme_content():
    """Load README.md content."""
    readme_path = Path(__file__).parent.parent / "README.md"
    return readme_path.read_text(encoding="utf-8")


@pytest.fixture
def generated_datasets():
    """Load generated datasets.yaml."""
    yaml_path = Path(__file__).parent.parent / "metadata" / "datasets.yaml"
    with yaml_path.open() as f:
        return yaml.safe_load(f)


def test_parsing_robustness(readme_content):
    """Test that parser runs without crashes on current README."""
    datasets = parse_markdown_table(readme_content)
    assert len(datasets) >= 40  # Sanity lower bound


def test_id_generation(generated_datasets):
    """Test that all dataset IDs are valid slugs."""
    import re
    pattern = re.compile(r"^[a-z0-9_-]+$")
    
    for dataset in generated_datasets:
        dataset_id = dataset["dataset_id"]
        assert pattern.match(dataset_id), f"Invalid dataset_id: {dataset_id}"


def test_horizons_mapping(generated_datasets):
    """Test that horizons are correctly parsed from checkmarks."""
    # Check that at least some datasets have horizons
    datasets_with_horizons = [d for d in generated_datasets if d["horizons"]]
    assert len(datasets_with_horizons) > 0, "No datasets have horizons parsed"
    
    # Valid horizon values
    valid_horizons = {"vst", "st", "mt", "lt"}
    
    for dataset in generated_datasets:
        for horizon in dataset["horizons"]:
            assert horizon in valid_horizons, f"Invalid horizon: {horizon}"


def test_schema_compliance(generated_datasets):
    """Test that generated datasets comply with basic schema requirements."""
    required_fields = [
        "dataset_id",
        "name",
        "type",
        "domain",
        "features",
        "time_coverage",
        "horizons",
        "regions_multiple",
        "access",
        "license",
        "citation",
        "source_paper",
    ]
    
    for dataset in generated_datasets:
        for field in required_fields:
            assert field in dataset, f"Missing field '{field}' in dataset {dataset.get('dataset_id', '?')}"
        
        # Check nested structures
        assert "start_date" in dataset["time_coverage"]
        assert "end_date" in dataset["time_coverage"]
        assert "url" in dataset["access"]
        assert "access_notes" in dataset["access"]
        assert "preferred_citation" in dataset["citation"]
        assert "in_baur_2024" in dataset["source_paper"]


def test_raw_fields_preserved(generated_datasets):
    """Test that raw fields are preserved when normalization is ambiguous."""
    # Find a dataset with complex resolution
    for dataset in generated_datasets:
        if dataset["resolution_raw"] == "d,m,y":
            assert dataset["resolution_minutes"] is None
            break
    else:
        pytest.skip("No dataset with complex resolution found")


def test_no_duplicate_ids(readme_content):
    """Test that no two datasets produce the same dataset_id."""
    datasets = parse_markdown_table(readme_content)
    ids = [d["dataset_id"] for d in datasets]
    duplicates = [did for did in ids if ids.count(did) > 1]
    assert not duplicates, f"Duplicate dataset_ids: {set(duplicates)}"


def test_in_baur_2024_derived(readme_content):
    """Test that in_baur_2024 is correctly derived from README footnote markers."""
    datasets = parse_markdown_table(readme_content)
    # ISO-NE (ID=1, no <sup>9</sup>) should be in original paper
    iso_ne = next(d for d in datasets if d["dataset_id"] == "iso-ne")
    assert iso_ne["source_paper"]["in_baur_2024"] is True

    # EWELD (ID=29<sup>9</sup>) should NOT be in original paper
    eweld = next(d for d in datasets if d["dataset_id"] == "eweld")
    assert eweld["source_paper"]["in_baur_2024"] is False


def test_round_trip_reproducibility(readme_content):
    """Test that re-parsing README produces the same output as checked-in datasets.yaml."""
    yaml_path = Path(__file__).parent.parent / "metadata" / "datasets.yaml"
    if not yaml_path.exists():
        pytest.skip("datasets.yaml not found")

    with yaml_path.open() as f:
        existing = yaml.safe_load(f)

    freshly_parsed = parse_markdown_table(readme_content)

    assert len(freshly_parsed) == len(existing), (
        f"Dataset count mismatch: parsed {len(freshly_parsed)}, existing {len(existing)}"
    )

    for parsed, saved in zip(freshly_parsed, existing):
        assert parsed["dataset_id"] == saved["dataset_id"], (
            f"dataset_id mismatch at position: {parsed['dataset_id']} vs {saved['dataset_id']}"
        )
        assert parsed == saved, (
            f"Mismatch for dataset '{parsed['dataset_id']}': re-run scripts/parse_readme.py to regenerate"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
