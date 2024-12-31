import os
import filecmp

from bibmgr.db_mgr import DbMgr
from bibmgr.test.unit_test.soln_data import soln

class TestDbMgr:

    def setup_class(self):
        self.tester = DbMgr()

    def check_results(self):
        for item in self.tester.info:
            for key in self.tester.info[item]:
                assert soln[item][key] == self.tester.info[item][key]

    def test_read_bibtex(self):
        self.tester.read_bibtex("bibmgr/test/unit_test/test.bib")
        self.check_results()

    def test_read_yaml(self):
        self.tester.read_yaml("bibmgr/test/unit_test/test.yaml")
        self.check_results()

    def test_write_yaml(self):
        self.tester.write_yaml("test2.yaml")
        assert os.path.exists("test2.yaml")
        assert filecmp.cmp("bibmgr/test/unit_test/test.yaml", "test2.yaml")
        os.remove("test2.yaml")
