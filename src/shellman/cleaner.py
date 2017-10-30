# -*- coding: utf-8 -*-

import sys
from builtins import object
from collections import defaultdict, namedtuple

from .reader import DocGroup, DocType
from .tag import GROUP_TAGS, TAGS


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ShellmanWarning(object):
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


class OrphanBlockWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(OrphanBlockWarning, self).__init__(
            ShellmanWarning.ORPHAN, path, lineno, message)


class InvalidBlockWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(InvalidBlockWarning, self).__init__(
            ShellmanWarning.INVALID, path, lineno, message)


class UnknownTagWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(UnknownTagWarning, self).__init__(
            ShellmanWarning.UNKNOWN, path, lineno, message)


class UnknownGroupTagWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(UnknownGroupTagWarning, self).__init__(
            ShellmanWarning.UNKNOWN_GROUP, path, lineno, message)


class OccurrencesWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(OccurrencesWarning, self).__init__(
            ShellmanWarning.OCCURRENCES, path, lineno, message)


class LinesWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(LinesWarning, self).__init__(
            ShellmanWarning.LINES, path, lineno, message)


class EmptyWarning(ShellmanWarning):
    def __init__(self, path, lineno, message):
        super(EmptyWarning, self).__init__(
            ShellmanWarning.EMPTY, path, lineno, message)


class Cleaner(object):
    def __init__(self,
                 doc_object=None,
                 tags=TAGS,
                 group_tags=GROUP_TAGS):
        self.warnings = []
        self.blocks = []
        self.groups = []
        self.tags = tags
        self.group_tags = group_tags

        if doc_object is not None:
            self.clean(doc_object.blocks)

    def __bool__(self):
        return not self.warnings

    @staticmethod
    def _arranged_blocks(blocks):
        arranged_blocks = defaultdict(lambda: [])
        for block in blocks:
            arranged_blocks[block.tag].append(block)
        return arranged_blocks

    def _clean_blocks(self):
        for block in self.blocks:
            tag = self.tags[block.tag]
            self._clean_lines(tag, block)
            self._clean_empty(tag, block)
        arranged_blocks = self._arranged_blocks(self.blocks)
        for tag_name, blocks in arranged_blocks.items():
            tag = self.tags[tag_name]
            self._clean_occurrences(tag, blocks)

    def _clean_groups(self):
        for group in self.groups:
            group_tag = group.blocks[0].tag
            group_tags = self.group_tags[group_tag]
            for block in group.blocks:
                tag = group_tags[block.tag]
                self._clean_lines(tag, block)
                self._clean_empty(tag, block)
            arranged_blocks = self._arranged_blocks(group.blocks)
            for tag_name, blocks in arranged_blocks.items():
                tag = group_tags[tag_name]
                self._clean_occurrences(tag, blocks)

    def _clean_lines(self, tag, block):
        if tag.lines == 1 and block.lines_number > 1:
            self.warnings.append(LinesWarning(
                block.path, block.lineno,
                '%s (%d/1)' % (tag.name, block.lines_number)))

    def _clean_empty(self, tag, block):
        if tag.header and not block.value:
            self.warnings.append(EmptyWarning(
                block.path, block.lineno, tag.name))

    def _clean_occurrences(self, tag, blocks):
        occurrences = len(blocks)
        if tag.occurrences == 1 and occurrences > 1:
            for block in blocks[1:]:
                self.warnings.append(OccurrencesWarning(
                    block.path, block.lineno,
                    '%s (%d/1)' % (tag.name, occurrences)))

    def _preclean_group(self, group):
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
                    groups = []
                    for group_name, group in self.group_tags.items():
                        if block_tag in group:
                            groups.append(group_name)
                    warning_message = block_tag
                    if groups:
                        warning_message += ' (found outside group %s)' % (
                            '/'.join(groups))
                    self.warnings.append(UnknownTagWarning(
                        block.path, block.lineno, warning_message))
        if current_group:
            self.groups.append(current_group)

    def clean(self, groups):
        for group in groups:
            self._preclean_group(group)
        self._clean_blocks()
        self._clean_groups()

    def minified(self):
        minified_blocks = defaultdict(lambda: [])
        for block in self.blocks:
            minified_blocks[block.tag].append(block.values)
        minified_groups = defaultdict(lambda: [])
        for group in self.groups:
            group_tag = group.blocks[0].tag
            minified_group = defaultdict(lambda: [])
            for block in group.blocks:
                minified_group[block.tag].append(block.values)
            minified_groups[group_tag].append(minified_group)
        return namedtuple('minified', 'blocks groups')(
            minified_blocks, minified_groups)

    # TODO: add sorting and format options
    def warn(self):
        for warning in sorted(self.warnings, key=lambda w: w.lineno):
            err(str(warning))
