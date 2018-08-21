# -*- coding: utf-8 -*-

"""
Shellman package.

Shellman is a Python utility that read a file and search for special comments
beginning with two sharps (##). It can recognize doxygen-like tags, such as
brief, desc, fn, author, so you can write documentation in your shell scripts.

After having retrieved the documentation comments, shellman will be able to
write this documentation as text, man, or markdown format on stdout.
"""

__version__ = '0.2.2'

# from .cleaner import Cleaner
from .reader import DocFile, DocStream
# from .formatter import Formatter


__all__ = ['DocFile', 'DocStream']
