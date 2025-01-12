import filecmp
import os
import unittest

from bibmgr.bib_parser import BibParser
from bibmgr.tests.unit_tests.common import check_results, soln


class TestBibParser(unittest.TestCase):

    def setup_class(self):
        self.tester = BibParser()

    def test_parse_bib_type(self):
        self.tester.parse_bib_line("type", "book")
        assert self.tester.next_item.get_type() == "book"

    def test_parse_bib_authors(self):
        expected_result = [
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
        ]
        self.tester.parse_bib_line("author", " Tyler  H.  Chang ")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]
        self.tester.parse_bib_line("author", "\n\nChang,\tTyler H.  ")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]
        self.tester.parse_bib_line("author", """
            Tyler H. Chang  \t and
            TH Chang""")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]
        self.tester.parse_bib_line("author", "Chang, Tyler H."
                                   "   and\nChang, TH ")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]

    def test_parse_bib_title(self):
        test_title = "The {TEST}: A title worthy of testing"
        self.tester.parse_bib_line("title", test_title)
        assert self.tester.next_item.get_title() == test_title

    def test_parse_bib_year(self):
        test_year = "2025"
        self.tester.parse_bib_line("year", test_year)
        assert self.tester.next_item.get_year() == int(test_year)

    def test_parse_bib_venue(self):
        test_venue = "Journal of Testing"
        self.tester.parse_bib_line("journal", test_venue)
        assert self.tester.next_item.get_venue() == test_venue
        test_venue = "Proc. Testing"
        self.tester.parse_bib_line("booktitle", test_venue)
        assert self.tester.next_item.get_venue() == test_venue

    def test_parse_bib_series(self):
        test_series = "Collection of Tests"
        self.tester.parse_bib_line("series", test_series)
        assert self.tester.next_item.get_series() == test_series

    def test_parse_bib_volume(self):
        test_volume = "0"
        self.tester.parse_bib_line("volume", test_volume)
        assert self.tester.next_item.get_volume() == int(test_volume)

    def test_parse_bib_number(self):
        test_number = "Volume 0"
        self.tester.parse_bib_line("number", test_number)
        assert self.tester.next_item.get_number() == test_number

    def test_parse_bib_articleno(self):
        test_number = "0"
        self.tester.parse_bib_line("articleno", test_number)
        assert self.tester.next_item.get_articleno() == int(test_number)

    def test_parse_bib_pages(self):
        self.tester.parse_bib_line("pages", "1 -- 10")
        assert self.tester.next_item.get_pages() == [1, 10]
        self.tester.parse_bib_line("pages", "10")
        assert self.tester.next_item.get_pages() == [10]

    def test_parse_bib_publisher(self):
        test_publisher = "Assoc. Testing, Ltd."
        self.tester.parse_bib_line("publisher", test_publisher)
        assert self.tester.next_item.get_publisher() == test_publisher
        self.tester.parse_bib_line("publisher", "Bad Pub")
        assert self.tester.next_item.get_publisher() == test_publisher

    def test_parse_bib_address(self):
        test_address = "123 New York Ave, SF, CA, USA"
        self.tester.parse_bib_line("address", test_address)
        assert self.tester.next_item.get_address() == test_address

    def test_parse_bib_doi(self):
        test_doi = "helloworld.1234.567"
        self.tester.parse_bib_line("doi", test_doi)
        assert self.tester.next_item.get_doi() == test_doi
        self.tester.parse_bib_line("doi", f"https://doi.org/{test_doi}")
        assert self.tester.next_item.get_doi() == test_doi
        self.tester.parse_bib_line("doi", f"doi.org/{test_doi}")
        assert self.tester.next_item.get_doi() == test_doi

    def test_parse_bib_url(self):
        test_url = "www.helloworld.com"
        self.tester.parse_bib_line("url", test_url)
        assert self.tester.next_item.get_url() == test_url

    def test_parse_bib_isbn(self):
        test_isbn = "1234.567.8910"
        self.tester.parse_bib_line("isbn", test_isbn)
        assert self.tester.next_item.get_isbn() == test_isbn

    def test_parse_bib_git(self):
        test_git = "www.github.com/thchang/bib-manager"
        self.tester.parse_bib_line("git", test_git)
        assert self.tester.next_item.get_git() == test_git

    def test_parse_bib_web(self):
        test_web = "www.helloworld.com"
        self.tester.parse_bib_line("web", test_web)
        assert self.tester.next_item.get_web() == test_web

    def test_parse_bib_note(self):
        test_note = r"""Lorem ipsum blah blah blah.
        \url{https://github.com/thchang/bib-manager} --- go check it out!

        Yours truly,
        T. H. Chang
        """
        test_note2 = (
            "Lorem ipsum blah blah blah. "
            r"\url{https://github.com/thchang/bib-manager} "
            "--- go check it out! Yours truly, T. H. Chang"
        )
        self.tester.parse_bib_line("note", test_note)
        assert self.tester.next_item.get_note() == test_note2

    def test_parse_bib_descrip(self):
        test_descrip = """
        This is my bibtex parser and manager. It requires testing...
        """
        self.tester.parse_bib_line("descrip", test_descrip)
        assert self.tester.next_item.get_descrip() == test_descrip.strip()

    def test_parse_bib_keyword(self):
        test_tags = ["bib manager", "parser", "OSS", "BibTex", "LaTeX"]
        for tag in test_tags:
            self.tester.parse_bib_line("keywords", tag)
        assert self.tester.next_item.get_tags() == test_tags

    def test_parse_bib_line(self):
        with self.assertRaises(ValueError):
            self.tester.parse_bib_line("bad_key", "oopsie!")

    def test_parse_bib_file(self):
        self.tester = BibParser()
        for entry in self.tester.parse_bib_file("bibmgr/tests/data/test.bib"):
            check_results(entry)

    def test_write_bib_file(self):
        self.tester = BibParser()
        self.tester.write_bib_file("bibmgr/tests/data/test2.bib", soln)
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        # Cleanup
        os.remove("bibmgr/tests/data/test2.bib")
