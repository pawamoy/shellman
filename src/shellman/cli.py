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

# from .formatter import get_formatter
from .checker import Checker
from .reader import DocFile, DocStream
from .tag import add_default_group_tags, add_default_tags


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
        '-f', '--format', dest='format', default='text',
        choices=['text', 'man', 'markdown'],
        help='format to write to (text)')
    parser.add_argument(
        '-o', '--output', action='store', dest='output',
        default=sys.stdout,
        help='file to write to (stdout by default)')
    # parser.add_argument(
    #     '-t', '--tags', action='store', dest='tags', type=parse_tags,
    #     help='tags to parse. Specify tags to parse with the path to a YAML '
    #          'file or a string in the following format: '
    #          '"NAME,SECTION,OCCURRENCES,LINES,HEADER,TYPE[|...]". '
    #          'where NAME is the tag name (like env), SECTION is the related '
    #          'section name (like Environment variables), OCCURRENCES and '
    #          'LINES are 1 or +, HEADER is 0, 1, y[es], n[o], true or false, '
    #          'and TYPE is "script" (s), "function" (f). or "both" (b), '
    #          'OCCURRENCES, LINES, HEADER and TYPE are optional, defaults are '
    #          '1, 1, no, script. '
    #          'Prefix them with o=, l=, h=, t= to provide only some of them, '
    #          'unordered, like kwargs in Python. '
    #          'Example: "the_tag,The tag,1,+,y,t=f". '
    #          'Separate tags with | (pipe) character.')
    # parser.add_argument(
    #     '-T', '--add-default-tags', action='store_true',
    #     dest='add_default_tags', help='Add all the default tags to be parsed.')
    # parser.add_argument(
    #     '-F', '--add-default-function-tags', action='store_true',
    #     dest='add_default_function_tags',
    #     help='Add the default function tags to be parsed.')
    # parser.add_argument(
    #     '-S', '--add-default-script-tags', action='store_true',
    #     dest='add_default_script_tags',
    #     help='Add the default script tags to be parsed.')
    parser.add_argument(
        '-w', '--warn', action='store_true', dest='warn',
        help='actually display the warnings (false)')
    parser.add_argument('FILE', type=valid_file, nargs='*',
                        help='path to the file(s) to read')
    return parser


# def parse_tags(arg):
#     try:
#         valid_file(arg)
#         return parse_yaml_tags(arg)
#     except argparse.ArgumentTypeError:
#         return parse_string_tags(arg)


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

    # if args.tags:
    #     dispatch_tags(args.tags)
    #     if args.add_default_tags:
    #         add_default_tags()
    #     else:
    #         if args.add_default_script_tags:
    #             add_default_script_tags()
    #         if args.add_default_function_tags:
    #             add_default_function_tags()
    # else:
    #     add_default_tags()

    add_default_tags()
    add_default_group_tags()

    if args.FILE:
        cleaned_docs = [Checker(DocFile(file)) for file in args.FILE]
    else:
        try:
            cleaned_docs = [Checker(DocStream(sys.stdin))]
        except KeyboardInterrupt:
            cleaned_docs = []

    if args.warn:
        for cleaned_doc in cleaned_docs:
            cleaned_doc.warn()

    if args.nice:
        return 0
    if all(cleaned_docs):
        return 0
    return 1
