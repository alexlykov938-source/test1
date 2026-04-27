# YouTube Reports

CLI tool for generating reports from YouTube video metrics CSV files.

## Installation

```bash
pip install tabulate pytest
pip install -e .
```

## Usage

```bash
# Single file
python -m youtube_reports.main --files stats1.csv --report clickbait

# Multiple files (combined into one report)
python -m youtube_reports.main --files stats1.csv stats2.csv --report clickbait

# After pip install (using the entry point)
youtube-reports --files stats1.csv stats2.csv --report clickbait
```

### Example output

```
+-----------------------------------------+------+----------------+
| title                                   | ctr  | retention_rate |
+-----------------------------------------+------+----------------+
| Секрет который скрывают тимлиды         | 25.0 | 22             |
| Как я спал по 4 часа и ничего не понял  | 22.5 | 28             |
| Как я задолжал ревьюеру 1000 строк кода | 21.0 | 35             |
| Купил джуну макбук и он уволился        | 19.0 | 38             |
| Я бросил IT и стал фермером             | 18.2 | 35             |
+-----------------------------------------+------+----------------+
```

## Running tests

```bash
pytest
```

## Adding a new report

1. Create a new file in `youtube_reports/reports/`, e.g. `top_performers.py`.
2. Define a class inheriting from `BaseReport` and decorate it with `@register("top_performers")`.
3. Import the module in `youtube_reports/reports/__init__.py`.

```python
# youtube_reports/reports/top_performers.py
from .base import BaseReport, register

@register("top_performers")
class TopPerformersReport(BaseReport):
    @property
    def columns(self):
        return ["title", "views", "likes"]

    def filter(self, rows):
        return [r for r in rows if int(r["views"]) > 100_000]

    def sort(self, rows):
        return sorted(rows, key=lambda r: int(r["views"]), reverse=True)
```

That's it — the new report is immediately available via `--report top_performers`.
