# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Main test script."""

from shellman.cli import main


def test_main():
    """Main test method."""
    assert main(['tests/fakescripts/minimal.sh']) == 0
