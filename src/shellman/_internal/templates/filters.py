# This module contains Jinja filters.

from __future__ import annotations

import re
import textwrap
from collections import defaultdict
from itertools import groupby
from shutil import get_terminal_size
from typing import TYPE_CHECKING, Any

from jinja2.filters import _GroupTuple, make_attrgetter, pass_environment
from markupsafe import escape

if TYPE_CHECKING:
    from collections.abc import Sequence

    from jinja2 import Environment


def do_groffautoescape(string: str) -> str:
    """Automatically Groff-escape dashes, single/double quotes, dots and dollar signs in a string.

    Parameters:
        string: The string to escape.

    Returns:
        The escaped string.
    """
    return string.replace("-", "\\-").replace("'", "\\'").replace('"', '\\"').replace(".", "\\.").replace("$", "\\f$")


def do_groffstrong(string: str) -> str:
    """Mark a string as Groff strong.

    Parameters:
        string: The string to convert.

    Returns:
        The updated string.
    """
    return "\\fB" + string + "\\fR"


def do_groffemphasis(string: str) -> str:
    """Mark a string as Groff emphasis.

    Parameters:
        string: The string to convert

    Returns:
        The updated string.
    """
    return "\\fI" + string + "\\fR"


def do_groffautoemphasis(string: str) -> str:
    """Automatically mark uppercase words as Groff emphasis.

    Parameters:
        string: The string to convert.

    Returns:
        The updated string.
    """
    return re.sub(r"(\b[A-Z_0-9]{2,}\b)", r"\\fI\1\\fR", string)


def do_groffautostrong(string: str) -> str:
    """Automatically mark words starting with `-` or `--` as Groff strong.

    Parameters:
        string: The string to convert.

    Returns:
        The updated string.
    """
    return re.sub(r"(--?[\w-]+=?)", r"\\fB\1\\fR", string)


def do_groffauto(string: str, *, escape: bool = True) -> str:
    """Convert a string to the Groff format.

    Parameters:
        string: The string to convert.
        escape: Whether to escape the result.

    Returns:
        A Groff string.
    """
    string = do_groffautoemphasis(string)
    string = do_groffautostrong(string)
    if escape:
        string = do_groffautoescape(string)
    return string


def do_firstword(string: str, delimiters: str = " ") -> str:
    """Get the first word of a string.

    Parameters:
        string: The string.
        delimiters: The delimiter characters.


    Returns:
        The string's first word.
    """
    # FIXME: maybe use a regex instead: ^[\w_]+
    for i, char in enumerate(string):
        if char in delimiters:
            return string[:i]
    return string


def do_body(string_or_list: str | Sequence[str], delimiter: str = " ") -> str | None:
    """Get the body of a text.

    Parameters:
        string_or_list: Given text.


    Returns:
        The text's body.
    """
    if isinstance(string_or_list, str):
        return string_or_list.split(delimiter, 1)[1]
    if isinstance(string_or_list, list):
        return "\n".join(string_or_list[1:])
    return None


def do_firstline(string_or_list: str | Sequence[str]) -> str | None:
    """Get the first line of a text.

    Parameters:
        string_or_list: Given text.


    Returns:
        The text's first line.
    """
    if isinstance(string_or_list, str):
        return string_or_list.split("\n", 1)[0]
    if isinstance(string_or_list, list):
        return string_or_list[0]
    return None


def console_width(default: int = 80) -> int:
    """Return current console width.

    Parameters:
        default: The default value if width cannot be retrieved.

    Returns:
        The console width.
    """
    # only solution that works with stdin redirected from file
    # https://stackoverflow.com/questions/566746
    return get_terminal_size((default, 20)).columns


