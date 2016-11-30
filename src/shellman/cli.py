# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later,
  but that will cause problems: the code will get executed twice:

  - When you run `python -mshellman` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``shellman.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``shellman.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import os
import sys

from .formatter import get_formatter
from .doc import Doc


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """

    f = sys.argv[1]
    doc = Doc(f).read()
    fmt = os.environ.get('SHELLMAN_FORMAT', 'text')
    get_formatter(fmt)(doc).write()

    return 0
