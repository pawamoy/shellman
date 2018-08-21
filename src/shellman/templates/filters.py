import re


def groff_auto_escape(string):
    return string.replace('-', '\-').replace("'", "\\'").replace('.', '\.').replace('$', '\\f$')


def groff_strong(string):
    return '\\fB' + string + '\\fR'


def groff_emphasis(string):
    return '\\fI' + string + '\\fR'


def groff_auto_emphasis(string):
    return re.sub(r'([A-Z_]+)', r'\\fI\1\\fR', string)


def groff_auto_strong(string):
    return re.sub(r'(--?[a-z0-9-]+=?)', r'\\fB\1\\fR', string)


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
    'first_word': first_word,
    'first_line': first_line,
    'body': body,
    'trim_join': trim_join
}
