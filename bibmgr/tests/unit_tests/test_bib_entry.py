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

    def test_set_get_volume(self):
        test_volume = "0"
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_volume([5])
        assert tester.get_volume() is None
        tester.set_volume(test_volume)
        assert tester.get_volume() == int(test_volume)

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
        assert tester.get_articleno() == int(test_number)

    def test_set_get_pages(self):
        tester = BibEntry()
        with self.assertRaises(TypeError):
            tester.set_pages(5)
        with self.assertRaises(TypeError):
            tester.set_pages([])
        assert tester.get_pages() is None
        tester.set_pages([1, 10])
        assert tester.get_pages() == [1, 10]
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
        test1_dict = {
            'authors': [
                ['Tyler H.', 'Chang'],
                ['Layne T.', 'Watson'],
                ['Thomas C. H.', 'Lux'],
                ['Ali R.', 'Butt'],
                ['Kirk W.', 'Cameron'],
                ['Yili', 'Hong']
            ],
            'title': (
                'Algorithm 1012: {DELAUNAYSPARSE}: {I}nterpolation via a '
                'sparse subset of the {D}elaunay triangulation in medium to '
                'high dimensions'
            ),
            'year': 2020,
            'type': 'article',
            'venue': 'ACM Transactions on Mathematical Software',
            'series': 'Collections of the ACM',
            'volume': 46,
            'number': '4',
            'articleno': 38,
            'pages': [20],
            'publisher': 'Association of Computing Machinery',
            'address': 'New York, NY, USA',
            'doi': '10.1145/3422818',
            'url': 'https://dl.acm.org/doi/10.1145/3422818',
            'isbn': '0098-3500',
            'git': 'https://github.com/vtopt/DelaunaySparse',
            'web': 'https://vtopt.github.io/DelaunaySparse',
            'descrip': '',
            'tags': ['software', 'algorithms', 'delaunay triangulation'],
        }
        test1_bib = (
            "@article{chang2020algorithm,\n"
            "\tauthor = {Chang, Tyler H. and Watson, Layne T. and "
            "Lux, Thomas C. H. and Butt, Ali R. and Cameron, Kirk W. "
            "and Hong, Yili},\n"
            "\ttitle = {Algorithm 1012: {DELAUNAYSPARSE}: "
            "{I}nterpolation via a sparse subset of the {D}elaunay "
            "triangulation in medium to high dimensions},\n"
            "\tyear = {2020},\n"
            "\tjournal = {ACM Transactions on Mathematical Software},\n"
            "\tseries = {Collections of the ACM},\n"
            "\tvolume = {46},\n"
            "\tnumber = {4},\n"
            "\tarticleno = {38},\n"
            "\tnumpages = {20},\n"
            "\tpublisher = {Association of Computing Machinery},\n"
            "\taddress = {New York, NY, USA},\n"
            "\tdoi = {10.1145/3422818},\n"
            "\turl = {https://dl.acm.org/doi/10.1145/3422818},\n"
            "\tisbn = {0098-3500},\n"
            "\tgit = {https://github.com/vtopt/DelaunaySparse},\n"
            "\tweb = {https://vtopt.github.io/DelaunaySparse},\n"
            "\tkeywords = {software, algorithms, delaunay triangulation},\n"
            "}"
        )
        test2_dict = {
            'authors': [['Tyler H.', 'Chang']],
            'title': (
                '{GPU} Saturation for Multiple Matrix-Vector Multiplications'
            ),
            'year': 2016,
            'type': 'Bachelor\'s Thesis',
            'publisher': (
                'Department of Computer Science, Virginia Wesleyan University'
            ),
            'address': 'Virginia Beach, VA, USA',
            'tags': [],
        }
        test2_bib = (
            "@misc{chang2016gpu,\n"
            "\tauthor = {Chang, Tyler H.},\n"
            "\ttitle = {{GPU} Saturation for Multiple Matrix-Vector "
            "Multiplications},\n"
            "\tyear = {2016},\n"
            "\thowpublished = {Bachelor's Thesis},\n"
            "\tpublisher = {Department of Computer Science, Virginia Wesleyan "
            "University},\n"
            "\taddress = {Virginia Beach, VA, USA},\n"
            "}"
        )
        test3_dict = {
            'authors': [
                ['Manisha', 'Garg'],
                ['Tyler H.', 'Chang'],
                ['Krishnan', 'Raghavan']
            ],
            'title': (
                '{SF-SFD}: {S}tochastic optimization of {F}ourier '
                'coefficients for space-filling designs'
            ),
            'year': 2023,
            'type': 'inproceedings',
            'venue': 'Proc. 2023 Winter Simulation Conference (WSC 2023)',
            'series': None,
            'volume': None,
            'number': None,
            'articleno': None,
            'pages': [3636, 3646],
            'publisher': 'ACM',
            'address': 'San Antonio, TX, USA',
            'doi': '10.1109/WSC60868.2023.10408245',
            'url': None,
            'isbn': None,
            'git': None,
            'web': None,
            'note': None,
            'descrip': '',
            'tags': [],
        }
        test3_bib = (
            "@inproceedings{garg2023sfsfd,\n"
            "\tauthor = {Garg, Manisha and Chang, Tyler H. and Raghavan, "
            "Krishnan},\n"
            "\ttitle = {{SF-SFD}: {S}tochastic optimization of {F}ourier "
            "coefficients for space-filling designs},\n"
            "\tyear = {2023},\n"
            "\tbooktitle = {Proc. 2023 Winter Simulation Conference (WSC "
            "2023)},\n"
            "\tpages = {3636--3646},\n"
            "\torganization = {ACM},\n"
            "\tlocation = {San Antonio, TX, USA},\n"
            "\tdoi = {10.1109/WSC60868.2023.10408245},\n"
            "}"
        )
        test4_dict = {
            'authors': [['Tyler H.', 'Chang']],
            'title': (
                'Mathematical Software for Multiobjective Optimization '
                'Problems'
             ),
            'year': 2020,
            'type': 'phdthesis',
            'publisher': (
                'Department of Computer Science, Virginia Polytechnic '
                'Institute and State University (Virginia Tech)'
            ),
            'address': 'Blacksburg, VA, USA',
            'url': 'http://hdl.handle.net/10919/98915',
            'note': (
                '{\\bf Dept. of Computer Science Nominee for Outstanding '
                'Dissertation Award}'
             ),
            'descrip': '',
        }
        test4_bib = (
            "@phdthesis{chang2020mathematical,\n"
            "\tauthor = {Chang, Tyler H.},\n"
            "\ttitle = {Mathematical Software for Multiobjective Optimization "
            "Problems},\n"
            "\tyear = {2020},\n"
            "\tschool = {Department of Computer Science, Virginia "
            "Polytechnic Institute and State University (Virginia Tech)},\n"
            "\taddress = {Blacksburg, VA, USA},\n"
            "\turl = {http://hdl.handle.net/10919/98915},\n"
            "\tnote = {{\\bf Dept. of Computer Science Nominee for "
            "Outstanding Dissertation Award}},\n"
            "}"
        )
        test5_dict = {
            'authors': [
                ['Tyler H.', 'Chang'],
                ['Stefan M.', 'Wild'],
                ['Hyrum', 'Dickinson']
            ],
            'title': (
                '{ParMOO}: {P}ython library for parallel multiobjective '
                'simulation optimization'
            ),
            'year': 2024,
            'type': 'techreport',
            'number': 'Version 0.4.1',
            'publisher': 'Argonne National Laboratory',
            'address': 'Lemont, Illinois, USA',
            'url': 'https://parmoo.readthedocs.io/_/downloads/en/latest/pdf/',
            'descrip': (
                'These are just the readthedocs pages for my '
                'ParMOO software, but there are features in here that are not '
                'publication worthy so there may be reasons to cite the docs '
                'over the paper itself.'
            ),
        }
        test5_bib = (
            "@techreport{chang2024parmoo,\n"
            "\tauthor = {Chang, Tyler H. and Wild, Stefan M. and Dickinson, "
            "Hyrum},\n"
            "\ttitle = {{ParMOO}: {P}ython library for parallel "
            "multiobjective simulation optimization},\n"
            "\tyear = {2024},\n"
            "\tnumber = {Version 0.4.1},\n"
            "\tinstitution = {Argonne National Laboratory},\n"
            "\taddress = {Lemont, Illinois, USA},\n"
            "\turl = "
            "{https://parmoo.readthedocs.io/_/downloads/en/latest/pdf/},\n"
            "\tdescrip = {These are just the readthedocs pages for my "
            "ParMOO software, but there are features in here that are not "
            "publication worthy so there may be reasons to cite the docs "
            "over the paper itself.},\n"
            "}"
        )

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
