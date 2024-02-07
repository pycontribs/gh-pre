"""Tests"""

from typer.testing import CliRunner

from gh_pre.__main__ import app


runner = CliRunner()


def test_main() -> None:
    """CLI Tests"""
    result = runner.invoke(app, ["--help", "--config=tests/pre.yml"])
    assert result.exit_code == 0, result.stdout
    assert "Pre helps you chain releases on github." in result.stdout
