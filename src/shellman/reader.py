"""Module to read a file/stream and pre-process the documentation lines.

Algorithm is as follows:

1. preprocess_stream: yield documentation lines.
2. preprocess_lines: group documentation lines as blocks of documentation.
3. process_blocks: tidy blocks by tag in a dictionary.
"""

from __future__ import annotations

import logging
import os
import re
from collections import defaultdict
from typing import Iterable, Iterator, Sequence

from shellman.tags import TAGS, Tag

logger = logging.getLogger(__name__)

tag_value_regex = re.compile(r"^\s*[\\@]([_a-zA-Z][\w-]*)\s+(.+)$")
tag_no_value_regex = re.compile(r"^\s*[\\@]([_a-zA-Z][\w-]*)\s*$")


class DocType:
    """Enumeration of the possible types of documentation."""

    TAG = "T"
    """A tag."""

    TAG_VALUE = "TV"
    """A tag its value."""

    VALUE = "V"
    """A value."""

    INVALID = "I"
    """Invalid type."""


class DocLine:
    """A documentation line."""

    def __init__(self, path: str, lineno: int, tag: str | None, value: str) -> None:
        """Initialize the doc line.

        Parameters:
            path: The origin file path.
            lineno: The line number in the file.
            tag: The line's tag, if any.
            value: The line's value.
        """
        self.path = path
        self.lineno = lineno
        self.tag = tag or ""
        self.value = value

    def __str__(self) -> str:
        doc_type = self.doc_type
        if doc_type == DocType.TAG_VALUE:
            s = f'{self.tag}, "{self.value}"'
        elif doc_type == DocType.TAG:
            s = self.tag
        elif doc_type == DocType.VALUE:
            s = '"%s"' % self.value
        else:
            s = "invalid"
        return f"{self.path}:{self.lineno}: {doc_type}: {s}"

    @property
    def doc_type(self) -> str:
        """The line's doc type."""
        if self.tag:
            if self.value:
                return DocType.TAG_VALUE
            return DocType.TAG
        if self.value is not None:
            return DocType.VALUE
        return DocType.INVALID


class DocBlock:
    """A documentation block."""

    def __init__(self, lines: list[DocLine] | None = None) -> None:
        """Initialize the doc block.

        Parameters:
            lines: The block's doc lines.
        """
        if lines is None:
            lines = []
        self.lines = lines

    def __bool__(self) -> bool:
        return bool(self.lines)

    def __str__(self) -> str:
        return "\n".join([str(line) for line in self.lines])

    def append(self, line: DocLine) -> None:
        """Append a line to the block.

        Parameters:
            line: The doc line to append.
        """
        self.lines.append(line)

    @property
    def doc_type(self) -> str:
        """The block type."""
        return self.lines[0].doc_type

    @property
    def first_line(self) -> DocLine:
        """The block's first doc line."""
        return self.lines[0]

    @property
    def lines_number(self) -> int:
        """The number of lines in the block."""
        return len(self.lines)

    @property
    def path(self) -> str:
        """The block's origin file path."""
        return self.first_line.path

    @property
    def lineno(self) -> int:
        """The block's first line number."""
        return self.first_line.lineno

    @property
    def tag(self) -> str:
        """The block's tag."""
        if self.lines:
            return self.first_line.tag
        return ""

    @property
    def value(self) -> str:
        """The block's first line."""
        return self.first_line.value

    @property
    def values(self) -> list[str]:
        """The block's lines."""
        return [line.value for line in self.lines]


class DocStream:
    """A stream of shell code or documentation."""

    def __init__(self, stream: Iterable[str], filename: str = "") -> None:
        """Initialize the documentation file.

        Parameters:
            stream: A text stream.
            filename: An optional file name.
        """
        self.filepath = None
        self.filename = filename
        self.sections = _process_blocks(_preprocess_lines(_preprocess_stream(stream)))


class DocFile:
    """A shell script or documentation file."""

    def __init__(self, path: str) -> None:
        """Initialize the documentation file.

        Parameters:
            path: The path to the file.
        """
        self.filepath = path
        self.filename = os.path.basename(path)
        with open(path, encoding="utf-8") as stream:
            try:
                self.sections = _process_blocks(_preprocess_lines(_preprocess_stream(stream)))
            except UnicodeDecodeError:
                logger.error(f"Cannot read file {path}")  # noqa: TRY400
                self.sections = {}


def _preprocess_stream(stream: Iterable[str]) -> Iterator[tuple[str, int, str]]:
    name = getattr(stream, "name", "")
    for lineno, line in enumerate(stream, 1):
        line = line.lstrip(" \t").rstrip("\n")  # noqa: PLW2901
        if line.startswith("##"):
            yield name, lineno, line


def _preprocess_lines(lines: Iterable[tuple[str, int, str]]) -> Iterator[DocBlock]:
    current_block = DocBlock()
    for path, lineno, line in lines:
        line = line[3:]  # noqa: PLW2901
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


def _process_blocks(blocks: Iterable[DocBlock]) -> dict[str, list[Tag]]:
    sections: dict[str, list[Tag]] = defaultdict(list)
    for block in blocks:
        tag_class = TAGS.get(block.tag, TAGS[None])
        sections[block.tag].append(tag_class.from_lines(block.lines))
    return dict(sections)


def _merge(docs: Sequence[DocStream | DocFile], filename: str) -> DocStream:
    final_doc = DocStream(stream=[], filename=filename)
    for doc in docs:
        for section, values in doc.sections.items():
            if section not in final_doc.sections:
                final_doc.sections[section] = []
            final_doc.sections[section].extend(values)
    return final_doc
