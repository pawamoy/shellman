# -*- coding: utf-8 -*-

"""
Formatter module.

This module contains the classes to render the documentation
in different formats.
"""

from __future__ import print_function

import sys

from . import __version__
from .tag import TAGS, GROUP_TAGS


def get_formatter(fmt):
    """
    Formatter class getter, given a format.

    Args:
        fmt (str): format for which to get a formatter class

    Returns:
        a subclass of BaseFormatter class
    """
    if fmt == 'text':
        return TextFormatter
    elif fmt == 'man':
        return ManFormatter
    elif fmt == 'markdown':
        return MarkdownFormatter
    else:
        raise ValueError('shellman: error: incorrect format %s' % fmt)


class Section(object):
    def __init__(self, name, contents=None):
        self.name = name
        self.contents = contents


class Formatter(object):
    def __init__(self,
                 sections=None,
                 group_sections=None,
                 remove_leading_spaces=1,
                 remove_trailing_spaces=True,
                 concatenate_lines=True,
                 concatenation_string=' ',
                 keep_empty_lines=True,
                 keep_newline_when_post_indent_multiple_of=2):
        self.sections = sections
        self.group_sections = group_sections
        self.remove_leading_spaces = remove_leading_spaces
        self.remove_trailing_spaces = remove_trailing_spaces
        self.concatenate_lines = concatenate_lines
        self.concatenation_string = concatenation_string
        self.keep_empty_lines = keep_empty_lines
        self.keep_newline_when_post_indent_multiple_of = keep_newline_when_post_indent_multiple_of

    def format(self, cleaned_docs):
        minified = cleaned_docs.minified()
        sections = []
        for section in self.sections:
            if section in minified.blocks:
                print(self.format_section(TAGS[section].section_name,
                                          minified.blocks[section]))
            elif section in minified.groups:
                for group in minified.groups:
                    for group_section in self.group_sections:
                        pass  # output group section

    # TODO: write a format function that follows the original file docs order
    def format_follow(self, cleaned_docs):
        pass

    def format_section(self, name, contents):
        return '%s\n%s' % (name, ''.join(self.format_lines(l) for l in contents))

    def format_lines(self, values):
        return ' '.join(values)


class TextFormatter(Formatter):
    def format_lines(self, values):
        line = ''
        for value in values:
            if not value:
                if self.keep_empty_lines:
                    line += '\n\n'
                continue
            if self.remove_leading_spaces:
                count = self.remove_leading_spaces
                while value[0] == ' ' and count > 0:
                    value = value[1:]
                    count -= 1
            if self.remove_trailing_spaces:
                value = value.rstrip(' ')
            if not self.concatenate_lines:
                line += value + '\n'
                continue
            if self.keep_newline_when_post_indent_multiple_of == 0:
                value += '\n'
            elif (self.keep_newline_when_post_indent_multiple_of and
                      (len(value) - len(value.lstrip(' ')) %
                          self.keep_newline_when_post_indent_multiple_of)) == 0:
                    value += '\n'
            else:
                value += ' '
            line += value
        return line + '\n'

