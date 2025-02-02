import unittest

from bibmgr.bib_entry import BibEntry
from bibmgr.dict_database import DictDatabase
from bibmgr.tests.data.test_entries import test1_dict, test2_dict


class TestDictDatabase(unittest.TestCase):

    def test_create_entry(self):
        tester = DictDatabase()
        with self.assertRaises(TypeError):
            tester.create_entry(test1_dict)
        assert len([ei for ei in tester.entries()]) == 0
        tester.create_entry(BibEntry(test1_dict))
        assert "chang2020algorithm" in tester.keys()
        with self.assertRaises(KeyError):
            tester.create_entry(BibEntry(test1_dict))
        assert len([ei for ei in tester.entries()]) == 1

    def test_read_entry(self):
        tester = DictDatabase()
        with self.assertRaises(KeyError):
            tester.read_entry("chang2020algorithm")
        tester.create_entry(BibEntry(test1_dict))
        entry = tester.read_entry("chang2020algorithm")
        assert entry.get_key() == "chang2020algorithm"

    def test_update_entry(self):
        tester = DictDatabase()
        with self.assertRaises(KeyError):
            tester.update_entry("chang2020algorithm", "title", "TOMS Alg 1012")
        tester.create_entry(BibEntry(test1_dict))
        tester.update_entry("chang2020algorithm", "title", "TOMS Alg 1012")
        with self.assertRaises(KeyError):
            tester.read_entry("chang2020algorithm")
        entry = tester.read_entry("chang2020toms")
        assert entry.get_key() == "chang2020toms"

    def test_delete_entry(self):
        tester = DictDatabase()
        with self.assertRaises(KeyError):
            tester.delete_entry("chang2020algorithm")
        tester.create_entry(BibEntry(test1_dict))
        entry = tester.delete_entry("chang2020algorithm")
        assert entry.get_key() == "chang2020algorithm"

    def test_entries(self):
        tester = DictDatabase()
        with self.assertRaises(TypeError):
            [ei for ei in tester.entries(5)]
        tester.create_entry(BibEntry(test1_dict))
        tester.create_entry(BibEntry(test2_dict))
        for entry in tester.entries():
            assert entry.get_key() in ["chang2020algorithm", "chang2016gpu"]
        for entry in tester.entries(lambda x: "software" in x.tags):
            assert entry.get_key() in ["chang2020algorithm"]

    def test_keys(self):
        tester = DictDatabase()
        with self.assertRaises(TypeError):
            [ki for ki in tester.keys(5)]
        tester.create_entry(BibEntry(test1_dict))
        tester.create_entry(BibEntry(test2_dict))
        for key in tester.keys():
            assert key in ["chang2020algorithm", "chang2016gpu"]
        for key in tester.keys(lambda x: "software" in x.tags):
            assert key in ["chang2020algorithm"]

    def test_contains(self):
        tester = DictDatabase()
        tester.create_entry(BibEntry(test1_dict))
        assert tester.contains("chang2020algorithm")
        assert not tester.contains("chang2016gpu")

    def test_size(self):
        tester = DictDatabase()
        assert tester.size() == 0
        tester.create_entry(BibEntry(test1_dict))
        assert tester.size() == 1
        tester.create_entry(BibEntry(test2_dict))
        assert tester.size() == 2
