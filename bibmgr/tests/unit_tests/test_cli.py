import filecmp
import io
from unittest import mock
import os
import sys
import unittest

from bibmgr.bib_entry import BibEntry
from bibmgr.cli import DatabaseCLI
from bibmgr.tests.data.test_entries import test1_dict, test2_dict
from bibmgr.tests.unit_tests.common import check_results, soln


class TestDatabaseCLI(unittest.TestCase):

    def test_add_entry(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        with mock.patch('builtins.input', return_value="y"):
            tester.clear()
        input_seq = [
            "paper",
            "",
            "article",
            "Chang, Tyler H. and Watson, Layne T. and Lux, Thomas C. H. "
            "and Butt, Ali R. and Cameron, Kirk W. and Hong, Yili",
            "Algorithm 1012: {DELAUNAYSPARSE}: {I}nterpolation via a sparse "
            "subset of the {D}elaunay triangulation in medium to high "
            "dimensions",
            "2020",
            "ACM Transactions on Mathematical Software",
            "Collections of the ACM",
            "46",
            "4",
            "38",
            "20",
            "Association of Computing Machinery",
            "New York, NY, USA",
            "10.1145/3422818",
            "https://dl.acm.org/doi/10.1145/3422818",
            "0098-3500",
            "https://vtopt.github.io/DelaunaySparse",
            "https://github.com/vtopt/DelaunaySparse",
            "",
            "",
            "software, algorithms, delaunay triangulation",
            "Yes",
        ]
        with mock.patch('builtins.input', side_effect=input_seq):
            tester.add_entry()
        assert tester.database.contains(BibEntry(test1_dict).get_key())

    def test_delete_entry(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.force = True
        tester.clear()
        tester.database.create_entry(BibEntry(test1_dict))
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.delete_entry("none")
        assert cpt_out.getvalue() == "none not found, aborting.\n"
        assert tester.database.size() == 1
        cpt_out.truncate(0)
        cpt_out.seek(0)
        test1_key = BibEntry(test1_dict).get_key()
        tester.delete_entry(test1_key)
        assert cpt_out.getvalue() == f"Will delete: {test1_key}\n"
        assert tester.database.size() == 0

    def test_filter_predicate(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.force = True
        tester.clear()
        tester.database.create_entry(BibEntry(test1_dict))
        cpt_out.truncate(0)
        cpt_out.seek(0)
        with self.assertRaises(RuntimeError):
            tester.filter()
        with self.assertRaises(ValueError):
            tester.set_predicate("the publication year == 2020")
        with self.assertRaises(ValueError):
            tester.set_predicate("year=2020")
        with self.assertRaises(AttributeError):
            tester.set_predicate("funding == 4k")
        with self.assertRaises(AttributeError):
            tester.set_predicate("DOE in funding_agency")
        tester.set_predicate("year < 2021")
        tester.filter()
        assert cpt_out.getvalue() == "0 items filtered\n"
        assert tester.database.size() == 1
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.set_predicate("Chang in authors")
        tester.filter()
        assert cpt_out.getvalue() == "0 items filtered\n"
        assert tester.database.size() == 1
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.set_predicate("Le Cun in authors")
        tester.filter()
        assert cpt_out.getvalue() == "1 items filtered\n"
        assert tester.database.size() == 0

    def test_load_data(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.force = True
        tester.clear()
        tester.database.create_entry(BibEntry(test1_dict))
        tester.save_data(tester.cache_file)
        cpt_out.truncate(0)
        cpt_out.seek(0)
        with self.assertRaises(RuntimeError):
            tester.load_data("word")
        tester.load_data(tester.cache_file)
        assert cpt_out.getvalue() == (
            f"found duplicate: {BibEntry(test1_dict).get_key()}; skipping...\n"
            "Will load 1 entries\n"
        )
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.load_data(tester.cache_file, overwrite=True)
        assert cpt_out.getvalue() == "Will load 1 entries\n"
        tester.clear()
        tester.load_data("bibmgr/tests/data/test.bib")
        for entry in tester.database.entries():
            check_results(entry)

    def test_save_data(self):
        if os.path.exists("bibmgr/tests/data/test_cli_save.yaml"):
            os.remove("bibmgr/tests/data/test_cli_save.yaml")
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.force = True
        tester.clear()
        tester.database.create_entry(BibEntry(test1_dict))
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.save_data("bibmgr/tests/data/test_cli_save.yaml")
        assert cpt_out.getvalue() == (
            "Will write 1 entries to bibmgr/tests/data/test_cli_save.yaml\n"
        )
        tester.clear()
        tester.database.create_entry(BibEntry(test2_dict))
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.save_data("bibmgr/tests/data/test_cli_save.yaml")
        assert cpt_out.getvalue() == (
            "Found an existing file\n"
            "Loaded 1 new entries\n"
            "Have 1 existing entries\n"
            "Merged to 2 total entries\n"
            "Will write 2 entries to bibmgr/tests/data/test_cli_save.yaml\n"
        )
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.save_data("bibmgr/tests/data/test_cli_save.yaml")
        assert cpt_out.getvalue() == (
            "Found an existing file\n"
            "Loaded 2 new entries\n"
            "Have 2 existing entries\n"
            "Merged to 2 total entries\n"
            "Will write 2 entries to bibmgr/tests/data/test_cli_save.yaml\n"
        )
        assert os.path.exists("bibmgr/tests/data/test_cli_save.yaml")
        assert filecmp.cmp("bibmgr/tests/data/test_cli_save.yaml",
                           tester.cache_file)
        os.remove("bibmgr/tests/data/test_cli_save.yaml")
        if os.path.exists("bibmgr/tests/data/test2.bib"):
            os.remove("bibmgr/tests/data/test2.bib")
        tester.clear()
        tester.save_data("bibmgr/tests/data/test2.bib")
        for key in soln:
            tester.database.create_entry(BibEntry(soln[key]))
        tester.save_data("bibmgr/tests/data/test2.bib")
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        os.remove("bibmgr/tests/data/test2.bib")

    def test_show(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.force = True
        tester.clear()
        tester.database.create_entry(BibEntry(test1_dict))
        tester.database.create_entry(BibEntry(test2_dict))
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.show()
        assert cpt_out.getvalue() == (
            f"{BibEntry(test1_dict)}\n{BibEntry(test2_dict)}\n"
        )
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.set_predicate("year == 2020")
        tester.show()
        assert cpt_out.getvalue() == f"{BibEntry(test1_dict)}\n"
        cpt_out.truncate(0)
        cpt_out.seek(0)
        tester.show(BibEntry(test2_dict).get_key())
        assert cpt_out.getvalue() == f"{BibEntry(test2_dict)}\n"

    def test_update_entry(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        tester.force = True
        tester.clear()
        tester.database.create_entry(BibEntry(test1_dict))
        cpt_out.truncate(0)
        cpt_out.seek(0)
        with self.assertRaises(ValueError):
            tester.update_entry("tyler's special venue", "home")
        with self.assertRaises(KeyError):
            tester.update_entry("tyler.venue", "home")
        test1_key = BibEntry(test1_dict).get_key()
        tester.update_entry(f"{test1_key}.venue", "home")
        assert tester.database.read_entry(test1_key).get_venue() == "home"
        assert cpt_out.getvalue() == (
            f"Will update: {test1_key}\n"
            f"Old value: {BibEntry(test1_dict)}\n"
            f"New value: {tester.database.read_entry(test1_key)}\n"
        )

    def test_continue(self):
        cpt_out = io.StringIO()
        sys.stdout = cpt_out
        tester = DatabaseCLI()
        with mock.patch('builtins.input', return_value="No"):
            assert (not tester._user_continue())
        assert cpt_out.getvalue() == "Aborting.\n"
