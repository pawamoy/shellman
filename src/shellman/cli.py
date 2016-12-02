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

from .doc import Doc
from .formatter import get_formatter


def main(argv=None):
    """
    Main function.

    Args:
        argv (list): expected path of file to read

    Returns:
        int: 0, unless exception

    Get the file to parse, construct a Doc object, get file's doc,
    get the wanted format from environment variable SHELLMAN_FORMAT
    (default to text), get the according formatter class, instantiate it
    with acquired doc and write on stdout.
    """

    if argv is None:
        argv = sys.argv[1:]

    f = argv[0]
    doc = Doc(f).read()
    fmt = os.environ.get('SHELLMAN_FORMAT', 'text')
    get_formatter(fmt)(doc).write()

    return 0
