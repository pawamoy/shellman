# -*- coding: utf-8 -*-

"""
Doc module.

This module contains the class Doc.
"""

from __future__ import print_function

import os
import re

import sys

from .tag import FN_TAG, FN_TAGS, TAGS, Tag


def err(*args, **kwargs):
    """Wrapper around print function to output on stderr."""
    print(*args, file=sys.stderr, **kwargs)


def _tag_value(line):
    """
    Get the tag and/or its value from a documentation comment (line).

    Args:
        line (str): the documentation comment.

    Returns:
        tuple: tag, rest of the line. tag can be None.
    """
    line = line.lstrip('#')
    first_char = line.lstrip(' ')[0]
    if first_char in '@\\':
        words = line.lstrip(' ').split(' ')
        return words[0][1:], ' '.join(words[1:])

    if len(line) > 1:
        if line[0] == ' ':
            return None, line[1:]
    return None, line


class Doc(object):
    """
    Doc class.

    Instantiate with the path of a file.
    This class provides a public method ``read`` to use when you actually
    want to read the file and get its documentation as dict of nested lists.
    """

    def __init__(self, file, whitelist=None):
        """
        Init method.

        Args:
            file (str): path to the file to read.
            whitelist (dict): dict of tags to not check.
        """
        self.file = file
        self.doc = {k: None for k in TAGS}
        self.doc['_file'] = os.path.basename(self.file)
        self.doc['_fn'] = []
        if whitelist is None:
            self.whitelist = {}
        else:
            self.whitelist = whitelist

    def _update_value(self, tag, value, end=False):
        """
        Update the value of the given tag.

        It will append the value to the current tag or append a new tag and
        initialize it with the value.

        Args:
            tag (str): a doc tag such as brief, author, ...
            value (str): the value written after the tag
            end (bool): append a new tag (don't append value to current one)

        Returns:
            bool: True if tag has ended, False otherwise
        """
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

    def _update_fn_value(self, tag, value, end=False):
        """
        Update the value of the given function tag.

        It will append the value to the current tag or append a new tag and
        initialize it with the value.

        Args:
            tag (str): a doc tag such as brief, author, ...
            value (str): the value written after the tag
            end (bool): append a new tag (don't append value to current one)

        Returns:
            bool: True if tag has ended, False otherwise
        """
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

    # pylama:ignore=R701,C901,R0912
    def _read(self, warn=False, nice=True, failfast=False):
        """
        Read the file, build the documentation as dict of nested lists.

        After a call to this method, documentation is still accessible via
        self.doc attribute.

        Returns:
            dict: built documentation.
        """
        current_tag = None
        in_tag = False
        in_function = False
        warnings = []
        with open(self.file) as f:

            for i, line in enumerate(f):
                line = line.lstrip(' \t')

                if line == '\n':
                    current_tag = None
                    in_tag = False
                    continue

                if not re.search(r'^##', line):
                    current_tag = None
                    in_tag = False
                    continue

                tag, value = _tag_value(line)

                if tag is None:
                    if not in_tag:
                        if current_tag not in self.whitelist.keys():
                            warnings.append('%d: line ignored' % (i + 1))
                            if not nice and failfast:
                                break
                        continue

                    if in_function:
                        in_tag = self._update_fn_value(current_tag, value)
                    else:
                        in_tag = self._update_value(current_tag, value)

                    continue

                current_tag = tag

                if tag == FN_TAG:
                    in_function = True
                    self.doc['_fn'].append({k: None for k in FN_TAGS})
                    in_tag = self._update_fn_value(current_tag, value,
                                                   end=True)

                else:
                    if in_function and tag in FN_TAGS.keys():
                        in_tag = self._update_fn_value(current_tag, value,
                                                       end=True)
                    elif tag in TAGS.keys():
                        in_function = False
                        if (TAGS[tag].occurrences == Tag.MANY or
                                self.doc[tag] is None):
                            in_tag = self._update_value(current_tag, value,
                                                        end=True)
                        else:
                            warnings.append('%d: tag "%s" should be unique' % (
                                i + 1, current_tag))
                            if not nice and failfast:
                                break
                    elif tag not in self.whitelist.keys():
                        warnings.append('%d: invalid tag "%s"' % (
                            i + 1, current_tag))
                        if not nice and failfast:
                            break

        if warn and warnings:
            for warning in warnings:
                err('%s:%s' % (self.file, warning))

        ok = nice or not warnings

        return self.doc, ok

    def read(self):
        """Wrapper around self._read (no warn, nice, no failfast)."""
        doc, _ = self._read(warn=False, nice=True, failfast=False)
        return doc

    def check(self, warn=True, nice=True, failfast=False):
        """Wrapper around self._read to check documentation."""
        _, ok = self._read(warn=warn, nice=nice, failfast=failfast)
        return ok
