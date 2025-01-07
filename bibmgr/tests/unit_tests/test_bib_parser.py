import copy
import filecmp
import os
import unittest

from bibmgr.bib_parser import BibParser
from bibmgr.tests.unit_tests.common import check_results, soln


class TestBibParser(unittest.TestCase):

    def setup_class(self):
        self.tester = BibParser()
        self.tester.nextItem = copy.deepcopy(self.tester.template)

    def test_parse_bib_type(self):
        self.tester.parse_bib_line("type", "book")
        assert self.tester.nextItem['type'] == "book"

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
        for i, itemi in enumerate(self.tester.nextItem['authors']):
            assert itemi == expected_result[i]
        self.tester.parse_bib_line("author", "\n\nChang,\tTyler H.  ")
        for i, itemi in enumerate(self.tester.nextItem['authors']):
            assert itemi == expected_result[i]
        self.tester.parse_bib_line("author", """
            Tyler H. Chang  \t and
            TH Chang""")
        for i, itemi in enumerate(self.tester.nextItem['authors']):
            assert itemi == expected_result[i]
        self.tester.parse_bib_line("author", "Chang, Tyler H."
                                   "   and\nChang, TH ")
        for i, itemi in enumerate(self.tester.nextItem['authors']):
            assert itemi == expected_result[i]

    def test_parse_bib_title(self):
        test_title = "The {TEST}: A title worthy of testing"
        self.tester.parse_bib_line("title", test_title)
        assert self.tester.nextItem['title'] == test_title

    def test_parse_bib_year(self):
        test_year = "2025"
        self.tester.parse_bib_line("year", test_year)
        assert self.tester.nextItem['year'] == int(test_year)

    def test_parse_bib_venue(self):
        test_venue = "Journal of Testing"
        self.tester.parse_bib_line("journal", test_venue)
        assert self.tester.nextItem['venue'] == test_venue
        test_venue = "Proc. Testing"
        self.tester.parse_bib_line("booktitle", test_venue)
        assert self.tester.nextItem['venue'] == test_venue

    def test_parse_bib_series(self):
        test_series = "Collection of Tests"
        self.tester.parse_bib_line("series", test_series)
        assert self.tester.nextItem['series'] == test_series

    def test_parse_bib_volume(self):
        test_volume = "0"
        self.tester.parse_bib_line("volume", test_volume)
        assert self.tester.nextItem['volume'] == int(test_volume)

    def test_parse_bib_number(self):
        test_number = "Volume 0"
        self.tester.parse_bib_line("number", test_number)
        assert self.tester.nextItem['number'] == test_number

    def test_parse_bib_articleno(self):
        test_number = "0"
        self.tester.parse_bib_line("articleno", test_number)
        assert self.tester.nextItem['articleno'] == int(test_number)

    def test_parse_bib_pages(self):
        self.tester.parse_bib_line("pages", "1 -- 10")
        assert self.tester.nextItem['pages'] == [1, 10]
        self.tester.parse_bib_line("pages", "10")
        assert self.tester.nextItem['pages'] == [10]

    def test_parse_bib_publisher(self):
        test_publisher = "Assoc. Testing, Ltd."
        self.tester.parse_bib_line("publisher", test_publisher)
        assert self.tester.nextItem['publisher'] == test_publisher
        self.tester.parse_bib_line("publisher", "Bad Pub")
        assert self.tester.nextItem['publisher'] == test_publisher

    def test_parse_bib_address(self):
        test_address = "123 New York Ave, SF, CA, USA"
        self.tester.parse_bib_line("address", test_address)
        assert self.tester.nextItem['address'] == test_address

    def test_parse_bib_doi(self):
        test_doi = "helloworld.1234.567"
        self.tester.parse_bib_line("doi", test_doi)
        assert self.tester.nextItem['doi'] == test_doi
        self.tester.parse_bib_line("doi", f"https://doi.org/{test_doi}")
        assert self.tester.nextItem['doi'] == test_doi
        self.tester.parse_bib_line("doi", f"doi.org/{test_doi}")
        assert self.tester.nextItem['doi'] == test_doi

    def test_parse_bib_url(self):
        test_url = "www.helloworld.com"
        self.tester.parse_bib_line("url", test_url)
        assert self.tester.nextItem['url'] == test_url

    def test_parse_bib_isbn(self):
        test_isbn = "1234.567.8910"
        self.tester.parse_bib_line("isbn", test_isbn)
        assert self.tester.nextItem['isbn'] == test_isbn

    def test_parse_bib_git(self):
        test_git = "www.github.com/thchang/bib-manager"
        self.tester.parse_bib_line("git", test_git)
        assert self.tester.nextItem['git'] == test_git

    def test_parse_bib_web(self):
        test_web = "www.helloworld.com"
        self.tester.parse_bib_line("web", test_web)
        assert self.tester.nextItem['web'] == test_web

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
        assert self.tester.nextItem['note'] == test_note2

    def test_parse_bib_descrip(self):
        test_descrip = """
        This is my bibtex parser and manager. It requires testing...
        """
        self.tester.parse_bib_line("descrip", test_descrip)
        assert self.tester.nextItem['descrip'] == test_descrip.strip()

    def test_parse_bib_keyword(self):
        test_tags = ["bib manager", "parser", "OSS", "BibTex", "LaTeX"]
        for tag in test_tags:
            self.tester.parse_bib_line("keywords", tag)
        assert self.tester.nextItem['tags'] == test_tags

    def test_add_bib_item(self):
        # Add an item with a complicated name
        self.tester = BibParser()
        self.tester.nextItem = copy.deepcopy(self.tester.template)
        self.tester.parse_bib_line("author", " Tyler H. Chang and Chang, TH")
        self.tester.parse_bib_line("title", " The For when {TEST}:\n tough")
        self.tester.parse_bib_line("year", "2025")
        self.tester.parse_bib_line("booktitle", "Proc. Testing 2")
        self.tester.parse_bib_line("git", "github.com/thchang/bib-manager")
        test_copy = copy.deepcopy(self.tester.nextItem)
        self.tester.add_bib_item()
        assert 'chang2025test' in self.tester.info
        for key in self.tester.info['chang2025test']:
            assert key in test_copy
            assert self.tester.info['chang2025test'][key] == test_copy[key]
        for key in test_copy:
            assert key in self.tester.info['chang2025test']
            assert self.tester.info['chang2025test'][key] == test_copy[key]
        # Try to add a duplicate with a different venue
        self.tester.nextItem = copy.deepcopy(self.tester.template)
        self.tester.parse_bib_line("author", " Tyler H. Chang and Chang, TH")
        self.tester.parse_bib_line("title", " The For when {TEST}:\n tough")
        self.tester.parse_bib_line("year", "2025")
        self.tester.parse_bib_line("booktitle", "Proc. Testing 2")  # changed
        self.tester.parse_bib_line("git", "github.com/thchang/bib-manager")
        self.tester.add_bib_item()
        for key in self.tester.info['chang2025test']:
            assert key in test_copy
            assert self.tester.info['chang2025test'][key] == test_copy[key]
        for key in test_copy:
            assert key in self.tester.info['chang2025test']
            assert self.tester.info['chang2025test'][key] == test_copy[key]

    def test_parse_bib_line(self):
        with self.assertRaises(ValueError):
            self.tester.parse_bib_line("bad_key", "oopsie!")

    def test_parse_bib_file(self):
        self.tester = BibParser()
        self.tester.parse_bib_file("bibmgr/tests/data/test.bib")
        check_results(self.tester)

    def test_write_bib_file(self):
        self.tester = BibParser()
        self.tester.info = soln
        self.tester.write_bib_file("bibmgr/tests/data/test2.bib")
        assert os.path.exists("bibmgr/tests/data/test2.bib")
        assert filecmp.cmp("bibmgr/tests/data/written_test.bib",
                           "bibmgr/tests/data/test2.bib")
        # Cleanup
        os.remove("bibmgr/tests/data/test2.bib")
