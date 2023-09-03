"""Module that contains the command line application."""

# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m shellman` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `shellman.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `shellman.__main__` in `sys.modules`.

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Sequence

from shellman import __version__, templates
from shellman.context import DEFAULT_JSON_FILE, _get_context, _update
from shellman.reader import DocFile, DocStream, _merge

if TYPE_CHECKING:
    from shellman.templates import Template


def _valid_file(value: str) -> str:
    if value == "-":
        return value
    if not value:
        raise argparse.ArgumentTypeError("'' is not a valid file path")
    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("%s is not a valid file path" % value)
    if os.path.isdir(value):
        raise argparse.ArgumentTypeError("%s is a directory, not a regular file" % value)
    return value


def get_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(prog="shellman")

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
        choices=templates._parser_choices(),
        default="helptext",
        dest="template",
        help="the Jinja2 template to use. "
        'Prefix with "path:" to specify the path '
        "to a custom template. "
        "Available templates: %s" % ", ".join(templates._names()),
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
        type=_valid_file,
        nargs="*",
        help="path to the file(s) to read. Use - to read on standard input.",
    )
    return parser


def _render(template: Template, doc: DocFile | DocStream | None = None, **context: dict) -> str:
    shellman: dict[str, Any] = {"doc": {}}
    if doc is not None:
        shellman["doc"] = doc.sections
        shellman["filename"] = doc.filename
        shellman["filepath"] = doc.filepath
    shellman["today"] = datetime.now(tz=timezone.utc).date()
    shellman["version"] = __version__

    if "shellman" in context:
        _update(shellman, context.pop("shellman"))

    return template.render(shellman=shellman, **context)


def _write(contents: str, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as write_stream:
        print(contents, file=write_stream)


def _common_ancestor(docs: Sequence[DocFile | DocStream]) -> str:
    splits: list[tuple[str, str]] = [os.path.split(doc.filepath) for doc in docs if doc.filepath]
    vertical = []
    depth = 1
    while True:
        if not all(len(s) >= depth for s in splits):
            break
        vertical.append([s[depth - 1] for s in splits])
        depth += 1
    common = ""
    for vert in vertical:
        if vert.count(vert[0]) != len(vert):
            break
        common = vert[0]
    return common or "<VARIOUS_INPUTS>"


def _is_format_string(string: str) -> bool:
    if re.search(r"{[a-zA-Z_][\w]*}", string):
        return True
    return False


def _guess_filename(output: str, docs: Sequence[DocFile | DocStream] | None = None) -> str:
    if output and not _is_format_string(output):
        return os.path.basename(output)
    if docs:
        return _common_ancestor(docs)
    return ""


def _output_name_variables(doc: DocFile | DocStream | None = None) -> dict:
    if doc:
        basename, ext = os.path.splitext(doc.filename)
        abspath = os.path.abspath(doc.filepath or doc.filename)
        dirpath = os.path.split(abspath)[0] or "."
        dirname = os.path.basename(dirpath)
        return {
            "filename": doc.filename,
            "filepath": abspath,
            "basename": basename,
            "ext": ext,
            "dirpath": dirpath,
            "dirname": dirname,
            "vcsroot": _get_vcs_root(dirpath),
        }
    return {}


_vcs_root_cache: dict[str, str] = {}


def _get_vcs_root(path: str) -> str:
    if path in _vcs_root_cache:
        return _vcs_root_cache[path]
    original_path = path
    while not any(os.path.exists(os.path.join(path, vcs)) for vcs in (".git", ".hg", ".svn")):
        path = os.path.dirname(path)
        if path == "/":
            path = ""
            break
    _vcs_root_cache[original_path] = path
    return path


def main(args: list[str] | None = None) -> int:
    """Run the main program.

    This function is executed when you type `shellman` or `python -m shellman`.

    Get the file to parse, construct a Doc object, get file's doc,
    get the according formatter class, instantiate it
    with acquired doc and write on specified file (stdout by default).

    Parameters:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    templates._load_plugin_templates()

    parser = get_parser()
    opts = parser.parse_args(args)

    # Catch errors as early as possible
    if opts.merge and len(opts.FILE) < 2:  # noqa: PLR2004
        print(
            "shellman: warning: --merge option is ignored with less than 2 inputs",
            file=sys.stderr,
        )

    if not opts.FILE and opts.output and _is_format_string(opts.output):
        parser.print_usage(file=sys.stderr)
        print(
            "shellman: error: cannot format output name without file inputs. "
            "Please remove variables from output name, or provide file inputs",
            file=sys.stderr,
        )
        return 2

    # Immediately get the template to throw error if not found
    if opts.template.startswith("path:"):
        template = templates._get_custom_template(opts.template[5:])
    else:
        template = templates.templates[opts.template]

    context = _get_context(opts)

    # Render template with context only
    if not opts.FILE:
        if not context:
            parser.print_usage(file=sys.stderr)
            print("shellman: error: please specify input file(s) or context", file=sys.stderr)
            return 1
        contents = _render(template, None, **context)
        if opts.output:
            _write(contents, opts.output)
        else:
            print(contents)
        return 0

    # Parse input files
    docs: list[DocFile | DocStream] = []
    for file in opts.FILE:
        if file == "-":
            docs.append(DocStream(sys.stdin, filename=_guess_filename(opts.output)))
        else:
            docs.append(DocFile(file))

    # Optionally merge the parsed contents
    if opts.merge:
        new_filename = _guess_filename(opts.output, docs)
        docs = [_merge(docs, new_filename)]

    # If opts.output contains variables, each input has its own output
    if opts.output and _is_format_string(opts.output):
        for doc in docs:
            _write(
                _render(template, doc, **context),
                opts.output.format(**_output_name_variables(doc)),
            )
    # Else, concatenate contents (no effect if already merged), then output to file or stdout
    else:
        contents = "\n\n\n".join(_render(template, doc, **context) for doc in docs)
        if opts.output:
            _write(contents, opts.output)
        else:
            print(contents)

    return 0
