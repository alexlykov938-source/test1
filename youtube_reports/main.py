"""CLI entry point for youtube_reports."""

import argparse
import sys

from tabulate import tabulate

from youtube_reports.reader import read_csv_files
from youtube_reports.reports import get_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate reports from YouTube video metrics CSV files."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        metavar="FILE",
        help="One or more CSV files with video metrics.",
    )
    parser.add_argument(
        "--report",
        required=True,
        metavar="REPORT",
        help="Report type to generate (e.g. clickbait).",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        rows = read_csv_files(args.files)
        report = get_report(args.report)
        result = report.generate(rows)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not result:
        print("No data matches the report criteria.")
        return

    table = [{col: row[col] for col in report.columns} for row in result]
    print(tabulate(table, headers="keys", tablefmt="pretty"))


if __name__ == "__main__":
    main()
