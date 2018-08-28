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

from .reader import DocFile, DocStream, merge
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
        raise argparse.ArgumentTypeError("%s is not a valid file path" % value)
    elif os.path.isdir(value):
        raise argparse.ArgumentTypeError(
            "%s is a directory, not a regular file" % value
        )
    return value


def get_parser():
    """Return a parser for the command line arguments."""
    parser = argparse.ArgumentParser()

    mxg = parser.add_mutually_exclusive_group()

    parser.add_argument(
        "-0",
        "-n",
        "--nice",
        action="store_true",
        dest="nice",
        help="be nice: return 0 even if warnings (default: false)",
    )
    mxg.add_argument(
        "-c",
        "--check",
        action="store_true",
        dest="check",
        help="only check if the documentation is correct, no output (default: false)",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        default="",
        help="template format to choose (different for each template)",
    )
    parser.add_argument(
        "-t",
        "--template",
        choices=templates.parser_choices(),
        default="helptext",
        dest="template",
        help='the Jinja2 template to use. Prefix with "path:" to specify the path '
        'to a directory containing a file named "index". '
        "Available templates: %s" % ", ".join(templates.names()),
    )
    parser.add_argument(
        "-m",
        "--merge",
        action="store_true",
        dest="merge",
        help="when multiple files as input, merge their sections in the output (default: false)",
    )
    mxg.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        default=None,
        help="file to write to (default: stdout)",
    )
    mxg.add_argument(
        "-O",
        "--multiple-output",
        action="store",
        dest="multiple_output",
        default=None,
        help="output file path formatted for each input file. "
        "You can use the following variables: "
        "{filename} and {format} (default: not used)",
    )
    parser.add_argument(
        "-w",
        "--warn",
        action="store_true",
        dest="warn",
        help="actually display the warnings (default: false)",
    )
    parser.add_argument(
        "FILE", type=valid_file, nargs="*", help="path to the file(s) to read"
    )
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
    docs = []

    if len(args.FILE) > 1 and args.multiple_output and args.merge:
        print(
            "shellman: error: cannot merge multiple files and output in multiple files.\n"
            "                 Please use --output instead, or remove --merge."
        )
        return 2

    if args.FILE:
        for file in args.FILE:
            docs.append(DocFile(file))
            # if args.warn:
            #     doc.warn()
            # success &= bool(doc)
    else:
        print("shellman: reading on standard input -", file=sys.stderr)
        try:
            docs.append(DocStream(sys.stdin, name=args.output or ""))
            # if args.warn:
            #     doc.warn()
            # success &= bool(doc)
        except KeyboardInterrupt:
            pass

    template = templates.templates[args.template]

    if len(docs) == 1:
        doc = docs[0]
        contents = get_contents(template, args.format, doc)
        if args.output:
            write(contents, args.output)
        elif args.multiple_output:
            write(
                contents,
                args.multiple_output.format(filename=doc.filename, format=args.format),
            )
        else:
            print(contents)
    else:
        if args.output or not args.multiple_output:
            if args.merge:
                doc = merge(
                    docs, os.path.basename(args.output or common_ancestor(docs))
                )
                contents = get_contents(template, args.format, doc)
            else:
                contents = "\n\n\n".join(
                    get_contents(template, args.format, doc) for doc in docs
                )
            if args.output:
                write(contents, args.output)
            else:
                print(contents)
        elif args.multiple_output:
            for doc in docs:
                contents = get_contents(template, args.format, doc)
                write(
                    contents,
                    args.multiple_output.format(
                        filename=doc.filename, format=args.format
                    ),
                )

    return 0 if args.nice or success else 1


def get_contents(template, format, doc):
    return template.render(format, doc=doc, shellman_version=__version__)


def write(contents, filepath):
    with open(filepath, "w") as write_stream:
        print(contents, file=write_stream)


def common_ancestor(docs):
    splits = [os.path.split(doc.filepath) for doc in docs]
    vertical = []
    depth = 1
    while True:
        if not all(len(s) >= depth for s in splits):
            break
        vertical.append([s[depth - 1] for s in splits])
        depth += 1
    common = ""
    for v in vertical:
        if v.count(v[0]) != len(v):
            break
        common = v[0]
    return common or "<VARIOUS_INPUTS>"
