
import jinja
import re
import yaml

class Parser:

    def __init__(self):
        self.template = {
            'authors': [],
            'title': None,
            'year': None,
            'type': None,
            'publisher': {},
            'venue': {},
            'doi': None,
            'url': None,
            'isbn': None,
            'git': None,
            'web': None,
            'note': None,
            'descrip': None,
            'tags': [],
        }
        self.nextItem = None
        self.nextKey = None
        self.info = {}

    def parse_bib_key(self, key):
        self.nextKey = ""
        self.nextItem = self.template.copy()

    def parse_bib_type(self, btype):
        self.nextItem['type'] = btype

    def parse_bib_authors(self, authors):
        first_names = []
        last_names = []
        for name in names.split(" and "):
            name_list = name.strip().split(",")
            if len(name_list) <= 1:
                name_list = name.strip().split()
                self.nextItem['authors'].append(
                    (" ".join(name_list[:-1]).strip(), name_list[-1].strip())
                )
            else:
                self.nextItem['authors'].append(
                    (" ".join(name_list[1:]).strip(), name_list[0].strip())
                )
        self.nextKey = self.nextItem['authors'][0][1]

    def parse_bib_title(self, title):
        self.nextItem['title'] = title

    def parse_bib_year(self, year):
        self.nextItem['year'] = year
        self.nextKey += str(year)

    def parse_bib_publisher(self, publisher):
        self.nextItem['publisher'] = publisher

    def parse_bib_venue(self, venue):
        self.nextItem['venue'] = venue

    def parse_bib_doi(self, doi):
        self.nextItem['doi'] = doi

    def parse_bib_url(self, url):
        self.nextItem['url'] = url

    def parse_bib_isbn(self, isbn):
        self.nextItem['isbn'] = isbn

    def parse_bib_git(self, git):
        self.nextItem['git'] = git

    def parse_bib_web(self, web):
        self.nextItem['web'] = web

    def parse_bib_note(self, note):
        self.nextItem['note'] = note

    def parse_bib_descrip(self, descrip):
        self.nextItem['descrip'] = descrip

    def add_tag(self, tag):
        self.nextItem['tags'].append(tag)

    def add_item(self):
        self.info[self.nextKey] = self.nextItem

    def read_yaml(self, filename):
        with open(filename, "r") as fp:
            self.info = yaml.safe_load(fp)

    def read_bibtex(self, filename):
        fullitem1 = re.compile("(\w+)[ ]*=[ ]*{(.+)},")
        fullitem2 = re.compile("(\w+)[ ]*=[ ]*{(.+)}")
        fullitem3 = re.compile('(\w+)[ ]*=[ ]*"(.+)",')
        fullitem4 = re.compile('(\w+)[ ]*=[ ]*"(.+)"')
        startitem1 = re.compile("(\w+)[ ]*=[ ]*{(.+)")
        startitem2 = re.compile('(\w+)[ ]*=[ ]*"(.+)')
        enditem1 = re.compile("(.+)},")
        enditem2 = re.compile('(.+)",')
        with open(filename, "r") as fp:
            for line in fp:
                if m := fullitem1.match(line):
                    pass # TODO
                elif m := fullitem2.match(line):
                    pass # TODO
                elif m := fullitem3.match(line):
                    pass # TODO
                elif m := fullitem4.match(line):
                    pass # TODO
                elif m := startitem1.match(line):
                    pass # TODO
                elif m := startitem2.match(line):
                    pass # TODO
                elif m := enditem1.match(line):
                    pass # TODO
                elif m := enditem2.match(line):
                    pass # TODO
                else:
                    pass # TODO

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        with open(filename, "w") as fp:
            for key in self.info:
                self.info[key]
