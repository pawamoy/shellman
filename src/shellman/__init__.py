"""
shellman package.

Read documentation from shell script comments and render it with templates.

shellman reads specified FILEs and searches for special comments
beginning with two sharps (##).
It extracts documentation from these comment lines,
and then generate a document by rendering a template.
The template rendering is done with Jinja2.
See http://jinja.pocoo.org/docs/2.10/templates/.
"""

from typing import List

from .reader import DocFile, DocStream
from .templates import Template

__all__: List[str] = ["DocFile", "DocStream", "Template"]  # noqa: WPS410
__version__ = "0.4.1"  # noqa: WPS410 (the only __variables__ we use)
