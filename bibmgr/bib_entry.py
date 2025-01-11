from datetime import datetime


class BibEntry:
    """ Class for storing a single bibliography entry.

    Contains the following "setter" methods:

     - `add_bib_authors(authors)`,
     - `set_bib_title(title)`,
     - `set_bib_year(year)`,
     - `set_bib_type(type)`,
     - `set_bib_venue(venue)`,
     - `set_bib_series(series)`,
     - `set_bib_volume(volume)`,
     - `set_bib_number(number)`,
     - `set_bib_articleno(articleno)`,
     - `set_bib_pages(pages)`,
     - `set_bib_publisher(publisher)`,
     - `set_bib_address(address)`,
     -  `set_bib_doi(doi)`,
     -  `set_bib_url(url)`,
     -  `set_bib_isbn(isbn)`,
     -  `set_bib_git(git)`,
     -  `set_bib_web(web)`,
     -  `set_bib_note(note)`,
     -  `set_bib_descrip(descrip)`, and
     -  `add_bib_keyword(tags)`,

    and the following "getter" methods:

     - `get_bib_key()`,

    and the following converter methods:

     - `to_dict()`.

    """

    __slots__ = [
        'authors',
        'title',
        'year',
        'type',
        'venue',
        'series',
        'volume',
        'number',
        'articleno',
        'pages',
        'publisher',
        'address',
        'doi',
        'url',
        'isbn',
        'git',
        'web',
        'note',
        'descrip',
        'tags',
    ]

    def __init__(self, dict_rep=None):
        """ Constructor for the BibEntry class.

        Args:
            dict_rep (dict, optional): A dict representation of this BibEntry,
                which will be used to initialize the object when provided.
                Otherwise, all slots are initialized to empty values.

        """

        self.authors = []
        self.title = None
        self.year = None
        self.type = None
        self.venue = None
        self.series = None
        self.volume = None
        self.number = None
        self.articleno = None
        self.pages = None
        self.publisher = None
        self.address = None
        self.doi = None
        self.url = None
        self.isbn = None
        self.git = None
        self.web = None
        self.note = None
        self.descrip = None
        self.tags = []
        if dict_rep is not None:
            if not isinstance(dict_rep, dict):
                raise TypeError("dict_rep must be a dict when present, not"
                                f" {type(dict_rep)}")
            for key in dict_rep:
                if key in self.__slots__:
                    setattr(self, key, dict_rep[key])

    def add_bib_authors(self, authors):
        """ Adds the author to the bib item.

        Args:
            authors (list of str, list of list of str): The author(s) to add
                for this entry.

        """

        if not isinstance(authors, list):
            raise TypeError("expected a list of authors or names, got:"
                            f" {type(authors)}")
        if isinstance(authors[0], str):
            self.authors.append([ni.strip() for ni in authors])
        elif isinstance(authors[0], list) and isinstance(authors[0][0], str):
            for name in authors:
                self.authors.append([ni.strip() for ni in name])
        elif isinstance(authors[0], list):
            raise TypeError("expected a list of authors or names, got:"
                            f" list of lists of {type(authors[0][0])}")
        else:
            raise TypeError("expected a list of authors or names, got:"
                            f" list of {type(authors[0])}")

    def set_bib_title(self, title):
        """ Sets the article title for the bib item.

        Args:
            title (str): The type for this bib entry.

        """

        if not isinstance(title, str):
            raise TypeError("expected a string specifying the title, got:"
                            f" {type(title)}")
        self.title = title.strip()

    def set_bib_year(self, year):
        """ Sets the publication year for the bib item.

        Args:
            year (str or int): The year for this bib entry.

        """

        if not isinstance(year, str) and not isinstance(year, int):
            raise TypeError("expected a string or int specifying the year, "
                            f" got: {type(year)}")
        self.year = int(str(year).strip())

    def set_bib_type(self, btype):
        """ Sets the entry type for the bib item.

        Args:
            btype (str): The type for this bib entry.

        """

        if not isinstance(btype, str):
            raise TypeError("expected a string specifying the btype, got:"
                            f" {type(btype)}")
        self.type = btype.strip()

    def set_bib_venue(self, venue):
        """ Sets the publication venue for the bib item.

        Args:
            venue (str): The venue for this bib entry.

        """

        if not isinstance(venue, str):
            raise TypeError("expected a string specifying the venue, got:"
                            f" {type(venue)}")
        self.venue = venue.strip()

    def set_bib_series(self, series):
        """ Sets the publisher series for the bib item.

        Args:
            series (str): The series for this bib entry.

        """

        if not isinstance(series, str):
            raise TypeError("expected a string specifying the series, got:"
                            f" {type(series)}")
        self.series = series.strip()

    def set_bib_volume(self, volume):
        """ Sets the publication volume for the bib item.

        Args:
            volume (str or int): The volume for this bib entry.

        """

        if not isinstance(volume, str) and not isinstance(volume, int):
            raise TypeError("expected a string or int specifying the volume, "
                            f" got: {type(volume)}")
        self.volume = int(str(volume).strip())

    def set_bib_number(self, number):
        """ Sets the publication number for the bib item.

        Args:
            number (str or int): The number for this bib entry.

        """

        if not isinstance(number, str) and not isinstance(number, int):
            raise TypeError("expected a string or int specifying the number, "
                            f" got: {type(number)}")
        self.number = str(number).strip()

    def set_bib_articleno(self, articleno):
        """ Sets the article number for the bib item.

        Args:
            articleno (str or int): The article articleno for this bib entry.

        """

        if not isinstance(articleno, str) and not isinstance(articleno, int):
            raise TypeError("expected a string or int specifying the article "
                            f"number, got: {type(articleno)}")
        self.articleno = int(str(articleno).strip())

    def set_bib_pages(self, pages):
        """ Sets the page number(s) for the bib item.

        Args:
            pages (list of ints): The page numbers (if applicable) or number of
                pages for this bib entry.

        """

        if not isinstance(pages, list):
            raise TypeError("expected a list specifying the number of pages "
                            "(if unnumbered) or the starting/ending page "
                            f"numbers (if numbered), got: {type(pages)}")
        elif len(pages) not in (1, 2):
            raise TypeError("expected a list specifying the number of pages "
                            "(if unnumbered) or the starting/ending page "
                            "numbers (if numbered), got: "
                            f"list of length {len(pages)}")
        self.pages = []
        for page in pages:
            self.pages.append(int(str(page).strip()))

    def set_bib_publisher(self, publisher):
        """ Sets the publisher name for the bib item.

        Args:
            publisher (str): The publisher or associated org for this bib
                entry.

        """

        if not isinstance(publisher, str):
            raise TypeError("expected a string specifying the publisher, got:"
                            f" {type(publisher)}")
        self.publisher = publisher.strip()

    def set_bib_address(self, address):
        """ Sets the publisher address for the bib item.

        Args:
            address (str): The address or location for this bib entry.

        """

        if not isinstance(address, str):
            raise TypeError("expected a string specifying the address, got:"
                            f" {type(address)}")
        self.address = address.strip()

    def set_bib_doi(self, doi):
        """ Sets the doi for the bib item.

        Args:
            doi (str): The doi for this bib entry.

        """

        if not isinstance(doi, str):
            raise TypeError("expected a string specifying the doi, got:"
                            f" {type(doi)}")
        self.doi = doi.strip().replace(
            r"https://doi.org/",
            ""
        ).replace(
            r"http://doi.org/",
            ""
        ).replace(
            r"doi.org/",
            ""
        )

    def set_bib_url(self, url):
        """ Sets the url for the bib item.

        Args:
            url (str): The url for this bib entry.

        """

        if not isinstance(url, str):
            raise TypeError("expected a string specifying the url, got:"
                            f" {type(url)}")
        self.url = url.strip()

    def set_bib_isbn(self, isbn):
        """ Sets the ISBN for the bib item.

        Args:
            isbn (str): The ISBN for this bib entry.

        """

        if not isinstance(isbn, str):
            raise TypeError("expected a string specifying the ISBN, got:"
                            f" {type(isbn)}")
        self.isbn = isbn.strip()

    def set_bib_git(self, git):
        """ Sets the Git repo for the bib item.

        Args:
            git (str): The Git repo web address for this bib entry.

        """

        if not isinstance(git, str):
            raise TypeError("expected a string specifying the Git page, got:"
                            f" {type(git)}")
        self.git = git.strip()

    def set_bib_web(self, web):
        """ Sets an additional web address for the bib item.

        Args:
            web (str): The web for this bib entry.

        """

        if not isinstance(web, str):
            raise TypeError("expected a string specifying the url, got:"
                            f" {type(web)}")
        self.web = web.strip()

    def set_bib_note(self, note):
        """ Adds any publication notes for the bib item.

        Args:
            note (str): Any notes on this bib entry.

        """

        if not isinstance(note, str):
            raise TypeError("expected a string specifying the note(s), got:"
                            f" {type(note)}")
        self.note = note.strip()

    def set_bib_descrip(self, descrip):
        """ My personal description/reading notes for this bib item.

        Args:
            descrip (str): Any descriptions or personal reading notes on this
                bib entry.

        """

        if not isinstance(descrip, str):
            raise TypeError("expected a string specifying the description, "
                            f"got: {type(descrip)}")
        self.descrip = descrip.strip()

    def add_bib_keyword(self, tag):
        """ Attaches relevant tags/keywords to the bib item for easy lookup.

        Args:
            tag (str): Any keywords or tags for this bib entry.

        """

        if isinstance(tag, str):
            self.tags.append(tag.strip())
        elif isinstance(tag, list):
            for ti in tag:
                if isinstance(ti, str):
                    self.tags.append(ti.strip())
                else:
                    raise TypeError("expected a list or string specifying the "
                                    f"keyword(s), got: {type(ti)}")
        else:
            raise TypeError("expected a list or string specifying the "
                            f"keyword(s), got: {type(tag)}")

    def get_bib_key(self):
        """ Create a key for this entry of form: LastNameYearFirstWordOfTitle.

        Returns:
            str: The proposed bibliography entry key.

        """

        ignores = [
            'a', 'an', 'the', 'that', 'than',
            'and', 'but', 'or', 'nor', 'for', 'so', 'yet',
            'at', 'above', 'in', 'into', 'like', 'near',
            'of', 'off', 'on', 'once', 'onto', 'over',
            'past', 'under', 'upon',
            'when', 'whence', 'with',
        ]
        if len(self.authors) > 0:
            last_name = self.authors[0][-1].lower()
        elif self.publisher is not None:
            last_name = "".join(
                [ni[0] for ni in self.publisher.split()
                 if ni.lower() not in ignores]
            ).lower()
        else:
            raise ValueError("Cannot generate key for bib item with no authors"
                             " and no publisher")
        if self.year is not None:
            year = self.year
        else:
            year = int(datetime.now().year)
        first_word = ""
        for word in self.title.split():
            word = word.replace("-", "").replace(":", "")
            word = word.replace("{", "").replace("}", "")
            if len(word) > 2 and word.lower() not in ignores:
                first_word = word.lower()
                break
        return f"{last_name}{year}{first_word}"

    def to_dict(self):
        """ Convert this bib entry into a Python dict format.

        Returns:
            dict: A dictionary with a key for each attribute, containing the
                corresponding value from this BibEntry object's slot.

        """

        dict_rep = {}
        for key in self.__slots__:
            dict_rep[key] = getattr(self, key)
        return dict_rep
