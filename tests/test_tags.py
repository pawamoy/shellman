"""Tests for the `tags` module."""

from shellman._internal.reader import DocLine
from shellman._internal.tags import (
    AuthorTag,
    BriefTag,
    BugTag,
    CaveatTag,
    CopyrightTag,
    DateTag,
    DescTag,
    EnvTag,
    ErrorTag,
    ExampleTag,
    ExitTag,
    FileTag,
    FunctionTag,
    HistoryTag,
    LicenseTag,
    NoteTag,
    OptionTag,
    SeealsoTag,
    StderrTag,
    StdinTag,
    StdoutTag,
    UsageTag,
    VersionTag,
)


def test_author_tag() -> None:
    """Test author tag."""
    lines = [DocLine(tag="author", value="John Doe", path="test_path", lineno=1)]
    tag = AuthorTag.from_lines(lines)
    assert isinstance(tag, AuthorTag)
    assert tag.text == "John Doe"


def test_brief_tag() -> None:
    """Test brief tag."""
    lines = [DocLine(tag="brief", value="This is a brief summary.", path="test_path", lineno=2)]
    tag = BriefTag.from_lines(lines)
    assert isinstance(tag, BriefTag)
    assert tag.text == "This is a brief summary."


def test_bug_tag() -> None:
    """Test bug tag."""
    lines = [DocLine(tag="bug", value="Fix issue #123", path="test_path", lineno=3)]
    tag = BugTag.from_lines(lines)
    assert isinstance(tag, BugTag)
    assert tag.text == "Fix issue #123"


def test_caveat_tag() -> None:
    """Test caveat tag."""
    lines = [DocLine(tag="caveat", value="Use with caution.", path="test_path", lineno=4)]
    tag = CaveatTag.from_lines(lines)
    assert isinstance(tag, CaveatTag)
    assert tag.text == "Use with caution."


def test_copyright_tag() -> None:
    """Test copyright tag."""
    lines = [DocLine(tag="copyright", value="Copyright 2023.", path="test_path", lineno=5)]
    tag = CopyrightTag.from_lines(lines)
    assert isinstance(tag, CopyrightTag)
    assert tag.text == "Copyright 2023."


def test_date_tag() -> None:
    """Test date tag."""
    lines = [DocLine(tag="date", value="2023-01-01", path="test_path", lineno=6)]
    tag = DateTag.from_lines(lines)
    assert isinstance(tag, DateTag)
    assert tag.text == "2023-01-01"


def test_desc_tag() -> None:
    """Test description tag."""
    lines = [DocLine(tag="desc", value="This is a description.", path="test_path", lineno=7)]
    tag = DescTag.from_lines(lines)
    assert isinstance(tag, DescTag)
    assert tag.text == "This is a description."


def test_env_tag() -> None:
    """Test env tag."""
    lines = [
        DocLine(tag="env", value="VAR_NAME Variable description", path="test_path", lineno=8),
        DocLine(tag=None, value="Additional details.", path="test_path", lineno=9),
    ]
    tag = EnvTag.from_lines(lines)
    assert isinstance(tag, EnvTag)
    assert tag.name == "VAR_NAME"
    assert tag.description == "Variable description\nAdditional details."


def test_example_tag() -> None:
    """Test example tag."""
    lines = [
        DocLine(tag="example", value="Example brief", path="test_path", lineno=10),
        DocLine(tag="example-code", value="bash", path="test_path", lineno=11),
        DocLine(tag=None, value="echo 'Hello, World!'", path="test_path", lineno=12),
        DocLine(tag="example-description", value="This is an example.", path="test_path", lineno=13),
    ]
    tag = ExampleTag.from_lines(lines)
    assert isinstance(tag, ExampleTag)
    assert tag.brief == "Example brief"
    assert tag.code == "echo 'Hello, World!'"
    assert tag.code_lang == "bash"
    assert tag.description == "This is an example."


def test_error_tag() -> None:
    """Test error tag."""
    lines = [DocLine(tag="error", value="An error occurred.", path="test_path", lineno=14)]
    tag = ErrorTag.from_lines(lines)
    assert isinstance(tag, ErrorTag)
    assert tag.text == "An error occurred."


def test_exit_tag() -> None:
    """Test exit tag."""
    lines = [
        DocLine(tag="exit", value="1 Error occurred", path="test_path", lineno=15),
        DocLine(tag=None, value="Additional details.", path="test_path", lineno=16),
    ]
    tag = ExitTag.from_lines(lines)
    assert isinstance(tag, ExitTag)
    assert tag.code == "1"
    assert tag.description == "Error occurred\nAdditional details."


