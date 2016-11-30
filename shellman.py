#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
import sys

SHELLMAN_VERSION = '1.1'


class Tag(object):
    MANY = '+'

    def __init__(self, occurrences, lines):
        self.occurrences = occurrences
        self.lines = lines


TAGS = {
    'author':    Tag(Tag.MANY, 1),
    'bug':       Tag(Tag.MANY, Tag.MANY),
    'brief':     Tag(1,  1),
    'caveat':    Tag(Tag.MANY, Tag.MANY),
    'copyright': Tag(1, Tag.MANY),
    'date':      Tag(1, 1),
    'desc':      Tag(1, Tag.MANY),
    'env':       Tag(Tag.MANY, Tag.MANY),
    'error':     Tag(Tag.MANY, Tag.MANY),
    'example':   Tag(Tag.MANY, Tag.MANY),
    'exit':      Tag(Tag.MANY, Tag.MANY),
    'file':      Tag(Tag.MANY, Tag.MANY),
    'history':   Tag(1, Tag.MANY),
    'license':   Tag(1, Tag.MANY),
    'note':      Tag(Tag.MANY, Tag.MANY),
    'option':    Tag(Tag.MANY, Tag.MANY),
    'seealso':   Tag(Tag.MANY, 1),
    'stderr':    Tag(Tag.MANY, Tag.MANY),
    'stdin':     Tag(Tag.MANY, Tag.MANY),
    'stdout':    Tag(Tag.MANY, Tag.MANY),
    'usage':     Tag(Tag.MANY, Tag.MANY),
    'version':   Tag(1, 1)
}

FN_TAG = 'fn'
FN_TAGS = {
    'fn':      Tag(1, 1),
    'brief':   Tag(1, 1),
    'desc':    Tag(1, Tag.MANY),
    'param':   Tag(Tag.MANY, Tag.MANY),
    'pre':     Tag(Tag.MANY, Tag.MANY),
    'return':  Tag(Tag.MANY, Tag.MANY),
    'seealso': Tag(Tag.MANY, 1),
    'stderr':  Tag(Tag.MANY, Tag.MANY),
    'stdin':   Tag(Tag.MANY, Tag.MANY),
    'stdout':  Tag(Tag.MANY, Tag.MANY)
}

FUNCTION_ORDER = (
    'fn',
    'brief',
    'desc',
    'param',
    'stdin',
    'stdout',
    'stderr',
    'return',
    'pre',
    'seealso',
)


