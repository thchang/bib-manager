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
        self.info = {}

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

    def _parse_bib_title(self, title):
        """ Sets the article title for the next item. """

        self.nextItem['title'] = title.strip()

    def _parse_bib_year(self, year):
        """ Sets the publication year for the next item. """

        self.nextItem['year'] = int(year.strip())

    def _parse_bib_venue(self, venue):
        """ Sets the publication venue for the next item. """

        self.nextItem['venue'] = venue.strip()

    def _parse_bib_series(self, series):
        """ Sets the publisher series for the next item. """

        self.nextItem['series'] = series.strip()

    def _parse_bib_volume(self, volume):
        """ Sets the publication volume for the next item. """

        self.nextItem['volume'] = int(volume.strip())

    def _parse_bib_number(self, number):
        """ Sets the publication number for the next item. """

        self.nextItem['number'] = number.strip()

    def _parse_bib_articleno(self, number):
        """ Sets the article number for the next item. """

        self.nextItem['articleno'] = int(number.strip())

    def _parse_bib_pages(self, pages):
        """ Sets the page number(s) for the next item. """

        self.nextItem['pages'] = []
        for page in pages.split('-'):
            if page != '':
                self.nextItem['pages'].append(int(page.strip()))

    def _parse_bib_publisher(self, publisher):
        """ Sets the publisher name for the next item. """

        if self.nextItem['publisher'] is None:
            self.nextItem['publisher'] = publisher.strip()

    def _parse_bib_address(self, address):
        """ Sets the publisher address for the next item. """

        location_re = re.compile(r"[^,]+,\s*[^,]+,(\s*[^,]+)*")
        if self.nextItem['address'] is None or location_re.match(address):
            self.nextItem['address'] = address.strip()

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

        value = " ".join(value.strip().split())
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

        last_name = self.nextItem['authors'][0][-1].lower()
        year = self.nextItem['year']
        first_word = ""
        for word in self.nextItem['title'].split():
            word = word.replace("-", "").replace(":", "")
            word = word.replace("{", "").replace("}", "")
            if len(word) > 2 and word.lower() not in [
                'a', 'an', 'the', 'that', 'than',
                'and', 'but', 'or', 'nor', 'for', 'so', 'yet',
                'at', 'above', 'in', 'into', 'like', 'near',
                'of', 'off', 'on', 'once', 'onto', 'over',
                'past', 'under', 'upon',
                'when', 'whence', 'with',
            ]:
                first_word = word.lower()
                break
        nextKey = f"{last_name}{year}{first_word}"
        if nextKey not in self.info:
            self.info[nextKey] = self.nextItem
        else:
            # TBD implement key collision policy in the future
            print(f"Warning: duplicate item '{nextKey}' not added...")
        self.nextItem = None

    def parse_bib_file(self, filename):
        """ Parse an entire .bib file, and store in the internal database.

        Args:
            filename (str, path-like object): The path to the file to parse.

        """

        next_item = (
            r'\@(?P<type>\w+){[\w-]+,|'
            r'\%[ ]*(?P<comment>[^\n]+)\n|'
            r'(?P<fullkey>\w+)\s*=\s*(?P<value>'
            r'"(?:\\"|[^"])*"|\w+),?|'
            r'(?P<halfkey>\w+)\s*=\s*{'
        )
        re_next_item = re.compile(next_item)

        with open(filename, "r") as fp:
            bib_data = fp.read()

        next_descrip = ""
        pos = 0

        while m := re_next_item.search(bib_data, pos):
            if m.group('type'):
                if self.nextItem is not None:
                    self.add_bib_item()
                self.nextItem = copy.deepcopy(self.template)
                self._parse_bib_type(m.group('type').strip())
                self._parse_bib_descrip(next_descrip.strip())
                next_descrip = ""
                pos = m.end()
            elif m.group('comment'):
                next_descrip = " ".join([next_descrip, m.group('comment')])
                pos = m.end()
            elif m.group('fullkey') and m.group('value'):
                # Drop the opening/closing quotes from the match
                if m.group('value')[0] == '"' and m.group('value')[-1] == '"':
                    value = m.group('value')[1:-1]
                else:
                    value = m.group('value')
                self.parse_bib_line(m.group('fullkey'), value)
                pos = m.end()
            elif m.group('halfkey'):
                # Parse nested braces manually
                start = m.end()
                brace_count = 1
                end = start
                while brace_count > 0 and end < len(bib_data):
                    if bib_data[end] == '{':
                        brace_count += 1
                    elif bib_data[end] == '}':
                        brace_count -= 1
                    end += 1
                self.parse_bib_line(m.group('halfkey'), bib_data[start:end-1])
                pos = end
            else:
                raise RuntimeError(f"Unmatched expression: {m}")
        if self.nextItem is not None:
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
                    if item1[key2] is None:
                        continue
                    elif key2 == 'authors':
                        author_names = [f"{last}, {first}"
                                        for [first, last] in item1[key2]]
                        fp.write("\tauthor = {"
                                 f"{' and '.join(author_names)}}},\n")
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
                            pages = [str(pp) for pp in item1[key2]]
                            fp.write(f"\tpages = {{{'--'.join(pages)}}},\n")
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
