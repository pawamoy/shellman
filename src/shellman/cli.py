# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import io
import os
import re
import sys
from datetime import date

from . import __version__, templates
from .context import DEFAULT_JSON_FILE, get_context, update
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
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--context",
        dest="context",
        nargs="+",
        help="context to inject when rendering the template. "
        "You can pass JSON strings or key=value pairs. "
        "Example: `--context project=hello '{\"version\": [0, 3, 1]}'`.",
    )

    parser.add_argument(
        "--context-file",
        dest="context_file",
        help="JSON file to read context from. "
        "By default shellman will try to read the file '%s' "
        "in the current directory." % DEFAULT_JSON_FILE,
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
        action="store_true",
        help="with multiple input files, merge their contents in the output "
        "instead of appending (default: %(default)s). ",
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        default=None,
        help="file to write to (default: stdout). "
        "You can use the following variables in the output name: "
        "{basename}, {ext}, {filename} (equal to {basename}.{ext}), "
        "{filepath}, {dirname}, {dirpath}, and {vcsroot} "
        "(git and mercurial supported). "
        "They will be populated from each input file.",
    )

    parser.add_argument(
        "FILE",
        type=valid_file,
        nargs="*",
        help="path to the file(s) to read. Use - to read on standard input.",
    )
    return parser


def render(template, doc=None, **context):
    shellman = {"doc": {}}
    if doc is not None:
        shellman["doc"] = doc.sections
        shellman["filename"] = doc.filename
        shellman["filepath"] = doc.filepath
    shellman["today"] = date.today()
    shellman["version"] = __version__

    if "shellman" in context:
        update(shellman, context.pop("shellman"))

    return template.render(shellman=shellman, **context)


def write(contents, filepath):
    with io.open(filepath, "w", encoding="utf-8") as write_stream:
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


def output_name_variables(doc=None):
    if doc:
        basename, ext = os.path.splitext(doc.filename)
        dirpath = os.path.split(doc.filepath)[0]
        dirname = os.path.basename(dirpath)
        return dict(
            filename=doc.filename,
            filepath=doc.filepath,
            basename=basename,
            ext=ext,
            dirpath=dirpath,
            dirname=dirname,
            vcsroot=get_vcs_root(dirpath)
        )
    return {}


_vcs_root_cache = {}


def get_vcs_root(path):
    if path in _vcs_root_cache:
        return _vcs_root_cache[path]
    original_path = path
    while not any(os.path.exists(os.path.join(path, vcs))
                  for vcs in (".git", ".hg", ".svn")):
        path = os.path.dirname(path)
        if path == "/":
            path = ""
    _vcs_root_cache[original_path] = path
    return path


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
        if not context:
            print(
                "shellman: error: please specify "
                "input file(s) or context",
                file=sys.stderr
            )
            return 1
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
        new_filename = guess_filename(args.output, docs)
        docs = [merge(docs, new_filename)]

    # If args.output contains variables, each input has its own output
    if args.output and is_format_string(args.output):
        for doc in docs:
            write(
                render(template, doc, **context),
                args.output.format(**output_name_variables(doc)),
            )
    # Else, concatenate contents (no effect if already merged), then output to file or stdout
    else:
        contents = "\n\n\n".join(render(template, doc, **context) for doc in docs)
        if args.output:
            write(contents, args.output)
        else:
            print(contents)

    return 0
