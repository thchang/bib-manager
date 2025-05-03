import argparse
from importlib.metadata import version
import os
import pathlib

from .cli import DatabaseCLI


def parse_args():
    """ Helper for parsing the command line args. """

    parser = argparse.ArgumentParser(
        prog="bibmgr",
        description=(
            "CLI tool for managing, annotating, & searching bib entries"
        ),
        usage="%(prog)s",
    )
    subparsers = parser.add_subparsers(
        dest="command",
        description="The bibmgr command to execute",
        help="""Execute a single command with the bibmgr program.

            With each command, bibliography entries are written to a cache file
            stored in the install dir.

            Run one of the following commands to manipulate the entries in the
            cache:

            add, autofill, clear, delete, filter, load, save, show, tag, and
            update.

            Since commands are executed upon the cache, the save command should
            be used to "commit" entries to a permanent save file, which can be
            specified or configured via environment variable.

            Use `bibmgr --help` for a list of valid values for CMD.

            Use `bibmgr CMD --help` to get more info on a specific CMD.
        """,
        metavar="CMD"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=version("bibmgr")
    )
    add_parser = subparsers.add_parser(
        "add",
        description="Adds a new entry to the current cache"
    )
    autofill_parser = subparsers.add_parser(
        "autofill",
        description="Autofills missing fields for all entries in the cache"
    )
    clear_parser = subparsers.add_parser(
        "clear",
        description="Clears all entries from the current cache"
    )
    delete_parser = subparsers.add_parser(
        "delete",
        description="Deletes a single entry from the current cache"
    )
    filter_parser = subparsers.add_parser(
        "filter",
        description="Filters the cache to get entries satisfying a predicate"
    )
    load_parser = subparsers.add_parser(
        "load",
        description="Loads another database of bib entries into the cache"
    )
    save_parser = subparsers.add_parser(
        "save",
        description="Saves the current set of bib entries to a file"
    )
    show_parser = subparsers.add_parser(
        "show",
        description="Shows current set of bib entries"
    )
    tag_parser = subparsers.add_parser(
        "tag",
        description="Adds a specific tag/keyword to any/all items in the cache"
    )
    update_parser = subparsers.add_parser(
        "update",
        description="Updates an existing bib entry"
    )
    add_parser.add_argument(
        "-v", "--value",
        dest="value",
        type=str,
        help="""VALUE is either a BibTex-style string representing the entry
            to add or the path to a .bib file to add entries from.

            When VALUE is omitted, the user is prompted to input information
            about the new entry manually.
        """,
        metavar="VALUE"
    )
    autofill_parser.add_argument(
        "-o", "--overwrite",
        dest="overwrite",
        action="store_true",
        help="""Overwrite existing fields in the cache with values found on
            Crossref.
        """,
    )
    delete_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        required=True,
        type=str,
        help="Any BibEntry whose key is KEY will be deleted from the cache",
        metavar="KEY"
    )
    filter_parser.add_argument(
        "-p", "--predicate",
        dest="predicate",
        required=True,
        type=str,
        help="""Filter the cache to only entries that satisfy PRED.

            PRED should resemble a Python boolean expression.
        """,
        metavar="PRED"
    )
    load_parser.add_argument(
        "-f", "--filename",
        dest="filename",
        type=pathlib.Path,
        help="""FILE is an existing .yaml or .bib file to load from.

              If the cache is not empty, the contents of FILE will be merged
              with those in the cache with a preference for keeping the
              current contents of the cache whenever there is a conflict.

              Use the --overwrite flag to clear the cache when loading.

              When omitted, defaults to load from 'BIBMGR_DATABASE_SAVE_PATH'
              environment variable or './bibmgr_db.yaml' if unset.
        """,
        metavar="FILE"
    )
    load_parser.add_argument(
        "-o", "--overwrite",
        dest="overwrite",
        action="store_true",
        help="Set to discard the current contents of the cache when loading."
    )
    load_parser.add_argument(
        "-m", "--merge",
        dest="merge",
        action="store_true",
        help="Set to resolve conflicts by merging tags for duplicate entries."
    )
    load_parser.add_argument(
        "-u", "--update",
        dest="update",
        action="store_true",
        help="""Set to load and update entries that are already in the cache.

        When omitted, the default behavior is to load all entries in the file
        and append them to the cache or skip them if they are already in the
        cache (unless the --overwrite flag is set, in which case loaded entries
        are favored over existing entries).

        When the --update flag is set, only entries that are already in the
        cache are loaded and the behavior is to update these entries by
        overwriting them with contents from the file.

        """
    )
    save_parser.add_argument(
        "-f", "--filename",
        dest="filename",
        type=pathlib.Path,
        help="""FILE is the name of a .yaml or .bib file to save to.

              If FILE already exists, the contents will be merged with those in
              the cache before saving with a preference for keeping the
              contents of the cache whenever there is a conflict.

              Use the --overwrite flag to delete the current contents of FILE
              when saving.

              When omitted, defaults to save to 'BIBMGR_DATABASE_SAVE_PATH'
              environment variable or './bibmgr_db.yaml' if unset.
        """,
        metavar="FILE"
    )
    save_parser.add_argument(
        "-o", "--overwrite",
        dest="overwrite",
        action="store_true",
        help="Set to discard the current contents of FILE when saving."
    )
    show_parser.add_argument(
        "-p", "--predicate",
        dest="predicate",
        type=str,
        help="""Show only the entries in the cache that satisfy PRED.

            PRED should resemble a Python boolean expression.
        """,
        metavar="PRED"
    )
    show_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        type=str,
        help="Show only the entry whose key is KEY",
        metavar="KEY"
    )
    tag_parser.add_argument(
        "-t", "--tag",
        dest="tags",
        required=True,
        type=str,
        help="""A comma-separated list of tags that will be added to the
        contents of the cache
        """,
        metavar="TAG"
    )
    tag_parser.add_argument(
        "-p", "--predicate",
        dest="predicate",
        type=str,
        help="""Tag only the entries in the cache that satisfy PRED.

            PRED should resemble a Python boolean expression.
        """,
        metavar="PRED"
    )
    tag_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        type=str,
        help="Tag only one entry in the cache whose key is KEY.",
        metavar="KEY"
    )
    update_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        required=True,
        type=str,
        help="""A compouned key of the form KEY="key.field" specifying both the
        key for the entry to update and the field to update.

        Example:
            To update the 'authors' field of 'chang2020algorithm', use:
            '--key=chang2020algorithm.authors'
        """,
        metavar="KEY"
    )
    update_parser.add_argument(
        "-v", "--value",
        dest="value",
        required=True,
        type=str,
        help="Will assign VALUE to assign to the field at the compound KEY."
    )
    for subparser in [
        add_parser, autofill_parser, clear_parser, delete_parser,
        filter_parser, load_parser, save_parser, tag_parser, update_parser,
        # show_parser,  # quiet / force is not relevant for this command
    ]:
        subparser.add_argument(
            "--force",
            dest="force",
            action="store_true",
            help="Force the results of the command without checking first."
        )
        subparser.add_argument(
            "-q", "--quiet",
            dest="quiet",
            action="store_true",
            help="Quiet any diagnostics/logs printed by the command."
        )
    return parser.parse_args()


