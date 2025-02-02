from bibmgr.bib_entry import BibEntry
from bibmgr.bib_parser import BibParser


class DictDatabase:

    __slots__ = [
        'bib_parser',
        'info'
    ]

    def __init__(self):
        """ Constructor for the database manager. """

        self.bib_parser = BibParser()
        self.info = {}

    def create_entry(self, entry):
        """ Create a new entry in the internal database using the default key.

        Args:
            entry (BibEntry): The bibliography entry to add -- the key is
                generated automatically from the entry.

        Raises:
            TypeError: If entry is not a BibEntry object.

            RuntimeError: If a key collision occurs.

        """

        if not isinstance(entry, BibEntry):
            raise TypeError(f"expected a BibEntry object, got: {type(entry)}")
        key = entry.get_key()
        if self.contains(key):
            raise KeyError(f"duplicate key '{key}' requested")
        else:
            self.info[key] = entry

    def read_entry(self, entry_key):
        """ Read an existing entry from the internal database.

        Args:
            entry_key (str): The key of the entry to read.

        Returns:
            BibEntry: The entry stored under the entry_key.

        Raises:
            RuntimeError: If the entry_key cannot be found.

        """

        if not self.contains(entry_key):
            raise KeyError(f"no key '{entry_key}' in current database")
        return self.info[entry_key]

    def update_entry(self, entry_key, update_field, update_value):
        """ Update an existing entry in the internal database.

        Also fixes the entry key if needed.

        Args:
            entry_key (str): The key of the entry to update.

            update_field (str): The field to update in that entry.

            update_value (str or int): The new value for that entry.

        Raises:
            RuntimeError: If the entry_key cannot be found.

        """

        if not self.contains(entry_key):
            raise KeyError(f"no key '{entry_key}' in current database")
        self.bib_parser.next_item = self.info[entry_key]
        self.bib_parser.parse_line(update_field, update_value)
        if self.bib_parser.next_item.get_key() != entry_key:
            self.create_entry(self.delete_entry(entry_key))

    def delete_entry(self, entry_key):
        """ Delete an existing entry from the internal database.

        Args:
            entry_key (str): The key of the entry to delete.

        Returns:
            BibEntry: The deleted entry.

        Raises:
            RuntimeError: If the entry_key cannot be found.

        """

        if not self.contains(entry_key):
            raise KeyError(f"no key '{entry_key}' in current database")
        return self.info.pop(entry_key)

    def entries(self, predicate=None):
        """ Iterate over the entries in the current database and yield them.

        Args:
            predicate (func, optional): Only yields the entries that satisfy
                the predicate. When omitted, all entries are yielded.

        Yields:
            BibEntry: The entries from the internal database.

        Raises:
            TypeError: If the predicate is not a valid function.

        """

        if predicate is not None:
            if not callable(predicate):
                raise TypeError(f"predicate '{predicate}' is not callable")
            for key in self.info:
                if predicate(self.info[key]):
                    yield self.info[key]
        else:
            for key in self.info:
                yield self.info[key]

    def keys(self, predicate=None):
        """ Iterate over the keys in the current database and yield them.

        Args:
            predicate (func, optional): Only yields the keys whose entries
                satisfy the predicate. When omitted, all keys are yielded.

        Yields:
            str: The key for a bib entry in the internal database.

        Raises:
            TypeError: If the predicate is not a valid function.

        """

        if predicate is not None:
            if not callable(predicate):
                raise TypeError(f"predicate '{predicate}' is not callable")
            for key in self.info:
                if predicate(self.info[key]):
                    yield key
        else:
            for key in self.info:
                yield key

    def contains(self, key):
        """ Check the internal database for the given key.

        Args:
            key (str): The key to check for.

        Returns:
            bool: True if found, False otherwise.

        """

        return key in self.info

    def size(self):
        """ Get the size of the current database.

        Returns:
            int: The number of items in the current database.

        """

        return len(self.info)
