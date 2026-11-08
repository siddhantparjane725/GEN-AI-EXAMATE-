"""Reusable record loading and query functions."""

import json
from pathlib import Path

DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "records.json"
)


def load_records(path=None):
    """Load all records from the JSON dataset."""
    data_path = Path(path) if path else DEFAULT_DATA_PATH

    with data_path.open(encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("Dataset must contain a list of records")

    return records


def search(records, keyword):
    """Case-insensitive keyword search across all fields."""
    term = keyword.strip().casefold()

    if not term:
        return records

    return [
        record for record in records
        if term in json.dumps(record, ensure_ascii=False).casefold()
    ]


def count_by(records, field="category"):
    """Count records grouped by category."""
    counts = {}

    for record in records:
        key = str(record.get(field) or "uncategorized")
        counts[key] = counts.get(key, 0) + 1

    return dict(sorted(counts.items()))


def get_by_id(records, record_id):
    """Find a record by record_id; return None if missing."""
    wanted = record_id.strip().casefold()

    return next(
        (
            record for record in records
            if str(record.get("record_id", "")).casefold() == wanted
        ),
        None
    )
