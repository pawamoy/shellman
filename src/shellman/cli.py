# -*- coding: utf-8 -*-

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
from datetime import date

from .reader import DocFile, DocStream
from . import templates
from . import __version__


def valid_file(value):
    """
    Check if given file exists and is a regular file.

    Args:
        value (str): path to the file.

    Raises:
        argparse.ArgumentTypeError: if not valid.

    Returns:
        str: original value argument.
    """
    if not value:
        raise argparse.ArgumentTypeError("'' is not a valid file path")
    elif not os.path.exists(value):
        raise argparse.ArgumentTypeError("%s is not a valid file path" %
                                         value)
    elif os.path.isdir(value):
        raise argparse.ArgumentTypeError("%s is a directory, "
                                         "not a regular file" % value)
    return value


def get_parser():
    """Return a parser for the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-0', '-n', '--nice', action='store_true', dest='nice',
        help='be nice: return 0 even if warnings (false)')
    parser.add_argument(
        '-c', '--check', action='store_true', dest='check',
        help='check if the documentation is correct (false)')
    parser.add_argument(
        '-f', '--format', dest='format', default='',
        help='template format to choose (different for each template)')
    parser.add_argument(
        '-t', '--template', choices=templates.parser_choices(),
        default='helptext', dest='template',
        help='The Jinja2 template to use. Prefix with "path:" to specify the path '
             'to a directory containing a file named "index". '
             'Available templates: %s' % ', '.join(templates.names()))
    parser.add_argument(
        '-o', '--output', action='store', dest='output',
        default=None,
        help='file to write to (stdout by default)')
    parser.add_argument(
        '-w', '--warn', action='store_true', dest='warn',
        help='actually display the warnings (false)')
    parser.add_argument('FILE', type=valid_file, nargs='*',
                        help='path to the file(s) to read')
    return parser


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
    parser = get_parser()
    args = parser.parse_args(argv)

    success = True
    doc = None

    if args.FILE:
        for file in args.FILE:
            doc = DocFile(file)
            if args.warn:
                doc.warn()
            success &= bool(doc)
    else:
        try:
            doc = DocStream(sys.stdin)
            if args.warn:
                doc.warn()
            success &= bool(doc)
        except KeyboardInterrupt:
            pass

    if doc is None:
        return 1

    if args.format and not args.format.startswith('.'):
        args.format = '.' + args.format
    template = templates.templates[args.template].get(args.format)

    indent = 4
    rendered = template.render(
        doc=doc,
        context=dict(
            indent=indent,
            indent_str=indent * " ",
            section_order=templates.SECTION_ORDER
        ),
        shellman_version=__version__,
        now=date.today()
    )

    if args.output is not None:
        with open(args.output, 'w') as write_stream:
            print(rendered, file=write_stream)
    else:
        print(rendered)

    return 0 if args.nice or success else 1
