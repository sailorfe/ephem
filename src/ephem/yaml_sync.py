# import sqlite3
# import os
import yaml
from pathlib import Path
from datetime import datetime
import re
from typing import Dict, List, Optional
from .db import get_db_path, view_charts, add_chart, create_tables


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def get_charts_dir():
    db_path = get_db_path()
    return db_path.parent / "charts"


def ensure_charts_dir():
    charts_dir = get_charts_dir()
    charts_dir.mkdir(parents=True, exist_ok=True)
    return charts_dir


def chart_to_yaml_dict(chart: Dict) -> Dict:
    yaml_dict = {
        "name": chart["name"],
        "timestamp_utc": chart["timestamp_utc"],
        "timestamp_input": chart["timestamp_input"],
    }

    if chart["latitude"] is not None and chart["longitude"] is not None:
        yaml_dict["latitude"] = chart["latitude"]
        yaml_dict["longitude"] = chart["longitude"]

    yaml_dict["_metadata"] = {
        "created": datetime.now().isoformat(),
        "source": "ephem_cli",
        "tags": [],
    }

    return yaml_dict


def yaml_dict_to_chart(yaml_dict: Dict, filename: str) -> Dict:
    name = yaml_dict.get("name", Path(filename).stem.replace("-", " ").title())

    return {
        "name": name,
        "timestamp_utc": yaml_dict["timestamp_utc"],
        "timestamp_input": yaml_dict["timestamp_input"],
        "latitude": yaml_dict.get("latitude"),
        "longitude": yaml_dict.get("longitude"),
    }


def get_yaml_filename(name: str) -> str:
    slug = slugify(name)
    if not slug:  # fallback if slugify returns empty
        slug = "unnamed-chart"
    return f"{slug}.yaml"


def export_chart_to_yaml(chart: Dict) -> Path:
    charts_dir = ensure_charts_dir()
    filename = get_yaml_filename(chart["name"])
    filepath = charts_dir / filename

    yaml_dict = chart_to_yaml_dict(chart)

    with open(filepath, "w") as f:
        yaml.dump(yaml_dict, f, default_flow_style=False, sort_keys=False)

    return filepath


def load_yaml_chart(filepath: Path) -> Optional[Dict]:
    try:
        with open(filepath, "r") as f:
            yaml_dict = yaml.safe_load(f)
        return yaml_dict_to_chart(yaml_dict, filepath.name)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def find_yaml_files() -> List[Path]:
    charts_dir = get_charts_dir()
    if not charts_dir.exists():
        return []
    return list(charts_dir.glob("*.yaml"))


def bootstrap_yaml_from_db() -> List[Path]:
    charts = view_charts()
    created_files = []

    print(f"Bootstrapping {len(charts)} YAML files from database...")

    for chart in charts:
        filepath = export_chart_to_yaml(chart)
        created_files.append(filepath)
        print(f"Created: {filepath.name}")

    return created_files


def find_chart_by_content(chart_data: Dict, db_charts: List[Dict]) -> Optional[Dict]:
    for db_chart in db_charts:
        if (
            db_chart["name"] == chart_data["name"]
            and db_chart["timestamp_utc"] == chart_data["timestamp_utc"]
            and db_chart["timestamp_input"] == chart_data["timestamp_input"]
            and db_chart["latitude"] == chart_data["latitude"]
            and db_chart["longitude"] == chart_data["longitude"]
        ):
            return db_chart
    return None


def get_file_mtime(filepath: Path) -> datetime:
    return datetime.fromtimestamp(filepath.stat().st_mtime)


def sync_yaml_to_db() -> Dict[str, List[str]]:
    results = {"added": [], "conflicts": [], "errors": []}

    yaml_files = find_yaml_files()
    db_charts = view_charts()

    print(f"Syncing {len(yaml_files)} YAML files...")

    for yaml_path in yaml_files:
        try:
            yaml_chart = load_yaml_chart(yaml_path)
            if not yaml_chart:
                continue

            # look for existing chart in DB
            existing = find_chart_by_content(yaml_chart, db_charts)
            if not existing:
                add_chart(
                    yaml_chart["name"],
                    yaml_chart["timestamp_utc"],
                    yaml_chart["timestamp_input"],
                    yaml_chart["latitude"],
                    yaml_chart["longitude"],
                )
                results["added"].append(yaml_path.name)
                print(f"Added to DB: {yaml_path.name}")
            else:
                print(f"Already in DB: {yaml_path.name}")

        except Exception as e:
            results["errors"].append(f"{yaml_path.name}: {e}")
            print(f"Error processing {yaml_path.name}: {e}")

    return results


def full_sync():
    print("💫 Syncing database...")

    create_tables()

    yaml_files = {f.stem for f in find_yaml_files()}
    db_charts = view_charts()

    missing_yamls = []
    for chart in db_charts:
        expected_filename = get_yaml_filename(chart["name"])
        expected_stem = Path(expected_filename).stem
        if expected_stem not in yaml_files:
            missing_yamls.append(chart)

    if missing_yamls:
        print(f"\nCreating YAML files for {len(missing_yamls)} database entries...")
        for chart in missing_yamls:
            export_chart_to_yaml(chart)

    # sync any YAML-only entries back to DB
    print("\nSyncing YAML files to database...")
    results = sync_yaml_to_db()

    print("\n🪐 Sync complete!")
    if results["added"]:
        print(f"Added {len(results['added'])} new entries to database")
    if results["errors"]:
        print(f"Errors: {len(results['errors'])}")
        for error in results["errors"]:
            print(f"  - {error}")


def add_chart_with_yaml(
    name: str, timestamp_utc: str, timestamp_input: str, latitude=None, longitude=None
):
    add_chart(name, timestamp_utc, timestamp_input, latitude, longitude)

    chart = {
        "name": name,
        "timestamp_utc": timestamp_utc,
        "timestamp_input": timestamp_input,
        "latitude": latitude,
        "longitude": longitude,
    }

    yaml_path = export_chart_to_yaml(chart)
    print("Saved to database (ID will be assigned)")
    print(f"Created: {yaml_path.name}")

    return yaml_path
