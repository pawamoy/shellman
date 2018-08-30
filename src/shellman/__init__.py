# -*- coding: utf-8 -*-

"""
Shellman package.

Shellman is a Python utility that read a file and search for special comments
beginning with two sharps (##).

After having retrieved the documentation comments, shellman will be able to
write this documentation by rendering a builtin or third-party template.
"""

__version__ = "0.3.0"

from .reader import DocFile, DocStream
from .templates import Template

__all__ = ["DocFile", "DocStream", "Template"]
