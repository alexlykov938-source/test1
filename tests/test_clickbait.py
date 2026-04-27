"""Tests for the clickbait report."""

import pytest

from youtube_reports.reports.clickbait import ClickbaitReport

ROWS = [
    {"title": "Clickbait King",        "ctr": "25.0", "retention_rate": "22"},
    {"title": "Decent Content",        "ctr": "18.2", "retention_rate": "35"},
    {"title": "High Retention",        "ctr": "22.0", "retention_rate": "75"},  # filtered out
    {"title": "Low CTR",               "ctr": "9.5",  "retention_rate": "30"},  # filtered out
    {"title": "Edge CTR=15",           "ctr": "15.0", "retention_rate": "20"},  # filtered out (not >)
    {"title": "Edge Retention=40",     "ctr": "20.0", "retention_rate": "40"},  # filtered out (not <)
    {"title": "Almost Clickbait",      "ctr": "21.0", "retention_rate": "35"},
]


@pytest.fixture()
def report():
    return ClickbaitReport()


def test_filter_keeps_clickbait(report):
    result = report.filter(ROWS)
    titles = [r["title"] for r in result]
    assert "Clickbait King" in titles
    assert "Decent Content" in titles
    assert "Almost Clickbait" in titles


def test_filter_excludes_high_retention(report):
    result = report.filter(ROWS)
    titles = [r["title"] for r in result]
    assert "High Retention" not in titles


def test_filter_excludes_low_ctr(report):
    result = report.filter(ROWS)
    titles = [r["title"] for r in result]
    assert "Low CTR" not in titles


def test_filter_excludes_exact_ctr_boundary(report):
    result = report.filter(ROWS)
    titles = [r["title"] for r in result]
    assert "Edge CTR=15" not in titles


def test_filter_excludes_exact_retention_boundary(report):
    result = report.filter(ROWS)
    titles = [r["title"] for r in result]
    assert "Edge Retention=40" not in titles


def test_sort_descending_by_ctr(report):
    result = report.generate(ROWS)
    ctrs = [float(r["ctr"]) for r in result]
    assert ctrs == sorted(ctrs, reverse=True)


def test_columns(report):
    assert report.columns == ["title", "ctr", "retention_rate"]


def test_generate_empty_when_no_matches(report):
    rows = [{"title": "Safe", "ctr": "5.0", "retention_rate": "90"}]
    assert report.generate(rows) == []
