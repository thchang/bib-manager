import yaml

from .bib_entry import BibEntry
from .dict_database import DictDatabase


class DatabaseManager(DictDatabase):
    """ An extension of the core database structure with additional methods for
    parsing bib and yaml files.

    Inherits from DictDatabase.

    Methods:
        read_yaml(filename)
        read_bibtex(filename)
        write_yaml(filename)
        write_bibtex(filename, comment=False)
        autofill(overwrite=False)

    """

    __slots__ = [
        'bib_parser',
        'info'
    ]

    def __init__(self):
        """ Constructor for the database manager. """

        super().__init__()

    def read_yaml(self, filename):
        """ Load database from a yaml file.

        Args:
            filename (str or path-like object): The path to the file to load
                bibliography entries from.

        """

        with open(filename, "r") as fp:
            info_dict = yaml.safe_load(fp)
        for next_key in info_dict:
            self.create_entry(BibEntry(info_dict[next_key]))

    def read_bibtex(self, filename):
        """ Load database from a BibTex file.

        Args:
            filename (str or path-like object): The path to the file to load
                bibliography entries from.

        """

        with open(filename, "r") as fp:
            for entry in self.bib_parser.parse_file(fp):
                self.create_entry(entry)

    def write_yaml(self, filename):
        """ Write database to a yaml file.

        Args:
            filename (str or path-like object): The path to the file to write
                bibliography entries to.

        """

        info_dict = {}
        for entry in self.entries():
            info_dict[entry.get_key()] = entry.to_dict()
        with open(filename, "w") as fp:
            yaml.dump(info_dict, fp)

    def write_bibtex(self, filename, comment=False):
        """ Write database to a BibTex file.

        Args:
            filename (str or path-like object): The path to the file to write
                bibliography entries to.
            comment (bool, optional): Print the description field as a comment
                at the top of the bib entry when True. Defaults to False.

        """

        with open(filename, "w") as fp:
            for entry in self.entries():
                self.bib_parser.write_file(entry, fp, comment=comment)

    def autofill(self, overwrite=False):
        """ Autofill missing fields for all entries via crossref lookup.

        Args:
            overwrite (bool, optional): Overwrite existing fields with
                crossref lookups. Defaults to False.

        """

        for entry in self.entries():
            entry.autofill(overwrite)
