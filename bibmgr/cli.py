import argparse
import os
import re

from bibmgr.bib_entry import BibEntry
from bibmgr.database_mgr import DatabaseManager


class DatabaseCLI:
    """ A CLI for interacting with the BibMgr Database.

    Uses the following helper methods:

     * `add_entry(entry_data)`
     * `delete_entry(entry_key)`
     * `filter(predicate)`
     * `load_data(filepath)`
     * `save_data(filepath)` TBD
     * `show(entry_key, predicate)`
     * `update_entry(entry_key, update_key, update_data)` TBD
     * `parse_args()` TBD
     * `parse_predicate(pred_str)`
     * `predicate(x)`
     * `print_help()`
     * `run(args)` TBD

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

    def add_entry(self, entry_data):
        """ Add a new entry to the cache. """

        new_entry = BibEntry(entry_data)
        print(f"Will add: {new_entry}\n")
        response = input("Continue? (y/n): ")
        if response == "y":
            self.database.create_entry(new_entry)
            self.database.write_yaml(self.cache_file)
        else:
            print("Aborting.")

    def delete_entry(self, entry_key):
        """ Delete an entry from the cache. """

        if self.database.contains(entry_key):
            print(f"Will delete: {self.database.read_entry(entry_key)}\n")
            response = input("Continue? (y/n): ")
            if len(response) > 0:
                response = response[0].lower()
            if response == "y":
                self.delete_entry(entry_key)
                self.database.write_yaml(self.cache_file)
            else:
                print("Aborting.")
        else:
            print(f"{entry_key} not found, aborting.")

    def filter(self):
        """ Filter the current contents of the cache. """

        if self.pred_str is None:
            raise ValueError("No predicate to filter")
        temp_db = DatabaseManager()
        for entry in self.database.entries(self.predicate):
            temp_db.create_entry(entry)
        print(f"{self.database.size() - temp_db.size()} items filtered")
        response = input("Continue? (y/n): ")
        if response == "y":
            self.database = temp_db
            self.database.write_yaml(self.cache_file)
        else:
            print("Aborting.")

    def load_data(self, filepath):
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
        print(f"Will load {temp_db.size()} entries\n")
        response = input("Continue? (y/n): ")
        if response == "y":
            for entry in temp_db.entries():
                try:
                    self.database.create_entry(entry)
                except RuntimeError:
                    print(f"found duplicate entry: {entry};\nskipping...")
            self.database.write_yaml(self.cache_file)
        else:
            print("Aborting.")

    def show(self):
        """ Display the current contents of the cache. """

        if self.pred_str is None:
            for entry in self.database.entries():
                print(entry)
        else:
            for entry in self.database.entries(self.predicate):
                print(entry)

    def parse_args(self):
        """ Get the CL args."""

        parser = argparse.ArgumentParser(description="Database CLI Tool")
        subparsers = parser.add_subparsers(
            dest="command",
            help="Available commands"
        )
        subparsers.add_parser("show", help="Show contents of the database")
        add_parser = subparsers.add_parser(
            "add",
            help="Add a new entry to the database"
        )
        add_parser.add_argument(
            "entry_data",
            type=str,
            help="Data for the new entry (as a string)"
        )
        return parser.parse_args()

    def parse_predicate(self, pred_str):
        """ Parses the predicate string and raises errors if illegal.

        Args:
            pred_str (str): The predicate string to parse.

        """

        legal_preds = re.compile(
            r'(\w+)\s*'
            r'(==|!=|<|<=|>|>=)'
            r'\s*(\w+)'
        )
        if m := legal_preds.match(pred_str):
            self.pred_str = f"get_{m.group(1)}() {m.group(2)} {m.group(3)}"
        else:
            raise RuntimeError(
                f"Illegal predicate: {pred_str}. "
                "Hint: use one of the following ops in the predicate: "
                "== , != , < , <= , > , >="
            )

    def predicate(self, x):
        """ Helper function that executes the predicate on a bib entry

        Args:
            x (BibEntry): The entry on which the predicate is executed.

        """

        return exec(f"{x}.{self.pred_str}")

    def print_help(self, cmd):
        """ Display a help message.

        Args:
            cmd (str or str-like): The command that failed.

        """

        print(f"Command {cmd} not recognized.\nFor help, use bibmgr --help")

    def run(self, args):
        """ Run the command for the args given.

        Args:
            args (arg-dict): The args returned by the argparser.

        """

        if args.command == "show":
            self.show_contents()
        elif args.command == "load":
            self.add_entry(args.entry_data)
        elif args.command == "add":
            self.add_entry(args.entry_data)
        else:
            self.print_help(args.command)


if __name__ == "__main__":

    cli = DatabaseCLI()
    args = cli.parse_args()
    cli.run(args)
