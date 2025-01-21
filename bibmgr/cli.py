import argparse
import pathlib
import os

from bibmgr.database_mgr import DatabaseManager

class DatabaseCLI:

    def __init__(self):
        """Initialize the CLI with a Database instance."""

        self.cache_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "bibcache.yaml"
        )
        self.database = DatabaseManager()
        if os.path.exists(cache):
            self.database.read_yaml(cache)

    def show(self):
        """Display the contents of the database."""

        for entry in self.database.entries():
            print(entry)

    def add_entry(self, entry_data):
        """Add a new entry to the database."""

        self.create_entry(entry_data)
        self.database.write_yaml(self.cache_file)

    def load_data(self, filepath):
        """Load a database of existing entries into the cache."""

        if not os.path.exists(filepath):
            raise RuntimeError(f"{filepath} does not exist")
        temp_db = DatabaseManager()
        if filepath.split(".")[-1].lower() == "bib":
            temp_db.read_bibtex(filepath)
        else:
            temp_db.read_yaml(filepath)
        for entry in temp_db.entries():
            try:
                self.create_entry(entry)
            except RuntimeError:
                print(f"found duplicate entry: {entry};\nskipping...")
        self.database.write_yaml(self.cache_file)

    def parse_args(self):
        """Get the CLI application."""

        parser = argparse.ArgumentParser(description="Database CLI Tool")
        subparsers = parser.add_subparsers(dest="command",
                                           help="Available commands")
        # Show contents command
        subparsers.add_parser("show", help="Show contents of the database")
        # Add entry command
        add_parser = subparsers.add_parser("add", help="Add a new entry to the database")
        add_parser.add_argument("entry_data", type=str, help="Data for the new entry (as a string)")

        return parser.parse_args()

    def run(args):

        if args.command == "show":
            self.show_contents()
        elif args.command == "add":
            self.add_entry(args.entry_data)
        else:
            parser.print_help()

if __name__ == "__main__":
    from database import Database  # Replace this with the actual import

    db_file = "database_file.db"  # Replace with the actual file name
    db = Database(db_file)  # Initialize the Database instance
    db.read()  # Load data from the file

    cli = DatabaseCLI(db)
    cli.run()

