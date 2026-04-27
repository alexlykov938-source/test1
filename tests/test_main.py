"""Integration tests for the CLI entry point."""

import textwrap
from pathlib import Path

import pytest

from youtube_reports.main import main


@pytest.fixture()
def stats_file(tmp_path: Path):
    content = textwrap.dedent("""\
        title,ctr,retention_rate,views,likes,avg_watch_time
        Я бросил IT и стал фермером,18.2,35,45200,1240,4.2
        Как я спал по 4 часа и ничего не понял,22.5,28,128700,3150,3.1
        Почему сеньоры не носят галстуки,9.5,82,31500,890,8.9
        Секрет который скрывают тимлиды,25.0,22,254000,8900,2.5
        Купил джуну макбук и он уволился,19.0,38,87600,2100,4.5
        Честный обзор на печеньки в офисе,6.0,91,12300,450,10.2
    """)
    f = tmp_path / "stats.csv"
    f.write_text(content, encoding="utf-8")
    return f


def test_clickbait_report_runs(stats_file, capsys):
    main(["--files", str(stats_file), "--report", "clickbait"])
    out = capsys.readouterr().out
    assert "Секрет который скрывают тимлиды" in out
    assert "Как я спал по 4 часа и ничего не понял" in out
    assert "Я бросил IT и стал фермером" in out
    assert "Купил джуну макбук и он уволился" in out
    # High-retention videos should NOT appear
    assert "Почему сеньоры не носят галстуки" not in out
    assert "Честный обзор на печеньки в офисе" not in out


def test_clickbait_sorted_by_ctr_desc(stats_file, capsys):
    main(["--files", str(stats_file), "--report", "clickbait"])
    out = capsys.readouterr().out
    lines = [l for l in out.splitlines() if "," not in l]  # rough row filter
    # Find positions of known titles in output
    pos_top = out.index("Секрет который скрывают тимлиды")   # ctr=25
    pos_mid = out.index("Как я спал по 4 часа")               # ctr=22.5
    assert pos_top < pos_mid


def test_unknown_report_exits(stats_file):
    with pytest.raises(SystemExit) as exc_info:
        main(["--files", str(stats_file), "--report", "nonexistent"])
    assert exc_info.value.code != 0


def test_missing_file_exits(tmp_path):
    with pytest.raises(SystemExit) as exc_info:
        main(["--files", "ghost.csv", "--report", "clickbait"])
    assert exc_info.value.code != 0


def test_two_files_combined(tmp_path, capsys):
    f1 = tmp_path / "s1.csv"
    f1.write_text(
        "title,ctr,retention_rate\nVideo A,25.0,20\n", encoding="utf-8"
    )
    f2 = tmp_path / "s2.csv"
    f2.write_text(
        "title,ctr,retention_rate\nVideo B,20.0,30\n", encoding="utf-8"
    )
    main(["--files", str(f1), str(f2), "--report", "clickbait"])
    out = capsys.readouterr().out
    assert "Video A" in out
    assert "Video B" in out
