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

    def add_tag(self, tag):
        self._parse_bib_item(tag)

    def read_yaml(self, filename):
        with open(filename, "r") as fp:
            self.info = yaml.safe_load(fp)

    def read_bibtex(self, filename):
        self.parse_bib_file(filename)

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        with open(filename, "w") as fp:
            for key1 in self.info:
                item1 = self.info[key1]
                if 'type' in item1 and item1['type'] in [
                    'article', 'book', 'booklet', 'conference', 'inbook',
                    'incollection', 'inproceedings', 'manual', 'mastersthesis',
                    'misc', 'phdthesis', 'proceedings', 'techreport',
                    'unpublished'
                ]:
                    fp.write(f"@{item1['type']}{{{key1},\n")
                else:
                    fp.write(f"@misc{{{key1},\n")
                for key2 in item1:
                    fp.write(f"\t{key2} = {{{item1[key2]}}},\n")
                fp.write("}\n\n")


if __name__ == "__main__":
    dbmgr = DbMgr()
    dbmgr.read_bibtex("bibmgr/tests/data/test.bib")
    dbmgr.write_yaml("bibmgr/test.yaml")
    print("{")
    for key1 in dbmgr.info:
        print(f"\t{key1}: {{")
        item1 = dbmgr.info[key1]
        for key2 in item1:
            if isinstance(item1[key2], str):
                print(f"\t\t{key2}: '{item1[key2]}',")
            else:
                print(f"\t\t{key2}: {item1[key2]},")
        print("\t},")
    print("}")
