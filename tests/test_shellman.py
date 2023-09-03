"""Main test script."""

import os

import pytest

from shellman.cli import main as cli_main
from shellman.context import get_cli_context, get_context, get_env_context, update
from shellman.reader import preprocess_lines, preprocess_stream
from shellman.templates import filters


def get_fake_script(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "fakescripts", name)


class TestCommandLine:
    def test_main(self):
        assert cli_main([]) == 1
        assert cli_main(["-c", "hello=world"]) == 0
        assert cli_main([get_fake_script("simple.sh")]) == 0


class TestFilters:
    def test_do_groffautoemphasis(self):
        string = "I'm SO emphaSIzed!"
        assert filters.do_groffautoemphasis(string) == "I'm \\fISO\\fR emphaSIzed!"

    def test_do_groffautostrong(self):
        string = "I'm -so --strong!"
        assert filters.do_groffautostrong(string) == "I'm \\fB-so\\fR \\fB--strong\\fR!"

    def test_do_smartwrap(self):
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


class TestTemplates:
    pass


class TestContext:
    def test_get_cli_context(self):
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

    def test_get_env_context(self):
        os.environ["SHELLMAN_CONTEXT_HELLO"] = "world"
        assert get_env_context() == {"hello": "world"}
        del os.environ["SHELLMAN_CONTEXT_HELLO"]

    def test_get_context(self):
        from collections import namedtuple

        args = namedtuple("args", "context_file context")(None, None)
        assert get_context(args) == {}

    def test_update(self):
        d1 = {"hello": {"world": "what's up?"}}
        d2 = {"hello": {"universe": "????"}, "byebye": "universe"}
        update(d1, d2)
        assert d1 == {"hello": {"world": "what's up?", "universe": "????"}, "byebye": "universe"}


class TestReader:
    def test_preprocess_stream(self):
        script = get_fake_script("simple.sh")
        with open(script) as stream:
            assert list(preprocess_stream(stream)) == [
                (script, 3, "## \\brief Just a demo"),
                (script, 4, "## \\desc This script actually does nothing."),
                (script, 8, "## \\option -h, --help"),
                (script, 9, "## Print this help and exit."),
                (script, 14, "## \\usage demo [-h]"),
            ]

    def test_preprocess_lines(self):
        script = get_fake_script("simple.sh")
        with open(script) as stream:
            blocks = list(preprocess_lines(preprocess_stream(stream)))
        print(blocks)


class TestTags:
    pass


if __name__ == "__main__":
    pytest.main()
