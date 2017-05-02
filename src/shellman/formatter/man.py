# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Man formatter module.

This module contains the ManFormatter class.
"""

import re
import sys

from .. import __version__
from ..tag import FUNCTION_ORDER
from .base import BaseFormatter


class ManFormatter(BaseFormatter):
    """
    Man page formatter class.

    This formatter will output documentation as a man page.
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

    def esc(self, string):
        if string:
            return string.replace('-', '\\-').replace("'", "\\(cq")
        return string

    def write_init(self):
        self.out('.if n.ad l')
        self.out('.nh')
        self.out('.TH %s 1 "%s" "Shellman %s" "User Commands"' % (
            self.doc['_file'], self.esc(self.doc['date']) or '', __version__))

    def render_single_many(self, title, value):
        if value:
            self.out('.SH "%s"' % title)
            self.out('%s' % self.esc(''.join(value)))

    def render_multi_many(self, title, value):
        if value:
            self.out('.SH "%s"' % title)
            for v in value:
                if len(v) == 1:
                    s = v[0].split(' ')
                    h, b = s[0], ' '.join(s[1:]).rstrip('\n')
                else:
                    h, b = v[0].rstrip('\n'), ''.join(v[1:]).rstrip('\n')
                self.out('.IP "\\fB%s\\fR" 4' % h)
                self.out(self.esc(b))

    def render_multi_many_no_head(self, title, value):
        if value:
            self.out('.SH "%s"' % title)
            for v in value:
                self.out('%s' % self.esc(''.join(v)))

    def render_authors(self, title):
        if self.doc['author']:
            self.out('.SH "%s"' % title)
            for author in self.doc['author']:
                self.out('.br')
                self.out(author)

    def render_bugs(self, title):
        self.render_multi_many_no_head(title, self.doc['bug'])

    def render_caveats(self, title):
        self.render_multi_many_no_head(title, self.doc['caveat'])

    def render_copyright(self, title):
        self.render_single_many(title, self.doc['copyright'])

    def render_date(self, title):
        pass

    def render_description(self, title):
        self.render_single_many(title, self.doc['desc'])

    def render_environment_variables(self, title):
        self.render_multi_many(title, self.doc['env'])

    def render_errors(self, title):
        self.render_multi_many_no_head(title, self.doc['error'])

    def render_examples(self, title):
        self.render_multi_many(title, self.doc['example'])

    def render_exit_status(self, title):
        self.render_multi_many(title, self.doc['exit'])

    def render_files(self, title):
        self.render_multi_many(title, self.doc['file'])

    def render_function_fn(self, fn):
        self.out('.IP "\\fB%s\\fR" 4' % self.esc(fn['fn']))

    def render_function_brief(self, fn):
        if fn['brief']:
            self.out('%s' % self.esc(fn['brief']))
            self.out('')

    def render_function_desc(self, fn):
        if fn['desc']:
            self.out('%s' % self.esc(''.join(fn['desc'])))

    def render_function_param(self, fn):
        if fn['param']:
            self.out('.ul')
            self.out('Parameters:')
            for param in fn['param']:
                if len(param) == 1:
                    s = param[0].split(' ')
                    param, desc = s[0], s[1:]
                    self.out('  \\fB%-12s\\fR %s' % (
                        param, self.esc(' '.join(desc)).rstrip('\n')))
                else:
                    param, desc = param[0], param[1:]
                    self.out('  \\fB%s\\fR' % self.esc(param).rstrip('\n'))
                    self.out('    %s' % self.esc(''.join(desc)))
            self.out('')

    def render_function_pre(self, fn):
        if fn['pre']:
            self.out('.ul')
            self.out('Preconditions:')
            for pre in fn['pre']:
                self.out('  %s' % self.esc(''.join(pre)))
            self.out('')

    def render_function_return(self, fn):
        if fn['return']:
            self.out('.ul')
            self.out('Return code:')
            for ret in fn['return']:
                self.out('  %s' % self.esc(''.join(ret)))
            self.out('')

    def render_function_seealso(self, fn):
        if fn['seealso']:
            self.out('.ul')
            self.out('See also:')
            for seealso in fn['seealso']:
                self.out('  %s' % self.esc(''.join(seealso)))
            self.out('')

    def render_function_stderr(self, fn):
        if fn['stderr']:
            self.out('.ul')
            self.out('Standard error:')
            for stderr in fn['stderr']:
                self.out('  %s' % self.esc(''.join(stderr)))
            self.out('')

    def render_function_stdin(self, fn):
        if fn['stdin']:
            self.out('.ul')
            self.out('Standard input:')
            for stdin in fn['stdin']:
                self.out('  %s' % self.esc(''.join(stdin)))
            self.out('')

    def render_function_stdout(self, fn):
        if fn['stdout']:
            self.out('.ul')
            self.out('Standard output:')
            for stdout in fn['stdout']:
                self.out('  %s' % self.esc(''.join(stdout)))
            self.out('')

    def render_function(self, fn):
        for order in FUNCTION_ORDER:
            getattr(self, 'render_function_%s' % order)(fn)

    def render_functions(self, title):
        if not self.doc['_fn']:
            return

        self.out('.SH "%s"' % title)
        # summary
        for fn in self.doc['_fn']:
            self.out('%s' % self.esc(fn['fn']))
            self.out('.br')

        # all
        for fn in self.doc['_fn']:
            self.render_function(fn)

    def render_history(self, title):
        self.render_single_many(title, self.doc['history'])

    def render_license(self, title):
        self.render_single_many(title, self.doc['license'])

    def render_name(self, title):
        if self.doc['brief']:
            self.out('.SH "%s"' % title)
            # pylama:ignore=W1401
            self.out('%s \- %s' % (self.doc['_file'],
                                   self.esc(self.doc['brief'])))

    def render_notes(self, title):
        self.render_multi_many_no_head(title, self.doc['note'])

    def render_options(self, title):
        if not self.doc['option']:
            return
        self.out('.SH "%s"' % title)
        for option in self.doc['option']:
            self.out('.IP "\\fB%s\\fR" 4' % option[0]
                     .rstrip('\n')
                     .replace(',', '\\fR,\\fB'))
            sys.stdout.write(''.join(option[1:]))

    def render_see_also(self, title):
        pass

    def render_stderr(self, title):
        pass

    def render_stdin(self, title):
        pass

    def render_stdout(self, title):
        pass

    def render_usage(self, title):
        if not self.doc['usage']:
            return
        self.out('.SH "%s"' % title)
        rep_reg_opt = re.compile(r'(--?[a-z0-9-]+=?)')
        rep_reg_arg = re.compile(r'([A-Z]+)')
        for usage in self.doc['usage']:
            syn = ''.join(usage)
            name, syn = syn.split(' ', 1)
            syn = rep_reg_arg.sub(r'\\fI\1\\fR', syn)  # order is important!
            syn = rep_reg_opt.sub(r'\\fB\1\\fR', syn)
            self.out('.br')
            sys.stdout.write('\\fB%s\\fR %s' % (
                name, self.esc(syn)))

    def render_version(self, title):
        pass
