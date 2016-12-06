# -*- coding: utf-8 -*-

# Copyright (c) 2015 Timothée Mazzucotelli
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Main test script."""
import pytest

from shellman.cli import main
from shellman.doc import Doc
from shellman.formatter import get_formatter
from shellman.tag import TAGS, Tag


class TestMain(object):
    def test_doc_read_returns_0(self):
        """Assert that reading a file returns 0."""
        assert main(['tests/fakescripts/minimal.sh']) == 0
        assert main(['tests/fakescripts/empty.sh']) == 0
        assert main(['tests/fakescripts/complete.sh']) == 0
        assert main(['tests/fakescripts/script_tags.sh']) == 0
        assert main(['tests/fakescripts/function_tags.sh']) == 0
        assert main(['tests/fakescripts/doc_breaks.sh']) == 0

    def test_wrong_doc_check_fails(self):
        assert not Doc('tests/fakescripts/wrong.sh').check(
            nice=False, failfast=False)

    def test_correctly_ignore_whitelisted_tag(self, capsys):
        doc = Doc('tests/fakescripts/invalid.sh', whitelist={'customx': Tag()})
        assert doc.check(nice=True, warn=True, failfast=False)
        out, err = capsys.readouterr()
        assert 'customx' not in err
        assert not doc.check(nice=False, warn=True, failfast=True)
        out, err = capsys.readouterr()
        assert 'customy' in err
        assert not doc.check(nice=False, warn=True, failfast=False)
        assert doc.check(nice=True, warn=True, failfast=True)

    def test_wrong_doc_check_fails_fast(self):
        assert not Doc('tests/fakescripts/wrong.sh').check(
            nice=False, failfast=True)

    def test_empty_file_gives_empty_doc(self):
        expected_doc = {k: None for k in TAGS.keys()}
        expected_doc['_file'] = 'empty.sh'
        expected_doc['_fn'] = []
        assert Doc('tests/fakescripts/empty.sh').read() == expected_doc


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


class TestFunctionTags(object):
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


class TestDocBreaks(object):
    fakescript = 'tests/fakescripts/doc_breaks.sh'
    doc = Doc(fakescript).read()

    def test_doc_breaks_for_1_many_tag(self):
        assert isinstance(self.doc['desc'], list)
        assert len(self.doc['desc']) == 2
        assert self.doc['desc'] == ['first line\n', 'second line\n']

    def test_doc_breaks_for_many_many_tag(self):
        assert isinstance(self.doc['usage'], list)
        assert len(self.doc['usage']) == 1
        assert isinstance(self.doc['usage'][0], list)
        assert len(self.doc['usage'][0]) == 2
        assert self.doc['usage'] == [['first line\n', 'second line\n']]


class TestFormatter(object):
    fakescripts = [
        'tests/fakescripts/complete.sh',
        'tests/fakescripts/empty.sh',
        'tests/fakescripts/minimal.sh',
    ]

    docs = [Doc(fakescript).read() for fakescript in fakescripts]

    def test_get_formatter(self):
        with pytest.raises(ValueError) as ve:
            get_formatter('unknown')
        assert all(x in str(ve.value) for x in ('incorrect format', 'unknown'))

    def test_text_formatter(self):
        formatter = get_formatter('text')
        for doc in self.docs:
            formatter(doc).write()

    def test_man_formatter(self):
        formatter = get_formatter('man')
        for doc in self.docs:
            formatter(doc).write()

    def test_markdown_formatter(self):
        formatter = get_formatter('markdown')
        for doc in self.docs:
            formatter(doc).write()


class TestCommandLine(object):
    def test_whitelist_option(self, capsys):
        assert main(['tests/fakescripts/invalid.sh',
                     '-cwi', 'customx:1+,customy']) == 0
        out, err = capsys.readouterr()
        assert 'invalid' not in err
        assert 'ignored' not in err
