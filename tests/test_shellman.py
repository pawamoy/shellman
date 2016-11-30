# -*- coding: utf-8 -*-
from shellman.cli import main


def test_main():
    assert main([]) == 0