class Doc(object):
    def __init__(self, file):
        self.file = file
        self.doc = {k: None for k in TAGS.keys()}
        self.doc['_file'] = os.path.basename(self.file)
        self.doc['_fn'] = []

    @staticmethod
    def tag_value(line):
        line = line.lstrip('#')
        first_char = line.lstrip(' ')[0]
        if first_char in '@\\':
            words = line.lstrip(' ').split(' ')
            return words[0][1:], ' '.join(words[1:])

        if len(line) > 1:
            if line[0] == ' ':
                return None, line[1:]
        return None, line

    def update_value(self, tag, value, end=False):
        if TAGS[tag].occurrences == Tag.MANY:
            if TAGS[tag].lines == Tag.MANY:
                if self.doc[tag] is None:
                    self.doc[tag] = [[]]
                elif end:
                    self.doc[tag].append([])
                self.doc[tag][-1].append(value)
                return True
            if self.doc[tag] is None:
                self.doc[tag] = []
            self.doc[tag].append(value.rstrip('\n'))
            return False
        if TAGS[tag].lines == Tag.MANY:
            if self.doc[tag] is None:
                self.doc[tag] = []
            self.doc[tag].append(value)
            return True
        self.doc[tag] = value.rstrip('\n')
        return False

    def update_fn_value(self, tag, value, end=False):
        if FN_TAGS[tag].occurrences == Tag.MANY:
            if FN_TAGS[tag].lines == Tag.MANY:
                if self.doc['_fn'][-1][tag] is None:
                    self.doc['_fn'][-1][tag] = [[]]
                elif end:
                    self.doc['_fn'][-1][tag].append([])
                self.doc['_fn'][-1][tag][-1].append(value)
                return True
            if self.doc['_fn'][-1][tag] is None:
                self.doc['_fn'][-1][tag] = []
            self.doc['_fn'][-1][tag].append(value.rstrip('\n'))
            return False
        if FN_TAGS[tag].lines == Tag.MANY:
            if self.doc['_fn'][-1][tag] is None:
                self.doc['_fn'][-1][tag] = []
            self.doc['_fn'][-1][tag].append(value)
            return True
        self.doc['_fn'][-1][tag] = value.rstrip('\n')
        return False

    def read(self):
        current_tag = None
        in_tag = False
        in_function = False
        with open(self.file) as f:
            for line in f:
                line = line.lstrip(' \t')
                if line == '\n':
                    current_tag = None
                    in_tag = False
                elif re.search(r'^##', line):
                    tag, value = Doc.tag_value(line)
                    if tag is not None:
                        current_tag = tag
                        if tag == FN_TAG:
                            in_function = True
                            self.doc['_fn'].append(
                                {k: None for k in FN_TAGS.keys()})
                            in_tag = self.update_fn_value(
                                current_tag, value, end=True)
                        else:
                            if in_function and tag in FN_TAGS.keys():
                                in_tag = self.update_fn_value(
                                    current_tag, value, end=True)
                            elif tag in TAGS.keys():
                                in_function = False
                                in_tag = self.update_value(
                                    current_tag, value, end=True)
                            else:
                                continue  # ignore invalid tags
                    else:
                        if in_tag:
                            if in_function:
                                in_tag = self.update_fn_value(
                                    current_tag, value)
                            else:
                                in_tag = self.update_value(current_tag, value)
                        else:
                            pass  # doc without tag, ignored
        return self.doc


class Formatter(object):
    SECTIONS_ORDER = ()

    def __init__(self, doc):
        self.doc = doc
        self.render = {
            'AUTHORS': self.get_render('authors'),
            'BUGS': self.get_render('bugs'),
            'CAVEATS': self.get_render('caveats'),
            'COPYRIGHT': self.get_render('copyright'),
            'DATE': self.get_render('date'),
            'DESCRIPTION': self.get_render('description'),
            'ENVIRONMENT VARIABLES': self.get_render('environment_variables'),
            'ERRORS': self.get_render('errors'),
            'EXAMPLES': self.get_render('examples'),
            'EXIT STATUS': self.get_render('exit_status'),
            'FILES': self.get_render('files'),
            'FUNCTIONS': self.get_render('functions'),
            'HISTORY': self.get_render('history'),
            'LICENSE': self.get_render('license'),
            'NAME': self.get_render('name'),
            'NOTES': self.get_render('notes'),
            'OPTIONS': self.get_render('options'),
            'SEE ALSO': self.get_render('see_also'),
            'STDERR': self.get_render('stderr'),
            'STDIN': self.get_render('stdin'),
            'STDOUT': self.get_render('stdout'),
            'SYNOPSIS': self.get_render('usage'),
            'USAGE': self.get_render('usage'),
            'VERSION': self.get_render('version')
        }

    def get_render(self, section):
        attr = 'render_%s' % section
        if not hasattr(self, attr):
            return lambda: None
        return getattr(self, attr)

    def write(self):
        self.write_init()
        for section in self.SECTIONS_ORDER:
            self.render[section](section)

    def write_init(self):
        pass


