import copy
import re


class BibParser:
    """ Class for parsing bibtex entries.

    Contains the following public methods:

     - `parse_bib_line(key, value)` parses a single line from a BibTex file;
     - `add_bib_item()` adds the next item into the internal database and
       resolves key conflicts; and
     - `parse_bib_file(filename)` parses an entire BibTex file.
     - `write_bib_file(filename)` writes an entire BibTex file.

    """

    __slots__ = [
        'template',
        'nextItem',
        'nextKey',
        'info'
    ]

    def __init__(self):
        """ Constructor for BibParser class.

        Initializes all slots for the BibParser class.

        """

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

    def _parse_bib_key(self):
        """ Resets the next key and entry for the internal database. """

        self.nextKey = ""
        self.nextItem = copy.deepcopy(self.template)

    def _parse_bib_type(self, btype):
        """ Sets the entry type for the next item. """

        self.nextItem['type'] = btype

    def _parse_bib_authors(self, authors):
        """ Sets the author list for the next item. """

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

    def _parse_bib_title(self, title):
        """ Sets the article title for the next item. """

        self.nextItem['title'] = title

    def _parse_bib_year(self, year):
        """ Sets the publication year for the next item. """

        self.nextItem['year'] = int(year)
        self.nextKey += str(year)

    def _parse_bib_venue(self, venue):
        """ Sets the publication venue for the next item. """

        self.nextItem['venue'] = venue

    def _parse_bib_series(self, series):
        """ Sets the publisher series for the next item. """

        self.nextItem['series'] = series

    def _parse_bib_volume(self, volume):
        """ Sets the publication volume for the next item. """

        self.nextItem['volume'] = int(volume)

    def _parse_bib_number(self, number):
        """ Sets the publication number for the next item. """

        self.nextItem['number'] = number

    def _parse_bib_articleno(self, number):
        """ Sets the article number for the next item. """

        self.nextItem['articleno'] = int(number)

    def _parse_bib_pages(self, pages):
        """ Sets the page number(s) for the next item. """

        self.nextItem['pages'] = []
        for page in pages.split('-'):
            if page != '':
                self.nextItem['pages'].append(int(page))

    def _parse_bib_publisher(self, publisher):
        """ Sets the publisher name for the next item. """

        if 'publisher' not in self.nextItem:
            self.nextItem['publisher'] = publisher

    def _parse_bib_address(self, address):
        """ Sets the publisher address for the next item. """

        location_re1 = re.compile(
                "[a-zA-Z\\,': ]+,[ ]*[a-zA-Z\\,': ]+,[ ]*[a-zA-Z\\,': ]+")
        location_re2 = re.compile("[a-zA-Z\\,': ]+,[ ]*[a-zA-Z\\,': ]+")
        if 'address' not in self.nextItem or \
                location_re1.match(address) or location_re2.match(address):
            self.nextItem['address'] = address

    def _parse_bib_doi(self, doi):
        """ Sets the doi for the next item. """

        self.nextItem['doi'] = doi.replace("https://doi.org/",
                                           "").replace("doi.org/", "")

    def _parse_bib_url(self, url):
        """ Sets the url for the next item. """

        self.nextItem['url'] = url

    def _parse_bib_isbn(self, isbn):
        """ Sets the ISBN for the next item. """

        self.nextItem['isbn'] = isbn

    def _parse_bib_git(self, git):
        """ Sets the Git repo for the next item. """

        self.nextItem['git'] = git

    def _parse_bib_web(self, web):
        """ Sets an additional web address for the next item. """

        self.nextItem['web'] = web

    def _parse_bib_note(self, note):
        """ Adds any publication notes for the next item. """

        self.nextItem['note'] = note

    def _parse_bib_descrip(self, descrip):
        """ Adds my personal description of the next item. """

        self.nextItem['descrip'] = descrip

    def _parse_bib_keyword(self, tag):
        """ Attaches keywords to the next item for easy lookup. """

        self.nextItem['tags'].append(tag)

    def parse_bib_line(self, key, value):
        """ Parse a single line of a bib file and attach the appropriate
        attributes to the next item.

        Args:
            key (str): The key that was extracted by the parser.

            value (int, str, list, dict): The corresponding value that was
                extracted by the parser.

        """

        if key.strip().lower() == 'author':
            self._parse_bib_authors(value)
        elif key.strip().lower() == 'title':
            self._parse_bib_title(value)
        elif key.strip().lower() == 'year':
            self._parse_bib_year(value)
        elif key.strip().lower() in ['type', 'howpublished']:
            self._parse_bib_type(value)
        elif key.strip().lower() in ['publisher', 'institution',
                                     'organization', 'school']:
            self._parse_bib_publisher(value)
        elif key.strip().lower() in ['journal', 'booktitle']:
            self._parse_bib_venue(value)
        elif key.strip().lower() in ['volume']:
            self._parse_bib_volume(value)
        elif key.strip().lower() in ['number']:
            self._parse_bib_number(value)
        elif key.strip().lower() in ['articleno']:
            self._parse_bib_articleno(value)
        elif key.strip().lower() in ['pages', 'numpages']:
            self._parse_bib_pages(value)
        elif key.strip().lower() == 'series':
            self._parse_bib_series(value)
        elif key.strip().lower() in ['address', 'location']:
            self._parse_bib_address(value)
        elif key.strip().lower() == 'doi':
            self._parse_bib_doi(value)
        elif key.strip().lower() == 'url':
            self._parse_bib_url(value)
        elif key.strip().lower() == 'isbn':
            self._parse_bib_isbn(value)
        elif key.strip().lower() == 'git':
            self._parse_bib_git(value)
        elif key.strip().lower() == 'web':
            self._parse_bib_web(value)
        elif key.strip().lower() == 'note':
            self._parse_bib_note(value)
        elif key.strip().lower() in ['descrip', 'summary']:
            self._parse_bib_descrip(value)
        elif key.strip().lower() == 'keywords':
            for tag in value.strip().split(","):
                self._parse_bib_keyword(tag.strip())
        else:
            raise ValueError(f"'{key}' with value '{value}' is not a "
                             "recognized key at this time")

    def add_bib_item(self):
        """ Add the current "next item" under construction into the internal
        database.

        Constructs the key for this item from the author and year (if
        applicable) and resolves key conflicts as needed.

        """

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

    def parse_bib_file(self, filename):
        """ Parse an entire BibTex (.bib) file, and store in the internal
        database.

        Args:
            filename (str, path-like object): The path to the file to parse.

        """

        newentry = re.compile("\\@(\\w+){(.+),")
        comment = re.compile("\\% (.+)")
        fullitem1 = re.compile("(\\w+)[ ]*=[ ]*{(.+)},")
        fullitem2 = re.compile("(\\w+)[ ]*=[ ]*{(.+)}")
        fullitem3 = re.compile('(\\w+)[ ]*=[ ]*"(.+)",')
        fullitem4 = re.compile('(\\w+)[ ]*=[ ]*"(.+)"')
        startitem1 = re.compile("(\\w+)[ ]*=[ ]*{(.*)")
        startitem2 = re.compile('(\\w+)[ ]*=[ ]*"(.*)')
        enditem1 = re.compile("(.*)},")
        enditem2 = re.compile('(.*)",')
        enditem3 = re.compile("(.*)}")
        enditem4 = re.compile('(.*)"')
        miditem = re.compile("(.+)")
        self.nextItem = copy.deepcopy(self.template)
        with open(filename, "r") as fp:
            nextKey = ""
            nextValue = ""
            nextDescrip = ""
            for line in fp:
                if m := newentry.match(line.strip()):
                    if self.nextKey is not None:
                        self.add_bib_item()
                    self._parse_bib_key()
                    self._parse_bib_type(m.group(1))
                    self._parse_bib_descrip(nextDescrip.strip())
                    nextDescrip = ""
                elif m := comment.match(line.strip()):
                    if m.group(1) != "":
                        nextDescrip = " ".join([nextDescrip, m.group(1)])
                elif m := fullitem1.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_bib_line(nextKey, nextValue)
                    nextKey = ""
                    nextValue = ""
                elif m := fullitem2.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_bib_line(nextKey, nextValue)
                    nextKey = ""
                    nextValue = ""
                elif m := fullitem3.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_bib_line(nextKey, nextValue)
                    nextKey = ""
                    nextValue = ""
                elif m := fullitem4.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                    self.parse_bib_line(nextKey, nextValue)
                    nextKey = ""
                    nextValue = ""
                elif m := startitem1.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                elif m := startitem2.match(line.strip()):
                    nextKey = m.group(1)
                    nextValue = m.group(2)
                elif m := enditem1.match(line.strip()):
                    if m.group(1) != "":
                        nextValue = " ".join([nextValue, m.group(1)])
                    self.parse_bib_line(nextKey, nextValue)
                    nextKey = ""
                    nextValue = ""
                elif m := enditem2.match(line.strip()):
                    if m.group(1) != "":
                        nextValue = " ".join([nextValue, m.group(1)])
                    self.parse_bib_line(nextKey, nextValue)
                    nextKey = ""
                    nextValue = ""
                elif m := enditem3.match(line.strip()):
                    if m.group(1) != "":
                        nextValue = " ".join([nextValue, m.group(1)])
                    if nextKey != "":
                        self.parse_bib_line(nextKey, nextValue)
                        nextKey = ""
                        nextValue = ""
                elif m := enditem4.match(line.strip()):
                    if m.group(1) != "":
                        nextValue = " ".join([nextValue, m.group(1)])
                    if nextKey != "":
                        self.parse_bib_line(nextKey, nextValue)
                        nextKey = ""
                        nextValue = ""
                elif m := miditem.match(line.strip()):
                    if m.group(1) != "":
                        nextValue = " ".join([nextValue, m.group(1)])
                else:
                    pass
        if self.nextKey is not None:
            self.add_bib_item()

    def write_bib_file(self, filename):
        """ Write an entire BibTex (.bib) file from the internal database.

        Args:
            filename (str, path-like object): The path to the file to write.

        """

        with open(filename, "w") as fp:
            for key1 in self.info:
                item1 = self.info[key1]
                ttype = None
                if 'type' in item1 and item1['type'] in [
                    'article', 'book', 'booklet', 'conference', 'inbook',
                    'incollection', 'inproceedings', 'manual', 'mastersthesis',
                    'misc', 'phdthesis', 'proceedings', 'techreport',
                    'unpublished'
                ]:
                    ttype = item1['type']
                    fp.write(f"@{item1['type']}{{{key1},\n")
                else:
                    ttype = 'misc'
                    fp.write(f"@misc{{{key1},\n")
                for key2 in item1:
                    if key2 == 'authors':
                        fp.write("\tauthor = {"
                                 f"{' and '.join(item1[key2])}}},\n")
                    elif key2 == 'venue':
                        if ttype == 'article':
                            fp.write(f"\tjournal = {{{item1[key2]}}},\n")
                        else:
                            fp.write(f"\tbooktitle = {{{item1[key2]}}},\n")
                    elif key2 == 'type':
                        if ttype == 'misc':
                            fp.write(f"\thowpublished = {{{item1[key2]}}},\n")
                    elif key2 == 'pages':
                        if len(item1[key2]) > 1:
                            fp.write("\tpages = {"
                                     f"{'--'.join(item1[key2])}}},\n")
                        elif len(item1[key2]) > 0:
                            fp.write(f"\tnumpages = {{{item1[key2][0]}}},\n")
                    elif key2 == 'publisher':
                        if ttype in ['conference', 'inproceedings',
                                     'proceedings']:
                            fp.write(f"\torganization = {{{item1[key2]}}},\n")
                        elif ttype in ['manual', 'techreport']:
                            fp.write(f"\tinstitution = {{{item1[key2]}}},\n")
                        elif ttype in ['mastersthesis', 'phdthesis']:
                            fp.write(f"\tschool = {{{item1[key2]}}},\n")
                        else:
                            fp.write(f"\tpublisher = {{{item1[key2]}}},\n")
                    elif key2 == 'address':
                        if ttype in ['conference', 'inproceedings',
                                     'proceedings']:
                            fp.write(f"\tlocation = {{{item1[key2]}}},\n")
                        else:
                            fp.write(f"\taddress = {{{item1[key2]}}},\n")
                    elif key2 == 'tags':
                        fp.write("\tkeywords = {"
                                 f"{', '.join(item1[key2])}}},\n")
                    else:
                        fp.write(f"\t{key2} = {{{item1[key2]}}},\n")
                fp.write("}\n\n")
