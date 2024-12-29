
from db_mgr import DbMgr

class TestDbMgr:

    def __init__(self):
        self.tester = DbMgr()
        self.soln = 

    def test_read_bibtex():
        self.tester.read_bibtex("test.bib")
        for item in self.tester.info:
            for key in self.tester.info[item]:
                assert self.tester2.info[item][key] == self.tester.info[item][key]

    def test_read_yaml():
        self.tester.read_yaml("test.yaml")
    #tester1.write_yaml("test2.yaml")
    tester2 = DbMgr()
    tester2.read_yaml("test.yaml")
