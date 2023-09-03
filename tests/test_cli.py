"""Tests for the `cli` module."""

from __future__ import annotations

import pytest

from shellman import cli
from shellman.cli import main as cli_main
from shellman.templates import filters
from tests.conftest import get_fake_script


def test_main() -> None:
    """Basic CLI test."""
    assert cli_main([]) == 1
    assert cli_main(["-c", "hello=world"]) == 0
    assert cli_main([get_fake_script("simple.sh")]) == 0


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "shellman" in captured.out


def test_do_groffautoemphasis() -> None:
    """Test Groff auto-emphasis on uppercase words."""
    string = "I'm SO emphaSIzed!"
    assert filters.do_groffautoemphasis(string) == "I'm \\fISO\\fR emphaSIzed!"


def test_do_groffautostrong() -> None:
    """Test Groff auto-strong on words prefixed with `-` or `--`."""
    string = "I'm -so --strong!"
    assert filters.do_groffautostrong(string) == "I'm \\fB-so\\fR \\fB--strong\\fR!"


def test_do_smartwrap() -> None:
    """Test smart-wrapping algorithm."""
    text = (
        "Some text.\n\n"
        "A very long line: Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit, sed do eiusmod tempor incididunt "
        "ut labore et dolore magna aliqua."
    )
    code_blocks = (
        "Code block:\n  hello\nEnd.\n\n  "
        "another code block\n  with very long lines: "
        "Lorem ipsum dolor sit amet, consectetur "
        "adipiscing elit, sed do eiusmod tempor incididunt "
        "ut labore et dolore magna aliqua."
    )

    assert (
        filters.do_smartwrap(text, width=40) == "    Some text.\n\n"
        "    A very long line: Lorem ipsum dolor\n"
        "    sit amet, consectetur adipiscing\n"
        "    elit, sed do eiusmod tempor\n"
        "    incididunt ut labore et dolore magna\n"
        "    aliqua."
    )
    assert (
        filters.do_smartwrap(code_blocks, width=40) == "    Code block:\n"
        "      hello\n"
        "    End.\n\n"
        "      another code block\n"
        "      with very long lines: Lorem ipsum dolor sit amet, "
        "consectetur adipiscing elit, sed do eiusmod tempor incididunt "
        "ut labore et dolore magna aliqua."
    )
