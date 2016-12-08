# -*- coding: utf-8 -*-

"""Main test script."""


from shellman.cli import main


def test_main():
    """Main test method."""

    assert main([]) == 0