def do_smartwrap(text: str, indent: int = 4, width: int | None = None, *, indentfirst: bool = True) -> str:
    """Smartly wrap the given text.

    Parameters:
        text: The text to wrap.
        indent: The indentation to use (number of spaces).
        width: The desired text width.
        indentfirst: Whether to indent the first line too.

    Returns:
        The wrapped text.
    """
    if width is None or width < 0:
        c_width = console_width(default=79)
        if width is None:
            width = c_width or 79
        else:
            width += c_width

    indent_str = indent * " "
    to_join = defaultdict(lambda: False)
    lines = text.split("\n")
    previous = True
    for i, line in enumerate(lines):
        if not (line == "" or line[0] in (" ", "\t")):
            if previous:
                to_join[i] = True
            previous = True
        else:
            previous = False
    joined_lines = [lines[0]]
    for i in range(1, len(lines)):
        if to_join[i]:
            joined_lines.append(" " + lines[i])
        else:
            joined_lines.append("\n" + lines[i])
    new_text = "".join(joined_lines)
    new_text_lines = new_text.split("\n")
    wrapper = textwrap.TextWrapper(subsequent_indent=indent_str)
    wrap_indented_text_lines = []
    first_line = new_text_lines[0]
    if not (first_line == "" or first_line[0] in (" ", "\t")):
        if indentfirst:
            wrapper.width = width
            wrapper.initial_indent = indent_str
        else:
            wrapper.width = width - indent
            wrapper.initial_indent = ""
        wrap_indented_text_lines.append(wrapper.fill(first_line))
    elif first_line:
        wrap_indented_text_lines.append(indent_str + first_line)
    else:
        wrap_indented_text_lines.append("")
    wrapper.width = width
    wrapper.initial_indent = indent_str
    for line in new_text_lines[1:]:
        if not (line == "" or line[0] in (" ", "\t")):
            wrap_indented_text_lines.append(wrapper.fill(line))
        elif line:
            wrap_indented_text_lines.append(indent_str + line)
        else:
            wrap_indented_text_lines.append("")
    return "\n".join(wrap_indented_text_lines)


def do_format(string: str, *args: Any, **kwargs: Any) -> str:
    """Override Jinja's format filter to use format method instead of % operator.

    Parameters:
        string: The string to format.
        *args: Arguments passed to `str.format`.
        **kwargs: Keyword arguments passed to `str.format`.


    Returns:
        The formatted string.
    """
    return string.format(*args, **kwargs)


@pass_environment
def do_groupby(
    environment: Environment,
    value: Sequence[Any],
    attribute: str,
    *,
    sort: bool = True,
) -> list[tuple[str, list[Any]]]:
    """Override Jinja's groupby filter to add un(sort) option.

    Parameters:
        environment: Passed by Jinja.
        value: The value to group.
        attribute: The attribute to use for grouping/sorting.

    Returns:
        The value grouped by the given attribute.
    """
    expr = make_attrgetter(environment, attribute)

    # Original behavior: groups are sorted
    if sort:
        return [_GroupTuple(key, list(values)) for key, values in groupby(sorted(value, key=expr), expr)]

    # Added behavior: original order of appearance is kept
    all_groups = [expr(_) for _ in value]
    group_set = set()
    unique_groups = []
    for group in all_groups:
        if group not in group_set:
            unique_groups.append(group)
            group_set.add(group)
    grouped = {k: list(v) for k, v in groupby(sorted(value, key=expr), expr)}
    return [_GroupTuple(group, grouped[group]) for group in unique_groups]


def do_escape(value: str, except_starts_with: list[str] | None = None) -> str:
    """Escape (HTML) given text.

    Parameters:
        except_starts_with: Each line starting with at least one of the prefixes
            listed in this parameter will not be escaped.

    Returns:
        The escaped text.
    """
    predicate = (
        (lambda line: any(line.startswith(string) for string in except_starts_with))
        if except_starts_with is not None
        else lambda line: False
    )
    return "\n".join(line if line == "" or predicate(line) else escape(line) for line in value.split("\n"))


FILTERS = {
    "groffstrong": do_groffstrong,
    "groffemphasis": do_groffemphasis,
    "groffautostrong": do_groffautostrong,
    "groffautoemphasis": do_groffautoemphasis,
    "groffautoescape": do_groffautoescape,
    "groffauto": do_groffauto,
    "groupby": do_groupby,
    "firstword": do_firstword,
    "firstline": do_firstline,
    "body": do_body,
    "smartwrap": do_smartwrap,
    "format": do_format,
    "escape": do_escape,
}
"""The Jinja filters."""
