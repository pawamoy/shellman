# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class BaseFormatter(object):
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
