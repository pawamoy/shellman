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

import argparse
import os
import sys

from .doc import Doc
from .formatter import get_formatter
from .tag import Tag


def main(argv=None):
    """
    Main function.

    Args:
        argv (list): options and path to file to read

    Returns:
        int: 0, unless exception

    Get the file to parse, construct a Doc object, get file's doc,
    get the according formatter class, instantiate it
    with acquired doc and write on specified file (stdout by default).
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-0', '-n', '--nice', action='store_true', dest='nice',
        help='be nice: return 0 even if warnings (false)')
    parser.add_argument(
        '-1', '--failfast', action='store_true', dest='failfast',
        help='exit 1 at first warning encountered '
             '(only useful when not nice) (false)')
    parser.add_argument(
        '-c', '--check', action='store_true', dest='check',
        help='check if the documentation is correct (false)')
    parser.add_argument(
        '-f', '--format', dest='format', default='text',
        choices=['text', 'man', 'markdown'],
        help='format to write to (text)')
    parser.add_argument(
        '-i', '--whitelist', '--ignore', action='store', dest='whitelist',
        help='whitelisted tags: "customtag:1+,customtag2"')
    parser.add_argument(
        '-o', '--output', action='store', dest='output',
        default=sys.stdout,
        help='file to write to (stdout by default)')
    parser.add_argument(
        '-w', '--warn',  action='store_true', dest='warn',
        help='actually display the warnings (false)')

    def valid_file(value):
        if not value:
            raise argparse.ArgumentTypeError("'' is not a valid file path")
        elif not os.path.exists(value):
            raise argparse.ArgumentTypeError("%s is not a valid file path" %
                                             value)
        elif os.path.isdir(value):
            raise argparse.ArgumentTypeError("%s is a directory, "
                                             "not a regular file" % value)
        return value

    parser.add_argument('FILE', type=valid_file,
                        help='path to the file to read')

    args = parser.parse_args(argv)

    if args.whitelist:
        new_whitelist = {}
        for tag in args.whitelist.split(','):
            if ':' in tag:
                tag, spec = tag.split(':')
                occ, lines = spec
                new_whitelist[tag] = Tag(occurrences=occ, lines=lines)
            else:
                new_whitelist[tag] = Tag()

        args.whitelist = new_whitelist

    doc = Doc(args.FILE, whitelist=args.whitelist)

    if args.check:
        ok = doc.check(args.warn, args.nice, args.failfast)
        return 0 if ok else 1
    else:
        doc_read = doc.read()
        fmt = args.format
        formatter = get_formatter(fmt)
        formatter(doc_read, output=args.output).write()
