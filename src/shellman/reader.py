# -*- coding: utf-8 -*-

"""
Module to read a file/stream and pre-process the documentation lines.

Algorithm is as follows:
1. preprocess_stream: yield documentation lines.
2. preprocess_lines: group documentation lines as blocks of documentation.
3. process_blocks: tidy blocks by tag in a dictionary.

"""

import os
import re
from collections import defaultdict

from .tags import TAGS

tag_value_regex = re.compile(r"^\s*[\\@]([_a-zA-Z][\w-]*)\s+(.+)$")
tag_no_value_regex = re.compile(r"^\s*[\\@]([_a-zA-Z][\w-]*)\s*$")


class DocType:
    TAG = "T"
    TAG_VALUE = "TV"
    VALUE = "V"
    INVALID = "I"


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
            s = "invalid"
        return "%s:%s: %s: %s" % (self.path, self.lineno, doc_type, s)

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

    # Python 2 compatibility
    def __nonzero__(self):
        return bool(self.lines)

    def __str__(self):
        return "\n".join([str(line) for line in self.lines])

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
        if self.lines:
            return self.first_line.tag
        return ""

    @property
    def value(self):
        return self.first_line.value

    @property
    def values(self):
        return [line.value for line in self.lines]


class DocStream:
    def __init__(self, stream, filename=""):
        self.filepath = None
        self.filename = filename
        self.sections = process_blocks(preprocess_lines(preprocess_stream(stream)))


class DocFile:
    def __init__(self, path):
        self.filepath = path
        self.filename = os.path.basename(path)
        with open(path) as stream:
            try:
                self.sections = process_blocks(
                    preprocess_lines(preprocess_stream(stream))
                )
            except UnicodeDecodeError:
                print("Cannot read file %s" % path)
                self.sections = []


def preprocess_stream(stream):
    name = getattr(stream, "name", "")
    for lineno, line in enumerate(stream, 1):
        line = line.lstrip(" \t").rstrip("\n")
        if line.startswith("## "):
            yield name, lineno, line


def preprocess_lines(lines):
    current_block = DocBlock()
    for path, lineno, line in lines:
        line = line[3:]
        res = tag_value_regex.search(line)
        if res:
            tag, value = res.groups()
            if current_block and not tag.startswith(current_block.tag + "-"):
                yield current_block
                current_block = DocBlock()
            current_block.append(DocLine(path, lineno, tag, value))
        else:
            res = tag_no_value_regex.search(line)
            if res:
                tag = res.groups()[0]
                if current_block and not tag.startswith(current_block.tag + "-"):
                    yield current_block
                    current_block = DocBlock()
                current_block.append(DocLine(path, lineno, tag, ""))
            else:
                current_block.append(DocLine(path, lineno, None, line))
    if current_block:
        yield current_block


def process_blocks(blocks):
    sections = defaultdict(list)
    for block in blocks:
        tag_class = TAGS.get(block.tag, TAGS[None])
        sections[block.tag].append(tag_class.from_lines(block.lines))
    return dict(sections)


def merge(docs, filename):
    final_doc = DocStream(stream=[], filename=filename)
    for doc in docs:
        for section, values in doc.sections.items():
            if section not in final_doc.sections:
                final_doc.sections[section] = []
            final_doc.sections[section].extend(values)
    return final_doc
