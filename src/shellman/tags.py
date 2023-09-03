"""Section module.

This module contains the Section class.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from shellman.reader import DocLine


class Tag:
    """Base class for tags."""

    def __init__(self, text: str) -> None:
        """Initialize the tag.

        Parameters:
            text: The tag's text.
        """
        self.text = text

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> Tag:
        """Parse a sequence of lines into a tag instance.

        Parameters:
            lines: The sequence of lines to parse.

        Returns:
            A tag instance.
        """
        return cls(text="\n".join(line.value for line in lines))


class AuthorTag(Tag):
    """A tag representing an author."""


class BugTag(Tag):
    """A tag representing a bug note."""


class BriefTag(Tag):
    """A tag representing a summary."""


class CaveatTag(Tag):
    """A tag representing caveats."""


class CopyrightTag(Tag):
    """A tag representing copyright information."""


class DateTag(Tag):
    """A tag representing a date."""


class DescTag(Tag):
    """A tag representing a description."""


class EnvTag(Tag):
    """A tag representing an environment variable used by the script."""

    def __init__(self, name: str, description: str) -> None:
        """Initialize the tag.

        Parameters:
            name: The variable name.
            description: The variable description.
        """
        self.name = name
        self.description = description

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> EnvTag:  # noqa: D102
        name, description = "", []
        for line in lines:
            if line.tag == "env":
                split = line.value.split(" ", 1)
                if len(split) > 1:
                    name = split[0]
                    description.append(split[1])
                else:
                    name = split[0]
            else:
                description.append(line.value)
        return EnvTag(name=name, description="\n".join(description))


class ErrorTag(Tag):
    """A tag representing a known error."""


class ExampleTag(Tag):
    """A tag representing a code/shell example."""

    def __init__(self, brief: str, code: str, code_lang: str, description: str) -> None:
        """Initialize the tag.

        Parameters:
            brief: The example's summary.
            code: The example's code.
            code_lang: The example's language.
            description: The example's description.
        """
        self.brief = brief
        self.code = code
        self.code_lang = code_lang
        self.description = description

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


class ExitTag(Tag):
    """A tag representing an exit code."""

    def __init__(self, code: str, description: str) -> None:
        """Initialize the tag.

        Parameters:
            code: The exit code.
            description: The code description.
        """
        self.code = code
        self.description = description

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> ExitTag:  # noqa: D102
        code, description = "", []
        for line in lines:
            if line.tag == "exit":
                split = line.value.split(" ", 1)
                if len(split) > 1:
                    code = split[0]
                    description.append(split[1])
                else:
                    code = split[0]
            else:
                description.append(line.value)
        return ExitTag(code=code, description="\n".join(description))


class FileTag(Tag):
    """A tag representing a file used by a script."""

    def __init__(self, name: str, description: str) -> None:
        """Initialize the tag.

        Parameters:
            name: The file name text.
            description: The file description.
        """
        self.name = name
        self.description = description

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> FileTag:  # noqa: D102
        name, description = "", []
        for line in lines:
            if line.tag == "file":
                split = line.value.split(" ", 1)
                if len(split) > 1:
                    name = split[0]
                    description.append(split[1])
                else:
                    name = split[0]
            else:
                description.append(line.value)
        return FileTag(name=name, description="\n".join(description))


class FunctionTag(Tag):
    """A tag representing a shell function."""

    def __init__(
        self,
        prototype: str,
        brief: str,
        description: str,
        arguments: Sequence[str],
        preconditions: Sequence[str],
        return_codes: Sequence[str],
        seealso: Sequence[str],
        stderr: Sequence[str],
        stdin: Sequence[str],
        stdout: Sequence[str],
    ):
        """Initialize the tag.

        Parameters:
            prototype: The function's prototype.
            brief: The function's summary.
            description: The function's description.
            arguments: The function's arguments.
            preconditions: The function's preconditions.
            return_codes: The function's return codes.
            seealso: The function's "see also" information.
            stderr: The function's standard error.
            stdin: The function's standard input.
            stdout: The function's standard output.
        """
        self.prototype = prototype
        self.brief = brief
        self.description = description
        self.arguments = arguments
        self.preconditions = preconditions
        self.return_codes = return_codes
        self.seealso = seealso
        self.stderr = stderr
        self.stdin = stdin
        self.stdout = stdout

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


class HistoryTag(Tag):
    """A tag representing a script's history."""


class LicenseTag(Tag):
    """A tag representing a license."""


class NoteTag(Tag):
    """A tag representing a note."""


class OptionTag(Tag):
    """A tag representing a command-line option."""

    def __init__(self, short: str, long: str, positional: str, default: str, group: str, description: str) -> None:
        """Initialize the tag.

        Parameters:
            short: The option short flag.
            long: The option long flag.
            positional: The option positional arguments.
            default: The option default value.
            group: The option group.
            description: The option description.
        """
        self.short = short
        self.long = long
        self.positional = positional
        self.default = default
        self.group = group
        self.description = description
        self.__signature: str = None  # type: ignore[assignment]

    @property
    def signature(self) -> str:
        """The signature of the option."""
        if self.__signature is not None:
            return self.__signature
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
        self.__signature = sign
        return self.__signature

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


class SeealsoTag(Tag):
    """A tag representing "See Also" information."""


class StderrTag(Tag):
    """A tag representing the standard error of a script/function."""


class StdinTag(Tag):
    """A tag representing the standard input of a script/function."""


class StdoutTag(Tag):
    """A tag representing the standard output of a script/function."""


class UsageTag(Tag):
    """A tag representing the command-line usage of a script."""

    def __init__(self, program: str, command: str) -> None:
        """Initialize the tag.

        Parameters:
            program: The program name.
            command: The command-line usage.
        """
        self.program = program
        self.command = command

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


class VersionTag(Tag):
    """A tag representing a version."""

    def __init__(self, text: str) -> None:
        """Initialize the tag.

        Parameters:
            text: The version text.
        """
        self.text = text

    @classmethod
    def from_lines(cls, lines: Sequence[DocLine]) -> VersionTag:  # noqa: D102
        # TODO: only first line kept. Change it?
        return VersionTag(text=lines[0].value)


TAGS: dict[str | None, type[Tag]] = {
    None: Tag,
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
