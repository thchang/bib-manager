import filecmp
import os
import unittest

from bibmgr.bib_entry import BibEntry
from bibmgr.bib_parser import BibParser
from bibmgr.tests.unit_tests.common import check_results, soln


class TestBibParser(unittest.TestCase):

    def setup_class(self):
        self.tester = BibParser()

    def test_parse_type(self):
        self.tester.parse_line("type", "book")
        assert self.tester.next_item.get_type() == "book"

    def test_parse_authors(self):
        expected_result = [
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
        ]
        self.tester.parse_line("author", " Tyler  H.  Chang ")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]
        self.tester.parse_line("author", "\n\nChang,\tTyler H.  ")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]
        self.tester.parse_line("author", """
            Tyler H. Chang  \t and
            TH Chang""")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]
        self.tester.parse_line("author", "Chang, Tyler H.   and\nChang, TH ")
        for i, itemi in enumerate(self.tester.next_item.get_authors()):
            assert itemi == expected_result[i]

    def test_parse_editors(self):
        expected_result = [
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
        ]
        self.tester.parse_line("editor", " Tyler  H.  Chang ")
        for i, itemi in enumerate(self.tester.next_item.get_editors()):
            assert itemi == expected_result[i]
        self.tester.parse_line("editor", "\n\nChang,\tTyler H.  ")
        for i, itemi in enumerate(self.tester.next_item.get_editors()):
            assert itemi == expected_result[i]
        self.tester.parse_line("editor", """
            Tyler H. Chang  \t and
            TH Chang""")
        for i, itemi in enumerate(self.tester.next_item.get_editors()):
            assert itemi == expected_result[i]
        self.tester.parse_line("editor", "Chang, Tyler H.   and\nChang, TH ")
        for i, itemi in enumerate(self.tester.next_item.get_editors()):
            assert itemi == expected_result[i]

    def test_parse_title(self):
        test_title = "The {TEST}: A title worthy of testing"
        self.tester.parse_line("title", test_title)
        assert self.tester.next_item.get_title() == test_title

    def test_parse_year(self):
        test_year = "2025"
        self.tester.parse_line("year", test_year)
        assert self.tester.next_item.get_year() == int(test_year)

    def test_parse_month(self):
        test_month = "jan"
        self.tester.parse_line("month", test_month)
        assert self.tester.next_item.get_month() == test_month

    def test_parse_venue(self):
        test_venue = "Journal of Testing"
        self.tester.parse_line("journal", test_venue)
        assert self.tester.next_item.get_venue() == test_venue
        test_venue = "Proc. Testing"
        self.tester.parse_line("booktitle", test_venue)
        assert self.tester.next_item.get_venue() == test_venue

    def test_parse_series(self):
        test_series = "Collection of Tests"
        self.tester.parse_line("series", test_series)
        assert self.tester.next_item.get_series() == test_series

    def test_parse_edition(self):
        test_edition = "1st Edition"
        self.tester.parse_line("edition", test_edition)
        assert self.tester.next_item.get_edition() == test_edition

    def test_parse_chapter(self):
        test_chapter = "Ch. 1"
        self.tester.parse_line("chapter", test_chapter)
        assert self.tester.next_item.get_chapter() == test_chapter

    def test_parse_volume(self):
        test_volume = "0"
        self.tester.parse_line("volume", test_volume)
        assert self.tester.next_item.get_volume() == test_volume

    def test_parse_number(self):
        test_number = "Volume 0"
        self.tester.parse_line("number", test_number)
        assert self.tester.next_item.get_number() == test_number

    def test_parse_articleno(self):
        test_number = "0"
        self.tester.parse_line("articleno", test_number)
        assert self.tester.next_item.get_articleno() == int(test_number)

    def test_parse_pages(self):
        self.tester.parse_line("pages", "1 -- 10")
        assert self.tester.next_item.get_pages() == ["1", "10"]
        self.tester.parse_line("pages", "10")
        assert self.tester.next_item.get_pages() == [10]

    def test_parse_publisher(self):
        test_publisher = "Assoc. Testing, Ltd."
        self.tester.parse_line("publisher", test_publisher)
        assert self.tester.next_item.get_publisher() == test_publisher
        self.tester.parse_line("publisher", "Bad Pub")
        assert self.tester.next_item.get_publisher() == test_publisher

    def test_parse_address(self):
        test_address = "123 New York Ave, SF, CA, USA"
        self.tester.parse_line("address", test_address)
        assert self.tester.next_item.get_address() == test_address

    def test_parse_doi(self):
        test_doi = "helloworld.1234.567"
        self.tester.parse_line("doi", test_doi)
        assert self.tester.next_item.get_doi() == test_doi
        self.tester.parse_line("doi", f"https://doi.org/{test_doi}")
        assert self.tester.next_item.get_doi() == test_doi
        self.tester.parse_line("doi", f"doi.org/{test_doi}")
        assert self.tester.next_item.get_doi() == test_doi

    def test_parse_url(self):
        test_url = "www.helloworld.com"
        self.tester.parse_line("url", test_url)
        assert self.tester.next_item.get_url() == test_url

    def test_parse_isbn(self):
        test_isbn = "1234.567.8910"
        self.tester.parse_line("isbn", test_isbn)
        assert self.tester.next_item.get_isbn() == test_isbn

    def test_parse_issn(self):
        test_issn = "1234.567.8910"
        self.tester.parse_line("issn", test_issn)
        assert self.tester.next_item.get_issn() == test_issn

    def test_parse_git(self):
        test_git = "www.github.com/thchang/bib-manager"
        self.tester.parse_line("git", test_git)
        assert self.tester.next_item.get_git() == test_git

    def test_parse_web(self):
        test_web = "www.helloworld.com"
        self.tester.parse_line("web", test_web)
        assert self.tester.next_item.get_web() == test_web

    def test_parse_note(self):
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
        self.tester.parse_line("note", test_note)
        assert self.tester.next_item.get_note() == test_note2

    def test_parse_descrip(self):
        test_descrip = """
        This is my bibtex parser and manager. It requires testing...
        """
        self.tester.parse_line("descrip", test_descrip)
        assert self.tester.next_item.get_descrip() == test_descrip.strip()

    def test_parse_keyword(self):
        test_tags = ["bib manager", "parser", "OSS", "BibTex", "LaTeX"]
        for tag in test_tags:
            self.tester.parse_line("keywords", tag)
        assert self.tester.next_item.get_tags() == test_tags

    def test_parse_line(self):
        with self.assertRaises(KeyError):
            self.tester.parse_line("bad_key", "oopsie!")

    def test_parse_file(self):
        self.tester = BibParser()
        with open("bibmgr/tests/data/test.bib", "r") as fp:
            for entry in self.tester.parse_file(fp):
                check_results(entry)
        self.tester = BibParser()
        test_data = ""
        with open("bibmgr/tests/data/test.bib", "r") as fp:
            test_data = fp.read()
        for entry in self.tester.parse_file(test_data):
            check_results(entry)

    def test_write_file(self):
        self.tester = BibParser()
        with open("bibmgr/tests/data/test2.bib", "w") as fp:
            for next_key in soln:
                self.tester.write_file(BibEntry(soln[next_key]), fp)
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        # Cleanup
        os.remove("bibmgr/tests/data/test2.bib")
