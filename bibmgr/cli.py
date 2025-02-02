import os
import re

from bibmgr.bib_entry import BibEntry
from bibmgr.bib_parser import BibParser
from bibmgr.database_manager import DatabaseManager


class DatabaseCLI:
    """ A CLI for interacting with the BibMgr Database.

    Provides the following interface methods:

     * `add_entry()`
     * `clear()`
     * `delete_entry(entry_key)`
     * `filter()`
     * `load_data(filepath, overwrite=False)`
     * `save_data(filepath, overwrite=False)`
     * `set_predicate(pred_str)`
     * `show(entry_key)`
     * `update_entry(entry_key, update_field, update_data)`

    And the following helper methods:

     * `_predicate(x)`
     * `_print(message)`
     * `_user_continue()`

     * `parse_args()` TBD
     * `run(args)` TBD

    Together, these are used to build the bibmgr CLI, defined in `__main__.py`.

    """

    def __init__(self):
        """ Initialize the CLI from the cache file. """

        self.cache_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "bibcache.yaml"
        )
        self.database = DatabaseManager()
        self.pred_str = None
        if os.path.exists(self.cache_file):
            self.database.read_yaml(self.cache_file)
        self.force = False
        self.verbose = True

    def add_entry(self):
        """ Add a new entry to the cache. """

        parser = BibParser()
        parser.next_item = BibEntry()
        next_val = input("Enter publication type: ")
        valid_types = [
            'article', 'book', 'booklet', 'conference', 'inbook',
            'incollection', 'inproceedings', 'manual', 'mastersthesis',
            'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished'
        ]
        if next_val not in valid_types:
            self._print("Warning: Publication type should usually be one of: ")
            self._print(", ".join(valid_types))
            next_val = input("Re-enter publication type: ")
            while len(next_val.strip()) == 0:
                next_val = input("Type required. Enter publication type: ")
        parser.parse_line("type", next_val)
        for (next_key, instructions) in [
            ("authors", "Enter authors separated by 'and'"),
            ("title", "Enter publication title"),
            ("year", "Enter publication year"),
            ("venue", "Enter journal, conference booktitle, or other venue"),
            ("series", "Enter publisher series"),
            ("volume", "Enter volume number"),
            ("number", "Enter issue number"),
            ("articleno", "Enter article number"),
            ("pages", "Enter pages either first--last or num pages"),
            ("publisher", "Enter publisher name"),
            ("address", "Enter publisher address or conference location"),
            ("doi", "Enter doi if known"),
            ("url", "Enter official publication url"),
            ("isbn", "Enter publication ISBN"),
            ("web", "Enter any additional authors' website"),
            ("git", "Enter any git repo for the project"),
            ("note", "Enter any publisher's notes"),
            ("descrip", "Enter a short description of this entry"),
            ("tags", "Enter a comma-separated list of keywords"),
        ]:
            next_val = input(
                f"Enter {next_key} {instructions} (leave blank if none): "
            )
            if len(next_val.strip()) > 0:
                parser.parse_line(next_key, next_val)
        self._print(f"Will add: {parser.next_item}")
        if self._user_continue():
            self.database.create_entry(parser.next_item)
            self.database.write_yaml(self.cache_file)

    def clear(self):
        """ Clear the cache. """

        if os.path.exists(self.cache_file):
            self._print(f"Will remove {self.database.size()} items stored in "
                        f"{self.cache_file}")
            if self._user_continue():
                os.remove(self.cache_file)
                self.database = DatabaseManager()

    def delete_entry(self, entry_key):
        """ Delete an entry from the cache. """

        if self.database.contains(entry_key):
            self._print(f"Will delete: {entry_key}")
            if self._user_continue():
                self.database.delete_entry(entry_key)
                self.database.write_yaml(self.cache_file)
        else:
            self._print(f"{entry_key} not found, aborting.")

    def filter(self):
        """ Filter the current contents of the cache. """

        if self.pred_str is None:
            raise RuntimeError("No predicate to filter")
        temp_db = DatabaseManager()
        for entry in self.database.entries(self._predicate):
            temp_db.create_entry(entry)
        self._print(f"{self.database.size() - temp_db.size()} items filtered")
        if self._user_continue():
            self.database = temp_db
            self.database.write_yaml(self.cache_file)

    def load_data(self, filepath, overwrite=False):
        """ Load a database of existing entries into the cache.

        Args:
            filepath (path-like object): The path to the file to load.

        """

        if not os.path.exists(filepath):
            raise RuntimeError(f"{filepath} does not exist")
        temp_db = DatabaseManager()
        if filepath.split(".")[-1].lower() == "bib":
            temp_db.read_bibtex(filepath)
        else:
            temp_db.read_yaml(filepath)
        if overwrite:
            self.database = temp_db
        else:
            for entry in temp_db.entries():
                try:
                    self.database.create_entry(entry)
                except KeyError:
                    self._print(
                        f"found duplicate: {entry.get_key()}; skipping..."
                    )
        self._print(f"Will load {temp_db.size()} entries")
        if self._user_continue():
            self.database.write_yaml(self.cache_file)

    def save_data(self, filepath, overwrite=False):
        """ Write all entries in the current cache to a file.

        Args:
            filepath (path-like object): The path to the file to write.

        """

        if os.path.exists(filepath):
            self._print("Found an existing file")
            if not overwrite:
                temp_db = DatabaseManager()
                if filepath.split(".")[-1].lower() == "bib":
                    temp_db.read_bibtex(filepath)
                else:
                    temp_db.read_yaml(filepath)
                self._print(f"Loaded {temp_db.size()} new entries")
                self._print(f"Have {self.database.size()} existing entries")
                for entry in temp_db.entries():
                    try:
                        self.database.create_entry(entry)
                    except KeyError:
                        continue
                self._print(f"Merged to {self.database.size()} total entries")
        self._print(f"Will write {self.database.size()} entries to {filepath}")
        if self._user_continue():
            if filepath.split(".")[-1].lower() == "bib":
                self.database.write_bibtex(filepath)
            else:
                self.database.write_yaml(filepath)
            self.database.write_yaml(self.cache_file)

    def set_predicate(self, pred_str):
        """ Parses the predicate string and raises errors if illegal.

        Args:
            pred_str (str): The predicate string to parse.

        """

        single_preds = re.compile(
            r'(\w+)\s*'
            r'(==|!=|<|<=|>|>=)'
            r'\s*([\w\s]+)'
        )
        list_preds = re.compile(
            r'([\w\s]+\w)\s*'
            r'in'
            r'\s*(\w+)'
        )
        if m := single_preds.match(pred_str):
            if not hasattr(BibEntry, f"get_{m.group(1)}"):
                raise AttributeError(f"attribute '{m.group(1)}' is not valid")
            self.pred_str = (f'str(x.get_{m.group(1)}()) {m.group(2)}'
                             f' "{m.group(3)}"')
        elif m := list_preds.match(pred_str):
            if not hasattr(BibEntry, f"get_{m.group(2)}"):
                raise AttributeError(f"attribute '{m.group(2)}' is not valid")
            self.pred_str = f'"{m.group(1)}" in str(x.get_{m.group(2)}())'
        else:
            raise ValueError(
                f"Illegal predicate: {pred_str}. "
                "Hint: use one of the following ops in the predicate: "
                "== , != , < , <= , > , >=, in"
            )

    def show(self, entry_key=None):
        """ Display the current contents of the cache. """

        if entry_key is not None:
            self._print(self.database.read_entry(entry_key))
        elif self.pred_str is None:
            for entry in self.database.entries():
                self._print(entry)
        else:
            for entry in self.database.entries(self._predicate):
                self._print(entry)

    def update_entry(self, entry_key, update_field, update_data):
        """ Modify a specific field of an existing entry.

        Args:
            entry_key (str): The key of the entry to modify.
            update_field (str): The field of the entry_key to modify.
            update_data (any): The new value to assign to the update key, which
                must match the type requirement for the update_field.

        """

        if not self.database.contains(entry_key):
            raise KeyError(f"{entry_key} is not in the current cache")
        self._print(f"Will update: {entry_key}")
        self._print(f"Old value: {self.database.read_entry(entry_key)}")
        self.database.update_entry(entry_key, update_field, update_data)
        self._print(f"New value: {self.database.read_entry(entry_key)}")
        if self._user_continue():
            self.database.write_yaml(self.cache_file)

    def _predicate(self, x):
        """ Helper function that executes the predicate on a bib entry

        Args:
            x (BibEntry): The entry on which the predicate is executed.

        """

        return eval(self.pred_str)

    def _print(self, message):
        """ Helper function that prints information when verbose """

        if self.verbose:
            print(message)

    def _user_continue(self):
        """ Helper function that checks with user to proceed.

        Returns:
            bool: True if the user elects to proceed, False otherwise.

        """

        if self.force:
            return True
        response = input("Continue? (y/n): ")
        if len(response) > 0 and response[0].lower() == "y":
            return True
        else:
            self._print("Aborting.")
            return False
