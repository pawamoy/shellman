# -*- coding: utf-8 -*-

"""
Module to read a file/stream and pre-process the documentation lines.

Algorithm is as follows:
1. preprocess_stream: filter blocks of documentation (blocks of lines
    starting with or without spaces, then double-hash)
2. preprocess_blocks: separate blocks by tag and groups of tags,
    transform them into DocBlock objects (composed of DocLine objects).
"""

# 3. arrange_blocks: return a named tuple with valid blocks (arranged by tag in
#     a dictionary), orphan lines and invalid lines.
#
# DocFile and DocStream object will stop after step 2, while DocStruct will
# execute every steps. It means that every block within a DocStruct has a tag
# (this is not true for DocFile and DocStream objects).

import os
import re
import sys
from collections import defaultdict

from .tags import TAGS

tag_value_regexp = re.compile(r'^\s*[\\@]([_a-zA-Z][\w-]*)\s+(.+)$')
tag_no_value_regexp = re.compile(r'^\s*[\\@]([_a-zA-Z][\w-]*)\s*$')


class DocType:
    TAG = 'T'
    TAG_VALUE = 'TV'
    VALUE = 'V'
    INVALID = 'I'


class DocLine:

    def __init__(self, path, lineno, tag, value):
        self.path = path
        self.lineno = lineno
        self.tag = tag
        self.value = value

    def __str__(self):
        doc_type = self.doc_type()
        if doc_type == DocType.TAG_VALUE:
            s = '%s, "%s"' % (self.tag, self.value)
        elif doc_type == DocType.TAG:
            s = self.tag
        elif doc_type == DocType.VALUE:
            s = '"%s"' % self.value
        else:
            s = 'invalid'
        return '%s:%s: %s: %s' % (self.path, self.lineno, doc_type, s)

    def doc_type(self):
        if self.tag:
            if self.value:
                return DocType.TAG_VALUE
            return DocType.TAG
        if self.value is not None:
            return DocType.VALUE
        return DocType.INVALID


class DocBlock:
    def __init__(self, lines=None):
        if lines is None:
            lines = []
        self.lines = lines

    def __bool__(self):
        return bool(self.lines)

    def __str__(self):
        return '\n'.join([str(line) for line in self.lines])

    def append(self, line):
        self.lines.append(line)

    @property
    def doc_type(self):
        return self.lines[0].doc_type()

    @property
    def first_line(self):
        return self.lines[0]

    @property
    def lines_number(self):
        return len(self.lines)

    @property
    def path(self):
        return self.first_line.path

    @property
    def lineno(self):
        return self.first_line.lineno

    @property
    def tag(self):
        return self.first_line.tag

    @property
    def value(self):
        return self.first_line.value

    @property
    def values(self):
        return [line.value for line in self.lines]


class DocGroup:
    def __init__(self, blocks=None):
        if blocks is None:
            blocks = []
        self.blocks = blocks

    def __bool__(self):
        return bool(self.blocks)

    def __str__(self):
        return '\n\n'.join([str(block) for block in self.blocks])

    def append(self, block):
        self.blocks.append(block)


class DocStream(DocGroup):
    def __init__(self, stream, name=''):
        super(DocStream, self).__init__()
        self.filename = name or stream.name
        self.blocks = list(preprocess_lines(preprocess_stream(stream)))
        self.sections = process_blocks(self.blocks)


class DocFile(DocGroup):
    def __init__(self, path):
        super(DocFile, self).__init__()
        self.filename = os.path.basename(path)
        with open(path) as stream:
            try:
                self.blocks = list(preprocess_lines(
                    preprocess_stream(stream)))
            except UnicodeDecodeError:
                print('Cannot read file %s' % path)
                self.blocks = []
        self.sections = process_blocks(self.blocks)


def preprocess_stream(stream):
    for lineno, line in enumerate(stream, 1):
        line = line.lstrip(' \t').rstrip('\n')
        if line.startswith('##'):
            yield stream.name, lineno, line


def preprocess_lines(lines):
    current_block = DocBlock()
    for path, lineno, line in lines:
        line = line.lstrip('#')
        res = tag_value_regexp.search(line)
        if res:
            tag, value = res.groups()
            if current_block and not tag.startswith(current_block.tag + '-'):
                yield current_block
                current_block = DocBlock()
            current_block.append(DocLine(
                path, lineno, tag, value))
        else:
            res = tag_no_value_regexp.search(line)
            if res:
                tag = res.groups()[0]
                if current_block and not tag.startswith(current_block.tag + '-'):
                    yield current_block
                    current_block = DocBlock()
                current_block.append(DocLine(
                    path, lineno, tag, ''))
            else:
                current_block.append(DocLine(
                    path, lineno, None, line[1:]))
    if current_block:
        yield current_block


def process_blocks(blocks):
    sections = defaultdict(list)
    for block in blocks:
        if block.tag is None:
            print('shellman: warning: untagged documentation between lines %d and %d' % (
                block.lineno, block.lines[-1].lineno
            ), file=sys.stderr)
            continue
        tag_class = TAGS.get(block.tag)
        if tag_class:
            sections[block.tag].append(tag_class.from_lines(block.lines))
    return dict(sections)
