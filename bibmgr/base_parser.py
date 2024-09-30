class Parser:

    def __init__(self):

        self.info = {
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

    def parse_authors(self, authors):
        self.info['author'] = authors

    def parse_title(self, title):
        self.info['title'] = title

    def parse_year(self, year):
        self.info['year'] = year

    def parse_publisher(self, publisher):
        self.info['publisher'] = publisher

    def parse_venue(self, venue):
        self.info['venue'] = venue

    def parse_doi(self, doi):
        self.info['doi'] = doi

    def parse_url(self, url):
        self.info['url'] = url

    def parse_isbn(self, isbn):
        self.info['isbn'] = isbn

    def parse_git(self, git):
        self.info['git'] = git

    def parse_web(self, web):
        self.info['web'] = web

    def parse_note(self, note):
        self.info['note'] = note

    def parse_descrip(self, descrip):
        self.info['descrip'] = descrip

    def add_tag(self, tag):
        self.info['tags'].append(tag)

    def read(self, filename):
        pass

    def write_yaml(self, filename):
        with open(filename, "a") as fp:
            fp.write()

    def write_bibtex(self, filename):
        pass
