"""Clickbait report: high CTR + low retention."""

from .base import BaseReport, register

CTR_THRESHOLD = 15.0
RETENTION_THRESHOLD = 40.0


@register("clickbait")
class ClickbaitReport(BaseReport):
    """
    Lists videos with CTR > 15% and retention_rate < 40%.

    These are videos that attract clicks but fail to hold viewers —
    a classic sign of clickbait content.
    """

    @property
    def columns(self) -> list[str]:
        return ["title", "ctr", "retention_rate"]

    def filter(self, rows: list[dict]) -> list[dict]:
        return [
            row for row in rows
            if float(row["ctr"]) > CTR_THRESHOLD
            and float(row["retention_rate"]) < RETENTION_THRESHOLD
        ]

    def sort(self, rows: list[dict]) -> list[dict]:
        return sorted(rows, key=lambda r: float(r["ctr"]), reverse=True)
