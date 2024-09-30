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

    def parse_authors(self, authors):
        self.nextItem['author'] = authors

    def parse_title(self, title):
        self.nextItem['title'] = title

    def parse_year(self, year):
        self.nextItem['year'] = year

    def parse_publisher(self, publisher):
        self.nextItem['publisher'] = publisher

    def parse_venue(self, venue):
        self.nextItem['venue'] = venue

    def parse_doi(self, doi):
        self.nextItem['doi'] = doi

    def parse_url(self, url):
        self.nextItem['url'] = url

    def parse_isbn(self, isbn):
        self.nextItem['isbn'] = isbn

    def parse_git(self, git):
        self.nextItem['git'] = git

    def parse_web(self, web):
        self.nextItem['web'] = web

    def parse_note(self, note):
        self.nextItem['note'] = note

    def parse_descrip(self, descrip):
        self.nextItem['descrip'] = descrip

    def add_tag(self, tag):
        self.nextItem['tags'].append(tag)

    def read(self, filename):
        pass

    def write_yaml(self, filename):
        with open(filename, "w") as fp:
            yaml.dump(self.info, fp)

    def write_bibtex(self, filename):
        with open(filename, "w") as fp:
            for key in self.info:
                self.info[key]
