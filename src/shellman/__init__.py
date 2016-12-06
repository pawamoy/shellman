# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Shellman package.

Shellman is a Python utility that read a file and search for special comments
beginning with two sharps (##). It can recognize doxygen-like tags, such as
brief, desc, fn, author, so you can write documentation in your shell scripts.

After having retrieved the documentation comments, shellman will be able to
write this documentation as text, man, or markdown format on stdout.
"""

__version__ = '0.2.0'
