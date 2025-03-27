"""Section module.

This module contains the Section class.
"""

from __future__ import annotations

import re
import sys
import warnings
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar

# YORE: EOL 3.10: Replace block with line 4.
if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from collections.abc import Sequence

    from shellman.reader import DocLine


# YORE: Bump 2: Remove block.
def __getattr__(name: str) -> Any:
    if name == "NameDescTag":
        warnings.warn("NameDescTag is deprecated, use ValueDescTag instead.", DeprecationWarning, stacklevel=2)
        return ValueDescTag
    raise AttributeError(f"module {__name__} has no attribute {name}")


class Tag:
    """Base class for tags."""

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> Tag:
        """Parse a sequence of lines into a tag instance.

        Parameters:
            lines: The sequence of lines to parse.

        Returns:
            A tag instance.
        """
        raise NotImplementedError


@dataclass
class TextTag(Tag):
    """A simple tag holding text only."""

    text: str
    """The tag's text."""

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> TextTag:  # noqa: D102
        return cls(text="\n".join(line.value for line in lines))


@dataclass
class ValueDescTag(Tag):
    """A tag holding a value and a description."""

    tag: ClassVar[str]
    """The tag name."""

    value_field_name: ClassVar[str] = "name"
    """The name of the field containing the value."""

    description_field_name: ClassVar[str] = "description"
    """The name of the field containing the description."""

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> Self:  # noqa: D102
        value, description = "", []
        for line in lines:
            if line.tag == cls.tag:
                split = line.value.split(" ", 1)
                if len(split) > 1:
                    value = split[0]
                    description.append(split[1])
                else:
                    value = split[0]
            else:
                description.append(line.value)
        return cls(**{cls.value_field_name: value, cls.description_field_name: "\n".join(description)})


@dataclass
class AuthorTag(TextTag):
    """A tag representing an author."""


@dataclass
class BugTag(TextTag):
    """A tag representing a bug note."""


@dataclass
class BriefTag(TextTag):
    """A tag representing a summary."""


@dataclass
class CaveatTag(TextTag):
    """A tag representing caveats."""


@dataclass
class CopyrightTag(TextTag):
    """A tag representing copyright information."""


@dataclass
class DateTag(TextTag):
    """A tag representing a date."""


@dataclass
class DescTag(TextTag):
    """A tag representing a description."""


@dataclass
class EnvTag(ValueDescTag):
    """A tag representing an environment variable used by the script."""

    tag: ClassVar[str] = "env"

    name: str
    """The environment variable name."""
    description: str
    """The environment variable description."""


@dataclass
class ErrorTag(TextTag):
    """A tag representing a known error."""


@dataclass
class ExampleTag(Tag):
    """A tag representing a code/shell example."""

    brief: str
    """The example's summary."""
    code: str
    """The example's code."""
    code_lang: str
    """The example's language."""
    description: str
    """The example's description."""

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> ExampleTag:  # noqa: D102
        brief, code, description = [], [], []
        code_lang = ""
        current = None
        for line in lines:
            if line.tag == "example":
                if line.value:
                    brief.append(line.value)
                current = "brief"
            elif line.tag == "example-code":
                if line.value:
                    code_lang = line.value
                current = "code"
            elif line.tag == "example-description":
                if line.value:
                    description.append(line.value)
                current = "description"
            elif current == "brief":
                brief.append(line.value)
            elif current == "code":
                code.append(line.value)
            elif current == "description":
                description.append(line.value)

        return ExampleTag(
            brief="\n".join(brief),
            code="\n".join(code),
            code_lang=code_lang,
            description="\n".join(description),
        )


@dataclass
class ExitTag(ValueDescTag):
    """A tag representing an exit code."""

    tag: ClassVar[str] = "exit"
    value_field_name: ClassVar[str] = "code"

    code: str
    """The exit code value."""
    description: str
    """The exit code description."""


@dataclass
class FileTag(ValueDescTag):
    """A tag representing a file used by a script."""

    tag: ClassVar[str] = "file"

    name: str
    """The file name/path."""
    description: str
    """The file description."""


