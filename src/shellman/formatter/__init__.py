# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Formatter module.

This module contains one Python module for each formatter, plus one for
the formatter base class.

It also provides a convenient function to get a formatter class given a
string argument describing this format.
"""

from .man import ManFormatter
from .markdown import MarkdownFormatter
from .text import TextFormatter


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
