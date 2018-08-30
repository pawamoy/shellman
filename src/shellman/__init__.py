# -*- coding: utf-8 -*-

"""
Shellman package.

Shellman is a Python utility that read a file and search for special comments
beginning with two sharps (##). It can recognize doxygen-like tags, such as
brief, desc, fn, author, so you can write documentation in your shell scripts.

After having retrieved the documentation comments, shellman will be able to
write this documentation as text, man, or markdown format on stdout.
"""

__version__ = "0.3.0"

from .reader import DocFile, DocStream


__all__ = ["DocFile", "DocStream"]

# TODO: context injection from command-line / environment variables
# TODO: re-implement --check option with warnings
# TODO: plugin architecture
# TODO: documentation (FILENAME of --merge, do not dup metavar in argparse help, docstrings)
# TODO: add filepath as an output variable, maybe also basename, ext, dirname, dirpath
