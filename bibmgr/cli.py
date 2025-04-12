import os
import re

from .bib_entry import BibEntry
from .bib_parser import BibParser
from .database_manager import DatabaseManager


class DatabaseCLI:
    """ A CLI for interacting with a BibMgr Database.

    Methods:
        add_entry(str_rep=None, filename=None)
        autofill(overwrite=False)
        clear()
        delete_entry(entry_key)
        filter()
        load_data(filepath, overwrite=False)
        save_data(filepath, overwrite=False)
        set_predicate(pred_str)
        show(entry_key=None)
        tag_entries(tags, entry_key=None)
        update_entry(compound_key, new_value)

    Private methods:
        _predicate(x)
        _print(message)
        _user_continue()

    The public methods are used to build the bibmgr CLI, defined in
    `__main__.py`.

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

    def add_entry(self, str_rep=None, filename=None):
        """ Add a new entry to the cache.

        Args:
            str_rep (str, optional): A string representation (BibTex syntax) of
                the entry to add. When both this and the filename are blank,
                defaults to prompting user for input.
            filename (path-like, optional): A filepath to a .bib file to load
                the entry(s) from. When both this and the str_rep are blank,
                defaults to prompting user for input.

        """

        parser = BibParser()
        if str_rep is not None:
            self._print(f"Will parse from: {str_rep}")
            for entry in parser.parse_file(str_rep):
                try:
                    self.database.create_entry(entry)
                    self._print(f"Will add: {entry}")
                except KeyError:
                    self._print(
                        f"found duplicate: {entry.get_key()}; skipping..."
                    )
        elif filename is not None:
            self._print(f"Will parse from: {filename}")
            with open(filename, "r") as fp:
                for entry in parser.parse_file(fp):
                    try:
                        self.database.create_entry(entry)
                        self._print(f"Will add: {entry}")
                    except KeyError:
                        self._print(
                            f"found duplicate: {entry.get_key()}; skipping..."
                        )
        else:
            parser.next_item = BibEntry()
            next_val = input("Enter publication type: ")
            valid_types = [
                'article', 'book', 'booklet', 'conference', 'inbook',
                'incollection', 'inproceedings', 'manual', 'mastersthesis',
                'misc', 'phdthesis', 'proceedings', 'techreport', 'unpublished'
            ]
            if next_val not in valid_types:
                self._print("Warning: Publication type is usually one of: ")
                self._print(", ".join(valid_types))
                next_val = input("Re-enter publication type: ")
                while len(next_val.strip()) == 0:
                    next_val = input("Type required. Enter publication type: ")
            parser.parse_line("type", next_val)
            # Attempt to autofill from DOI
            doi = input(f"Enter doi if known (leave blank if none): ")
            if len(doi.strip()) > 0:
                parser.parse_line("doi", doi.strip())
                if parser.next_item.autofill(overwrite=True):
                    self._print(f"Found: {parser.next_item}")
                    if self._user_continue():
                        self.database.write_yaml(self.cache_file)
                        return
            # Attempt to autofill from author, title, and year
            for (next_key, instructions) in [
                ("authors", "Enter authors separated by 'and'"),
                ("title", "Enter publication title"),
                ("year", "Enter publication year")
            ]:
                next_val = input(f"{instructions} (leave blank if none): ")
                if len(next_val.strip()) > 0:
                    parser.parse_line(next_key, next_val)
            if parser.next_item.autofill(overwrite=True):
                self._print(f"Found: {parser.next_item}")
                if self._user_continue():
                    self.database.write_yaml(self.cache_file)
                    return
            # Manually fill remaining fields
            for (next_key, instructions) in [
                # ("authors", "Enter authors separated by 'and'"),
                # ("title", "Enter publication title"),
                # ("year", "Enter publication year")
                ("venue", "Enter journal, conference book, or other venue"),
                ("series", "Enter publisher series"),
                ("volume", "Enter volume number"),
                ("number", "Enter issue number"),
                ("articleno", "Enter article number"),
                ("pages", "Enter pages either first--last or num pages"),
                ("publisher", "Enter publisher name"),
                ("address", "Enter publisher address or conference location"),
                # ("doi", "Enter doi if known"),
                ("url", "Enter official publication url"),
                ("isbn", "Enter publication ISBN"),
                ("web", "Enter any additional authors' website"),
                ("git", "Enter any git repo for the project"),
                ("note", "Enter any publisher's notes"),
                ("descrip", "Enter a short description of this entry"),
                ("tags", "Enter a comma-separated list of keywords"),
            ]:
                next_val = input(f"{instructions} (leave blank if none): ")
                if len(next_val.strip()) > 0:
                    parser.parse_line(next_key, next_val)
            try:
                self.database.create_entry(parser.next_item)
                self._print(f"Will add: {parser.next_item}")
            except KeyError:
                self._print(
                    f"found duplicate: {parser.next_item.get_key()};"
                    "skipping..."
                )
        if self._user_continue():
            self.database.write_yaml(self.cache_file)

    def autofill(self, overwrite=False):
        """ Autofill missing fields for entries in the cache via crossref.

        Args:
            overwrite (bool, optional): Overwrite existing fields with
                results from crossref lookup. Defaults to false.

        """

        self.database.autofill(overwrite)
        self._print(f"autofilled {self.database.size()} entries.\n"
                    "New database:")
        for entry in self.database.entries():
            self._print(entry)
        if self._user_continue():
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
        """ Delete an entry from the cache.

        Args:
            entry_key (str): The key of the entry to delete.

        """

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
            overwrite (bool, optional): Overwrite any existing data in the
                cache with the data stored at filepath when True. Default
                behavior (False) is to merge the current contents stored at
                filepath with the current contents of the cache (keeping data
                in the cache when there is a conflict) while loading.

        """

        if not os.path.exists(filepath):
            raise RuntimeError(f"{filepath} does not exist")
        temp_db = DatabaseManager()
        if str(filepath).split(".")[-1].lower() == "bib":
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
        self._print(f"Will load {temp_db.size()} entries from {filepath}")
        if self._user_continue():
            self.database.write_yaml(self.cache_file)

    def save_data(self, filepath, overwrite=False):
        """ Write all entries in the current cache to a file.

        Args:
            filepath (path-like object): The path to the file to write.
            overwrite (bool, optional): Overwrite any existing data at filepath
                with the contents of the cache when True. Default behavior
                (False) is to merge the current contents stored at filepath
                with the current contents of the cache before saving.

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
        """ Display the current contents of the cache.

        Args:
            entry_key (str, optional): When present, the key of the entry to
                show. Defaults to all items in the cache being shown.

        """

        if entry_key is not None:
            self._print(self.database.read_entry(entry_key))
        elif self.pred_str is None:
            for entry in self.database.entries():
                self._print(entry)
        else:
            for entry in self.database.entries(self._predicate):
                self._print(entry)

    def tag_entries(self, tags, entry_key=None):
        """ Add a comma separated list of tags to any/all items in the cache.

        Args:
            tags (str): A comma separated list of the tags to add.
            entry_key (str, optional): When present, the key of the entry to
                tag. Defaults to all items in the cache being tagged.

        """

        tag_list = tags.strip().split(",")
        if entry_key is not None:
            self.database.read_entry(entry_key).add_keyword(tag_list)
            self._print(f"Will tag {entry_key} with {tag_list}")
        elif self.pred_str is None:
            for entry in self.database.entries():
                entry.add_keyword(tag_list)
                self._print(f"Will tag {entry.get_key()} with {tag_list}")
        else:
            for entry in self.database.entries(self._predicate):
                entry.add_keyword(tag_list)
                self._print(f"Will tag {entry.get_key()} with {tag_list}")
        if self._user_continue():
            self.database.write_yaml(self.cache_file)

    def update_entry(self, compound_key, new_value):
        """ Modify a specific field of an existing entry.

        Args:
            compound_key (str): The entry key followed by field to update, in
                the format "key.field"
            new_value (str): The new value to assign to the update key.

        """

        if len(compound_key.strip().split(".")) != 2:
            raise ValueError(
                "The compounded key should be in the format 'key.field'. "
                f"'{compound_key}' is not valid"
            )
        [entry_key, update_field] = compound_key.strip().split(".")
        if not self.database.contains(entry_key):
            raise KeyError(f"{entry_key} is not in the current cache")
        self._print(f"Will update: {entry_key}")
        self._print(f"Old value: {self.database.read_entry(entry_key)}")
        self.database.update_entry(entry_key, update_field, new_value)
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
        """ Helper function that prints information when verbose.

        Args:
            message (str): The message to print.

        """

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
