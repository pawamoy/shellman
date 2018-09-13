import re
try:
    from shutil import get_terminal_size
except ImportError:
    from backports.shutil_get_terminal_size import get_terminal_size
import textwrap
from collections import defaultdict
from itertools import groupby

from jinja2.filters import _GroupTuple, environmentfilter, make_attrgetter
from jinja2.utils import escape


def do_groffautoescape(string):
    return (
        string.replace("-", "\\-")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace(".", "\\.")
        .replace("$", "\\f$")
    )


def do_groffstrong(string):
    return "\\fB" + string + "\\fR"


def do_groffemphasis(string):
    return "\\fI" + string + "\\fR"


def do_groffautoemphasis(string):
    return re.sub(r"(\b[A-Z_0-9]{2,}\b)", r"\\fI\1\\fR", string)


def do_groffautostrong(string):
    return re.sub(r"(--?[\w-]+=?)", r"\\fB\1\\fR", string)


def do_groffauto(string, escape=True):
    string = do_groffautoemphasis(string)
    string = do_groffautostrong(string)
    if escape:
        string = do_groffautoescape(string)
    return string


def do_firstword(string, delimiters=" "):
    # FIXME: maybe use a regex instead: ^[\w_]+
    for i, char in enumerate(string):
        if char in delimiters:
            return string[:i]
    return string


def do_body(string_or_list, delimiter=" "):
    if isinstance(string_or_list, str):
        return string_or_list.split(delimiter, 1)[1]
    elif isinstance(string_or_list, list):
        return "\n".join(string_or_list[1:])


def do_firstline(string_or_list):
    if isinstance(string_or_list, str):
        return string_or_list.split("\n", 1)[0]
    elif isinstance(string_or_list, list):
        return string_or_list[0]


def console_width(default=80):
    """
    Return current console width.

    Args:
        default (int): default value if width cannot be retrieved.

    Returns:
        int: console width.
    """
    # only solution that works with stdin redirected from file
    # https://stackoverflow.com/questions/566746
    return get_terminal_size((default, 20)).columns


def do_smartwrap(text, indent=4, width=None, indentfirst=True):
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


# Override Jinja2's format filter to use format method instead of % operator
def do_format(s, *args, **kwargs):
    return s.format(*args, **kwargs)


# Override Jinja2's groupby filter to add un(sort) option
@environmentfilter
def do_groupby(environment, value, attribute, sort=True):
    expr = make_attrgetter(environment, attribute)

    # Original behavior: groups are sorted
    if sort:
        return [
            _GroupTuple(key, list(values))
            for key, values in groupby(sorted(value, key=expr), expr)
        ]

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


def do_escapetextonly(value):
    return "\n".join(
        line if line == "" or line[0] in " \t" else escape(line)
        for line in value.split("\n")
    )


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
    "escapetextonly": do_escapetextonly,
}
