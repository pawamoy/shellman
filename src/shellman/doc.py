# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re

from .tag import FN_TAG, FN_TAGS, TAGS, Tag


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
