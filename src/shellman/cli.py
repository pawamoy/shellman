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
import re

from . import templates, __version__
from .context import get_context
from .reader import DocFile, DocStream, merge


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
    if value == "-":
        return value
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

    parser.add_argument(
        "--context",
        dest="context",
        nargs="+",
        help="context to inject. You can pass JSON strings or key=value pairs."
    )

    parser.add_argument(
        "--context-file",
        dest="context_file",
        help="JSON file to read context from."
    )

    parser.add_argument(
        "-t",
        "--template",
        metavar="TEMPLATE",
        choices=templates.parser_choices(),
        default="helptext",
        dest="template",
        help="the Jinja2 template to use. "
        'Prefix with "path:" to specify the path '
        "to a custom template. "
        "Available templates: %s" % ", ".join(templates.names()),
    )

    parser.add_argument(
        "-m",
        "--merge",
        dest="merge",
        nargs="?",
        metavar="FILENAME",
        const=True,
        default=False,
        help="with multiple input files, merge their contents in the output "
        "instead of appending (default: false)",
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        default=None,
        help="file to write to (default: stdout). You can use the {filename} variable.",
    )
    # parser.add_argument(
    #     "-w",
    #     "--warn",
    #     action="store_true",
    #     dest="warn",
    #     help="actually display the warnings (default: false)",
    # )
    # parser.add_argument(
    #     "-0",
    #     "-n",
    #     "--nice",
    #     action="store_true",
    #     dest="nice",
    #     help="be nice: return 0 even if warnings (default: false)",
    # )
    # mxg.add_argument(
    #     "-c",
    #     "--check",
    #     action="store_true",
    #     dest="check",
    #     help="only check if the documentation is correct, no output (default: false)",
    # )

    parser.add_argument(
        "FILE",
        type=valid_file,
        nargs="*",
        help="path to the file(s) to read. Use - to read on standard input.",
    )
    return parser


def render(template, doc=None, **context):
    shellman = dict()
    if doc is not None:
        shellman["doc"] = doc.sections
        shellman["filename"] = doc.filename
        shellman["filepath"] = doc.filepath
    shellman["today"] = date.today()
    shellman["version"] = __version__
    return template.render(shellman=shellman, **context)


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


def is_format_string(s):
    if re.search(r"{[a-zA-Z_][\w]*}", s):
        return True
    return False


def guess_filename(output, docs=None):
    if output and not is_format_string(output):
        return os.path.basename(output)
    if docs:
        return common_ancestor(docs)
    return ""


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
    templates.load_plugin_templates()

    parser = get_parser()
    args = parser.parse_args(argv)

    # Catch errors as early as possible
    if args.merge and len(args.FILE) < 2:
        print(
            "shellman: warning: --merge option is ignored with less than 2 inputs",
            file=sys.stderr,
        )

    if not args.FILE and args.output and is_format_string(args.output):
        print(
            "shellman: error: cannot format output name without file inputs. "
            "Please remove variables from output name, or provide file inputs",
            file=sys.stderr,
        )
        return 2

    # Immediately get the template to throw error if not found
    if args.template.startswith("path:"):
        template = templates.get_custom_template(args.template[5:])
    else:
        template = templates.templates[args.template]

    context = get_context(args)

    # Render template with context only
    if not args.FILE:
        contents = render(template, None, **context)
        if args.output:
            write(contents, args.output)
        else:
            print(contents)
        return 0

    # Parse input files
    docs = []
    for file in args.FILE:
        if file == "-":
            docs.append(DocStream(sys.stdin, filename=guess_filename(args.output)))
        else:
            docs.append(DocFile(file))

    # Optionally merge the parsed contents
    if args.merge:
        if isinstance(args.merge, str):
            new_filename = args.merge
        else:
            new_filename = guess_filename(args.output, docs)
        docs = [merge(docs, new_filename)]

    # If args.output contains variables, each input has its own output
    if args.output and is_format_string(args.output):
        for doc in docs:
            write(render(template, doc, **context), args.output.format(filename=doc.filename))
    # Else, concatenate contents (no effect if already merged), then output to file or stdout
    else:
        contents = "\n\n\n".join(render(template, doc, **context) for doc in docs)
        if args.output:
            write(contents, args.output)
        else:
            print(contents)

    # return 0 if args.nice or success else 1
    return 0
