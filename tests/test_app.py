"""Tests"""
from pytest import CaptureFixture
from gh_pre.__main__ import main

__author__ = "Sorin Sbarnea"
__copyright__ = "Sorin Sbarnea"
__license__ = "MIT"


def test_main(capsys: CaptureFixture[str]) -> None:
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main()
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
