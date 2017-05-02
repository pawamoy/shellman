# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Base formatter module.

This module contains the BaseFormatter class.
"""

from __future__ import print_function

import sys


class BaseFormatter(object):
    """
    Formatter base class.

    A formatter class has a SECTIONS_ORDER attribute to know in which order
    to output the different documentation sections (list of str).
    """

    SECTIONS_ORDER = ()

    def __init__(self, doc, output=None):
        """
        Init method.

        Args:
            doc (dict): doc generated through Doc object.

        Attributes:
            doc (dict): doc given to init.
            render (dict): mapping between doc section name and render method.
        """
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
        if output in (None, sys.stdout):
            self.output = sys.stdout
        else:
            self.output = open(output, 'w')

    def out(self, *args, **kwargs):
        """Wrapper around print to write into self.output."""
        print(*args, file=self.output, **kwargs)

    def get_render(self, section):
        """
        Generic method to get the render method given a section name.

        Args:
            section (str): the section name.

        Returns:
            func: the render method in this very instance.
        """
        attr = 'render_%s' % section
        if not hasattr(self, attr):
            return lambda: None
        return getattr(self, attr)

    def write(self):
        """Write documentation on stdout."""
        self.write_init()
        for section in self.SECTIONS_ORDER:
            self.render[section](section)

    def write_init(self):
        """Write some header on stdout (useful for man pages)."""
        pass

    def esc(self, string):
        """Escape some special characters in the string."""
        pass

    def render_single_many(self, title, value):
        """Render a (one occurrence, many lines) tag."""
        pass

    def render_multi_many(self, title, value):
        """Render a (many occurrence, many lines) tag."""
        pass

    def render_multi_many_no_head(self, title, value):
        """Render a (many occurrence, many lines) tag without header."""
        pass

    def render_authors(self, title):
        """Render authors section."""
        pass

    def render_bugs(self, title):
        """Render bugs section."""
        pass

    def render_caveats(self, title):
        """Render caveats section."""
        pass

    def render_copyright(self, title):
        """Render copyright section."""
        pass

    def render_date(self, title):
        """Render date section."""
        pass

    def render_description(self, title):
        """Render description section."""
        pass

    def render_environment_variables(self, title):
        """Render environment variables section."""
        pass

    def render_errors(self, title):
        """Render errors section."""
        pass

    def render_examples(self, title):
        """Render examples section."""
        pass

    def render_exit_status(self, title):
        """Render exit status section."""
        pass

    def render_files(self, title):
        """Render files section."""
        pass

    def render_function_fn(self, fn):
        """Render function prototype line."""
        pass

    def render_function_brief(self, fn):
        """Render function brief line."""
        pass

    def render_function_desc(self, fn):
        """Render function description lines."""
        pass

    def render_function_param(self, fn):
        """Render function params lines."""
        pass

    def render_function_pre(self, fn):
        """Render function preconditions lines."""
        pass

    def render_function_return(self, fn):
        """Render function return codes lines."""
        pass

    def render_function_seealso(self, fn):
        """Render function see also line."""
        pass

    def render_function_stderr(self, fn):
        """Render function stderr lines."""
        pass

    def render_function_stdin(self, fn):
        """Render function stdin lines."""
        pass

    def render_function_stdout(self, fn):
        """Render function stdout lines."""
        pass

    def render_function(self, fn):
        """Render a complete function."""
        pass

    def render_functions(self, title):
        """Render functions section."""
        pass

    def render_history(self, title):
        """Render history section."""
        pass

    def render_license(self, title):
        """Render license section."""
        pass

    def render_name(self, title):
        """Render name section."""
        pass

    def render_notes(self, title):
        """Render notes section."""
        pass

    def render_options(self, title):
        """Render options section."""
        pass

    def render_see_also(self, title):
        """Render see also section."""
        pass

    def render_stderr(self, title):
        """Render stderr section."""
        pass

    def render_stdin(self, title):
        """Render stdin section."""
        pass

    def render_stdout(self, title):
        """Render stdout section."""
        pass

    def render_usage(self, title):
        """Render usage section."""
        pass

    def render_version(self, title):
        """Render version section."""
        pass
