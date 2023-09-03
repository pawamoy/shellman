"""shellman package.

Read documentation from shell script comments and render it with templates.

shellman reads specified FILEs and searches for special comments
beginning with two sharps (##).
It extracts documentation from these comment lines,
and then generate a document by rendering a template.
The template rendering is done with Jinja2.
See https://jinja.palletsprojects.com/en/3.1.x/.
"""

from __future__ import annotations

from shellman.reader import DocFile, DocStream
from shellman.templates import Template

__all__: list[str] = ["DocFile", "DocStream", "Template"]
__version__ = "0.4.1"
