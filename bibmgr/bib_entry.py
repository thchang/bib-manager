from datetime import datetime


class BibEntry:
    """ Class for storing a single bibliography entry.

    Methods:
        add_authors(authors)
        add_editors(editors)
        set_title(title)
        set_year(year)
        set_month(month)
        set_type(type)
        set_venue(venue)
        set_series(series)
        set_edition(edition)
        set_chapter(chapter)
        set_volume(volume)
        set_number(number)
        set_articleno(articleno)
        set_pages(pages)
        set_publisher(publisher)
        set_address(address)
        set_doi(doi)
        set_url(url)
        set_isbn(isbn)
        set_issn(issn)
        set_git(git)
        set_web(web)
        set_note(note)
        set_descrip(descrip)
        add_keyword(tags)
        get_authors()
        get_editors()
        get_title()
        get_year()
        get_month()
        get_type()
        get_venue()
        get_series()
        get_edition()
        get_chapter()
        get_volume()
        get_number()
        get_articleno()
        get_pages()
        get_publisher()
        get_address()
        get_doi()
        get_url()
        get_isbn()
        get_issn()
        get_git()
        get_web()
        get_note()
        get_descrip()
        get_tags()
        get_key()
        to_dict()
        to_bib()
        __str__()

    """

    __slots__ = [
        'authors',
        'editors',
        'title',
        'year',
        'month',
        'type',
        'venue',
        'series',
        'edition',
        'chapter',
        'volume',
        'number',
        'articleno',
        'pages',
        'publisher',
        'address',
        'doi',
        'url',
        'isbn',
        'issn',
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

        Raises:
            TypeError: If an invalid dict_rep is given.

        """

        self.authors = []
        self.editors = []
        self.title = None
        self.year = None
        self.month = None
        self.type = None
        self.venue = None
        self.series = None
        self.edition = None
        self.chapter = None
        self.volume = None
        self.number = None
        self.articleno = None
        self.pages = None
        self.publisher = None
        self.address = None
        self.doi = None
        self.url = None
        self.isbn = None
        self.issn = None
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

    def add_authors(self, authors, reset=False):
        """ Adds the author to the bib item.

        Args:
            authors (list of str, list of list of str): The author(s) to add
                for this entry.

            reset (bool, optional): Reset the author list to empty before
                adding. Defaults to False.

        Raises:
            TypeError: If 'authors' does not match the expected type.

        """

        if not isinstance(authors, list):
            raise TypeError("expected a list of authors or names, got:"
                            f" {type(authors)}")
        if reset:
            self.authors = []
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

    def add_editors(self, editors, reset=False):
        """ Adds the editor to the bib item.

        Args:
            editors (list of str, list of list of str): The editor(s) to add
                for this entry.

            reset (bool, optional): Reset the editor list to empty before
                adding. Defaults to False.

        Raises:
            TypeError: If 'editors' does not match the expected type.

        """

        if not isinstance(editors, list):
            raise TypeError("expected a list of editors or names, got:"
                            f" {type(editors)}")
        if reset:
            self.editors = []
        if isinstance(editors[0], str):
            self.editors.append([ni.strip() for ni in editors])
        elif isinstance(editors[0], list) and isinstance(editors[0][0], str):
            for name in editors:
                self.editors.append([ni.strip() for ni in name])
        elif isinstance(editors[0], list):
            raise TypeError("expected a list of editors or names, got:"
                            f" list of lists of {type(editors[0][0])}")
        else:
            raise TypeError("expected a list of editors or names, got:"
                            f" list of {type(editors[0])}")

    def set_title(self, title):
        """ Sets the article title for the bib item.

        Args:
            title (str): The type for this bib entry.

        Raises:
            TypeError: If 'title' does not match the expected type.

        """

        if not isinstance(title, str):
            raise TypeError("expected a string specifying the title, got:"
                            f" {type(title)}")
        self.title = title.strip()

    def set_year(self, year):
        """ Sets the publication year for the bib item.

        Args:
            year (str or int): The year for this bib entry.

        Raises:
            TypeError: If 'year' does not match the expected type.

        """

        if not isinstance(year, str) and not isinstance(year, int):
            raise TypeError("expected a string or int specifying the year, "
                            f" got: {type(year)}")
        self.year = int(str(year).strip())

    def set_month(self, month):
        """ Sets the publication month for the bib item.

        Args:
            month (str): The month for this bib entry.

        Raises:
            TypeError: If 'month' does not match the expected type.

        """

        if not isinstance(month, str):
            raise TypeError("expected a string specifying the month, "
                            f" got: {type(month)}")
        self.month = month.strip()

    def set_type(self, btype):
        """ Sets the entry type for the bib item.

        Args:
            btype (str): The type for this bib entry.

        Raises:
            TypeError: If 'btype' does not match the expected type.

        """

        if not isinstance(btype, str):
            raise TypeError("expected a string specifying the btype, got:"
                            f" {type(btype)}")
        self.type = btype.strip()

    def set_venue(self, venue):
        """ Sets the publication venue for the bib item.

        Args:
            venue (str): The venue for this bib entry.

        Raises:
            TypeError: If 'venue' does not match the expected type.

        """

        if not isinstance(venue, str):
            raise TypeError("expected a string specifying the venue, got:"
                            f" {type(venue)}")
        self.venue = venue.strip()

    def set_series(self, series):
        """ Sets the publisher series for the bib item.

        Args:
            series (str): The series for this bib entry.

        Raises:
            TypeError: If 'series' does not match the expected type.

        """

        if not isinstance(series, str):
            raise TypeError("expected a string specifying the series, got:"
                            f" {type(series)}")
        self.series = series.strip()

    def set_edition(self, edition):
        """ Sets the edition for the bib item.

        Args:
            edition (str or int): The edition for this bib entry.

        Raises:
            TypeError: If 'edition' does not match the expected type.

        """

        if not isinstance(edition, str) and not isinstance(edition, int):
            raise TypeError("expected a string or int specifying the edition, "
                            f"got: {type(edition)}")
        self.edition = str(edition).strip()

    def set_chapter(self, chapter):
        """ Sets the chapter for the bib item.

        Args:
            chapter (str or int): The chapter for this bib entry.

        Raises:
            TypeError: If 'chapter' does not match the expected type.

        """

        if not isinstance(chapter, str) and not isinstance(chapter, int):
            raise TypeError("expected a string or int specifying the chapter, "
                            f"got: {type(chapter)}")
        self.chapter = str(chapter).strip()

    def set_volume(self, volume):
        """ Sets the publication volume for the bib item.

        Args:
            volume (str or int): The volume for this bib entry.

        Raises:
            TypeError: If 'volume' does not match the expected type.

        """

        if not isinstance(volume, str) and not isinstance(volume, int):
            raise TypeError("expected a string or int specifying the volume, "
                            f" got: {type(volume)}")
        self.volume = str(volume).strip()

    def set_number(self, number):
        """ Sets the publication number for the bib item.

        Args:
            number (str or int): The number for this bib entry.

        Raises:
            TypeError: If 'number' does not match the expected type.

        """

        if not isinstance(number, str) and not isinstance(number, int):
            raise TypeError("expected a string or int specifying the number, "
                            f" got: {type(number)}")
        self.number = str(number).strip()

    def set_articleno(self, articleno):
        """ Sets the article number for the bib item.

        Args:
            articleno (str or int): The article articleno for this bib entry.

        Raises:
            TypeError: If 'articleno' does not match the expected type.

        """

        if not isinstance(articleno, str) and not isinstance(articleno, int):
            raise TypeError("expected a string or int specifying the article "
                            f"number, got: {type(articleno)}")
        self.articleno = str(articleno).strip()

    def set_pages(self, pages):
        """ Sets the page number(s) for the bib item.

        Args:
            pages (list of ints or strs): The page numbers (if applicable) or
                number of pages for this bib entry.

        Raises:
            TypeError: If 'pages' does not match the expected type.

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
        if len(pages) == 1:
            self.pages.append(int(str(pages[0]).strip()))
        else:
            for page in pages:
                self.pages.append(str(page).strip())

    def set_publisher(self, publisher):
        """ Sets the publisher name for the bib item.

        Args:
            publisher (str): The publisher or associated org for this bib
                entry.

        Raises:
            TypeError: If 'publisher' does not match the expected type.

        """

        if not isinstance(publisher, str):
            raise TypeError("expected a string specifying the publisher, got:"
                            f" {type(publisher)}")
        self.publisher = publisher.strip()

    def set_address(self, address):
        """ Sets the publisher address for the bib item.

        Args:
            address (str): The address or location for this bib entry.

        Raises:
            TypeError: If 'address' does not match the expected type.

        """

        if not isinstance(address, str):
            raise TypeError("expected a string specifying the address, got:"
                            f" {type(address)}")
        self.address = address.strip()

    def set_doi(self, doi):
        """ Sets the doi for the bib item.

        Args:
            doi (str): The doi for this bib entry.

        Raises:
            TypeError: If 'doi' does not match the expected type.

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

    def set_url(self, url):
        """ Sets the url for the bib item.

        Args:
            url (str): The url for this bib entry.

        Raises:
            TypeError: If 'url' does not match the expected type.

        """

        if not isinstance(url, str):
            raise TypeError("expected a string specifying the url, got:"
                            f" {type(url)}")
        self.url = url.strip()

    def set_isbn(self, isbn):
        """ Sets the ISBN for the bib item.

        Args:
            isbn (str): The ISBN for this bib entry.

        Raises:
            TypeError: If 'isbn' does not match the expected type.

        """

        if not isinstance(isbn, str):
            raise TypeError("expected a string specifying the ISBN, got:"
                            f" {type(isbn)}")
        self.isbn = isbn.strip()

    def set_issn(self, issn):
        """ Sets the ISSN for the bib item.

        Args:
            issn (str): The ISSN for this bib entry.

        Raises:
            TypeError: If 'issn' does not match the expected type.

        """

        if not isinstance(issn, str):
            raise TypeError("expected a string specifying the ISSN, got:"
                            f" {type(issn)}")
        self.issn = issn.strip()

    def set_git(self, git):
        """ Sets the Git repo for the bib item.

        Args:
            git (str): The Git repo web address for this bib entry.

        Raises:
            TypeError: If 'git' does not match the expected type.

        """

        if not isinstance(git, str):
            raise TypeError("expected a string specifying the Git page, got:"
                            f" {type(git)}")
        self.git = git.strip()

    def set_web(self, web):
        """ Sets an additional web address for the bib item.

        Args:
            web (str): The web for this bib entry.

        Raises:
            TypeError: If 'web' does not match the expected type.

        """

        if not isinstance(web, str):
            raise TypeError("expected a string specifying the url, got:"
                            f" {type(web)}")
        self.web = web.strip()

    def set_note(self, note):
        """ Adds any publication notes for the bib item.

        Args:
            note (str): Any notes on this bib entry.

        Raises:
            TypeError: If 'note' does not match the expected type.

        """

        if not isinstance(note, str):
            raise TypeError("expected a string specifying the note(s), got:"
                            f" {type(note)}")
        self.note = note.strip()

    def set_descrip(self, descrip):
        """ My personal description/reading notes for this bib item.

        Args:
            descrip (str): Any descriptions or personal reading notes on this
                bib entry.

        Raises:
            TypeError: If 'descrip' does not match the expected type.

        """

        if not isinstance(descrip, str):
            raise TypeError("expected a string specifying the description, "
                            f"got: {type(descrip)}")
        self.descrip = descrip.strip()

    def add_keyword(self, tag, reset=False):
        """ Attaches relevant tags/keywords to the bib item for easy lookup.

        Args:
            tag (str): Any keywords or tags for this bib entry.

            reset (bool, optional): Reset the tags list to empty before
                adding. Defaults to False.

        Raises:
            TypeError: If 'tag' does not match the expected type.

        """

        if reset:
            self.tags = []
        if isinstance(tag, str):
            if tag.strip() not in self.tags:
                self.tags.append(tag.strip())
        elif isinstance(tag, list):
            for ti in tag:
                if isinstance(ti, str):
                    if ti.strip() not in self.tags:
                        self.tags.append(ti.strip())
                else:
                    raise TypeError("expected a list or string specifying the "
                                    f"keyword(s), got: {type(ti)}")
        else:
            raise TypeError("expected a list or string specifying the "
                            f"keyword(s), got: {type(tag)}")

    def get_key(self):
        """ Create a key for this entry of form: LastNameYearFirstWordOfTitle.

        Returns:
            str: The proposed bibliography entry key.

        Raises:
            ValueError: If it is not possible to generate a valid key for the
                current bib entry due to lack of required information (at least
                one author or publisher information).

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
        for char in ["{", "}", "'", '"', "\\", "`", ":", "-"]:
            last_name = last_name.replace(char, "")
        if self.year is not None:
            year = self.year
        else:
            year = int(datetime.now().year)
        first_word = ""
        for word in self.title.split():
            for char in ["{", "}", "'", '"', "\\", "`", ":", "-"]:
                word = word.replace(char, "")
            if len(word) > 2 and word.lower() not in ignores:
                first_word = word.lower()
                break
        return f"{last_name}{year}{first_word}"

    def get_authors(self):
        """ Gets the authors of the publication.

        Returns:
            list[list[str]]: A list of lists, where each inner list represents
                an author (first name, last name).

        """

        return self.authors

    def get_editors(self):
        """ Gets the editors of the publication.

        Returns:
            list[list[str]]: A list of lists, where each inner list represents
                an editor (first name, last name).

        """

        return self.editors

    def get_title(self):
        """ Gets the title of the publication.

        Returns:
            str: The title of the publication.

        """
        return self.title

    def get_year(self):
        """ Gets the year of the publication.

        Returns:
            int: The year of the publication.

        """

        return self.year

    def get_month(self):
        """ Gets the month of the publication.

        Returns:
            str: The month of the publication.

        """

        return self.month

    def get_type(self):
        """ Gets the type of the publication.

        Returns:
            str: The type of the publication.

        """

        return self.type

    def get_venue(self):
        """ Gets the venue of the publication.

        Returns:
            str: The venue of the publication.

        """

        return self.venue

    def get_series(self):
        """ Gets the series of the publication.

        Returns:
            str: The series of the publication.

        """

        return self.series

    def get_edition(self):
        """ Gets the edition of the publication.

        Returns:
            str: The edition of the publication.

        """

        return self.edition

    def get_chapter(self):
        """ Gets the chapter of the publication.

        Returns:
            str: The chapter of the publication.

        """

        return self.chapter

    def get_volume(self):
        """ Gets the volume of the publication.

        Returns:
            str: The volume of the publication.

        """

        return self.volume

    def get_number(self):
        """ Gets the issue number of the publication.

        Returns:
            str: The number of the publication.

        """

        return self.number

    def get_articleno(self):
        """ Gets the article number of the publication.

        Returns:
            int: The article number of the publication.

        """

        return self.articleno

    def get_pages(self):
        """ Gets the pages of the publication.

        Returns:
            list[int or str]: A list of integers representing the pages.

        """

        return self.pages

    def get_publisher(self):
        """ Gets the publisher of the publication.

        Returns:
            str: The publisher of the publication.

        """

        return self.publisher

    def get_address(self):
        """ Gets the address of the publication.

        Returns:
            str: The address of the publication.

        """

        return self.address

    def get_doi(self):
        """ Gets the DOI (Digital Object Identifier) of the publication.

        Returns:
            str: The DOI of the publication.

        """

        return self.doi

    def get_url(self):
        """ Gets the URL of the publication.

        Returns:
            str: The URL of the publication.

        """

        return self.url

    def get_isbn(self):
        """ Gets the ISBN of the publication.

        Returns:
            str: The ISBN of the publication.

        """

        return self.isbn

    def get_issn(self):
        """ Gets the ISSN of the publication.

        Returns:
            str: The ISSN of the publication.

        """

        return self.issn

    def get_git(self):
        """ Gets the Git repository URL of the publication.

        Returns:
            str: The Git repository URL of the publication.

        """

        return self.git

    def get_web(self):
        """ Gets the web link of the publication.

        Returns:
            str: The web link of the publication.

        """

        return self.web

    def get_note(self):
        """ Gets the note associated with the publication.

        Returns:
            str: The note of the publication.

        """

        return self.note

    def get_descrip(self):
        """ Gets the description of the publication.

        Returns:
            str: The description of the publication.

        """

        return self.descrip

    def get_tags(self):
        """ Gets the tags associated with the publication.

        Returns:
            list[str]: A list of tags.

        """

        return self.tags

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

    def to_bib(self):
        """ Generates a BibTex string representation of this entry.

        Returns:
            str: A BibTex-style entry.

        """

        bib_str = []
        # Get the type
        bib_type = None
        if (
            self.type is not None and
            self.type in [
                'article', 'book', 'booklet', 'conference', 'inbook',
                'incollection', 'inproceedings', 'manual', 'mastersthesis',
                'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished'
            ]
        ):
            bib_type = self.type
        else:
            bib_type = 'misc'
        bib_str.append(f"@{bib_type}{{{self.get_key()},")
        # Get the author names
        if len(self.authors) > 0:
            names = [f"{last}, {first}" for [first, last] in self.authors]
            bib_str.append(f"\tauthor = {{{' and '.join(names)}}},")
        # Get the editor names
        if len(self.editors) > 0:
            names = [f"{last}, {first}" for [first, last] in self.editors]
            bib_str.append(f"\teditor = {{{' and '.join(names)}}},")
        # Get the title
        if self.title is not None:
            bib_str.append(f"\ttitle = {{{self.title}}},")
        # Get the year
        if self.year is not None:
            bib_str.append(f"\tyear = {{{self.year}}},")
        # Get the month
        if self.month is not None:
            bib_str.append(f"\tmonth = {{{self.month}}},")
        # Get the howpublished
        if bib_type == 'misc' and self.type != 'misc':
            bib_str.append(f"\thowpublished = {{{self.type}}},")
        # Get the venue
        if self.venue is not None:
            if bib_type == 'article':
                bib_str.append(f"\tjournal = {{{self.venue}}},")
            else:
                bib_str.append(f"\tbooktitle = {{{self.venue}}},")
        # Get the series
        if self.series is not None:
            bib_str.append(f"\tseries = {{{self.series}}},")
        # Get the edition
        if self.edition is not None:
            bib_str.append(f"\tedition = {{{self.edition}}},")
        # Get the chapter
        if self.chapter is not None:
            bib_str.append(f"\tchapter = {{{self.chapter}}},")
        # Get the volume
        if self.volume is not None:
            bib_str.append(f"\tvolume = {{{self.volume}}},")
        # Get the issue number
        if self.number is not None:
            bib_str.append(f"\tnumber = {{{self.number}}},")
        # Get the article number
        if self.articleno is not None:
            bib_str.append(f"\tarticleno = {{{self.articleno}}},")
        # Get the page numbers
        if self.pages is not None:
            pages = [str(pp) for pp in self.pages]
            if len(self.pages) > 1:
                bib_str.append(f"\tpages = {{{'--'.join(pages)}}},")
            elif len(self.pages) > 0:
                bib_str.append(f"\tnumpages = {{{pages[0]}}},")
        # Get the publisher info
        if self.publisher is not None:
            if bib_type in ['conference', 'inproceedings', 'proceedings']:
                bib_str.append(f"\torganization = {{{self.publisher}}},")
            elif bib_type in ['manual', 'techreport']:
                bib_str.append(f"\tinstitution = {{{self.publisher}}},")
            elif bib_type in ['mastersthesis', 'phdthesis']:
                bib_str.append(f"\tschool = {{{self.publisher}}},")
            else:
                bib_str.append(f"\tpublisher = {{{self.publisher}}},")
        # Get the publisher address
        if self.address is not None:
            if bib_type in ['conference', 'inproceedings', 'proceedings']:
                bib_str.append(f"\tlocation = {{{self.address}}},")
            else:
                bib_str.append(f"\taddress = {{{self.address}}},")
        # Get the DOI
        if self.doi is not None:
            bib_str.append(f"\tdoi = {{{self.doi}}},")
        # Get the URL
        if self.url is not None:
            bib_str.append(f"\turl = {{{self.url}}},")
        # Get the ISBN
        if self.isbn is not None:
            bib_str.append(f"\tisbn = {{{self.isbn}}},")
        # Get the ISSN
        if self.issn is not None:
            bib_str.append(f"\tissn = {{{self.issn}}},")
        # Get the Git address
        if self.git is not None:
            bib_str.append(f"\tgit = {{{self.git}}},")
        # Get additional web address
        if self.web is not None:
            bib_str.append(f"\tweb = {{{self.web}}},")
        # Get any notes
        if self.note is not None:
            bib_str.append(f"\tnote = {{{self.note}}},")
        # Add any description
        if self.descrip is not None and self.descrip != "":
            bib_str.append(f"\tdescrip = {{{self.descrip}}},")
        # Add any keywords / tags
        if len(self.tags) > 0:
            bib_str.append(f"\tkeywords = {{{', '.join(self.tags)}}},")
        return "\n".join(bib_str) + "\n}"

    def auto_fill(self, overwrite=True):
        """ Attempt to clean/autofill this entry in the database using crossref.

        Args:
            overwrite (bool, optional): When True (default), overwrites the
                existing fields with the retrieved fields whenever they are
                found.  Otherwise, will only overwrite fields that are
                currently blank.

        Raises:
            requests.exceptions.RequestException: If any error occurs during
                crossref API request.

        """

        base_url = "https://api.crossref.org/works"  # The crossref query URL
        if self.title is not None and title != "":
            params = {"query": self.title.strip("{").strip("}")}
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise error for bad response
            new_entry = {}
            for i, candi in enumerate(response.json()["message"]["items"]):
                if (
                    len(self.authors) == 0 or
                    len(candi['author']) > 0 and
                    'family' in candi['author'][0].keys() and
                    self.authors[0][-1] in candi['author'][0]['family']
                ):
                    date = None
                    if ('published-print' in candi.keys()):
                        date = 'published-print'
                    elif ('published' in candi.keys()):
                        date = 'published'
                    if (
                        self.year None or date is not None and
                        'date-parts' in candi[date].keys() and
                        len(candidates[date]['date-parts']) > 0 and
                        len(candidates[date]['date-parts'][0]) > 0 and
                        self.year == candi[date]['date-parts'][0][0]
                    ):
                        if 'author' in candi.keys():
                            new_entry['author'] = [
                                [aj['given'], aj['family']]
                                for aj in candi['author']
                            ]
                        if (
                            'date-parts' in candi[date].keys() and
                            len(candidates[date]['date-parts']) > 0 and
                            len(candidates[date]['date-parts'][0]) > 0
                        ):
                            new_entry['year'] = candi[date]['date-parts'][0][0]
                        if 'month' in candi.keys():
                            new_entry['month'] = candi['month']
                        if 'type' in candi.keys():
                            new_entry['type'] = candi['type']
                        if 'venue' in candi.keys():
                            new_entry['venue'] = candi['venue']
                        if 'series' in candi.keys():
                            new_entry['series'] = candi['series']
                        if 'edition' in candi.keys():
                            new_entry['edition'] = candi['edition']
                        if 'chapter' in candi.keys():
                            new_entry['chapter'] = candi['chapter']
                        if 'volume' in candi.keys():
                            new_entry['volume'] = candi['volume']
                        if 'number' in candi.keys():
                            new_entry['number'] = candi['number']
                        if 'articleno' in candi.keys():
                            new_entry['articleno'] = candi['articleno']
                        if 'pages' in candi.keys():
                            new_entry['pages'] = candi['pages']
                        if 'publisher' in candi.keys():
                            new_entry['publisher'] = candi['publisher']
                        if 'address' in candi.keys():
                            new_entry['address'] = candi['address']
                        if 'doi' in candi.keys():
                            new_entry['doi'] = candi['doi']
                        if 'url' in candi.keys():
                            new_entry['url'] = candi['url']
                        if 'isbn' in candi.keys():
                            new_entry['isbn'] = candi['isbn']
                        if 'issn' in candi.keys():
                            new_entry['issn'] = candi['issn']
                        break
                if i > 4:
                    break  # Only do anything if found in the top 5
            for key in new_entry.keys():  # TBD fix this
                if self.key is None:
                    self.key = new_entry[key]

    def __str__(self):
        """ Convert this bib entry into a string.

        Returns:
            str: A string representation of this bibliography entry and its
                internal fields.

        """

        str_rep = f"{self.get_key()}\n"
        for key in self.__slots__:
            str_rep += f"\t{key}: {getattr(self, key)}\n"
        return str_rep
