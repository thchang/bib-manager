import yaml

from bibmgr.bib_parser import BibParser


class DbMgr:

    __slots__ = [
        'bib_parser',
        'info'
    ]

    def __init__(self):
        self.bib_parser = BibParser()
        self.info = {}

    def read_yaml(self, filename):
        with open(filename, "r") as fp:
            self.info = yaml.safe_load(fp)

    def read_bibtex(self, filename):
        for entry in self.bib_parser.parse_bib_file(filename):
            next_key = entry.get_key()
            if next_key not in self.info:
                self.info[next_key] = entry.to_dict()
            else:
                # TBD implement key collision policy in the future
                print(f"Warning: duplicate item '{next_key}' not added...")

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        self.bib_parser.write_bib_file(filename, self.info)
