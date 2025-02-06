import argparse
import os

from bibmgr.cli import DatabaseCLI


def parse_args():
    """ Get the CL args."""

    parser = argparse.ArgumentParser(
        prog="bibmgr",
        description="Database CLI Tool"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        description="available subcommands",
        help="Use `bibmgr CMD --help` to get more info on CMD"
    )
    add_parser = subparsers.add_parser(
        "add",
        description="Add a new entry to the current cache"
    )
    clear_parser = subparsers.add_parser(
        "clear",
        description="Clear all entries from the current cache"
    )
    delete_parser = subparsers.add_parser(
        "delete",
        description="Delete a single entry from the current cache"
    )
    filter_parser = subparsers.add_parser(
        "filter",
        description="Filter the cache to get entries satisfying a predicate"
    )
    load_parser = subparsers.add_parser(
        "load",
        description="Load another database of bib entries into the cache"
    )
    save_parser = subparsers.add_parser(
        "save",
        description="Save the current set of bib entries to a file"
    )
    show_parser = subparsers.add_parser(
        "show",
        description="Show current set of bib entries"
    )
    tag_parser = subparsers.add_parser(
        "tag",
        description="Add a specific tag/keyword to any/all items in the cache"
    )
    update_parser = subparsers.add_parser(
        "update",
        description="Update an existing bib entry"
    )
    delete_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        required=True,
        type=str,
        help="Key for the entry to delete"
    )
    filter_parser.add_argument(
        "-p", "--predicate",
        dest="predicate",
        required=True,
        type=str,
        help="A predicate resembling a Python boolean expression"
    )
    load_parser.add_argument(
        "-f", "--filename",
        dest="filename",
        type=str,
        help=("Path to the file to load from. "
              "When omitted, defaults to bibmgr_db.yaml or other file in the"
              " 'BIBMGR_DATABASE_SAVE_PATH' environment variable.")
    )
    save_parser.add_argument(
        "-f", "--filename",
        dest="filename",
        type=str,
        help=("Path to the file to save to. "
              "When omitted, defaults to bibmgr_db.yaml or other file in the"
              " 'BIBMGR_DATABASE_SAVE_PATH' environment variable.")
    )
    show_parser.add_argument(
        "-p", "--predicate",
        dest="predicate",
        type=str,
        help="A predicate resembling a Python boolean expression"
    )
    show_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        type=str,
        help="Key for the specific entry to show"
    )
    tag_parser.add_argument(
        "-t", "--tag",
        dest="tag",
        required=True,
        type=str,
        help="The tag or a comma-separated list of tags to add"
    )
    tag_parser.add_argument(
        "-p", "--predicate",
        dest="predicate",
        type=str,
        help="A predicate resembling a Python boolean expression"
    )
    tag_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        type=str,
        help="Key for the specific entry to tag"
    )
    update_parser.add_argument(
        "-k", "--key",
        dest="entry_key",
        required=True,
        type=str,
        help=("A key.field (compouned) for the entry to update, e.g., "
              "to update the 'authors' field of 'chang2020algorithm', use: "
              "'--key=chang2020algorithm.authors'")
    )
    update_parser.add_argument(
        "-v", "--value",
        dest="value",
        required=True,
        type=str,
        help="New value to assign to the entry to update"
    )
    return parser.parse_args()


def run(args):
    """ Run the command for the args given.

    Args:
        args (arg-dict): The args returned by the argparser.

    """

    bibdb = DatabaseCLI()
    if args.command == "add":
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
        print("For help, use 'bibmgr --help'")


if __name__ == "__main__":
    args = parse_args()
    try:
        run(args)
    except Exception as e:
        print(e)
