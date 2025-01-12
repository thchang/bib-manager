import yaml

from bibmgr.bib_parser import BibParser


class DbMgr(BibParser):

    __slots__ = [
        'template',
        'nextItem',
        'nextKey',
        'info'
    ]

    def __init__(self):
        super().__init__()

    def read_yaml(self, filename):
        with open(filename, "r") as fp:
            self.info = yaml.safe_load(fp)

    def read_bibtex(self, filename):
        self.parse_bib_file(filename)

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        self.write_bib_file(filename)
