import re
import shutil
import textwrap
from collections import defaultdict


def groff_auto_escape(string):
    return string\
        .replace('-', '\\-')\
        .replace("'", "\\'")\
        .replace('"', '\\"')\
        .replace('.', '\\.')\
        .replace('$', '\\f$')


def groff_strong(string):
    return '\\fB' + string + '\\fR'


def groff_emphasis(string):
    return '\\fI' + string + '\\fR'


def groff_auto_emphasis(string):
    return re.sub(r'(\b[A-Z_0-9]{2,}\b)', r'\\fI\1\\fR', string)


def groff_auto_strong(string):
    return re.sub(r'(--?[\w-]+=?)', r'\\fB\1\\fR', string)


def groff_auto(string, escape=True):
    string = groff_auto_emphasis(string)
    string = groff_auto_strong(string)
    if escape:
        string = groff_auto_escape(string)
    return string


def first_word(string, delimiter=' '):
    return string.split(delimiter)[0]


def body(string_or_list, delimiter=' '):
    if isinstance(string_or_list, str):
        return string_or_list.split(delimiter, 1)[1]
    elif isinstance(string_or_list, list):
        return '\n'.join(string_or_list[1:])


def first_line(string_or_list):
    if isinstance(string_or_list, str):
        return string_or_list.split('\n', 1)[0]
    elif isinstance(string_or_list, list):
        return string_or_list[0]


def trim_join(string_list, join_str=' '):
    return join_str.join(s.trim() for s in string_list)


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
    return shutil.get_terminal_size((default, 20)).columns


def smart_width(text, indent=4, width=None):
    if width is None or width < 0:
        c_width = console_width(default=79)
        if width is None:
            width = c_width
        else:
            width += c_width

    indent_str = indent * ' '
    to_join = defaultdict(lambda: False)
    lines = text.split('\n')
    previous = True
    for i, line in enumerate(lines):
        if not (line == '' or line[0] in (' ', '\t')):
            if previous:
                to_join[i] = True
            previous = True
        else:
            previous = False
    joined_lines = [lines[0]]
    for i in range(1, len(lines)):
        if to_join[i]:
            joined_lines.append(' ' + lines[i])
        else:
            joined_lines.append('\n' + lines[i])
    new_text = ''.join(joined_lines)
    new_text_lines = new_text.split('\n')
    wrap_indented_text_lines = []
    for line in new_text_lines:
        if not (line == '' or line[0] in (' ', '\t')):
            wrap_indented_text_lines.append(
                textwrap.fill(
                    line,
                    width,
                    initial_indent=indent_str,
                    subsequent_indent=indent_str
                )
            )
        else:
            wrap_indented_text_lines.append(indent_str + line)
    return '\n'.join(wrap_indented_text_lines)


def format(s, *args, **kwargs):
    return s.format(*args, **kwargs)


FILTERS = {
    'groff_auto_escape': groff_auto_escape,
    'groff_strong': groff_strong,
    'groff_emphasis': groff_emphasis,
    'groff_auto_strong': groff_auto_strong,
    'groff_auto_emphasis': groff_auto_emphasis,
    'groff_auto': groff_auto,
    'first_word': first_word,
    'first_line': first_line,
    'body': body,
    'trim_join': trim_join,
    'smart_width': smart_width,
    'format': format
}
