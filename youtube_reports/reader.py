"""Utilities for reading CSV data files."""

import csv
from pathlib import Path


def read_csv_files(paths: list[str]) -> list[dict]:
    """
    Read one or more CSV files and return a flat list of row dicts.

    Args:
        paths: File paths to read.

    Returns:
        Combined list of rows from all files.

    Raises:
        FileNotFoundError: If a given path does not exist.
        ValueError: If a file is empty or has no header row.
    """
    rows: list[dict] = []
    for path in paths:
        file = Path(path)
        if not file.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with file.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError(f"File is empty or has no header: {path}")
            rows.extend(reader)
    return rows
