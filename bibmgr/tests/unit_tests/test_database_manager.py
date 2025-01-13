import filecmp
import os

from bibmgr.bib_entry import BibEntry
from bibmgr.database_manager import DatabaseManager
from bibmgr.tests.unit_tests.common import check_results, soln


class TestDatabaseManager:

    def test_read_bibtex(self):
        tester = DatabaseManager()
        tester.read_bibtex("bibmgr/tests/data/test.bib")
        for key in tester.info:
            check_results(tester.info[key])

    def test_read_yaml(self):
        tester = DatabaseManager()
        tester.read_yaml("bibmgr/tests/data/test.yaml")
        for key in tester.info:
            check_results(tester.info[key])

    def test_write_bibtex(self):
        tester = DatabaseManager()
        for next_key in soln:
            next_entry = BibEntry(soln[next_key])
            tester.info[next_key] = next_entry
        tester.write_bibtex("bibmgr/tests/data/test2.bib")
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        os.remove("bibmgr/tests/data/test2.bib")

    def test_write_yaml(self):
        tester = DatabaseManager()
        for next_key in soln:
            next_entry = BibEntry(soln[next_key])
            tester.info[next_key] = next_entry
        tester.write_yaml("bibmgr/tests/data/test2.yaml")
        assert os.path.exists("bibmgr/tests/data/test2.yaml")
        assert filecmp.cmp("bibmgr/tests/data/test.yaml",
                           "bibmgr/tests/data/test2.yaml")
        os.remove("bibmgr/tests/data/test2.yaml")
