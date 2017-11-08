# -*- coding: utf-8 -*-

"""
Section module.

This module contains the Section class.
"""

# import argparse


class Section(object):
    """
    Section class.

    A section is a simple object with two attributes: occurrences and lines.
    """

    def __init__(self,
                 name,
                 verbose_name,
                 unique=False,
                 multiline=True):
        """
        Init method.

        Args:
            unique (bool): must this section must be unique?
            multiline (bool): can this section have multiple lines?
        """
        self.name = name
        self.verbose_name = verbose_name
        self.unique = unique
        self.multiline = multiline


class AuthorSection(Section):
    def __init__(self):
        super(AuthorSection, self).__init__(
            'author', 'Authors', unique=False, multiline=False)


class BugSection(Section):
    def __init__(self):
        super(BugSection, self).__init__(
            'bug', 'Bugs', unique=False, multiline=False)


class BriefSection(Section):
    def __init__(self):
        super(BriefSection, self).__init__(
            'brief', 'Brief', unique=True, multiline=False)


class CaveatSection(Section):
    def __init__(self):
        super(CaveatSection, self).__init__(
            'caveat', 'Caveats', unique=False, multiline=True)


class CopyrightSection(Section):
    def __init__(self):
        super(CopyrightSection, self).__init__(
            'copyright', 'Copyright', unique=True, multiline=True)


class DateSection(Section):
    def __init__(self):
        super(DateSection, self).__init__(
            'date', 'Date', unique=True, multiline=False)


class DescSection(Section):
    def __init__(self):
        super(DescSection, self).__init__(
            'desc', 'Description', unique=True, multiline=True)


class EnvSection(Section):
    def __init__(self):
        super(EnvSection, self).__init__(
            'env', 'Environment variables', unique=False, multiline=True)


class ErrorSection(Section):
    def __init__(self):
        super(ErrorSection, self).__init__(
            'error', 'Errors', unique=False, multiline=True)


class ExampleSection(Section):
    def __init__(self):
        super(ExampleSection, self).__init__(
            'example', 'Examples', unique=False, multiline=True)


class ExitSection(Section):
    def __init__(self):
        super(ExitSection, self).__init__(
            'exit', 'Exit status', unique=False, multiline=True)


class FileSection(Section):
    def __init__(self):
        super(FileSection, self).__init__(
            'file', 'Files', unique=False, multiline=True)


class HistorySection(Section):
    def __init__(self):
        super(HistorySection, self).__init__(
            'history', 'History', unique=True, multiline=True)


class LicenseSection(Section):
    def __init__(self):
        super(LicenseSection, self).__init__(
            'license', 'License', unique=True, multiline=True)


class NoteSection(Section):
    def __init__(self):
        super(NoteSection, self).__init__(
            'note', 'Notes', unique=False, multiline=True)


class OptionSection(Section):
    def __init__(self):
        super(OptionSection, self).__init__(
            'option', 'Options', unique=False, multiline=True)


class SeeAlsoSection(Section):
    def __init__(self):
        super(SeeAlsoSection, self).__init__(
            'seealso', 'See also', unique=False, multiline=False)


class StderrSection(Section):
    def __init__(self):
        super(StderrSection, self).__init__(
            'stderr', 'Standard error', unique=False, multiline=True)


class StdinSection(Section):
    def __init__(self):
        super(StdinSection, self).__init__(
            'stdin', 'Standard input', unique=False, multiline=True)


class StdoutSection(Section):
    def __init__(self):
        super(StdoutSection, self).__init__(
            'stdout', 'Standard output', unique=False, multiline=True)


class UsageSection(Section):
    def __init__(self):
        super(UsageSection, self).__init__(
            'usage', 'Usage', unique=False, multiline=True)


class VersionSection(Section):
    def __init__(self):
        super(VersionSection, self).__init__(
            'version', 'Version', unique=True, multiline=False)



# TODO: do checks on sections and grouped sections (a grouped section cannot be a section)
# TODO: maybe create a GroupedSection class

SECTIONS = {}
DEFAULT_SECTIONS = {
    'author': Section('author', 'Authors', '+', 1),
    'bug': Section('bug', 'Bugs', '+', '+'),
    'brief': Section('brief', 'Brief', 1, 1),
    'caveat': Section('caveat', 'Caveats', '+', '+'),
    'copyright': Section('copyright', 'Copyright', 1, '+'),
    'date': Section('date', 'Date', 1, 1),
    'desc': Section('desc', 'Description', 1, '+'),
    'env': Section('env', 'Environment variables', '+', '+', True),
    'error': Section('error', 'Errors', '+', '+', True),
    'example': Section('example', 'Examples', '+', '+', True),
    'exit': Section('exit', 'Exit status', '+', '+', True),
    'file': Section('file', 'Files', '+', '+', True),
    'history': Section('history', 'History', 1, '+'),
    'license': Section('license', 'License', 1, '+'),
    'note': Section('note', 'Notes', '+', '+'),
    'option': Section('option', 'Options', '+', '+', True),
    'seealso': Section('seealso', 'See also', '+', 1),
    'stderr': Section('stderr', 'Stderr', '+', '+'),
    'stdin': Section('stdin', 'Stdin', '+', '+'),
    'stdout': Section('stdout', 'Stdout', '+', '+'),
    'usage': Section('usage', 'Usage', '+', '+'),
    'version': Section('version', 'Version', 1, 1)
}

GROUP_SECTIONS = {}
DEFAULT_GROUP_SECTIONS = {
    'fn': {
        'fn': Section('fn', 'Function', 1, 1),
        'brief': Section('brief', 'Brief', 1, 1),
        'desc': Section('desc', 'Description', 1, '+'),
        'param': Section('param', 'Parameters', '+', '+', True),
        'pre': Section('pre', 'Pre-conditions', '+', '+'),
        'return': Section('return', 'Return code', '+', '+', True),
        'seealso': Section('seealso', 'See also', '+', 1),
        'stderr': Section('stderr', 'Standard error', '+', '+'),
        'stdin': Section('stdin', 'Standard input', '+', '+'),
        'stdout': Section('stdout', 'Standard output', '+', '+')
    }
}


# def dispatch_sections(sections):
#     for section in sections:
#         if section.type == 'script':
#             SCRIPT_SECTIONS[section.name] = section
#         elif section.type == 'function':
#             FN_SECTIONS[section.name] = section
#         elif section.type == 'both':
#             SCRIPT_SECTIONS[section.name] = section
#             FN_SECTIONS[section.name] = section


def add_default_sections():
    SECTIONS.update(DEFAULT_SECTIONS)


def add_default_group_sections():
    GROUP_SECTIONS.update(DEFAULT_GROUP_SECTIONS)


# def transform_sections_values(section, section, params):
#     if not section or not section:
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
#     return section, section, params
#
#
# # TODO: finish writing this
# def parse_yaml_sections(path):
#     import yaml
#     with open(path) as stream:
#         data = yaml.safe_load(stream)
#     for section_name, section_values in data.items():
#         print(section_name, section_values)
#
#
# def parse_string_sections(arg):
#     sections = []
#     for section in arg.split('|'):
#         params = section.split(',')
#         if len(params) < 2:
#             raise argparse.ArgumentTypeError('ERROR')
#         section_name, section_name = params[0], params[1]
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
#         section_name, section_name, params = transform_sections_values(
#             section_name, section_name, params_values)
#         sections.append(Section(section_name, section_name, *params_values))
#     return sections
