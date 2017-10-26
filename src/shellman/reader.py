# -*- coding: utf-8 -*-

import re
from builtins import object

tag_value_regexp = re.compile(r'^\s*[\\@]([_a-zA-Z]\w*)\s+(.+)$')
tag_no_value_regexp = re.compile(r'^\s*[\\@]([_a-zA-Z]\w*)\s*$')


class DocLine(object):
    TAG = 'T'
    TAG_VALUE = 'TV'
    VALUE = 'V'
    ORPHAN_VALUE = 'OV'
    INVALID = 'I'

    def __init__(self, path, lineno, tag, value, orphan):
        self.path = path
        self.lineno = lineno
        self.tag = tag
        self.value = value
        self.orphan = orphan

    def __str__(self):
        line_type = self.line_type()
        if line_type == self.TAG_VALUE:
            s = '%s, "%s"' % (self.tag, self.value)
        elif line_type == self.TAG:
            s = self.tag
        elif line_type in (self.VALUE, self.ORPHAN_VALUE):
            s = '"%s"' % self.value
        else:
            s = 'invalid'
        return '%s:%s: %s: %s' % (self.path, self.lineno, self.line_type(), s)

    def line_type(self):
        if self.tag:
            if self.value:
                return self.TAG_VALUE
            return self.TAG
        if self.value is not None:
            if self.orphan:
                return self.ORPHAN_VALUE
            return self.VALUE
        return self.INVALID


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


class DocFile(object):
    def __init__(self, path):
        self.blocks = list(preprocess_blocks(preprocess_file(path)))

    def __bool__(self):
        return bool(self.blocks)

    def __str__(self):
        return '\n\n'.join([str(block) for block in self.blocks])

    def append(self, block):
        self.blocks.append(block)


def preprocess_file(path):
    current_block = []
    with open(path) as stream:
        for lineno, line in enumerate(stream, 1):
            line = line.lstrip(' \t').rstrip('\n')
            if line.startswith('##'):
                current_block.append((path, lineno, line))
            else:
                if current_block:
                    yield current_block
                    current_block = []
        if current_block:
            yield current_block


def preprocess_blocks(blocks):
    for block in blocks:
        current_block = DocBlock()
        orphan = True
        for path, lineno, line in block:
            line = line.lstrip('#')
            res = tag_value_regexp.search(line)
            if res:
                if current_block:
                    yield current_block
                    current_block = DocBlock()
                orphan = False
                tag, value = res.groups()
                current_block.append(DocLine(path, lineno, tag, value, False))
                continue
            res = tag_no_value_regexp.search(line)
            if res:
                if current_block:
                    yield current_block
                    current_block = DocBlock()
                orphan = False
                tag = res.groups()[0]
                current_block.append(DocLine(path, lineno, tag, None, False))
                continue
            if orphan:
                current_block.append(DocLine(path, lineno, None, line, True))
            else:
                current_block.append(DocLine(path, lineno, None, line, False))
        if current_block:
            yield current_block
