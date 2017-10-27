# -*- coding: utf-8 -*-

import sys
from builtins import object
from collections import defaultdict

from .reader import DocGroup, DocType
from .tag import GROUP_TAGS, TAGS


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Warning(object):
    ORPHAN = 'orphan-block'
    INVALID = 'invalid-block'
    UNKNOWN = 'unknown-tag'
    UNKNOWN_GROUP = 'unknown-group-tag'
    OCCURRENCES = 'too-many-occurrences'
    LINES = 'too-many-lines'
    EMPTY = 'empty-tag'

    def __init__(self, message_type, path, lineno, message):
        self.message_type = message_type
        self.path = path
        self.lineno = lineno
        self.message = message

    def __str__(self):
        return '%s:%d: %s: %s' % (
            self.path, self.lineno, self.message_type, self.message)


class OrphanBlockWarning(Warning):
    def __init__(self, path, lineno, message):
        super(OrphanBlockWarning, self).__init__(
            Warning.ORPHAN, path, lineno, message)


class InvalidBlockWarning(Warning):
    def __init__(self, path, lineno, message):
        super(InvalidBlockWarning, self).__init__(
            Warning.INVALID, path, lineno, message)


class UnknownTagWarning(Warning):
    def __init__(self, path, lineno, message):
        super(UnknownTagWarning, self).__init__(
            Warning.UNKNOWN, path, lineno, message)


class UnknownGroupTagWarning(Warning):
    def __init__(self, path, lineno, message):
        super(UnknownGroupTagWarning, self).__init__(
            Warning.UNKNOWN_GROUP, path, lineno, message)


class OccurrencesWarning(Warning):
    def __init__(self, path, lineno, message):
        super(OccurrencesWarning, self).__init__(
            Warning.OCCURRENCES, path, lineno, message)


class LinesWarning(Warning):
    def __init__(self, path, lineno, message):
        super(LinesWarning, self).__init__(
            Warning.LINES, path, lineno, message)


class EmptyWarning(Warning):
    def __init__(self, path, lineno, message):
        super(EmptyWarning, self).__init__(
            Warning.EMPTY, path, lineno, message)


class Checker(object):
    def __init__(self,
                 doc_object,
                 tags=TAGS,
                 group_tags=GROUP_TAGS):
        self.warnings = []
        self.blocks = []
        self.groups = []
        self.arranged_blocks = defaultdict(lambda: [])
        self.arranged_groups = defaultdict(lambda: [])
        self.tags = tags
        self.group_tags = group_tags
        self._process(doc_object.blocks)
        self._check_blocks()
        self._check_groups()

    def __bool__(self):
        return not self.warnings

    def _check_blocks(self):
        for block in self.blocks:
            tag = self.tags[block.tag]
            self.arranged_blocks[tag.name].append(block)
            if tag.lines == 1 and block.lines_number > 1:
                self.warnings.append(LinesWarning(
                    block.path, block.lineno,
                    '%s (%d/1)' % (tag.name, block.lines_number)))
            if tag.header and not block.value:
                self.warnings.append(EmptyWarning(
                    block.path, block.lineno, tag.name))
        for tag_name, blocks in self.arranged_blocks.items():
            occurrences = len(blocks)
            if self.tags[tag_name].occurrences == 1 and occurrences > 1:
                for block in blocks[1:]:
                    self.warnings.append(OccurrencesWarning(
                        block.path, block.lineno,
                        '%s (%d/1)' % (tag_name, occurrences)))

    def _check_groups(self):
        pass

    def _process(self, blocks):
        for block in blocks:
            self._process_group(block)

    def _process_group(self, group):
        in_group = None
        current_group = DocGroup()
        for block in group.blocks:
            block_tag = block.tag

            if not block_tag:
                if block.doc_type == DocType.ORPHAN_VALUE:
                    self.warnings.append(OrphanBlockWarning(
                        block.path, block.lineno, block.value))
                else:
                    self.warnings.append(InvalidBlockWarning(
                        block.path, block.lineno, block.value))
                continue

            if in_group:
                if block_tag in self.group_tags[in_group]:
                    current_group.append(block)
                elif block_tag in self.tags:
                    in_group = None
                    self.blocks.append(block)
                    if current_group:
                        self.groups.append(current_group)
                        current_group = DocGroup()
                else:
                    in_group = None
                    if current_group:
                        self.groups.append(current_group)
                        current_group = DocGroup()
                    self.warnings.append(UnknownGroupTagWarning(
                        block.path, block.lineno, block_tag))
            else:
                if block_tag in self.group_tags:
                    in_group = block_tag
                    current_group.append(block)
                elif block_tag in self.tags:
                    self.blocks.append(block)
                else:
                    # TODO: check if block tag is in a group
                    # to improve warning message
                    self.warnings.append(UnknownTagWarning(
                        block.path, block.lineno, block_tag))
        if current_group:
            self.groups.append(current_group)

    def warn(self):
        for warning in self.warnings:
            err(str(warning))