def run(args):
    """ Run the command for the args given.

    Args:
        args (arg-dict): The args returned by the argparser.

    """

    bibdb = DatabaseCLI()
    if args.command in [
        "add", "autofill", "clear", "delete", "filter", "load", "save", "tag",
        "update",  # "show",  # quiet / force is not relevant for this command
    ]:
        if args.force is not None:
            bibdb.force = args.force
        if args.quiet is not None:
            bibdb.verbose = not args.quiet
    if args.command == "add":
        if args.value is not None:
            path = None
            try:
                path = pathlib.Path(args.value)
            except Exception:
                path = ""
            if os.path.exists(path):
                bibdb.add_entry(filename=args.value)
            else:
                bibdb.add_entry(str_rep=args.value)
        else:
            bibdb.add_entry()
    elif args.command == "autofill":
        bibdb.autofill(args.overwrite)
    elif args.command == "clear":
        bibdb.clear()
    elif args.command == "delete":
        bibdb.delete_entry(args.entry_key)
    elif args.command == "filter":
        bibdb.set_predicate(args.predicate)
        bibdb.filter()
    elif args.command == "load":
        filepath = None
        if args.filename is None:
            filepath = os.path.join(
                os.environ.get('BIBMGR_DATABASE_SAVE_PATH', os.getcwd()),
                "bibmgr_db.yaml"
            )
        else:
            filepath = args.filename
        if args.update:
            bibdb.update(filepath)
        else:
            bibdb.load_data(filepath, args.overwrite, args.merge)
    elif args.command == "save":
        if args.filename is None:
            filepath = os.path.join(
                os.environ.get('BIBMGR_DATABASE_SAVE_PATH', os.getcwd()),
                "bibmgr_db.yaml"
            )
            bibdb.save_data(filepath, args.overwrite)
        else:
            bibdb.save_data(args.filename, args.overwrite, comment=True)
    elif args.command == "show":
        if args.predicate is not None:
            bibdb.set_predicate(args.predicate)
        if args.entry_key is None:
            bibdb.show()
        else:
            bibdb.show(args.entry_key)
    elif args.command == "tag":
        if args.predicate is not None:
            bibdb.set_predicate(args.predicate)
        if args.entry_key is None:
            bibdb.tag_entries(args.tags)
        else:
            bibdb.tag_entries(args.tags, args.entry_key)
    elif args.command == "update":
        bibdb.update_entry(args.entry_key, args.value)
    else:
        print(f"Command '{args.command}' not recognized.")
        print("\nFor help, use 'bibmgr --help'")


def main():
    """ Driver for the main program. """

    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
