# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Main test script."""

from shellman.cli import main
from shellman.doc import Doc
from shellman.tag import TAGS, Tag


def test_main():
    """Assert that reading a file with few docs returns 0."""
    assert main(['tests/fakescripts/minimal.sh']) == 0


# liste des tests possibles !

# lecture

# tags uniques : le dernier est conservé
# tags multiples : tous sont gardés
# multi lignes : toutes les lignes sont gardées
# instructions entre docs : ce qu'il y a après n'est pas gardé
# ligne vide entre docs : idem
# fonctions

# écriture

# vérifier que l'écriture se passe bien

class TestScriptTags(object):
    fakescript = 'tests/fakescripts/script_tags.sh'
    doc = Doc(fakescript).read()

    def test_tags_correctly_read(self):
        """Assert all tags present in script are correctly read."""
        for name, tag in TAGS.items():
            assert self.doc[name]

    def test_multiple_tags(self):
        """Assert that all occurrences of multiple tag are kept."""
        for name, tag in TAGS.items():
            if tag.occurrences == Tag.MANY:
                assert isinstance(self.doc[name], list)
                assert len(self.doc[name]) == 2
                if tag.lines == Tag.MANY:
                    assert isinstance(self.doc[name][0], list)
                    assert isinstance(self.doc[name][1], list)
                    assert len(self.doc[name][0]) == 2
                    assert len(self.doc[name][1]) == 2
                    assert self.doc[name][0] == ['first occurrence\n',
                                                 'testing multi line\n']
                    assert self.doc[name][1] == ['second occurrence\n',
                                                 'testing multi line\n']
                else:
                    assert isinstance(self.doc[name][0], str)
                    assert isinstance(self.doc[name][1], str)
                    assert self.doc[name][0] == 'first occurrence'
                    assert self.doc[name][1] == 'second occurrence'

    def test_unique_tags(self):
        """Assert that only first occurrence of unique tag is kept."""
        for name, tag in TAGS.items():
            if tag.occurrences == 1:
                if tag.lines == Tag.MANY:
                    assert isinstance(self.doc[name], list)
                    assert len(self.doc[name]) == 2
                    assert self.doc[name][0] == 'first occurrence\n'
                    assert self.doc[name][1] == 'testing multi line\n'
                else:
                    assert isinstance(self.doc[name], str)
                    assert self.doc[name] == 'first occurrence'
