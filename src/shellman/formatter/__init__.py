# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .man import ManFormatter
from .markdown import MarkdownFormatter
from .text import TextFormatter


def get_formatter(fmt):
    if fmt == 'text':
        return TextFormatter
    elif fmt == 'man':
        return ManFormatter
    elif fmt in ('md', 'markdown'):
        return MarkdownFormatter
    else:
        raise ValueError('Env var SHELLMAN_FORMAT incorrect')
