# -*- coding: utf-8 -*-

"""
Read documentation from shell script comments and render it with templates.

shellman reads specified FILEs and searches for special comments
beginning with two sharps (##).
It extracts documentation from these comment lines,
and then generate a document by rendering a template.
The template rendering is done with Jinja2.
See http://jinja.pocoo.org/docs/2.10/templates/.
"""

__version__ = "0.3.4"

from .reader import DocFile, DocStream
from .templates import Template

__all__ = ["DocFile", "DocStream", "Template"]
