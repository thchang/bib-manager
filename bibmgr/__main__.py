import argparse
import os

from bibmgr.cli import DatabaseCLI


def parse_args():
    """ Get the CL args."""

    parser = argparse.ArgumentParser(description="Database CLI Tool")
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new entry to the current cache"
    )
    clear_parser = subparsers.add_parser(
        "clear",
        help="Clear all entries from the current cache"
    )
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a single entry from the current cache"
    )
    filter_parser = subparsers.add_parser(
        "filter",
        help="Filter the current cache to get entries that satisfy a predicate"
    )
    load_parser = subparsers.add_parser(
        "load",
        help="Load another database of bib entries into the cache"
    )
    save_parser = subparsers.add_parser(
        "save",
        help="Save the current set of bib entries to a file"
    )
    show_parser = subparsers.add_parser(
        "show",
        help="Show current set of bib entries"
    )
    tag_parser = subparsers.add_parser(
        "tag",
        help="Add a specific tag or keyword to any/all items in the cache"
    )
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing bib entry"
    )
    add_parser.add_argument(
        "entry_data",
        type=str,
        help="Data for the new entry (as a string)"
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
        if args.predicate is not None:
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
        bibdb.update_entry(args.key, args.value)
    else:
        print(f"Command '{args.command}' not recognized.")
        print("For help, use 'bibmgr --help'")


if __name__ == "__main__":
    args = parse_args()
    try:
        run(args)
    except Exception as e:
        print(e)
