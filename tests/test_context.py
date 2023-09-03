"""Tests for the `context` module."""

from __future__ import annotations

import os

from shellman.context import get_cli_context, get_context, get_env_context, update


def test_get_cli_context():
    assert get_cli_context([]) == {}
    assert get_cli_context([""]) == {}
    assert get_cli_context([" "]) == {}

    assert get_cli_context(["hello=world"]) == {"hello": "world"}
    assert get_cli_context(["hello=world", "hello=universe"]) == {"hello": "universe"}

    assert (
        get_cli_context(["hello.world=universe"])
        == get_cli_context(["hello=world", "hello.world=universe"])
        == {"hello": {"world": "universe"}}
    )
    assert get_cli_context(["hello.world=universe", "hello=world"]) == {"hello": "world"}
    assert get_cli_context(["hello.world.and.foobars=hello"]) == {"hello": {"world": {"and": {"foobars": "hello"}}}}

    assert get_cli_context(['{"hello": "world", "number": [1, 2]}']) == {"hello": "world", "number": [1, 2]}
    assert get_cli_context(['{"hello": "world"}', "hello=universe"]) == {"hello": "universe"}


def test_get_env_context():
    os.environ["SHELLMAN_CONTEXT_HELLO"] = "world"
    assert get_env_context() == {"hello": "world"}
    del os.environ["SHELLMAN_CONTEXT_HELLO"]


def test_get_context():
    from collections import namedtuple

    args = namedtuple("args", "context_file context")(None, None)
    assert get_context(args) == {}


def test_update():
    d1 = {"hello": {"world": "what's up?"}}
    d2 = {"hello": {"universe": "????"}, "byebye": "universe"}
    update(d1, d2)
    assert d1 == {"hello": {"world": "what's up?", "universe": "????"}, "byebye": "universe"}
