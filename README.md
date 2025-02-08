# bibmgr: A command-line bibliography manager

CLI tool for managing, annotating, & searching bib entries.

## Setup and Installation

Clone this project then pip install it from within the base directory.

```
git clone https://github.com/thchang/bib-manager
cd bib-manager && pip install -e .
```

Alternatively, clone and add to the `PYTHONPATH`

```
git clone https://github.com/thchang/bib-manager
cd bib-manager && export PYTHONPATH=`pwd`
```

The following dependencies are needed (will be fetched automatically by pip):

 * `pyyaml`

### Checking Installation

To check the installation, simply run the help function from the command line.

```
bibmgr --help
```

You should see a help message suggesting basic usage.

### Running Tests

This step should not be necessary for most users, but it may be useful to run
the unit tests to ensure proper installation.

To run the unit tests, after cloning install the tests then perform linting
with `flake8`, unit testing with `pytest`, and generate the code coverage with
`coverage report`.

```
cd bibmgr
pip install -e ".[test]"
flake8  # linting
pytest  # testing
coverage report  # generate code coverage
```

The following additional dependencies will be fetched for testing:

 * coverage
 * flake8
 * flake8-pyproject
 * pytest
 * pytest-cov

## Basic Usage

From the command line, run

```
bibmgr CMD [options]
```

where `CMD` is one of the following:

 * `add`,
 * `clear`,
 * `delete`,
 * `filter`,
 * `load`,
 * `save`,
 * `show`,
 * `tag`, or
 * `update`.

This executes a single command with the bibmgr program.

With each command, bibliography entries are written to a cache file stored in
the install dir.

Run various commands to manipulate the contents of this cache.

Use `CMD=add` to create a new entry -- either from a BibTex style string, a .bib
file, or by manually entering data as prompted.

Use `CMD=clear` to clear the current cache.

Use `CMD=delete` to delete a specific entry from the cache.

Use `CMD=filter` to filter entries from the cache according to some predicate.

Use `CMD=load` to merge entries from an existing yaml/bibtex file.

Use `CMD=save` to "commit" changes into an existing yaml/bibtex file.

Use `CMD=show` to view a single entry, multiple entries, or all contents of the
cache.

Use `CMD=tag` to tag a single entry, multiple entries, or all contents of the
cache with a comma-separated list of tags or keywords.

Use `CMD=update` to update one or more entries.

Use `bibmgr --help` for a list of valid values for CMD. Use `bibmgr CMD --help`
to get more info on a specific CMD.

## License

MIT license, see `LICENSE` file.

## Authors

Tyler Chang
