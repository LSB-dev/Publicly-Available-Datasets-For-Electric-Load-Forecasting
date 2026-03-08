#!/usr/bin/env python3
"""
Validate metadata/datasets.yaml against Pydantic models.
Exits with code 1 if validation fails.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, ValidationError, field_validator


# ============================================================================
# MODELS
# ============================================================================

class AccessModel(BaseModel):
    url: str
    access_notes: str


class TimeCoverageModel(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CitationModel(BaseModel):
    preferred_citation: str
    bibtex: Optional[str] = None


class SourcePaperModel(BaseModel):
    in_baur_2024: bool
    baur_2024_usage_count: Optional[int] = None


class DatasetModel(BaseModel):
    dataset_id: str
    name: str
    abbreviation: Optional[str] = None
    type: str
    domain: str
    domain_raw: str
    resolution_minutes: Optional[int] = None
    resolution_raw: str
    features: List[str]
    features_raw: str
    time_coverage: TimeCoverageModel
    time_coverage_raw: str
    duration_months: Optional[int] = None
    duration_raw: str
    horizons: List[str]
    regions_multiple: bool
    regions_raw: str
    access: AccessModel
    links: List[str]
    license: str
    citation: CitationModel
    source_paper: SourcePaperModel

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = {"collection", "file_archive", "platform_api", "unknown"}
        if v not in allowed:
            raise ValueError(f"Invalid type '{v}'. Must be one of {allowed}")
        return v

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, v: str) -> str:
        allowed = {"system", "residential", "industrial", "unknown"}
        if v not in allowed:
            raise ValueError(f"Invalid domain '{v}'. Must be one of {allowed}")
        return v

    @field_validator("horizons")
    @classmethod
    def validate_horizons(cls, v: List[str]) -> List[str]:
        allowed = {"vst", "st", "mt", "lt"}
        for h in v:
            if h not in allowed:
                raise ValueError(f"Invalid horizon '{h}'. Must be one of {allowed}")
        return v

    @field_validator("dataset_id")
    @classmethod
    def validate_dataset_id(cls, v: str) -> str:
        import re
        if not re.match(r"^[a-z0-9_-]+$", v):
            raise ValueError(f"dataset_id '{v}' contains invalid characters")
        return v


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    repo_root = Path(__file__).parent.parent
    yaml_path = repo_root / "metadata" / "datasets.yaml"

    if not yaml_path.exists():
        print(f"Error: {yaml_path} not found.", file=sys.stderr)
        sys.exit(1)

    raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        print("Error: datasets.yaml must be a YAML list.", file=sys.stderr)
        sys.exit(1)

    errors = []
    for i, entry in enumerate(raw):
        try:
            DatasetModel(**entry)
        except ValidationError as e:
            dataset_id = entry.get("dataset_id", f"<entry {i}>")
            errors.append(f"Dataset '{dataset_id}':\n{e}")

    if errors:
        print(f"Validation failed: {len(errors)} error(s) found.\n", file=sys.stderr)
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    print(f"Validation passed: {len(raw)} datasets validated successfully.")


if __name__ == "__main__":
    main()