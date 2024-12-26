
#import jinja
import copy
import re
import yaml

class Parser:

    def __init__(self):
        self.template = {
            'authors': [],
            'title': None,
            'year': None,
            'type': None,
            'venue': None,
            'series': None,
            'volume': None,
            'number': None,
            'articleno': None,
            'pages': None,
            'publisher': None,
            'address': None,
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

    def parse_bib_key(self):
        self.nextKey = ""
        self.nextItem = copy.deepcopy(self.template)

    def parse_bib_type(self, btype):
        self.nextItem['type'] = btype

    def parse_bib_authors(self, authors):
        first_names = []
        last_names = []
        for name in authors.split(" and "):
            name_list = name.strip().split(",")
            if len(name_list) <= 1:
                name_list = name.strip().split()
                self.nextItem['authors'].append(
                    [" ".join(name_list[:-1]).strip(), name_list[-1].strip()]
                )
            else:
                self.nextItem['authors'].append(
                    [" ".join(name_list[1:]).strip(), name_list[0].strip()]
                )
        self.nextKey = self.nextItem['authors'][0][1].lower()

    def parse_bib_title(self, title):
        self.nextItem['title'] = title

    def parse_bib_year(self, year):
        self.nextItem['year'] = int(year)
        self.nextKey += str(year)

    def parse_bib_venue(self, venue):
        self.nextItem['venue'] = venue

    def parse_bib_series(self, series):
        self.nextItem['series'] = series

    def parse_bib_volume(self, volume):
        self.nextItem['volume'] = int(volume)

    def parse_bib_number(self, number):
        self.nextItem['number'] = number

    def parse_bib_articleno(self, number):
        self.nextItem['articleno'] = int(number)

    def parse_bib_pages(self, pages):
        self.nextItem['pages'] = []
        for page in pages.split('-'):
            if page != '':
                self.nextItem['pages'].append(int(page))

    def parse_bib_publisher(self, publisher):
        if 'publisher' not in self.nextItem:
            self.nextItem['publisher'] = publisher

    def parse_bib_address(self, address):
        location_re1 = re.compile(
                "[a-zA-Z\\,': ]+,[ ]*[a-zA-Z\\,': ]+,[ ]*[a-zA-Z\\,': ]+")
        location_re2 = re.compile("[a-zA-Z\\,': ]+,[ ]*[a-zA-Z\\,': ]+")
        if 'address' not in self.nextItem or \
                location_re1.match(address) or location_re2.match(address):
            self.nextItem['address'] = address

    def parse_bib_doi(self, doi):
        self.nextItem['doi'] = doi.replace("https://doi.org/",
                "").replace("doi.org/", "")

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

    def parse_item(self, key, value):
        if key.strip().lower() == 'author':
            self.parse_bib_authors(value)
        elif key.strip().lower() == 'title':
            self.parse_bib_title(value)
        elif key.strip().lower() == 'year':
            self.parse_bib_year(value)
        elif key.strip().lower() in ['type', 'howpublished']:
            self.parse_bib_type(value)
        elif key.strip().lower() in ['publisher', 'institution',
                                     'organization', 'school']:
            self.parse_bib_publisher(value)
        elif key.strip().lower() in ['journal', 'booktitle']:
            self.parse_bib_venue(value)
        elif key.strip().lower() in ['volume']:
            self.parse_bib_volume(value)
        elif key.strip().lower() in ['number']:
            self.parse_bib_number(value)
        elif key.strip().lower() in ['articleno']:
            self.parse_bib_articleno(value)
        elif key.strip().lower() in ['pages', 'numpages']:
            self.parse_bib_pages(value)
        elif key.strip().lower() == 'series':
            self.parse_bib_series(value)
        elif key.strip().lower() in ['address', 'location']:
             self.parse_bib_address(value)
        elif key.strip().lower() == 'doi':
            self.parse_bib_doi(value)
        elif key.strip().lower() == 'url':
            self.parse_bib_url(value)
        elif key.strip().lower() == 'isbn':
            self.parse_bib_isbn(value)
        elif key.strip().lower() == 'git':
            self.parse_bib_git(value)
        elif key.strip().lower() == 'web':
            self.parse_bib_web(value)
        elif key.strip().lower() == 'note':
            self.parse_bib_note(value)
        elif key.strip().lower() in ['descrip', 'summary']:
            self.parse_bib_descrip(value)
        elif key.strip().lower() == 'keywords':
            for tag in value.strip().split(","):
                self.add_tag(tag)
        else:
            raise ValueError(f"'{key}' with value '{value}' is not a "
                             "recognized key at this time")

    def add_tag(self, tag):
        self.nextItem['tags'].append(tag)

    def add_item(self):
        if self.nextKey not in self.info and (self.nextKey + "a") not in \
                self.info:
            self.info[self.nextKey] = self.nextItem
        elif self.nextKey in self.info and (
                self.info[self.nextKey]['title'] == self.nextItem['title']):
            pass
        else:
            if self.nextKey in self.info:
                self.info[self.nextKey + "a"] = self.info[self.nextKey]
                self.info.pop(self.nextKey)
            nextLetter = "a"
            toAdd = True
            while (self.nextKey + nextLetter) in self.info:
                if (self.info[self.nextKey + nextLetter]['title'] ==
                        self.nextItem['title']):
                    toAdd = False
                    break
                nextLetter = chr(ord(nextLetter) + 1)
            if toAdd:
                self.info[self.nextKey + nextLetter] = self.nextItem
        self.nextItem = None

    def read_yaml(self, filename):
        with open(filename, "r") as fp:
            self.info = yaml.safe_load(fp)

    def read_bibtex(self, filename):
        newentry = re.compile("\\@(\\w+){(.+),")
        comment = re.compile("\\% .+")
        fullitem1 = re.compile("(\\w+)[ ]*=[ ]*{(.+)},")
        fullitem2 = re.compile("(\\w+)[ ]*=[ ]*{(.+)}")
        fullitem3 = re.compile('(\\w+)[ ]*=[ ]*"(.+)",')
        fullitem4 = re.compile('(\\w+)[ ]*=[ ]*"(.+)"')
        startitem1 = re.compile("(\\w+)[ ]*=[ ]*{(.+)")
        startitem2 = re.compile('(\\w+)[ ]*=[ ]*"(.+)')
        enditem1 = re.compile("(.+)},")
        enditem2 = re.compile('(.+)",')
        self.nextItem = copy.deepcopy(self.template)
        with open(filename, "r") as fp:
            nextKey = ""
            nextValue = ""
            nextDescrip = ""
            for line in fp:
                if m:= newentry.match(line.strip()):
                    if self.nextKey is not None:
                        self.add_item()
                    self.parse_bib_key()
                    self.parse_bib_type(m.group(1))
                    self.parse_bib_descrip(nextDescrip.strip())
                    nextDescrip = ""
                elif m := comment.match(line.strip()):
                    nextDescrip += " " + m.group(1)
                elif m := fullitem1.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_item(nextKey, nextValue)
                elif m := fullitem2.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_item(nextKey, nextValue)
                elif m := fullitem3.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_item(nextKey, nextValue)
                elif m := fullitem4.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_item(nextKey, nextValue)
                elif m := startitem1.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                elif m := startitem2.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                elif m := enditem1.match(line.strip()):
                    nextValue += m.group(1)
                    self.parse_item(nextKey, nextValue)
                elif m := enditem2.match(line.strip()):
                    nextValue += m.group(1)
                    self.parse_item(nextKey, nextValue)
                else:
                    pass
        if self.nextKey is not None:
            self.add_item()

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        with open(filename, "w") as fp:
            for key in self.info:
                self.info[key]


if __name__ == "__main__":
    tester1 = Parser()
    tester1.read_bibtex("test.bib")
    #tester1.write_yaml("test2.yaml")
    tester2 = Parser()
    tester2.read_yaml("test.yaml")
    for item in tester1.info:
        for key in tester1.info[item]:
            assert tester2.info[item][key] == tester1.info[item][key]