#
# class BaseFormatter(object):
#     """
#     Formatter base class.
#
#     A formatter class has a SECTIONS attribute to know in which order
#     to output the different documentation sections (list of str).
#     """
#
#     SECTIONS = ()
#     FUNCTION_SECTIONS = ()
#
#     def __init__(self,
#                  doc,
#                  output=None,
#                  sections=None,
#                  function_sections=None):
#         """
#         Init method.
#
#         Args:
#             doc (dict): doc generated through Doc object.
#
#         Attributes:
#             doc (dict): doc given to init.
#             render (dict): mapping between doc section name and render method.
#         """
#         self.doc = doc
#         if output in (None, sys.stdout):
#             self.output = sys.stdout
#         else:
#             self.output = open(output, 'w')
#         if sections:
#             self.sections = sections
#         else:
#             self.sections = self.__class__.SECTIONS
#         if function_sections:
#             self.function_sections = function_sections
#         else:
#             self.function_sections = self.__class__.FUNCTION_SECTIONS
#
#     def out(self, *args, **kwargs):
#         """Wrapper around print to write into self.output."""
#         print(*args, file=self.output, **kwargs)
#
#     def esc(self, string):
#         """Escape some special characters in the string."""
#         return string
#
#     def write(self):
#         """Write documentation on stdout."""
#         for section in self.sections:
#             self.render_section(section)
#
#     def render_section(self, section):
#         if section == 'fn' and '_fn' in self.doc and self.doc['_fn']:
#             self.render_functions()
#         elif section in self.doc and self.doc[section]:
#             related_tag = SCRIPT_TAGS.get(section, None)
#             if related_tag is None:
#                 return
#             self.render_tag(related_tag, self.doc[section])
#
#     def render_functions(self):
#         # override to add content here
#         # call super here
#         for fn in self.doc['_fn']:
#             for function_section in self.function_sections:
#                 if function_section in fn and fn[function_section]:
#                     self.render_function_section(function_section, fn)
#         # override to add content here
#
#     def render_function_section(self, section, fn):
#         related_tag = FN_TAGS.get(section, None)
#         if related_tag is None:
#             return
#         self.render_function_tag(related_tag, fn[section])
#
#     def render_tag(self, tag, doc):
#         render = getattr(self, 'render_' + tag.name, None)
#         if render is not None:
#             render(tag, doc)
#             return
#         self._render_tag(tag, doc)
#
#     def render_function_tag(self, tag, doc):
#         render = getattr(self, 'render_function_' + tag.name, None)
#         if render is not None:
#             render(tag, doc)
#             return
#         self._render_tag(tag, doc, indent='    ')
#
#     def _render_tag(self, tag, doc, indent=''):
#         if tag.occurrences == 1:
#             if tag.lines == 1:
#                 if tag.header:
#                     self.render_one_one_header(tag, doc, indent)
#                 else:
#                     self.render_one_one_no_header(tag, doc, indent)
#             else:
#                 if tag.header:
#                     self.render_one_many_header(tag, doc, indent)
#                 else:
#                     self.render_one_many_no_header(tag, doc, indent)
#         else:
#             if tag.lines == 1:
#                 if tag.header:
#                     self.render_many_one_header(tag, doc, indent)
#                 else:
#                     self.render_many_one_no_header(tag, doc, indent)
#             else:
#                 if tag.header:
#                     self.render_many_many_header(tag, doc, indent)
#                 else:
#                     self.render_many_many_no_header(tag, doc, indent)
#
#     def render_one_one_header(self, tag, value, indent):
#         """Render a (one occurrence, one line, header) tag."""
#         pass
#
#     def render_one_one_no_header(self, tag, value, indent):
#         """Render a (one occurrence, one line, no header) tag."""
#         pass
#
#     def render_one_many_header(self, tag, value, indent):
#         """Render a (one occurrence, many lines, header) tag."""
#         pass
#
#     def render_one_many_no_header(self, tag, value, indent):
#         """Render a (one occurrence, many lines, no header) tag."""
#         pass
#
#     def render_many_one_header(self, tag, value, indent):
#         """Render a (many occurrences, one line, header) tag."""
#         pass
#
#     def render_many_one_no_header(self, tag, value, indent):
#         """Render a (many occurrences, one line, no header) tag."""
#         pass
#
#     def render_many_many_header(self, tag, value, indent):
#         """Render a (many occurrences, many lines, header) tag."""
#         pass
#
#     def render_many_many_no_header(self, tag, value, indent):
#         """Render a (many occurrences, many lines, no header) tag."""
#         pass
#
#
# class ManFormatter(BaseFormatter):
#     """
#     Man page formatter class.
#
#     This formatter will output documentation as a man page.
#     """
#
#     SECTIONS = (
#         'brief',
#         'usage',
#         'desc',
#         'option',
#         'env',
#         'file',
#         'example',
#         'exit',
#         'fn',
#         'error',
#         'bug',
#         'caveat',
#         'author',
#         'copyright',
#         'license',
#         'history',
#         'note',
#         'seealso',
#     )
#     FUNCTION_SECTIONS = (
#         'fn',
#         'brief',
#         'desc',
#         'param',
#         'stdin',
#         'stdout',
#         'stderr',
#         'return',
#         'pre',
#         'seealso',
#     )
#
#     def esc(self, string):
#         if string:
#             return string.replace('-', '\\-').replace("'", "\\(cq")
#         return string
#
#     def header(self):
#         self.out('.if n.ad l')
#         self.out('.nh')
#         self.out('.TH %s 1 "%s" "Shellman %s" "User Commands"' % (
#             self.doc['_file'], self.esc(self.doc['date']) or '', __version__))
#
#     def render_one_many(self, tag, value):
#         if value:
#             self.out('.SH "%s"' % tag)
#             self.out('%s' % self.esc(''.join(value)))
#
#     def render_many_many(self, tag, value):
#         if value:
#             self.out('.SH "%s"' % tag)
#             for v in value:
#                 if len(v) == 1:
#                     s = v[0].split(' ')
#                     h, b = s[0], ' '.join(s[1:]).rstrip('\n')
#                 else:
#                     h, b = v[0].rstrip('\n'), ''.join(v[1:]).rstrip('\n')
#                 self.out('.IP "\\fB%s\\fR" 4' % h)
#                 self.out(self.esc(b))
#
#     def render_many_many_no_head(self, tag, value):
#         if value:
#             self.out('.SH "%s"' % tag)
#             for v in value:
#                 self.out('%s' % self.esc(''.join(v)))
#
#     def render_authors(self, tag):
#         if self.doc['author']:
#             self.out('.SH "%s"' % tag)
#             for author in self.doc['author']:
#                 self.out('.br')
#                 self.out(author)
#
#     def render_brief(self, tag):
#         if self.doc['brief']:
#             self.out('.SH "%s"' % tag)
#             # pylama:ignore=W1401
#             self.out('%s \- %s' % (self.doc['_file'],
#                                    self.esc(self.doc['brief'])))
#
#     def render_bugs(self, tag):
#         self.render_many_many_no_head(tag, self.doc['bug'])
#
#     def render_caveats(self, tag):
#         self.render_many_many_no_head(tag, self.doc['caveat'])
#
#     def render_copyright(self, tag):
#         self.render_one_many(tag, self.doc['copyright'])
#
#     def render_date(self, tag):
#         pass
#
#     def render_description(self, tag):
#         self.render_one_many(tag, self.doc['desc'])
#
#     def render_environment_variables(self, tag):
#         self.render_many_many(tag, self.doc['env'])
#
#     def render_errors(self, tag):
#         self.render_many_many_no_head(tag, self.doc['error'])
#
#     def render_examples(self, tag):
#         self.render_many_many(tag, self.doc['example'])
#
#     def render_exit_status(self, tag):
#         self.render_many_many(tag, self.doc['exit'])
#
#     def render_files(self, tag):
#         self.render_many_many(tag, self.doc['file'])
#
#     def render_function_fn(self, fn):
#         self.out('.IP "\\fB%s\\fR" 4' % self.esc(fn['fn']))
#
#     def render_function_brief(self, fn):
#         if fn['brief']:
#             self.out('%s' % self.esc(fn['brief']))
#             self.out('')
#
#     def render_function_desc(self, fn):
#         if fn['desc']:
#             self.out('%s' % self.esc(''.join(fn['desc'])))
#
#     def render_function_param(self, fn):
#         if fn['param']:
#             self.out('.ul')
#             self.out('Parameters:')
#             for param in fn['param']:
#                 if len(param) == 1:
#                     s = param[0].split(' ')
#                     param, desc = s[0], s[1:]
#                     self.out('  \\fB%-12s\\fR %s' % (
#                         param, self.esc(' '.join(desc)).rstrip('\n')))
#                 else:
#                     param, desc = param[0], param[1:]
#                     self.out('  \\fB%s\\fR' % self.esc(param).rstrip('\n'))
#                     self.out('    %s' % self.esc(''.join(desc)))
#             self.out('')
#
#     def render_function_pre(self, fn):
#         if fn['pre']:
#             self.out('.ul')
#             self.out('Preconditions:')
#             for pre in fn['pre']:
#                 self.out('  %s' % self.esc(''.join(pre)))
#             self.out('')
#
#     def render_function_return(self, fn):
#         if fn['return']:
#             self.out('.ul')
#             self.out('Return code:')
#             for ret in fn['return']:
#                 self.out('  %s' % self.esc(''.join(ret)))
#             self.out('')
#
#     def render_function_seealso(self, fn):
#         if fn['seealso']:
#             self.out('.ul')
#             self.out('See also:')
#             for seealso in fn['seealso']:
#                 self.out('  %s' % self.esc(''.join(seealso)))
#             self.out('')
#
#     def render_function_stderr(self, fn):
#         if fn['stderr']:
#             self.out('.ul')
#             self.out('Standard error:')
#             for stderr in fn['stderr']:
#                 self.out('  %s' % self.esc(''.join(stderr)))
#             self.out('')
#
#     def render_function_stdin(self, fn):
#         if fn['stdin']:
#             self.out('.ul')
#             self.out('Standard input:')
#             for stdin in fn['stdin']:
#                 self.out('  %s' % self.esc(''.join(stdin)))
#             self.out('')
#
#     def render_function_stdout(self, fn):
#         if fn['stdout']:
#             self.out('.ul')
#             self.out('Standard output:')
#             for stdout in fn['stdout']:
#                 self.out('  %s' % self.esc(''.join(stdout)))
#             self.out('')
#
#     def render_function(self, fn):
#         for order in FUNCTION_SECTIONS:
#             getattr(self, 'render_function_%s' % order)(fn)
#
#     def render_functions(self, tag):
#         if not self.doc['_fn']:
#             return
#
#         self.out('.SH "%s"' % tag)
#         # summary
#         for fn in self.doc['_fn']:
#             self.out('%s' % self.esc(fn['fn']))
#             self.out('.br')
#
#         # all
#         for fn in self.doc['_fn']:
#             self.render_function(fn)
#
#     def render_history(self, tag):
#         self.render_one_many(tag, self.doc['history'])
#
#     def render_license(self, tag):
#         self.render_one_many(tag, self.doc['license'])
#
#     def render_notes(self, tag):
#         self.render_many_many_no_head(tag, self.doc['note'])
#
#     def render_options(self, tag):
#         if not self.doc['option']:
#             return
#         self.out('.SH "%s"' % tag)
#         for option in self.doc['option']:
#             self.out('.IP "\\fB%s\\fR" 4' % option[0]
#                      .rstrip('\n')
#                      .replace(',', '\\fR,\\fB'))
#             sys.stdout.write(''.join(option[1:]))
#
#     def render_see_also(self, tag):
#         pass
#
#     def render_stderr(self, tag):
#         pass
#
#     def render_stdin(self, tag):
#         pass
#
#     def render_stdout(self, tag):
#         pass
#
#     def render_usage(self, tag):
#         if not self.doc['usage']:
#             return
#         self.out('.SH "%s"' % tag)
#         rep_reg_opt = re.compile(r'(--?[a-z0-9-]+=?)')
#         rep_reg_arg = re.compile(r'([A-Z]+)')
#         for usage in self.doc['usage']:
#             syn = ''.join(usage)
#             name, syn = syn.split(' ', 1)
#             syn = rep_reg_arg.sub(r'\\fI\1\\fR', syn)  # order is important!
#             syn = rep_reg_opt.sub(r'\\fB\1\\fR', syn)
#             self.out('.br')
#             sys.stdout.write('\\fB%s\\fR %s' % (
#                 name, self.esc(syn)))
#
#     def render_version(self, tag):
#         pass
#
#
# class MarkdownFormatter(BaseFormatter):
#     """
#     Markown formatter class.
#
#     This formatter will output documentation as Markdown.
#     """
#
#     SECTIONS = (
#         'brief',
#         'usage',
#         'desc',
#         'option',
#         'env',
#         'file',
#         'example',
#         'exit',
#         'fn',
#         'error',
#         'bug',
#         'caveat',
#         'author',
#         'copyright',
#         'license',
#         'history',
#         'note',
#         'seealso',
#     )
#     FUNCTION_SECTIONS = (
#         'fn',
#         'brief',
#         'desc',
#         'param',
#         'stdin',
#         'stdout',
#         'stderr',
#         'return',
#         'pre',
#         'seealso',
#     )
#
#     def header(self):
#         self.render_date(None)
#
#     def render_one_many(self, tag, value):
#         if value:
#             self.out(tag)
#             self.out('%s' % ''.join(value))
#             self.out('')
#
#     def render_many_many(self, tag, value):
#         if value:
#             self.out(tag)
#             for v in value:
#                 self.out('- `%s`:' % v[0].rstrip('\n'))
#                 if len(v) > 1:
#                     self.out('  %s' % ''.join(v[1:]).rstrip('\n'))
#             self.out('')
#
#     def render_many_many_no_head(self, tag, value):
#         if value:
#             self.out(tag)
#             for v in value:
#                 self.out('- %s' % v)
#             self.out('')
#
#     def render_authors(self, tag):
#         if self.doc['author']:
#             self.out('# Authors')
#             for v in self.doc['author']:
#                 self.out('- %s' % v)
#
#     def render_brief(self, tag):
#         self.out('**%s** - %s' % (self.doc['_file'], self.doc['brief']))
#
#     def render_bugs(self, tag):
#         self.render_many_many_no_head('# Bugs', self.doc['bug'])
#
#     def render_caveats(self, tag):
#         self.render_many_many_no_head('# Caveats', self.doc['caveat'])
#
#     def render_copyright(self, tag):
#         self.render_one_many('# Copyright', self.doc['copyright'])
#
#     def render_date(self, tag):
#         if self.doc['date']:
#             self.out('*Date: %s*' % self.doc['date'])
#             self.out('')
#
#     def render_description(self, tag):
#         if self.doc['desc']:
#             self.out('%s' % ''.join(self.doc['desc']))
#
#     def render_environment_variables(self, tag):
#         self.render_many_many('# Environment variables', self.doc['env'])
#
#     def render_errors(self, tag):
#         self.render_many_many_no_head('# Errors', self.doc['error'])
#
#     def render_examples(self, tag):
#         self.render_many_many('# Examples', self.doc['example'])
#
#     def render_exit_status(self, tag):
#         self.render_many_many('# Exit status', self.doc['exit'])
#
#     def render_files(self, tag):
#         self.render_many_many('# Files', self.doc['file'])
#
#     def render_function_fn(self, fn):
#         self.out('## %s' % fn['fn'])
#
#     def render_function_brief(self, fn):
#         if fn['brief']:
#             self.out('%s' % fn['brief'])
#             self.out('')
#
#     def render_function_desc(self, fn):
#         if fn['desc']:
#             self.out('%s' % fn['desc'])
#
#     def render_function_param(self, fn):
#         if fn['param']:
#             self.out('### Parameters')
#             for param in fn['param']:
#                 if len(param) == 1:
#                     s = param[0].split(' ')
#                     param, desc = s[0], s[1:]
#                     self.out('- `%s`: %s' % (
#                         param, ' '.join(desc).rstrip('\n')))
#                 else:
#                     param, desc = param[0], param[1:]
#                     self.out('- `%s`:' % param.rstrip('\n'))
#                     self.out('  %s' % ''.join(desc))
#             self.out('')
#
#     def render_function_pre(self, fn):
#         if fn['pre']:
#             self.out('### Preconditions')
#             self.out('%s' % fn['pre'])
#             self.out('')
#
#     def render_function_return(self, fn):
#         if fn['return']:
#             self.out('### Return code')
#             self.out('%s' % fn['return'])
#             self.out('')
#
#     def render_function_seealso(self, fn):
#         if fn['seealso']:
#             self.out('### See also')
#             self.out('%s' % fn['seealso'])
#             self.out('')
#
#     def render_function_stderr(self, fn):
#         if fn['stderr']:
#             self.out('### Standard error')
#             self.out('%s' % fn['stderr'])
#             self.out('')
#
#     def render_function_stdin(self, fn):
#         if fn['stdin']:
#             self.out('### Standard input')
#             self.out('%s' % fn['stdin'])
#             self.out('')
#
#     def render_function_stdout(self, fn):
#         if fn['stdout']:
#             self.out('### Standard output')
#             self.out('%s' % fn['stdout'])
#             self.out('')
#
#     def render_function(self, fn):
#         for order in FUNCTION_SECTIONS:
#             getattr(self, 'render_function_%s' % order)(fn)
#
#     def render_functions(self, tag):
#         if not self.doc['_fn']:
#             return
#
#         self.out('# Functions')
#         self.out('')
#         # summary
#         for fn in self.doc['_fn']:
#             self.out('- %s' % fn['fn'])
#         self.out('')
#         self.out('')
#         # all
#         for fn in self.doc['_fn']:
#             self.render_function(fn)
#
#     def render_history(self, tag):
#         self.render_one_many('# History', self.doc['history'])
#
#     def render_license(self, tag):
#         self.render_one_many('# License', self.doc['license'])
#
#     def render_notes(self, tag):
#         self.render_many_many_no_head('# Notes', self.doc['note'])
#
#     def render_options(self, tag):
#         self.render_many_many('# Options', self.doc['option'])
#
#     def render_see_also(self, tag):
#         pass
#
#     def render_stderr(self, tag):
#         pass
#
#     def render_stdin(self, tag):
#         pass
#
#     def render_stdout(self, tag):
#         pass
#
#     def render_usage(self, tag):
#         if self.doc['usage']:
#             self.out('# Usage')
#             for v in self.doc['usage']:
#                 if len(v) == 1:
#                     self.out('`%s`  ' % v[0].rstrip('\n'))
#                 else:
#                     self.out('```\n%s```' % ''.join(
#                         _v[7:] if _v[:7] == '       ' else _v for _v in v))
#             self.out('')
#
#     def render_version(self, tag):
#         if self.doc['version']:
#             self.out('# Version\n%s' % self.doc['version'])
#
#
# class TextFormatter(BaseFormatter):
#     """
#     Text formatter class.
#
#     This formatter will output documentation as simple text.
#     """
#
#     SECTIONS = (
#         'usage',
#         'desc',
#         'option',
#         'example',
#         'fn'
#     )
#     FUNCTION_SECTIONS = (
#         'fn',
#         'brief',
#         'desc',
#         'param',
#         'stdin',
#         'stdout',
#         'stderr',
#         'return',
#         'pre',
#         'seealso',
#     )
#
#     def render_one_one_no_header(self, tag, value, indent):
#         if value:
#             self.out(indent + tag.section_name + ':' + value)
#
#     def render_one_many_no_header(self, tag, value, indent):
#         if value:
#             self.out(indent + tag.section_name + ':')
#             self.out(indent + '  ' + ''.join(value))
#
#     def render_many_one_no_header(self, tag, value, indent):
#         if value:
#             self.out(indent + tag.section_name + ':')
#             for v in value:
#                 self.out(indent + '  ' + v)
#
#     def render_many_many_header(self, tag, value, indent):
#         if value:
#             self.out(indent + tag.section_name + ':')
#             for v in value:
#                 self.out(indent + '  ' + v[0].rstrip('\n'))
#                 if len(v) > 1:
#                     for vv in v[1:]:
#                         self.out(indent + '    ' + vv, end='')
#                     self.out('')
#
#     def render_many_many_no_header(self, tag, value, indent):
#         if value:
#             self.out(indent + tag.section_name + ':')
#             for v in value:
#                 self.out(indent + '  ' + ''.join(v))
#
#     def render_desc(self, tag, value):
#         if value:
#             self.out(''.join(value))
#
#     def render_function_fn(self, tag, value):
#         self.out('  ' + value)
#
#     def render_function_brief(self, tag, value):
#         if value:
#             self.out('    ' + value)
#             self.out('')
#
#     def render_function_desc(self, tag, value):
#         if value:
#             self.out('    ' + ''.join(value))
#
#     def render_function_param(self, tag, value):
#         if value:
#             self.out('    ' + tag.section_name + ':')
#             for param in value:
#                 if len(param) == 1:
#                     s = param[0].split(' ')
#                     param, desc = s[0], s[1:]
#                     self.out('      %-12s %s' % (
#                         param, ' '.join(desc).rstrip('\n')))
#                 else:
#                     param, desc = param[0], param[1:]
#                     self.out('      %s' % param.rstrip('\n'))
#                     self.out('        %s' % ''.join(desc))
#             self.out('')
#
#     def render_functions(self):
#         if not self.doc['_fn']:
#             return
#
#         self.out('Functions:')
#         self.out('')
#         for fn in self.doc['_fn']:
#             self.out('  ' + fn['fn'])
#         self.out('')
#         self.out('')
#         super().render_functions()
#
#     def render_brief(self, tag, value):
#         self.out('%s - %s' % (self.doc['_file'], value[0]))
#
#     def render_usage(self, tag, value):
#         if value:
#             self.out(tag.section_name + ': ' + ''.join(value[0]))
#             for v in value[1:]:
#                 self.out('       ' + ''.join(v))
