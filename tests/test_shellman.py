# -*- coding: utf-8 -*-

"""Main test script."""

import pytest

from shellman.templates import filters


class TestCommandLine:
    pass


class TestFilters:
    def test_do_groffautoemphasis(self):
        string = "I'm SO emphaSIzed!"
        assert filters.do_groffautoemphasis(string) == "I'm \\fISO\\fR emphaSIzed!"


class TestTemplates:
    pass


class TestContext:
    pass


class TestReader:
    pass


class TestTags:
    pass
