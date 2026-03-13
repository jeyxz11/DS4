
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional


def load_csv_to_dict(path: Path, key_field: str) -> Dict[str, Dict[str, str]]:

    path = Path(path)
    if not path.exists():
        return {}

    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row[key_field]: row for row in reader if key_field in row}


def write_dict_to_csv(
    path: Path,
    data: Dict[str, Dict[str, str]],
    fieldnames: List[str],
    sort_keys: bool = False,
) -> None:


    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        items = data.items()
        if sort_keys:
            items = sorted(items, key=lambda kv: kv[0])

        for _, row in items:
            writer.writerow(row)


def append_row_to_csv(path: Path, row: Dict[str, str], fieldnames: List[str]) -> None:

    path = Path(path)
    file_exists = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