def test_file_tag() -> None:
    """Test file tag."""
    lines = [
        DocLine(tag="file", value="config.yaml Configuration file", path="test_path", lineno=17),
        DocLine(tag=None, value="Additional details.", path="test_path", lineno=18),
    ]
    tag = FileTag.from_lines(lines)
    assert isinstance(tag, FileTag)
    assert tag.name == "config.yaml"
    assert tag.description == "Configuration file\nAdditional details."


def test_function_tag() -> None:
    """Test function tag."""
    lines = [
        DocLine(tag="function", value="my_function()", path="test_path", lineno=19),
        DocLine(tag="function-brief", value="A brief description.", path="test_path", lineno=20),
        DocLine(tag="function-description", value="Detailed description.", path="test_path", lineno=21),
        DocLine(tag="function-argument", value="arg1: Argument 1", path="test_path", lineno=22),
        DocLine(tag="function-return", value="0: Success", path="test_path", lineno=23),
    ]
    tag = FunctionTag.from_lines(lines)
    assert isinstance(tag, FunctionTag)
    assert tag.prototype == "my_function()"
    assert tag.brief == "A brief description."
    assert tag.description == "Detailed description."
    assert tag.arguments == ["arg1: Argument 1"]
    assert tag.return_codes == ["0: Success"]


def test_history_tag() -> None:
    """Test history tag."""
    lines = [DocLine(tag="history", value="Initial version.", path="test_path", lineno=24)]
    tag = HistoryTag.from_lines(lines)
    assert isinstance(tag, HistoryTag)
    assert tag.text == "Initial version."


def test_license_tag() -> None:
    """Test license tag."""
    lines = [DocLine(tag="license", value="MIT License.", path="test_path", lineno=25)]
    tag = LicenseTag.from_lines(lines)
    assert isinstance(tag, LicenseTag)
    assert tag.text == "MIT License."


def test_note_tag() -> None:
    """Test note tag."""
    lines = [DocLine(tag="note", value="This is a note.", path="test_path", lineno=26)]
    tag = NoteTag.from_lines(lines)
    assert isinstance(tag, NoteTag)
    assert tag.text == "This is a note."


def test_option_tag() -> None:
    """Test option tag."""
    lines = [
        DocLine(tag="option", value="-h, --help Show help message", path="test_path", lineno=27),
        DocLine(tag="option-default", value="False", path="test_path", lineno=28),
        DocLine(tag="option-group", value="General", path="test_path", lineno=29),
    ]
    tag = OptionTag.from_lines(lines)
    assert isinstance(tag, OptionTag)
    assert tag.short == "-h"
    assert tag.long == "--help"
    assert tag.positional == "Show help message"
    assert tag.default == "False"
    assert tag.group == "General"
    assert tag.description == ""


def test_seealso_tag() -> None:
    """Test seealso tag."""
    lines = [DocLine(tag="seealso", value="Related topic.", path="test_path", lineno=30)]
    tag = SeealsoTag.from_lines(lines)
    assert isinstance(tag, SeealsoTag)
    assert tag.text == "Related topic."


def test_stderr_tag() -> None:
    """Test stderr tag."""
    lines = [DocLine(tag="stderr", value="Error output.", path="test_path", lineno=31)]
    tag = StderrTag.from_lines(lines)
    assert isinstance(tag, StderrTag)
    assert tag.text == "Error output."


def test_stdin_tag() -> None:
    """Test stdin tag."""
    lines = [DocLine(tag="stdin", value="Input data.", path="test_path", lineno=32)]
    tag = StdinTag.from_lines(lines)
    assert isinstance(tag, StdinTag)
    assert tag.text == "Input data."


def test_stdout_tag() -> None:
    """Test stdout tag."""
    lines = [DocLine(tag="stdout", value="Output data.", path="test_path", lineno=33)]
    tag = StdoutTag.from_lines(lines)
    assert isinstance(tag, StdoutTag)
    assert tag.text == "Output data."


def test_usage_tag() -> None:
    """Test usage tag."""
    lines = [
        DocLine(tag="usage", value="my_program command", path="test_path", lineno=34),
        DocLine(tag=None, value="Additional usage details.", path="test_path", lineno=35),
    ]
    tag = UsageTag.from_lines(lines)
    assert isinstance(tag, UsageTag)
    assert tag.program == "my_program"
    assert tag.command == "command\nAdditional usage details."


def test_version_tag() -> None:
    """Test version tag."""
    lines = [DocLine(tag="version", value="1.0.0", path="test_path", lineno=36)]
    tag = VersionTag.from_lines(lines)
    assert isinstance(tag, VersionTag)
    assert tag.text == "1.0.0"