@dataclass
class FunctionTag(Tag):
    """A tag representing a shell function."""

    prototype: str
    """The function's prototype."""
    brief: str
    """The function's summary."""
    description: str
    """The function's description."""
    arguments: Sequence[str]
    """The function's arguments."""
    preconditions: Sequence[str]
    """The function's preconditions."""
    return_codes: Sequence[str]
    """The function's return codes."""
    seealso: Sequence[str]
    """The function's "see also" information."""
    stderr: Sequence[str]
    """The function's standard error."""
    stdin: Sequence[str]
    """The function's standard input."""
    stdout: Sequence[str]
    """The function's standard output."""

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> FunctionTag:  # noqa: D102
        brief = ""
        prototype = ""
        description = []
        arguments = []
        return_codes = []
        preconditions = []
        seealso = []
        stderr = []
        stdin = []
        stdout = []
        for line in lines:
            if line.tag == "function":
                prototype = line.value
            elif line.tag == "function-brief":
                brief = line.value
            elif line.tag == "function-description":
                description.append(line.value)
            elif line.tag == "function-argument":
                arguments.append(line.value)
            elif line.tag == "function-precondition":
                preconditions.append(line.value)
            elif line.tag == "function-return":
                return_codes.append(line.value)
            elif line.tag == "function-seealso":
                seealso.append(line.value)
            elif line.tag == "function-stderr":
                stderr.append(line.value)
            elif line.tag == "function-stdin":
                stdin.append(line.value)
            elif line.tag == "function-stdout":
                stdout.append(line.value)
            else:
                description.append(line.value)

        return FunctionTag(
            prototype=prototype,
            brief=brief,
            description="\n".join(description),
            arguments=arguments,
            preconditions=preconditions,
            return_codes=return_codes,
            seealso=seealso,
            stderr=stderr,
            stdin=stdin,
            stdout=stdout,
        )


@dataclass
class HistoryTag(TextTag):
    """A tag representing a script's history."""


@dataclass
class LicenseTag(TextTag):
    """A tag representing a license."""


@dataclass
class NoteTag(TextTag):
    """A tag representing a note."""


@dataclass
class OptionTag(Tag):
    """A tag representing a command-line option."""

    short: str
    """The option short flag."""
    long: str
    """The option long flag."""
    positional: str
    """The option positional arguments."""
    default: str
    """The option default value."""
    group: str
    """The option group."""
    description: str
    """The option description."""

    @cached_property
    def signature(self) -> str:
        """The signature of the option."""
        sign = ""
        if self.short:
            sign = self.short
            if self.long:
                sign += ", "
            elif self.positional:
                sign += " "
        if self.long:
            if not self.short:
                sign += "    "
            sign += self.long + " "
        if self.positional:
            sign += self.positional
        return sign

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> OptionTag:  # noqa: D102
        short, long, positional, default, group = "", "", "", "", ""
        description = []
        for line in lines:
            if line.tag == "option":
                search = re.search(
                    r"^(?P<short>-\w)?(?:, )?(?P<long>--[\w-]+)? ?(?P<positional>.+)?",
                    line.value,
                )
                if search:
                    short, long, positional = search.groups(default="")
                else:
                    positional = line.value
            elif line.tag == "option-default":
                default = line.value
            elif line.tag == "option-group":
                group = line.value
            else:
                description.append(line.value)
        return OptionTag(
            short=short,
            long=long,
            positional=positional,
            default=default,
            group=group,
            description="\n".join(description),
        )


@dataclass
class SeealsoTag(TextTag):
    """A tag representing "See Also" information."""


@dataclass
class StderrTag(TextTag):
    """A tag representing the standard error of a script/function."""


@dataclass
class StdinTag(TextTag):
    """A tag representing the standard input of a script/function."""


@dataclass
class StdoutTag(TextTag):
    """A tag representing the standard output of a script/function."""


@dataclass
class UsageTag(Tag):
    """A tag representing the command-line usage of a script."""

    program: str
    """The program name."""
    command: str
    """The command-line usage."""

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> UsageTag:  # noqa: D102
        program, command = "", ""
        split = lines[0].value.split(" ", 1)
        if len(split) > 1:
            program, command = split
        else:
            program = split[0]
        if len(lines) > 1:
            command = command + "\n" + "\n".join(line.value for line in lines[1:])
        return UsageTag(program=program, command=command)


@dataclass
class VersionTag(TextTag):
    """A tag representing a version."""


TAGS: dict[str | None, type[Tag]] = {
    None: TextTag,
    "author": AuthorTag,
    "bug": BugTag,
    "brief": BriefTag,
    "caveat": CaveatTag,
    "copyright": CopyrightTag,
    "date": DateTag,
    "desc": DescTag,
    "env": EnvTag,
    "error": ErrorTag,
    "example": ExampleTag,
    "exit": ExitTag,
    "file": FileTag,
    "function": FunctionTag,
    "history": HistoryTag,
    "license": LicenseTag,
    "note": NoteTag,
    "option": OptionTag,
    "seealso": SeealsoTag,
    "stderr": StderrTag,
    "stdin": StdinTag,
    "stdout": StdoutTag,
    "usage": UsageTag,
    "version": VersionTag,
}
