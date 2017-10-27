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

import re
from builtins import object

tag_value_regexp = re.compile(r'^\s*[\\@]([_a-zA-Z]\w*)\s+(.+)$')
tag_no_value_regexp = re.compile(r'^\s*[\\@]([_a-zA-Z]\w*)\s*$')


class DocType(object):
    TAG = 'T'
    TAG_VALUE = 'TV'
    VALUE = 'V'
    ORPHAN_VALUE = 'OV'
    INVALID = 'I'


class DocLine(object):

    def __init__(self, path, lineno, tag, value, orphan):
        self.path = path
        self.lineno = lineno
        self.tag = tag
        self.value = value
        self.orphan = orphan

    def __str__(self):
        doc_type = self.doc_type()
        if doc_type == DocType.TAG_VALUE:
            s = '%s, "%s"' % (self.tag, self.value)
        elif doc_type == DocType.TAG:
            s = self.tag
        elif doc_type in (DocType.VALUE, DocType.ORPHAN_VALUE):
            s = '"%s"' % self.value
        else:
            s = 'invalid'
        return '%s:%s: %s: %s' % (self.path, self.lineno, self.doc_type(), s)

    def doc_type(self):
        if self.tag:
            if self.value:
                return DocType.TAG_VALUE
            return DocType.TAG
        if self.value is not None:
            if self.orphan:
                return DocType.ORPHAN_VALUE
            return DocType.VALUE
        return DocType.INVALID


class DocBlock(object):
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


class DocMixin(object):
    def __init__(self):
        self.blocks = []

    def __bool__(self):
        return bool(self.blocks)

    def __str__(self):
        return '\n\n'.join([str(block) for block in self.blocks])

    def append(self, block):
        self.blocks.append(block)


class DocGroup(DocMixin):
    def __init__(self, blocks=None):
        super().__init__()
        if blocks is not None:
            self.blocks = blocks


class DocStream(DocMixin):
    def __init__(self, stream):
        super().__init__()
        self.blocks = list(preprocess_blocks(preprocess_stream(stream)))


class DocFile(DocMixin):
    def __init__(self, path):
        super().__init__()
        with open(path) as stream:
            try:
                self.blocks = list(
                    preprocess_blocks(
                        preprocess_stream(stream)))
            except UnicodeDecodeError:
                print('Cannot read file %s' % path)
                self.blocks = []


def preprocess_stream(stream):
    current_block = []
    for lineno, line in enumerate(stream, 1):
        line = line.lstrip(' \t').rstrip('\n')
        if line.startswith('##'):
            current_block.append((stream.name, lineno, line))
        else:
            if current_block:
                yield current_block
                current_block = []
    if current_block:
        yield current_block


def preprocess_blocks(blocks):
    for block in blocks:
        sub_blocks = []
        current_block = DocBlock()
        orphan = True
        for path, lineno, line in block:
            line = line.lstrip('#')
            res = tag_value_regexp.search(line)
            if res:
                if current_block:
                    sub_blocks.append(current_block)
                    current_block = DocBlock()
                orphan = False
                tag, value = res.groups()
                current_block.append(DocLine(
                    path, lineno, tag, value, False))
            else:
                res = tag_no_value_regexp.search(line)
                if res:
                    if current_block:
                        sub_blocks.append(current_block)
                        current_block = DocBlock()
                    orphan = False
                    tag = res.groups()[0]
                    current_block.append(DocLine(
                        path, lineno, tag, '', False))
                elif orphan:
                    current_block.append(DocLine(
                        path, lineno, None, line, True))
                else:
                    current_block.append(DocLine(
                        path, lineno, None, line, False))
        if current_block:
            sub_blocks.append(current_block)
        if len(sub_blocks) == 1:
            yield sub_blocks[0]
        else:
            yield DocGroup(sub_blocks)
