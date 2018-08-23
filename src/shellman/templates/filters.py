import re


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
    'trim_join': trim_join
}
