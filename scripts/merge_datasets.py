import yaml
from pathlib import Path

BASE_PATH = Path("metadata/datasets.yaml")
OVERRIDES_PATH = Path("metadata/overrides.yaml")
OUTPUT_PATH = Path("metadata/datasets_full.yaml")

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    base = load_yaml(BASE_PATH)
    overrides = load_yaml(OVERRIDES_PATH)
    merged = []
    license_overridden = 0
    citation_overridden = 0

    for entry in base:
        ds_id = entry.get("dataset_id")
        override = overrides.get(ds_id, {})
        # Merge license
        if "license" in override and override["license"] not in (None, ""):
            entry["license"] = override["license"]
            license_overridden += 1
        # Merge citation
        if "citation" in override:
            citation = override["citation"]
            if citation:
                for k, v in citation.items():
                    if v not in (None, ""):
                        entry.setdefault("citation", {})[k] = v
                        citation_overridden += 1
        merged.append(entry)

    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(merged, f, sort_keys=False, allow_unicode=True)

    print(f"Total datasets: {len(base)}")
    print(f"License overridden: {license_overridden}")
    print(f"Citation overridden: {citation_overridden}")

if __name__ == "__main__":
    main()
