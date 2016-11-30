# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
