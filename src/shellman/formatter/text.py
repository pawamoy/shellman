# -*- coding: utf-8 -*-

"""
Text formatter module.

This module contains the TextFormatter class.
"""

from ..tag import FUNCTION_ORDER
from .base import BaseFormatter


class TextFormatter(BaseFormatter):
    """
    Text formatter class.

    This formatter will output documentation as simple text.
    """

    SECTIONS_ORDER = (
        'SYNOPSIS',
        'DESCRIPTION',
        'OPTIONS',
        'EXAMPLES',
        'FUNCTIONS'
    )

    def render_single_many(self, title, value):
        if value:
            self.out(title)
            self.out('  %s' % ''.join(value))

    def render_multi_many(self, title, value):
        if value:
            self.out(title)
            for v in value:
                self.out('  %s' % v[0].rstrip('\n'))
                if len(v) > 1:
                    self.out('    %s' % ''.join(v[1:]))

    def render_multi_many_no_head(self, title, value):
        if value:
            self.out(title)
            for v in value:
                self.out('  %s' % v)

    def render_authors(self, title):
        self.out('Authors:')
        for v in self.doc['author']:
            self.out('  %s' % v)

    def render_bugs(self, title):
        self.render_multi_many_no_head('Bugs:', self.doc['bug'])

    def render_caveats(self, title):
        self.render_multi_many_no_head('Caveats:', self.doc['caveat'])

    def render_copyright(self, title):
        self.render_single_many('Copyright:', self.doc['copyright'])

    def render_date(self, title):
        self.out('Date: %s' % self.doc['date'])

    def render_description(self, title):
        if self.doc['desc']:
            self.out('%s' % ''.join(self.doc['desc']))

    def render_environment_variables(self, title):
        self.render_multi_many('Environment variables:', self.doc['env'])

    def render_errors(self, title):
        self.render_multi_many_no_head('Errors:', self.doc['error'])

    def render_examples(self, title):
        self.render_multi_many('Examples:', self.doc['example'])

    def render_exit_status(self, title):
        self.render_multi_many('Exit status:', self.doc['exit'])

    def render_files(self, title):
        self.render_multi_many('Files:', self.doc['file'])

    def render_function_fn(self, fn):
        self.out('  %s' % fn['fn'])

    def render_function_brief(self, fn):
        if fn['brief']:
            self.out('    %s' % fn['brief'])
            self.out('')

    def render_function_desc(self, fn):
        if fn['desc']:
            self.out('    %s' % fn['desc'])

    def render_function_param(self, fn):
        if fn['param']:
            self.out('    Parameters:')
            for param in fn['param']:
                if len(param) == 1:
                    s = param[0].split(' ')
                    param, desc = s[0], s[1:]
                    self.out('      %-12s %s' % (
                        param, ' '.join(desc).rstrip('\n')))
                else:
                    param, desc = param[0], param[1:]
                    self.out('      %s' % param.rstrip('\n'))
                    self.out('        %s' % ''.join(desc))
            self.out('')

    def render_function_pre(self, fn):
        if fn['pre']:
            self.out('    Preconditions:')
            self.out('      %s' % fn['pre'])
            self.out('')

    def render_function_return(self, fn):
        if fn['return']:
            self.out('    Return code:')
            self.out('      %s' % fn['return'])
            self.out('')

    def render_function_seealso(self, fn):
        if fn['seealso']:
            self.out('    See also:')
            self.out('      %s' % fn['seealso'])
            self.out('')

    def render_function_stderr(self, fn):
        if fn['stderr']:
            self.out('    Standard error:')
            self.out('      %s' % fn['stderr'])
            self.out('')

    def render_function_stdin(self, fn):
        if fn['stdin']:
            self.out('    Standard input:')
            self.out('      %s' % fn['stdin'])
            self.out('')

    def render_function_stdout(self, fn):
        if fn['stdout']:
            self.out('    Standard output:')
            self.out('      %s' % fn['stdout'])
            self.out('')

    def render_function(self, fn):
        for order in FUNCTION_ORDER:
            getattr(self, 'render_function_%s' % order)(fn)

    def render_functions(self, title):
        if not self.doc['_fn']:
            return

        self.out('Functions:')
        self.out('')
        # summary
        for fn in self.doc['_fn']:
            self.out('  %s' % fn['fn'])
        self.out('')
        self.out('')
        # all
        for fn in self.doc['_fn']:
            self.render_function(fn)

    def render_history(self, title):
        self.render_single_many('History:', self.doc['history'])

    def render_license(self, title):
        self.render_single_many('License:', self.doc['license'])

    def render_name(self, title):
        self.out('%s - %s' % (self.doc['_file'], self.doc['brief'][0]))

    def render_notes(self, title):
        self.render_multi_many_no_head('Notes:', self.doc['note'])

    def render_options(self, title):
        self.render_multi_many('Options:', self.doc['option'])

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
            self.out('Usage: %s' % ''.join(self.doc['usage'][0]))
            for v in self.doc['usage'][1:]:
                self.out('       %s' % ''.join(v))

    def render_version(self, title):
        self.out('Version: %s' % self.doc['version'])
