import os
import filecmp

from bibmgr.db_mgr import DbMgr
from bibmgr.tests.data.soln import soln


class TestDbMgr:

    def setup_class(self):
        self.tester = DbMgr()

    def check_results(self):
        for item in self.tester.info:
            for key in self.tester.info[item]:
                assert soln[item][key] == self.tester.info[item][key]

    def test_read_bibtex(self):
        self.tester.read_bibtex("bibmgr/tests/data/test.bib")
        self.check_results()

    def test_read_yaml(self):
        self.tester.read_yaml("bibmgr/tests/data/test.yaml")
        self.check_results()

    def test_write_bibtex(self):
        self.tester.read_bibtex("bibmgr/tests/data/test.bib")
        self.tester.write_bibtex("bibmgr/tests/data/test2.bib")
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        os.remove("bibmgr/tests/data/test2.bib")

    def test_write_yaml(self):
        self.tester.read_bibtex("bibmgr/tests/data/test.bib")
        self.tester.write_yaml("bibmgr/tests/data/test2.yaml")
        assert os.path.exists("bibmgr/tests/data/test2.yaml")
        assert filecmp.cmp("bibmgr/tests/data/test.yaml",
                           "bibmgr/tests/data/test2.yaml")
        os.remove("bibmgr/tests/data/test2.yaml")
