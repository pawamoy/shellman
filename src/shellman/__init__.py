# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""shellman package.

Write documentation in comments and render it with templates.
Read documentation from shell script comments and render it with templates.

shellman reads specified FILEs and searches for special comments
beginning with two sharps (##).
It extracts documentation from these comment lines,
and then generate a document by rendering a template.
The template rendering is done with Jinja2.
See https://jinja.palletsprojects.com/en/3.1.x/.
Write documentation in comments and render it with templates.
"""

from __future__ import annotations

from shellman._internal.cli import get_parser, main
from shellman._internal.context import DEFAULT_JSON_FILE, ENV_VAR_PREFIX
from shellman._internal.reader import (
    DocBlock,
    DocFile,
    DocLine,
    DocStream,
    DocType,
    tag_no_value_regex,
    tag_value_regex,
)
from shellman._internal.tags import (
    TAGS,
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
    Tag,
    TextTag,
    UsageTag,
    ValueDescTag,
    VersionTag,
)
from shellman._internal.templates import (
    Template,
    builtin_env,
    helptext,
    manpage,
    manpage_md,
    templates,
    usagetext,
    wikipage,
)
from shellman._internal.templates.filters import (
    FILTERS,
    console_width,
    do_body,
    do_escape,
    do_firstline,
    do_firstword,
    do_format,
    do_groffauto,
    do_groffautoemphasis,
    do_groffautoescape,
    do_groffautostrong,
    do_groffemphasis,
    do_groffstrong,
    do_groupby,
    do_smartwrap,
)

__all__: list[str] = [
    "DEFAULT_JSON_FILE",
    "ENV_VAR_PREFIX",
    "FILTERS",
    "TAGS",
    "AuthorTag",
    "BriefTag",
    "BugTag",
    "CaveatTag",
    "CopyrightTag",
    "DateTag",
    "DescTag",
    "DocBlock",
    "DocFile",
    "DocLine",
    "DocStream",
    "DocType",
    "EnvTag",
    "ErrorTag",
    "ExampleTag",
    "ExitTag",
    "FileTag",
    "FunctionTag",
    "HistoryTag",
    "LicenseTag",
    "NoteTag",
    "OptionTag",
    "SeealsoTag",
    "StderrTag",
    "StdinTag",
    "StdoutTag",
    "Tag",
    "Template",
    "TextTag",
    "UsageTag",
    "ValueDescTag",
    "VersionTag",
    "builtin_env",
    "console_width",
    "do_body",
    "do_escape",
    "do_firstline",
    "do_firstword",
    "do_format",
    "do_groffauto",
    "do_groffautoemphasis",
    "do_groffautoescape",
    "do_groffautostrong",
    "do_groffemphasis",
    "do_groffstrong",
    "do_groupby",
    "do_smartwrap",
    "get_parser",
    "helptext",
    "main",
    "manpage",
    "manpage_md",
    "tag_no_value_regex",
    "tag_value_regex",
    "templates",
    "usagetext",
    "wikipage",
]
