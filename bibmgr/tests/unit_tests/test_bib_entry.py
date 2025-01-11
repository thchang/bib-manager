import unittest

from bibmgr.bib_entry import BibEntry


class TestBibEntry(unittest.TestCase):

    def test_BibEntry_init(self):
        tester = BibEntry()
        for key in tester.__slots__:
            if getattr(tester, key) is not None:
                assert getattr(tester, key) == []
        with self.assertRaises(TypeError):
            BibEntry(5)
        my_dict = {'authors': "Tyler Chang",
                   'title': "BibManager",
                   'year': 2025,
                   'git': "https://github.com/thchang/bib-manager"
                   }
        tester = BibEntry(my_dict)
        for key in my_dict:
            assert getattr(tester, key) == my_dict[key]

    def test_set_bib_type(self):
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_type(5)
        assert tester.type is None
        tester.set_bib_type("book")
        assert tester.type == "book"

    def test_add_bib_authors(self):
        expected_result = [
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
        ]
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.add_bib_authors(5)
        assert len(tester.authors) == 0
        with self.assertRaises(TypeError):
            tester.add_bib_authors([5])
        assert len(tester.authors) == 0
        with self.assertRaises(TypeError):
            tester.add_bib_authors([[5]])
        assert len(tester.authors) == 0
        tester.add_bib_authors(["Tyler H.  ", "Chang"])
        tester.add_bib_authors([["Tyler H.", " Chang "]])
        tester.add_bib_authors([["Tyler H.", "Chang"], ["TH", "Chang"]])
        for i, itemi in enumerate(tester.authors):
            assert itemi == expected_result[i]

    def test_set_bib_title(self):
        test_title = "The {TEST}: A title worthy of testing"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_title(5)
        assert tester.title is None
        tester.set_bib_title(test_title)
        assert tester.title == test_title

    def test_set_bib_year(self):
        test_year = "2025"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_year([])
        assert tester.year is None
        tester.set_bib_year(test_year)
        assert tester.year == int(test_year)

    def test_set_bib_venue(self):
        test_venue = "Journal of Testing"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_venue(5)
        assert tester.venue is None
        tester.set_bib_venue(test_venue)
        assert tester.venue == test_venue

    def test_set_bib_series(self):
        test_series = "Collection of Tests"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_series(5)
        assert tester.series is None
        tester.set_bib_series(test_series)
        assert tester.series == test_series

    def test_set_bib_volume(self):
        test_volume = "0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_volume([5])
        assert tester.volume is None
        tester.set_bib_volume(test_volume)
        assert tester.volume == int(test_volume)

    def test_set_bib_number(self):
        test_number = "Volume 0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_number([5])
        assert tester.number is None
        tester.set_bib_number(test_number)
        assert tester.number == test_number

    def test_set_bib_articleno(self):
        test_number = "0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_articleno([5])
        assert tester.articleno is None
        tester.set_bib_articleno(test_number)
        assert tester.articleno == int(test_number)

    def test_set_bib_pages(self):
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_pages(5)
        with self.assertRaises(TypeError):
            tester.set_bib_pages([])
        assert tester.pages is None
        tester.set_bib_pages([1, 10])
        assert tester.pages == [1, 10]
        tester.set_bib_pages(["10"])
        assert tester.pages == [10]

    def test_set_bib_publisher(self):
        test_publisher = "Assoc. Testing, Ltd."
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_publisher(5)
        assert tester.publisher is None
        tester.set_bib_publisher(test_publisher)
        assert tester.publisher == test_publisher

    def test_set_bib_address(self):
        test_address = "123 New York Ave, SF, CA, USA"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_address(5)
        assert tester.address is None
        tester.set_bib_address(test_address)
        assert tester.address == test_address

    def test_set_bib_doi(self):
        test_doi = "helloworld.1234.567"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_doi(5)
        assert tester.doi is None
        tester.set_bib_doi(test_doi)
        assert tester.doi == test_doi
        tester.set_bib_doi(f"https://doi.org/{test_doi}")
        assert tester.doi == test_doi
        tester.set_bib_doi(f"http://doi.org/{test_doi}")
        assert tester.doi == test_doi
        tester.set_bib_doi(f"doi.org/{test_doi}")
        assert tester.doi == test_doi

    def test_set_bib_url(self):
        test_url = "www.helloworld.com"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_url(5)
        assert tester.url is None
        tester.set_bib_url(test_url)
        assert tester.url == test_url

    def test_set_bib_isbn(self):
        test_isbn = "1234.567.8910"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_isbn(5)
        assert tester.isbn is None
        tester.set_bib_isbn(test_isbn)
        assert tester.isbn == test_isbn

    def test_set_bib_git(self):
        test_git = "www.github.com/thchang/bib-manager"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_git(5)
        assert tester.git is None
        tester.set_bib_git(test_git)
        assert tester.git == test_git

    def test_set_bib_web(self):
        test_web = "www.helloworld.com"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_web(5)
        assert tester.web is None
        tester.set_bib_web(test_web)
        assert tester.web == test_web

    def test_set_bib_note(self):
        test_note = r"""Lorem ipsum blah blah blah.
        \url{https://github.com/thchang/bib-manager} --- go check it out!

        Yours truly,
        T. H. Chang
        """
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_note(5)
        assert tester.note is None
        tester.set_bib_note(test_note)
        assert tester.note == test_note.strip()

    def test_set_bib_descrip(self):
        test_descrip = """
        This is my bibtex parser and manager. It requires testing...
        """
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_bib_descrip(5)
        assert tester.descrip is None
        tester.set_bib_descrip(test_descrip)
        assert tester.descrip == test_descrip.strip()

    def test_add_bib_keyword(self):
        test_tags = ["bib manager", "parser", "OSS", "BibTex", "LaTeX"]
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.add_bib_keyword(5)
        with self.assertRaises(TypeError):
            tester.add_bib_keyword([5])
        assert len(tester.tags) == 0
        tester.add_bib_keyword(test_tags[0])
        tester.add_bib_keyword(test_tags[1:])
        assert tester.tags == test_tags

    def test_get_bib_key(self):
        test_key = "chang2025test"
        tester = BibEntry()
        with self.assertRaises(ValueError):
            tester.get_bib_key()
        tester.set_bib_title(" The For when {TEST}:\n tough")
        tester.set_bib_venue("Proc. Testing 2")
        tester.set_bib_publisher("The Chang Hunger for Angry Noob Gang")
        tester.set_bib_git("github.com/thchang/bib-manager")
        assert tester.get_bib_key() == test_key
        tester.add_bib_authors(
            [["Tyler H.", "Chang"], ["Chang", "TH"]]
        )
        tester.set_bib_year("2025")
        assert tester.get_bib_key() == test_key

    def test_to_dict(self):
        my_dict = {'authors': "Tyler Chang",
                   'title': "BibManager",
                   'year': 2025,
                   'git': "https://github.com/thchang/bib-manager"
                   }
        tester = BibEntry(my_dict).to_dict()
        for key in my_dict:
            assert my_dict[key] == tester[key]
