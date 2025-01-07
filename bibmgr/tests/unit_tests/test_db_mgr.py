import copy
import filecmp
import os

from bibmgr.db_mgr import DbMgr
from bibmgr.tests.unit_tests.common import check_results, soln


class TestDbMgr:

    def test_add_tag(self):
        tester = DbMgr()
        tester.nextItem = copy.deepcopy(tester.template)
        tester.add_tag("test")
        tester.add_tag("unit test")
        assert "test" in tester.nextItem['tags']
        assert "unit test" in tester.nextItem['tags']

    def test_read_bibtex(self):
        tester = DbMgr()
        tester.read_bibtex("bibmgr/tests/data/test.bib")
        check_results(tester)

    def test_read_yaml(self):
        tester = DbMgr()
        tester.read_yaml("bibmgr/tests/data/test.yaml")
        check_results(tester)

    def test_write_bibtex(self):
        tester = DbMgr()
        tester.info = soln
        tester.write_bibtex("bibmgr/tests/data/test2.bib")
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        os.remove("bibmgr/tests/data/test2.bib")

    def test_write_yaml(self):
        tester = DbMgr()
        tester.info = soln
        tester.write_yaml("bibmgr/tests/data/test2.yaml")
        assert os.path.exists("bibmgr/tests/data/test2.yaml")
        assert filecmp.cmp("bibmgr/tests/data/test.yaml",
                           "bibmgr/tests/data/test2.yaml")
        os.remove("bibmgr/tests/data/test2.yaml")
