import unittest

from bibmgr.bib_entry import BibEntry
from bibmgr.tests.data.test_entries import test1_dict, test1_bib, \
                                           test2_dict, test2_bib, \
                                           test3_dict, test3_bib, \
                                           test4_dict, test4_bib, \
                                           test5_dict, test5_bib


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

    def test_add_get_authors(self):
        expected_result = [
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
        ]
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.add_authors(5)
        assert len(tester.get_authors()) == 0
        with self.assertRaises(TypeError):
            tester.add_authors([5])
        assert len(tester.get_authors()) == 0
        with self.assertRaises(TypeError):
            tester.add_authors([[5]])
        assert len(tester.get_authors()) == 0
        tester.add_authors(["Tyler H.  ", "Chang"])
        tester.add_authors([["Tyler H.", " Chang "]])
        tester.add_authors([["Tyler H.", "Chang"], ["TH", "Chang"]])
        for i, itemi in enumerate(tester.get_authors()):
            assert itemi == expected_result[i]
        tester.add_authors(expected_result[0], reset=True)
        assert len(tester.get_authors()) == 1
        assert tester.get_authors()[0] == expected_result[0]

    def test_add_get_editors(self):
        expected_result = [
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["Tyler H.", "Chang"],
            ["TH", "Chang"],
        ]
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.add_editors(5)
        assert len(tester.get_editors()) == 0
        with self.assertRaises(TypeError):
            tester.add_editors([5])
        assert len(tester.get_editors()) == 0
        with self.assertRaises(TypeError):
            tester.add_editors([[5]])
        assert len(tester.get_editors()) == 0
        tester.add_editors(["Tyler H.  ", "Chang"])
        tester.add_editors([["Tyler H.", " Chang "]])
        tester.add_editors([["Tyler H.", "Chang"], ["TH", "Chang"]])
        for i, itemi in enumerate(tester.get_editors()):
            assert itemi == expected_result[i]
        tester.add_editors(expected_result[0], reset=True)
        assert len(tester.get_editors()) == 1
        assert tester.get_editors()[0] == expected_result[0]

    def test_set_get_title(self):
        test_title = "The {TEST}: A title worthy of testing"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_title(5)
        assert tester.get_title() is None
        tester.set_title(test_title)
        assert tester.get_title() == test_title

    def test_set_get_year(self):
        test_year = "2025"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_year([])
        assert tester.get_year() is None
        tester.set_year(test_year)
        assert tester.get_year() == int(test_year)

    def test_set_get_month(self):
        test_month = "January"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_month([])
        assert tester.get_month() is None
        tester.set_month(test_month)
        assert tester.get_month() == test_month

    def test_set_get_type(self):
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_type(5)
        assert tester.get_type() is None
        tester.set_type("book")
        assert tester.get_type() == "book"

    def test_set_get_venue(self):
        test_venue = "Journal of Testing"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_venue(5)
        assert tester.get_venue() is None
        tester.set_venue(test_venue)
        assert tester.get_venue() == test_venue

    def test_set_get_series(self):
        test_series = "Collection of Tests"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_series(5)
        assert tester.get_series() is None
        tester.set_series(test_series)
        assert tester.get_series() == test_series

    def test_set_get_edition(self):
        test_edition = "1st ed"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_edition([5])
        assert tester.get_edition() is None
        tester.set_edition(test_edition)
        assert tester.get_edition() == test_edition

    def test_set_get_chapter(self):
        test_chapter = "Ch. 1"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_chapter([5])
        assert tester.get_chapter() is None
        tester.set_chapter(test_chapter)
        assert tester.get_chapter() == test_chapter

    def test_set_get_volume(self):
        test_volume = "0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_volume([5])
        assert tester.get_volume() is None
        tester.set_volume(test_volume)
        assert tester.get_volume() == test_volume

    def test_set_get_number(self):
        test_number = "Volume 0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_number([5])
        assert tester.get_number() is None
        tester.set_number(test_number)
        assert tester.get_number() == test_number

    def test_set_get_articleno(self):
        test_number = "0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_articleno([5])
        assert tester.get_articleno() is None
        tester.set_articleno(test_number)
        assert tester.get_articleno() == test_number

    def test_set_get_pages(self):
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_pages(5)
        with self.assertRaises(TypeError):
            tester.set_pages([])
        assert tester.get_pages() is None
        tester.set_pages([1, 10])
        assert tester.get_pages() == ["1", "10"]
        tester.set_pages(["10"])
        assert tester.get_pages() == [10]

    def test_set_get_publisher(self):
        test_publisher = "Assoc. Testing, Ltd."
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_publisher(5)
        assert tester.get_publisher() is None
        tester.set_publisher(test_publisher)
        assert tester.get_publisher() == test_publisher

    def test_set_get_address(self):
        test_address = "123 New York Ave, SF, CA, USA"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_address(5)
        assert tester.get_address() is None
        tester.set_address(test_address)
        assert tester.get_address() == test_address

    def test_set_get_doi(self):
        test_doi = "helloworld.1234.567"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_doi(5)
        assert tester.get_doi() is None
        tester.set_doi(test_doi)
        assert tester.get_doi() == test_doi
        tester.set_doi(f"https://doi.org/{test_doi}")
        assert tester.get_doi() == test_doi
        tester.set_doi(f"http://doi.org/{test_doi}")
        assert tester.get_doi() == test_doi
        tester.set_doi(f"doi.org/{test_doi}")
        assert tester.get_doi() == test_doi

    def test_set_get_url(self):
        test_url = "www.helloworld.com"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_url(5)
        assert tester.get_url() is None
        tester.set_url(test_url)
        assert tester.get_url() == test_url

    def test_set_get_isbn(self):
        test_isbn = "1234.567.8910"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_isbn(5)
        assert tester.get_isbn() is None
        tester.set_isbn(test_isbn)
        assert tester.get_isbn() == test_isbn

    def test_set_get_issn(self):
        test_issn = "1234.567.8910"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_issn(5)
        assert tester.get_issn() is None
        tester.set_issn(test_issn)
        assert tester.get_issn() == test_issn

    def test_set_get_git(self):
        test_git = "www.github.com/thchang/bib-manager"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_git(5)
        assert tester.get_git() is None
        tester.set_git(test_git)
        assert tester.get_git() == test_git

    def test_set_get_web(self):
        test_web = "www.helloworld.com"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_web(5)
        assert tester.get_web() is None
        tester.set_web(test_web)
        assert tester.get_web() == test_web

    def test_set_get_note(self):
        test_note = r"""Lorem ipsum blah blah blah.
        \url{https://github.com/thchang/bib-manager} --- go check it out!

        Yours truly,
        T. H. Chang
        """
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_note(5)
        assert tester.get_note() is None
        tester.set_note(test_note)
        assert tester.get_note() == test_note.strip()

    def test_set_get_descrip(self):
        test_descrip = """
        This is my bibtex parser and manager. It requires testing...
        """
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_descrip(5)
        assert tester.get_descrip() is None
        tester.set_descrip(test_descrip)
        assert tester.get_descrip() == test_descrip.strip()

    def test_add_get_keyword(self):
        test_tags = ["bib manager", "parser", "OSS", "BibTex", "LaTeX"]
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.add_keyword(5)
        with self.assertRaises(TypeError):
            tester.add_keyword([5])
        assert len(tester.tags) == 0
        tester.add_keyword(test_tags[0])
        tester.add_keyword(test_tags[1:])
        assert tester.get_tags() == test_tags
        tester.add_keyword(test_tags[0], reset=True)
        assert tester.get_tags()[0] == test_tags[0]

    def test_get_key(self):
        test_key = "chang2025test"
        tester = BibEntry()
        with self.assertRaises(ValueError):
            tester.get_key()
        tester.set_title(" The For when {TEST}:\n tough")
        tester.set_venue("Proc. Testing 2")
        tester.set_publisher("The Chang Hunger for Angry Noob Gang")
        tester.set_git("github.com/thchang/bib-manager")
        assert tester.get_key() == test_key
        tester.add_authors(
            [["Tyler H.", "Chang"], ["Chang", "TH"]]
        )
        tester.set_year("2025")
        assert tester.get_key() == test_key

    def test_to_dict(self):
        my_dict = {'authors': "Tyler Chang",
                   'title': "BibManager",
                   'year': 2025,
                   'git': "https://github.com/thchang/bib-manager"
                   }
        tester = BibEntry(my_dict).to_dict()
        for key in my_dict:
            assert my_dict[key] == tester[key]

    def test_to_bib(self):

        tester = BibEntry(test1_dict)
        assert tester.to_bib() == test1_bib
        tester = BibEntry(test2_dict)
        assert tester.to_bib() == test2_bib
        tester = BibEntry(test3_dict)
        assert tester.to_bib() == test3_bib
        tester = BibEntry(test4_dict)
        assert tester.to_bib() == test4_bib
        tester = BibEntry(test5_dict)
        assert tester.to_bib() == test5_bib

    def test_autofill(self):

        tester = BibEntry(test1_dict)
        assert tester.autofill(overwrite=True)
        assert tester.get_authors()[0][-1] in test1_dict['authors'][0]
        assert tester.to_bib() != test1_bib
        tester = BibEntry(test2_dict)
        assert not tester.autofill(overwrite=True)
        assert tester.to_bib() == test2_bib
        tester = BibEntry(test3_dict)
        assert tester.autofill(overwrite=True)
        assert tester.get_doi().lower() == test3_dict['doi'].lower()
        assert tester.to_bib() != test3_bib
        tester = BibEntry(test4_dict)
        assert not tester.autofill(overwrite=True)
        assert tester.to_bib() == test4_bib
