import re

from bibmgr.bib_entry import BibEntry


class BibParser:
    """ Class for parsing bibtex entries.

    Contains the following public methods:

     - `parse_bib_line(key, value)` parses a single line from a BibTex file;
       resolves key conflicts; and
     - `parse_bib_file(filename)` parses an entire BibTex file.
     - `write_bib_file(filename)` writes an entire BibTex file.

    """

    __slots__ = [
        'next_item',
    ]

    def __init__(self):
        """ Constructor for BibParser class.

        Initializes all slots for the BibParser class.

        """

        self.next_item = None

    def parse_bib_line(self, key, value):
        """ Parse a single line of a bib file and attach the appropriate
        attributes to the next item.

        Args:
            key (str): The key that was extracted by the parser.

            value (int, str, list, dict): The corresponding value that was
                extracted by the parser.

        """

        value = " ".join(value.strip().split())
        if self.next_item is None:
            self.next_item = BibEntry()
        if key.strip().lower() == 'author':
            for author in value.split(" and "):
                names = author.strip().split(",")
                if len(names) <= 1:
                    names = author.strip().split()
                    self.next_item.add_authors(
                        [" ".join(names[:-1]).strip(), names[-1].strip()]
                    )
                else:
                    self.next_item.add_authors(
                        [" ".join(names[1:]).strip(), names[0].strip()]
                    )
        elif key.strip().lower() == 'title':
            self.next_item.set_title(value)
        elif key.strip().lower() == 'year':
            self.next_item.set_year(value)
        elif key.strip().lower() in ['type', 'howpublished']:
            self.next_item.set_type(value)
        elif key.strip().lower() in ['publisher', 'institution',
                                     'organization', 'school']:
            if (
                self.next_item.get_publisher() is None or
                key.strip().lower() in ['institution', 'organization',
                                        'school']
            ):
                self.next_item.set_publisher(value)
        elif key.strip().lower() in ['journal', 'booktitle']:
            self.next_item.set_venue(value)
        elif key.strip().lower() in ['volume']:
            self.next_item.set_volume(value)
        elif key.strip().lower() in ['number']:
            self.next_item.set_number(value)
        elif key.strip().lower() in ['articleno']:
            self.next_item.set_articleno(value)
        elif key.strip().lower() in ['pages', 'numpages']:
            pages = [pp for pp in value.replace('--', '-').split('-')
                     if pp.strip() != ""]
            self.next_item.set_pages(pages)
        elif key.strip().lower() == 'series':
            self.next_item.set_series(value)
        elif key.strip().lower() in ['address', 'location']:
            if (
                self.next_item.get_address() is None or
                key.strip().lower() == 'location'
            ):
                self.next_item.set_address(value)
        elif key.strip().lower() == 'doi':
            self.next_item.set_doi(value)
        elif key.strip().lower() == 'url':
            self.next_item.set_url(value)
        elif key.strip().lower() == 'isbn':
            self.next_item.set_isbn(value)
        elif key.strip().lower() == 'git':
            self.next_item.set_git(value)
        elif key.strip().lower() == 'web':
            self.next_item.set_web(value)
        elif key.strip().lower() == 'note':
            self.next_item.set_note(value)
        elif key.strip().lower() in ['descrip', 'summary']:
            self.next_item.set_descrip(value)
        elif key.strip().lower() == 'keywords':
            for tag in value.strip().split(","):
                self.next_item.add_keyword(tag)
        else:
            raise ValueError(f"'{key}' with value '{value}' is not a "
                             "recognized key at this time")

    def parse_bib_file(self, filename):
        """ Iterator that parses a .bib file and yields the entries.

        Args:
            filename (str, path-like object): The path to the file to parse.

        Yields:
            BibEntry: The next entry in the file.

        """

        str_next_item = (
            r'\@(?P<type>\w+){[\w-]+,|'
            r'\%[ ]*(?P<comment>[^\n]+)\n|'
            r'(?P<fullkey>\w+)\s*=\s*(?P<value>'
            r'"(?:\\"|[^"])*"|\w+),?|'
            r'(?P<halfkey>\w+)\s*=\s*{'
        )
        re_next_item = re.compile(str_next_item)

        with open(filename, "r") as fp:
            bib_data = fp.read()

        next_descrip = ""
        pos = 0

        while m := re_next_item.search(bib_data, pos):
            if m.group('type'):
                if self.next_item is not None:
                    yield self.next_item
                    self.next_item = None
                self.parse_bib_line('type', m.group('type').strip())
                self.parse_bib_line('descrip', next_descrip.strip())
                next_descrip = ""
                pos = m.end()
            elif m.group('comment'):
                next_descrip = " ".join([next_descrip, m.group('comment')])
                pos = m.end()
            elif m.group('fullkey') and m.group('value'):
                # Drop the opening/closing quotes from the match
                if m.group('value')[0] == '"' and m.group('value')[-1] == '"':
                    value = m.group('value')[1:-1]
                else:
                    value = m.group('value')
                self.parse_bib_line(m.group('fullkey'), value)
                pos = m.end()
            elif m.group('halfkey'):
                # Parse nested braces manually
                start = m.end()
                brace_count = 1
                end = start
                while brace_count > 0 and end < len(bib_data):
                    if bib_data[end] == '{':
                        brace_count += 1
                    elif bib_data[end] == '}':
                        brace_count -= 1
                    end += 1
                self.parse_bib_line(m.group('halfkey'), bib_data[start:end-1])
                pos = end
            else:
                raise RuntimeError(f"Unmatched expression: {m}")
        if self.next_item is not None:
            yield self.next_item
            self.next_item = None

    def write_bib_file(self, filename, info):
        """ Write an entire BibTex (.bib) file from the internal database.

        Args:
            filename (str or path-like object): The path to the file to write.
            info (dict[BibEntry]): A dictionary of bibliography entries.

        """

        with open(filename, "w") as fp:
            for key in info:
                self.next_item = BibEntry(info[key])
                fp.write(self.next_item.to_bib())
                fp.write("\n\n")