class Man(Formatter):
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
        print('.if n.ad l')
        print('.nh')
        print('.TH %s 1 "%s" "Shellman %s" "User Commands"' % (
            self.doc['_file'], self.esc(self.doc['date']) or '',
            SHELLMAN_VERSION))

    def render_single_many(self, title, value):
        if value:
            print('.SH "%s"' % title)
            print('%s' % self.esc(''.join(value)))

    def render_multi_many(self, title, value):
        if value:
            print('.SH "%s"' % title)
            for v in value:
                if len(v) == 1:
                    s = v[0].split(' ')
                    h, b = s[0], ' '.join(s[1:]).rstrip('\n')
                else:
                    h, b = v[0].rstrip('\n'), ''.join(v[1:]).rstrip('\n')
                print('.IP "\\fB%s\\fR" 4' % h)
                print(self.esc(b))

    def render_multi_many_no_head(self, title, value):
        if value:
            print('.SH "%s"' % title)
            for v in value:
                print('%s' % self.esc(''.join(v)))

    def render_authors(self, title):
        if self.doc['author']:
            print('.SH "%s"' % title)
            for author in self.doc['author']:
                print('.br')
                print(author)

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

    def _render_function_fn(self, fn):
        print('.IP "\\fB%s\\fR" 4' % self.esc(fn['fn']))

    def _render_function_brief(self, fn):
        if fn['brief']:
            print('%s' % self.esc(fn['brief']))
            print()

    def _render_function_desc(self, fn):
        if fn['desc']:
            print('%s' % self.esc(''.join(fn['desc'])))

    def _render_function_param(self, fn):
        if fn['param']:
            print('.ul')
            print('Parameters:')
            for param in fn['param']:
                if len(param) == 1:
                    s = param[0].split(' ')
                    param, desc = s[0], s[1:]
                    print('  \\fB%-12s\\fR %s' % (
                        param, self.esc(' '.join(desc)).rstrip('\n')))
                else:
                    param, desc = param[0], param[1:]
                    print('  \\fB%s\\fR' % self.esc(param).rstrip('\n'))
                    print('    %s' % self.esc(''.join(desc)))
            print()

    def _render_function_pre(self, fn):
        if fn['pre']:
            print('.ul')
            print('Preconditions:')
            for pre in fn['pre']:
                print('  %s' % self.esc(''.join(pre)))
            print()

    def _render_function_return(self, fn):
        if fn['return']:
            print('.ul')
            print('Return code:')
            for ret in fn['return']:
                print('  %s' % self.esc(''.join(ret)))
            print()

    def _render_function_seealso(self, fn):
        if fn['seealso']:
            print('.ul')
            print('See also:')
            for seealso in fn['seealso']:
                print('  %s' % self.esc(''.join(seealso)))
            print()

    def _render_function_stderr(self, fn):
        if fn['stderr']:
            print('.ul')
            print('Standard error:')
            for stderr in fn['stderr']:
                print('  %s' % self.esc(''.join(stderr)))
            print()

    def _render_function_stdin(self, fn):
        if fn['stdin']:
            print('.ul')
            print('Standard input:')
            for stdin in fn['stdin']:
                print('  %s' % self.esc(''.join(stdin)))
            print()

    def _render_function_stdout(self, fn):
        if fn['stdout']:
            print('.ul')
            print('Standard output:')
            for stdout in fn['stdout']:
                print('  %s' % self.esc(''.join(stdout)))
            print()

    def _render_function(self, fn):
        for order in FUNCTION_ORDER:
            getattr(self, '_render_function_%s' % order)(fn)

    def render_functions(self, title):
        if not self.doc['_fn']:
            return

        print('.SH "%s"' % title)
        # summary
        for fn in self.doc['_fn']:
            print('%s' % self.esc(fn['fn']))
            print('.br')

        # all
        for fn in self.doc['_fn']:
            self._render_function(fn)

    def render_history(self, title):
        self.render_single_many(title, self.doc['history'])

    def render_license(self, title):
        self.render_single_many(title, self.doc['license'])

    def render_name(self, title):
        if self.doc['brief']:
            print('.SH "%s"' % title)
            print('%s \- %s' % (self.doc['_file'],
                                self.esc(self.doc['brief'])))

    def render_notes(self, title):
        self.render_multi_many_no_head(title, self.doc['note'])

    def render_options(self, title):
        if not self.doc['option']:
            return
        print('.SH "%s"' % title)
        for option in self.doc['option']:
            print('.IP "\\fB%s\\fR" 4' % option[0]
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
        print('.SH "%s"' % title)
        rep_reg_opt = re.compile(r'(--?[a-z0-9-]+=?)')
        rep_reg_arg = re.compile(r'([A-Z]+)')
        for usage in self.doc['usage']:
            syn = ''.join(usage)
            syn = rep_reg_arg.sub(r'\\fI\1\\fR', syn)  # order is important!
            syn = rep_reg_opt.sub(r'\\fB\1\\fR', syn)
            print('.br')
            sys.stdout.write('\\fB%s\\fR %s' % (self.doc['_file'], self.esc(syn)))

    def render_version(self, title):
        pass


class Text(Formatter):
    SECTIONS_ORDER = (
        'SYNOPSIS',
        'DESCRIPTION',
        'OPTIONS',
        'EXAMPLES',
        'FUNCTIONS'
    )

    def render_single_many(self, title, value):
        if value:
            print(title)
            print('  %s' % ''.join(value))

    def render_multi_many(self, title, value):
        if value:
            print(title)
            for v in value:
                print('  %s' % v[0].rstrip('\n'))
                if len(v) > 1:
                    print('    %s' % ''.join(v[1:]))

    def render_multi_many_no_head(self, title, value):
        if value:
            print(title)
            for v in value:
                print('  %s' % v)

    def render_authors(self, title):
        print('Authors:')
        for v in self.doc['author']:
            print('  %s' % v)

    def render_bugs(self, title):
        self.render_multi_many_no_head('Bugs:', self.doc['bug'])

    def render_caveats(self, title):
        self.render_multi_many_no_head('Caveats:', self.doc['caveat'])

    def render_copyright(self, title):
        self.render_single_many('Copyright:', self.doc['copyright'])

    def render_date(self, title):
        print('Date: %s' % self.doc['date'])

    def render_description(self, title):
        if self.doc['desc']:
            print('%s' % ''.join(self.doc['desc']))

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

    def _render_function_fn(self, fn):
        print('  %s' % fn['fn'])

    def _render_function_brief(self, fn):
        if fn['brief']:
            print('    %s' % fn['brief'])
            print()

    def _render_function_desc(self, fn):
        if fn['desc']:
            print('    %s' % fn['desc'])

    def _render_function_param(self, fn):
        if fn['param']:
            print('    Parameters:')
            for param in fn['param']:
                if len(param) == 1:
                    s = param[0].split(' ')
                    param, desc = s[0], s[1:]
                    print('      %-12s %s' % (
                        param, ' '.join(desc).rstrip('\n')))
                else:
                    param, desc = param[0], param[1:]
                    print('      %s' % param.rstrip('\n'))
                    print('        %s' % ''.join(desc))
            print()

    def _render_function_pre(self, fn):
        if fn['pre']:
            print('    Preconditions:')
            print('      %s' % fn['pre'])
            print()

    def _render_function_return(self, fn):
        if fn['return']:
            print('    Return code:')
            print('      %s' % fn['return'])
            print()

    def _render_function_seealso(self, fn):
        if fn['seealso']:
            print('    See also:')
            print('      %s' % fn['seealso'])
            print()

    def _render_function_stderr(self, fn):
        if fn['stderr']:
            print('    Standard error:')
            print('      %s' % fn['stderr'])
            print()

    def _render_function_stdin(self, fn):
        if fn['stdin']:
            print('    Standard input:')
            print('      %s' % fn['stdin'])
            print()

    def _render_function_stdout(self, fn):
        if fn['stdout']:
            print('    Standard output:')
            print('      %s' % fn['stdout'])
            print()

    def _render_function(self, fn):
        for order in FUNCTION_ORDER:
            getattr(self, '_render_function_%s' % order)(fn)

    def render_functions(self, title):
        if not self.doc['_fn']:
            return

        print('Functions:')
        print()
        # summary
        for fn in self.doc['_fn']:
            print('  %s' % fn['fn'])
        print()
        print()
        # all
        for fn in self.doc['_fn']:
            self._render_function(fn)

    def render_history(self, title):
        self.render_single_many('History:', self.doc['history'])

    def render_license(self, title):
        self.render_single_many('License:', self.doc['license'])

    def render_name(self, title):
        print('%s - %s' % (self.doc['_file'], self.doc['brief'][0]))

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
            print('Usage: %s' % ''.join(self.doc['usage'][0]))
            for v in self.doc['usage'][1:]:
                print('       %s' % ''.join(v))

    def render_version(self, title):
        print('Version: %s' % self.doc['version'])


class Markdown(Formatter):
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
        print()

    def render_single_many(self, title, value):
        if value:
            print(title)
            print('%s' % ''.join(value))

    def render_multi_many(self, title, value):
        if value:
            print(title)
            for v in value:
                print('- `%s`' % v[0].rstrip('\n'))
                if len(v) > 1:
                    print('  %s' % ''.join(v[1:]))

    def render_multi_many_no_head(self, title, value):
        if value:
            print(title)
            for v in value:
                print('- %s' % v)

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
        print('*Date: %s*' % self.doc['date'])

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

    def _render_function_fn(self, fn):
        print('## %s' % fn['fn'])

    def _render_function_brief(self, fn):
        if fn['brief']:
            print('%s' % fn['brief'])
            print()

    def _render_function_desc(self, fn):
        if fn['desc']:
            print('%s' % fn['desc'])

    def _render_function_param(self, fn):
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
            print()

    def _render_function_pre(self, fn):
        if fn['pre']:
            print('### Preconditions')
            print('%s' % fn['pre'])
            print()

    def _render_function_return(self, fn):
        if fn['return']:
            print('### Return code')
            print('%s' % fn['return'])
            print()

    def _render_function_seealso(self, fn):
        if fn['seealso']:
            print('### See also')
            print('%s' % fn['seealso'])
            print()

    def _render_function_stderr(self, fn):
        if fn['stderr']:
            print('### Standard error')
            print('%s' % fn['stderr'])
            print()

    def _render_function_stdin(self, fn):
        if fn['stdin']:
            print('### Standard input')
            print('%s' % fn['stdin'])
            print()

    def _render_function_stdout(self, fn):
        if fn['stdout']:
            print('### Standard output')
            print('%s' % fn['stdout'])
            print()

    def _render_function(self, fn):
        for order in FUNCTION_ORDER:
            getattr(self, '_render_function_%s' % order)(fn)

    def render_functions(self, title):
        if not self.doc['_fn']:
            return

        print('# Functions')
        print()
        # summary
        for fn in self.doc['_fn']:
            print('- %s' % fn['fn'])
        print()
        print()
        # all
        for fn in self.doc['_fn']:
            self._render_function(fn)

    def render_history(self, title):
        self.render_single_many('# History', self.doc['history'])

    def render_license(self, title):
        self.render_single_many('# License', self.doc['license'])

    def render_name(self, title):
        print('**%s** - %s' % (self.doc['_file'], self.doc['brief'][0]))

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
            print('# Usage\n%s' % ''.join(self.doc['usage'][0]))
            for v in self.doc['usage'][1:]:
                print('- %s' % ''.join(v))

    def render_version(self, title):
        if self.doc['version']:
            print('# Version\n%s' % self.doc['version'])


def get_formatter(fmt):
    if fmt == 'text':
        return Text
    elif fmt == 'man':
        return Man
    elif fmt in ('md', 'markdown'):
        return Markdown
    else:
        raise ValueError('Env var SHELLMAN_FORMAT incorrect')


def main():
    f = sys.argv[1]
    doc = Doc(f).read()
    fmt = os.environ.get('SHELLMAN_FORMAT', 'text')
    get_formatter(fmt)(doc).write()


if __name__ == '__main__':
    sys.exit(main())
