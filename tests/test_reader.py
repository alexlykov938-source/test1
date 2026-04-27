"""Tests for the CSV reader utility."""

import textwrap
from pathlib import Path

import pytest

from youtube_reports.reader import read_csv_files


@pytest.fixture()
def csv_file(tmp_path: Path):
    """Factory fixture: returns a function that creates a named CSV file."""
    def _make(name: str, content: str) -> Path:
        f = tmp_path / name
        f.write_text(textwrap.dedent(content), encoding="utf-8")
        return f
    return _make


def test_read_single_file(csv_file):
    f = csv_file("a.csv", """\
        title,ctr,retention_rate
        Video A,20.0,30
        Video B,10.0,80
    """)
    rows = read_csv_files([str(f)])
    assert len(rows) == 2
    assert rows[0]["title"] == "Video A"
    assert rows[1]["ctr"] == "10.0"


def test_read_multiple_files(csv_file):
    f1 = csv_file("a.csv", "title,ctr,retention_rate\nVideo A,20.0,30\n")
    f2 = csv_file("b.csv", "title,ctr,retention_rate\nVideo B,10.0,80\n")
    rows = read_csv_files([str(f1), str(f2)])
    assert len(rows) == 2
    titles = [r["title"] for r in rows]
    assert "Video A" in titles
    assert "Video B" in titles


def test_file_not_found():
    with pytest.raises(FileNotFoundError, match="does_not_exist.csv"):
        read_csv_files(["does_not_exist.csv"])


def test_empty_file_raises(tmp_path: Path):
    f = tmp_path / "empty.csv"
    f.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="empty or has no header"):
        read_csv_files([str(f)])
