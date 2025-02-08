import argparse
import os
import pathlib

from bibmgr.cli import DatabaseCLI


def parse_args():
    """ Helper for parsing the command line args. """

    parser = argparse.ArgumentParser(
        prog="bibmgr",
        description=(
            "CLI tool for managing, annotating, & searching bib entries"
        ),
        usage="%(prog)s [options]",
        help="""Execute a single command with the bibmgr program.

            With each command, bibliography entries are written to a cache file
            stored in the install dir.

            Run various commands to manipulate the contents of this cache.

            Use CMD=save to "commit" changes into an existing yaml/bibtex file.

            Use CMD=load to merge entries from an existing yaml/bibtex file.
        """
    )
    subparsers = parser.add_subparsers(
        dest="command",
        description="The bibmgr command to execute",
        help="""Use `bibmgr --help` for a list of valid values for CMD.

            Use `bibmgr CMD --help` to get more info on a specific CMD.
        """,
        metavar="CMD"
    )
    add_parser = subparsers.add_parser(
        "add",
        description="Adds a new entry to the current cache",
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
        dest=args.overwrite,
        action="store_true",
        type=bool,
        help="Set to discard the current contents of the cache when loading."
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
        dest=args.overwrite,
        action="store_true",
        type=bool,
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
        dest="tag",
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
        add_parser, clear_parser, delete_parser, filter_parser, load_parser,
        save_parser, tag_parser, update_parser,
        # show_parser,  # quiet / force is not relevant for this command
    ]:
        subparser.add_argument(
            "--force",
            dest="force",
            action="store_true",
            type=bool,
            help="Force the results of the command without checking first."
        )
        subparser.add_argument(
            "-q", "--quiet",
            dest="quiet",
            action="store_true",
            type=bool,
            help="Quiet any diagnostics/logs printed by the command."
        )
    return parser.parse_args()


def run(args):
    """ Run the command for the args given.

    Args:
        args (arg-dict): The args returned by the argparser.

    """

    bibdb = DatabaseCLI()
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
            try:
                if os.path.exists(path):
                    bibdb.add_entry(filename=args.value)
                else:
                    bibdb.add_entry(str_rep=args.value)
            except ValueError:
                raise ValueError(
                    f'--value="{args.value}" is not a valid file or bib string'
                )
        else:
            bibdb.add_entry()
    elif args.command == "clear":
        bibdb.clear()
    elif args.command == "delete":
        bibdb.delete_entry(args.entry_key)
    elif args.command == "filter":
        bibdb.set_predicate(args.predicate)
        bibdb.filter()
    elif args.command == "load":
        if args.filename is None:
            filepath = os.environ.get(
                'BIBMGR_DATABASE_SAVE_PATH',
                str(os.path.join(os.getcwd(), "bibmgr_db.yaml"))
            )
            bibdb.load_data(filepath, args.overwrite)
        else:
            bibdb.load_data(args.filename, args.overwrite)
    elif args.command == "save":
        if args.filename is None:
            filepath = os.environ.get(
                'BIBMGR_DATABASE_SAVE_PATH',
                str(os.path.join(os.getcwd(), "bibmgr_db.yaml"))
            )
            bibdb.save_data(filepath, args.overwrite)
        else:
            bibdb.save_data(args.filename, args.overwrite)
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


if __name__ == "__main__":
    args = parse_args()
    try:
        run(args)
    except Exception as e:
        print(e)
