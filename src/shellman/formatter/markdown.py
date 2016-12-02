# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Markdown formatter module.

This module contains the MarkdownFormatter class.
"""

from ..tag import FUNCTION_ORDER
from .base import BaseFormatter


class MarkdownFormatter(BaseFormatter):
    """
    Markown formatter class.

    This formatter will output documentation as Markdown.
    """

    SECTIONS_ORDER = (
        'NAME',
        'SYNOPSIS',
        'DESCRIPTION',
        'OPTIONS',
        'ENVIRONMENT VARIABLES',
        'FILES',
        'EXAMPLES',
        'EXIT STATUS',
        'FUNCTIONS',
        'ERRORS',
        'BUGS',
        'CAVEATS',
        'AUTHORS',
        'COPYRIGHT',
        'LICENSE',
        'HISTORY',
        'NOTES',
        'SEE ALSO',
    )

    def write_init(self):
        self.render_date(None)

    def render_single_many(self, title, value):
        if value:
            print(title)
            print('%s' % ''.join(value))
            print('')

    def render_multi_many(self, title, value):
        if value:
            print(title)
            for v in value:
                print('- `%s`:' % v[0].rstrip('\n'))
                if len(v) > 1:
                    print('  %s' % ''.join(v[1:]).rstrip('\n'))
            print('')

    def render_multi_many_no_head(self, title, value):
        if value:
            print(title)
            for v in value:
                print('- %s' % v)
            print('')

    def render_authors(self, title):
        if self.doc['author']:
            print('# Authors')
            for v in self.doc['author']:
                print('- %s' % v)

    def render_bugs(self, title):
        self.render_multi_many_no_head('# Bugs', self.doc['bug'])

    def render_caveats(self, title):
        self.render_multi_many_no_head('# Caveat:', self.doc['caveat'])

    def render_copyright(self, title):
        self.render_single_many('# Copyright', self.doc['copyright'])

    def render_date(self, title):
        if self.doc['date']:
            print('*Date: %s*' % self.doc['date'])
            print('')

    def render_description(self, title):
        if self.doc['desc']:
            print('%s' % ''.join(self.doc['desc']))

    def render_environment_variables(self, title):
        self.render_multi_many('# Environment variables', self.doc['env'])

    def render_errors(self, title):
        self.render_multi_many_no_head('# Errors', self.doc['error'])

    def render_examples(self, title):
        self.render_multi_many('# Examples', self.doc['example'])

    def render_exit_status(self, title):
        self.render_multi_many('# Exit status', self.doc['exit'])

    def render_files(self, title):
        self.render_multi_many('# Files', self.doc['file'])

    def render_function_fn(self, fn):
        print('## %s' % fn['fn'])

    def render_function_brief(self, fn):
        if fn['brief']:
            print('%s' % fn['brief'])
            print('')

    def render_function_desc(self, fn):
        if fn['desc']:
            print('%s' % fn['desc'])

    def render_function_param(self, fn):
        if fn['param']:
            print('### Parameters')
            for param in fn['param']:
                if len(param) == 1:
                    s = param[0].split(' ')
                    param, desc = s[0], s[1:]
                    print('- `%s`: %s' % (
                        param, ' '.join(desc).rstrip('\n')))
                else:
                    param, desc = param[0], param[1:]
                    print('- `%s`:' % param.rstrip('\n'))
                    print('  %s' % ''.join(desc))
            print('')

    def render_function_pre(self, fn):
        if fn['pre']:
            print('### Preconditions')
            print('%s' % fn['pre'])
            print('')

    def render_function_return(self, fn):
        if fn['return']:
            print('### Return code')
            print('%s' % fn['return'])
            print('')

    def render_function_seealso(self, fn):
        if fn['seealso']:
            print('### See also')
            print('%s' % fn['seealso'])
            print('')

    def render_function_stderr(self, fn):
        if fn['stderr']:
            print('### Standard error')
            print('%s' % fn['stderr'])
            print('')

    def render_function_stdin(self, fn):
        if fn['stdin']:
            print('### Standard input')
            print('%s' % fn['stdin'])
            print('')

    def render_function_stdout(self, fn):
        if fn['stdout']:
            print('### Standard output')
            print('%s' % fn['stdout'])
            print('')

    def render_function(self, fn):
        for order in FUNCTION_ORDER:
            getattr(self, 'render_function_%s' % order)(fn)

    def render_functions(self, title):
        if not self.doc['_fn']:
            return

        print('# Functions')
        print('')
        # summary
        for fn in self.doc['_fn']:
            print('- %s' % fn['fn'])
        print('')
        print('')
        # all
        for fn in self.doc['_fn']:
            self.render_function(fn)

    def render_history(self, title):
        self.render_single_many('# History', self.doc['history'])

    def render_license(self, title):
        self.render_single_many('# License', self.doc['license'])

    def render_name(self, title):
        print('**%s** - %s' % (self.doc['_file'], self.doc['brief']))

    def render_notes(self, title):
        self.render_multi_many_no_head('# Notes', self.doc['note'])

    def render_options(self, title):
        self.render_multi_many('# Options', self.doc['option'])

    def render_see_also(self, title):
        pass

    def render_stderr(self, title):
        pass

    def render_stdin(self, title):
        pass

    def render_stdout(self, title):
        pass

    def render_usage(self, title):
        if self.doc['usage']:
            print('# Usage')
            for v in self.doc['usage']:
                if len(v) == 1:
                    print('`%s`  ' % v[0].rstrip('\n'))
                else:
                    print('```\n%s```' % ''.join(
                        _v[7:] if _v[:7] == '       ' else _v for _v in v))
            print('')

    def render_version(self, title):
        if self.doc['version']:
            print('# Version\n%s' % self.doc['version'])
