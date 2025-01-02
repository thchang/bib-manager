import os
import filecmp

from bibmgr.db_mgr import DbMgr
from bibmgr.tests.unit_tests.soln_data import soln

class TestDbMgr:

    def setup_class(self):
        self.tester = DbMgr()

    def check_results(self):
        for item in self.tester.info:
            for key in self.tester.info[item]:
                assert soln[item][key] == self.tester.info[item][key]

    def test_read_bibtex(self):
        self.tester.read_bibtex("bibmgr/tests/unit_tests/test.bib")
        self.check_results()

    def test_read_yaml(self):
        self.tester.read_yaml("bibmgr/tests/unit_tests/test.yaml")
        self.check_results()

    def test_write_yaml(self):
        self.tester.write_yaml("test2.yaml")
        assert os.path.exists("test2.yaml")
        assert filecmp.cmp("bibmgr/tests/unit_tests/test.yaml", "test2.yaml")
        os.remove("test2.yaml")
