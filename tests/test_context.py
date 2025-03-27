"""Tests for the `context` module."""

from __future__ import annotations

import os
from collections import namedtuple

from shellman._internal.context import _get_cli_context, _get_context, _get_env_context, _update


def test_get_cli_context() -> None:
    """Test getting context from CLI arguments."""
    assert _get_cli_context([]) == {}
    assert _get_cli_context([""]) == {}
    assert _get_cli_context([" "]) == {}

    assert _get_cli_context(["hello=world"]) == {"hello": "world"}
    assert _get_cli_context(["hello=world", "hello=universe"]) == {"hello": "universe"}

    assert (
        _get_cli_context(["hello.world=universe"])
        == _get_cli_context(["hello=world", "hello.world=universe"])
        == {"hello": {"world": "universe"}}
    )
    assert _get_cli_context(["hello.world=universe", "hello=world"]) == {"hello": "world"}
    assert _get_cli_context(["hello.world.and.foobars=hello"]) == {"hello": {"world": {"and": {"foobars": "hello"}}}}

    assert _get_cli_context(['{"hello": "world", "number": [1, 2]}']) == {"hello": "world", "number": [1, 2]}
    assert _get_cli_context(['{"hello": "world"}', "hello=universe"]) == {"hello": "universe"}


def test_get_env_context() -> None:
    """Test getting context from environment variables."""
    os.environ["SHELLMAN_CONTEXT_HELLO"] = "world"
    assert _get_env_context() == {"hello": "world"}
    del os.environ["SHELLMAN_CONTEXT_HELLO"]


def test_get_context() -> None:
    """Test getting context from default JSON file."""
    args = namedtuple("args", "context_file context")(None, None)  # type: ignore[arg-type,call-arg]  # noqa: PYI024
    assert _get_context(args) == {}  # type: ignore[arg-type]


def test_update() -> None:
    """Test the context updater/merger function."""
    d1 = {"hello": {"world": "what's up?"}}
    d2 = {"hello": {"universe": "????"}, "byebye": "universe"}
    _update(d1, d2)
    assert d1 == {"hello": {"world": "what's up?", "universe": "????"}, "byebye": "universe"}
