"""Tests for the `reader` module."""

from __future__ import annotations

from shellman.reader import preprocess_lines, preprocess_stream
from tests.conftest import get_fake_script


def test_preprocess_stream():
    script = get_fake_script("simple.sh")
    with open(script) as stream:
        assert list(preprocess_stream(stream)) == [
            (script, 3, "## \\brief Just a demo"),
            (script, 4, "## \\desc This script actually does nothing."),
            (script, 8, "## \\option -h, --help"),
            (script, 9, "## Print this help and exit."),
            (script, 14, "## \\usage demo [-h]"),
        ]


def test_preprocess_lines():
    script = get_fake_script("simple.sh")
    with open(script) as stream:
        blocks = list(preprocess_lines(preprocess_stream(stream)))
    print(blocks)
