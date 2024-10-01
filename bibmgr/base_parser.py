class Parser:

    def __init__(self):
        self.template = {
            'authors': [],
            'title': None,
            'year': None,
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
        self.info = []

    def parse_bib_authors(self, authors):
        self.nextItem['author'] = authors

    def parse_bib_title(self, title):
        self.nextItem['title'] = title

    def parse_bib_year(self, year):
        self.nextItem['year'] = year

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

    def read_yaml(self, filename):
        with open(filename, "r") as fp:
            self.info = yaml.safe_load(fp)

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        with open(filename, "w") as fp:
            for key in self.info:
                self.info[key]
