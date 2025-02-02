import io
from unittest.mock import patch
import sys
import unittest

from bibmgr.bib_entry import BibEntry
from bibmgr.cli import DatabaseCLI
from bibmgr.tests.data.test_entries import test1_dict, test1_bib


class TestDatabaseCLI(unittest.TestCase):

    @patch('builtins.input', return_value="Yes")
    def test_add_entry(self, mock_input):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.clear()
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.add_entry(test1_dict)
        assert cpt_out.getvalue() == f"Will add: {test1_bib}\n\n"
        assert tester.database.contains(BibEntry(test1_dict).get_key())

    @patch('builtins.input', return_value="Yes")
    def test_delete_entry(self, mock_input):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.clear()
        tester.add_entry(test1_dict)
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.delete_entry("none")
        assert cpt_out.getvalue() == "none not found, aborting.\n"
        assert tester.database.size() == 1
        cpt_out.truncate(0)
        cpt_out.seek(0)
        test1_key = BibEntry(test1_dict).get_key()
        tester.delete_entry(test1_key)
        assert cpt_out.getvalue() == f"Will delete: {test1_key}\n\n"
        assert tester.database.size() == 0

    @patch('builtins.input', return_value="Yes")
    def test_filter_predicate(self, mock_input):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.clear()
        tester.add_entry(test1_dict)
        cpt_out.truncate(0)
        cpt_out.seek(0)
        with self.assertRaises(ValueError):
            tester.filter()
        with self.assertRaises(RuntimeError):
            tester.parse_predicate("the publication year == 2020")
        with self.assertRaises(RuntimeError):
            tester.parse_predicate("year=2020")
        tester.parse_predicate("year == 2020")
        tester.filter()
        assert cpt_out.getvalue() == "0 items filtered\n"
        assert tester.database.size() == 1
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.parse_predicate("Chang in authors")
        tester.filter()
        assert cpt_out.getvalue() == "0 items filtered\n"
        assert tester.database.size() == 1
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.parse_predicate("Le Cun in authors")
        tester.filter()
        assert cpt_out.getvalue() == "1 items filtered\n"
        assert tester.database.size() == 0

    @patch('builtins.input', return_value="y")
    def test_save_load(self, mock_input):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.clear()
        tester.add_entry(test1_dict)
        cpt_out.truncate(0)
        cpt_out.seek(0)
        with self.assertRaises(RuntimeError):
            tester.load_data("word")
        tester.load_data(tester.cache_file)
        assert cpt_out.getvalue() == (
            "Will load 1 entries\n\nfound duplicate entry:"
            f" {BibEntry(test1_dict)};\nskipping...\n"
        )

    @patch('builtins.input', return_value="Y")
    def test_show(self, mock_input):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.clear()
        tester.add_entry(test1_dict)
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.show()
        assert cpt_out.getvalue() == f"{BibEntry(test1_dict)}\n"
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.parse_predicate("year == 2020")
        tester.show()
        assert cpt_out.getvalue() == f"{BibEntry(test1_dict)}\n"

    @patch('builtins.input', return_value="No")
    def test_continue(self, mock_input):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        assert (not tester.user_continue())
        assert cpt_out.getvalue() == "Aborting.\n"
