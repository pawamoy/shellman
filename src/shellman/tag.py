# -*- coding: utf-8 -*-

"""
Tag module.

This module contains the Tag class.

It also contains constants:

- the TAGS dictionary which represents the available tags that
  shellman will recognize.
- the FN_TAG string which is the tag that start a function documentation
  paragraph.
- the FN_TAGS dictionary which represents the available function tags that
  shellman will recognize.
- and the FUNCTION_ORDER list which represents the order in which the
  different function documentation tags will be written to stdout.
"""

# import argparse


class Tag(object):
    """
    Tag class.

    A tag is a simple object with two attributes: occurrences and lines.
    """

    def __init__(self,
                 name,
                 section_name,
                 occurrences=1,
                 lines=1,
                 header=False,
                 type='script'):
        """
        Init method.

        Args:
            occurrences (const/int): can be '+' or 1.
            lines (const/int): can be '+' or 1.
        """
        self.name = name
        self.section_name = section_name
        self.occurrences = occurrences
        self.lines = lines
        self.header = header
        self.type = type


# TODO: do checks on tags and grouped tags (a grouped tag cannot be a tag)
# TODO: maybe create a GroupedTag class

TAGS = {}
DEFAULT_TAGS = {
    'author': Tag('author', 'Authors', '+', 1),
    'bug': Tag('bug', 'Bugs', '+', '+'),
    'brief': Tag('brief', 'Brief', 1, 1),
    'caveat': Tag('caveat', 'Caveats', '+', '+'),
    'copyright': Tag('copyright', 'Copyright', 1, '+'),
    'date': Tag('date', 'Date', 1, 1),
    'desc': Tag('desc', 'Description', 1, '+'),
    'env': Tag('env', 'Environment variables', '+', '+', True),
    'error': Tag('error', 'Errors', '+', '+', True),
    'example': Tag('example', 'Examples', '+', '+', True),
    'exit': Tag('exit', 'Exit status', '+', '+', True),
    'file': Tag('file', 'Files', '+', '+', True),
    'history': Tag('history', 'History', 1, '+'),
    'license': Tag('license', 'License', 1, '+'),
    'note': Tag('note', 'Notes', '+', '+'),
    'option': Tag('option', 'Options', '+', '+', True),
    'seealso': Tag('seealso', 'See also', '+', 1),
    'stderr': Tag('stderr', 'Stderr', '+', '+'),
    'stdin': Tag('stdin', 'Stdin', '+', '+'),
    'stdout': Tag('stdout', 'Stdout', '+', '+'),
    'usage': Tag('usage', 'Usage', '+', '+'),
    'version': Tag('version', 'Version', 1, 1)
}

GROUP_TAGS = {}
DEFAULT_GROUP_TAGS = {
    'fn': {
        'fn': Tag('fn', 'Function', 1, 1),
        'brief': Tag('brief', 'Brief', 1, 1),
        'desc': Tag('desc', 'Description', 1, '+'),
        'param': Tag('param', 'Parameters', '+', '+', True),
        'pre': Tag('pre', 'Pre-conditions', '+', '+'),
        'return': Tag('return', 'Return code', '+', '+', True),
        'seealso': Tag('seealso', 'See also', '+', 1),
        'stderr': Tag('stderr', 'Standard error', '+', '+'),
        'stdin': Tag('stdin', 'Standard input', '+', '+'),
        'stdout': Tag('stdout', 'Standard output', '+', '+')
    }
}


# def dispatch_tags(tags):
#     for tag in tags:
#         if tag.type == 'script':
#             SCRIPT_TAGS[tag.name] = tag
#         elif tag.type == 'function':
#             FN_TAGS[tag.name] = tag
#         elif tag.type == 'both':
#             SCRIPT_TAGS[tag.name] = tag
#             FN_TAGS[tag.name] = tag


def add_default_tags():
    TAGS.update(DEFAULT_TAGS)


def add_default_group_tags():
    GROUP_TAGS.update(DEFAULT_GROUP_TAGS)


# def transform_tags_values(tag, section, params):
#     if not tag or not section:
#         raise argparse.ArgumentTypeError('ERROR')
#     if params[0] == '1':
#         params[0] = 1
#     elif params[0] not in (1, '+'):
#         raise argparse.ArgumentTypeError('ERROR')
#     if params[1] == '1':
#         params[1] = 1
#     elif params[1] not in (1, '+'):
#         raise argparse.ArgumentTypeError('ERROR')
#     if params[2] in ('y', 'yes', 1, '1', 'true', 'True'):
#         params[2] = True
#     elif params[2] in ('n', 'no', 0, '0', 'false', 'False'):
#         params[2] = False
#     elif params[2] not in (False, True):
#         raise argparse.ArgumentTypeError('ERROR')
#     if params[3] == 's':
#         params[3] = 'script'
#     elif params[3] == 'f':
#         params[3] = 'function'
#     elif params[3] == 'b':
#         params[3] = 'both'
#     elif params[3] not in ('script', 'function', 'both'):
#         raise argparse.ArgumentTypeError('ERROR')
#     return tag, section, params
#
#
# # TODO: finish writing this
# def parse_yaml_tags(path):
#     import yaml
#     with open(path) as stream:
#         data = yaml.safe_load(stream)
#     for tag_name, tag_values in data.items():
#         print(tag_name, tag_values)
#
#
# def parse_string_tags(arg):
#     tags = []
#     for tag in arg.split('|'):
#         params = tag.split(',')
#         if len(params) < 2:
#             raise argparse.ArgumentTypeError('ERROR')
#         tag_name, section_name = params[0], params[1]
#         params_values = [1, 1, False, 's']
#         if len(params) > 2:
#             kw = False
#             for i, param in enumerate(params[2:]):
#                 if '=' in param:
#                     kw = True
#                     kw_key, kw_value = param.split('=', 1)
#                     if kw_key in ('o=', 'occurrences='):
#                         params_values[0] = kw_value
#                     elif kw_key in ('l=', 'lines='):
#                         params_values[1] = kw_value
#                     elif kw_key in ('h=', 'header='):
#                         params_values[2] = kw_value
#                     elif kw_key in ('t=', 'type='):
#                         params_values[3] = kw_value
#                     else:
#                         raise argparse.ArgumentTypeError('ERROR')
#                 elif kw:
#                     raise argparse.ArgumentTypeError('ERROR')
#                 else:
#                     params_values[i] = param
#         tag_name, section_name, params = transform_tags_values(
#             tag_name, section_name, params_values)
#         tags.append(Tag(tag_name, section_name, *params_values))
#     return tags
