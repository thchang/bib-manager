import unittest

from bibmgr.bib_entry import BibEntry
from bibmgr.dict_database import DictDatabase
from bibmgr.tests.data.test_entries import test1_dict


class TestDictDatabase(unittest.TestCase):

    def test_create_entry(self):
        tester = DictDatabase()
        with self.assertRaises(TypeError):
            tester.create_entry(test1_dict)
        assert len([ei for ei in tester.entries()]) == 0
        tester.create_entry(BibEntry(test1_dict))
        assert "chang2020algorithm" in tester.keys()
        with self.assertRaises(RuntimeError):
            tester.create_entry(BibEntry(test1_dict))
        assert len([ei for ei in tester.entries()]) == 1
