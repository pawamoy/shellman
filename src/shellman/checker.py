# -*- coding: utf-8 -*-

import sys

from .reader import DocType, DocGroup
from .tag import TAGS, GROUP_TAGS


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Checker(object):
    def __init__(self,
                 doc_object,
                 tags=TAGS,
                 group_tags=GROUP_TAGS):
        self.warnings = []
        self.blocks = []
        self.groups = []
        self.tags = tags
        self.group_tags = group_tags
        self._process(doc_object.blocks)

    def _process(self, blocks):
        for block in blocks:
            if isinstance(block, DocGroup):
                self._process_group(block)
            else:
                self._process_block(block)

    def _process_block(self, block):
        block_type = block.doc_type
        if block_type in (DocType.TAG, DocType.TAG_VALUE):
            block_tag = block.tag
            if block_tag in self.tags or block_tag in self.group_tags:
                self.blocks.append(block)
            else:
                self.warnings.append(
                    '%s:%d: unknown tag: %s' % (
                        block.path,
                        block.lineno,
                        block_tag
                    )
                )
        elif block_type == DocType.ORPHAN_VALUE:
            self.warnings.append(
                '%s:%d: orphan block: %s' % (
                    block.path,
                    block.lineno,
                    block.value
                )
            )
        else:
            self.warnings.append(
                '%s:%d: invalid block: %s' % (
                    block.path,
                    block.lineno,
                    block.value
                )
            )

    def _process_group(self, group):
        in_group = None
        current_group = DocGroup()
        for block in group.blocks:
            block_tag = block.tag

            if not block_tag:
                if block.doc_type == DocType.ORPHAN_VALUE:
                    self.warnings.append(
                        '%s:%d: orphan block: %s' % (
                            block.path,
                            block.lineno,
                            block.value
                        )
                    )
                else:
                    self.warnings.append(
                        '%s:%d: invalid block: %s' % (
                            block.path,
                            block.lineno,
                            block.value
                        )
                    )
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
                    self.warnings.append(
                        '%s:%d: unknown group tag: %s' % (
                            block.path,
                            block.lineno,
                            block_tag
                        )
                    )
            else:
                if block_tag in self.group_tags:
                    in_group = block_tag
                    current_group.append(block)
                elif block_tag in self.tags:
                    self.blocks.append(block)
                else:
                    self.warnings.append(
                        '%s:%d: unknown tag: %s' % (
                            block.path,
                            block.lineno,
                            block_tag
                        )
                    )
