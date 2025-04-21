import re

from .bib_entry import BibEntry


class BibParser:
    """ Class for parsing bibtex entries.

    Methods:
        parse_line(key, value)
        parse_file(fp)
        write_file(entry, fp, comment=False)

    """

    __slots__ = [
        'next_item',
    ]

    def __init__(self):
        """ Constructor for the BibParser class.

        Initializes all slots for the BibParser class.

        """

        self.next_item = None

    def parse_line(self, key, value, overwrite=False):
        """ Parse a (key, value) pair BibTex entry and update the next entry.

        Args:
            key (str): A BibTex key that was extracted by the parser.

            value (int, str, list, dict): The corresponding value that was
                extracted by the parser.

            overwrite (bool, optional): Overwrite any existing entries for
                "updatable" entries such as authors and keywords, when True.
                Defaults to False.

        Raises:
            KeyError: If 'key' is not a supported / recognized BibTex key.

        """

        value = " ".join(value.strip().split())
        if self.next_item is None:
            self.next_item = BibEntry()
        if key.strip().lower() in ['author', 'authors']:
            for author in value.split(" and "):
                names = author.strip().split(",")
                if len(names) <= 1:
                    names = author.strip().split()
                    self.next_item.add_authors(
                        [" ".join(names[:-1]).strip(), names[-1].strip()],
                        reset=overwrite
                    )
                else:
                    self.next_item.add_authors(
                        [" ".join(names[1:]).strip(), names[0].strip()],
                        reset=overwrite
                    )
        elif key.strip().lower() in ['editor', 'editors']:
            for editor in value.split(" and "):
                names = editor.strip().split(",")
                if len(names) <= 1:
                    names = editor.strip().split()
                    self.next_item.add_editors(
                        [" ".join(names[:-1]).strip(), names[-1].strip()],
                        reset=overwrite
                    )
                else:
                    self.next_item.add_editors(
                        [" ".join(names[1:]).strip(), names[0].strip()],
                        reset=overwrite
                    )
        elif key.strip().lower() == 'title':
            self.next_item.set_title(value)
        elif key.strip().lower() == 'year':
            self.next_item.set_year(value)
        elif key.strip().lower() == 'month':
            self.next_item.set_month(value)
        elif key.strip().lower() in ['type', 'howpublished']:
            self.next_item.set_type(value)
        elif key.strip().lower() in ['publisher', 'institution',
                                     'organization', 'school']:
            if (
                self.next_item.get_publisher() is None or
                key.strip().lower() in [
                    'institution', 'organization', 'school'
                ] or
                overwrite
            ):
                self.next_item.set_publisher(value)
        elif key.strip().lower() in ['journal', 'booktitle', 'venue']:
            self.next_item.set_venue(value)
        elif key.strip().lower() in ['volume']:
            self.next_item.set_volume(value)
        elif key.strip().lower() in ['number', 'issue', 'version']:
            self.next_item.set_number(value)
        elif key.strip().lower() in ['articleno']:
            self.next_item.set_articleno(value)
        elif key.strip().lower() in ['pages', 'numpages']:
            pages = [
                pp for pp in
                value.replace('--', '-').replace('–', '-').split('-')
                if pp.strip() != ""
            ]
            self.next_item.set_pages(pages)
        elif key.strip().lower() == 'series':
            self.next_item.set_series(value)
        elif key.strip().lower() == 'edition':
            self.next_item.set_edition(value)
        elif key.strip().lower() == 'chapter':
            self.next_item.set_chapter(value)
        elif key.strip().lower() in ['address', 'location']:
            if (
                self.next_item.get_address() is None or
                key.strip().lower() == 'location' or
                overwrite
            ):
                self.next_item.set_address(value)
        elif key.strip().lower() == 'doi':
            self.next_item.set_doi(value)
        elif key.strip().lower() in ['preprint', 'url']:
            self.next_item.set_url(value)
        elif key.strip().lower() == 'isbn':
            self.next_item.set_isbn(value)
        elif key.strip().lower() == 'issn':
            self.next_item.set_issn(value)
        elif key.strip().lower() in ['git', 'software', 'code']:
            self.next_item.set_git(value)
        elif key.strip().lower() in ['web']:
            self.next_item.set_web(value)
        elif key.strip().lower() == 'note':
            self.next_item.set_note(value)
        elif key.strip().lower() in ['descrip', 'summary']:
            self.next_item.set_descrip(value)
        elif key.strip().lower() in ['keywords', 'tags']:
            for tag in value.strip().split(","):
                self.next_item.add_keyword(tag, reset=overwrite)
        else:
            raise KeyError(f"'{key}' with value '{value}' is not a "
                           "recognized key at this time")

    def parse_file(self, fp):
        """ Iterator that parses a BibTex file and yields the entries.

        Args:
            fp (file object): Reference to an open (readable) BibTex file.

        Yields:
            BibEntry: The next entry in the file.

        Raises:
            ValueError: If a line in the input file could not be parsed.
            This likely indicates an illegal or irregular syntax in the BibTex
            file.

        """

        str_next_item = (
            r'\@(?P<type>\w+){[\w-]+,|'
            r'\%[ ]*(?P<comment>[^\n]+)\n|'
            r'(?P<fullkey>\w+)\s*=\s*(?P<value>'
            r'"(?:\\"|[^"])*"|\w+),?|'
            r'(?P<halfkey>\w+)\s*=\s*{'
        )
        re_next_item = re.compile(str_next_item)

        next_descrip = ""
        pos = 0
        bib_data = ""
        if isinstance(fp, str):
            bib_data = fp
        else:
            bib_data = fp.read()
        while m := re_next_item.search(bib_data, pos):
            if m.group('type'):
                if self.next_item is not None:
                    yield self.next_item
                    self.next_item = None
                self.parse_line('type', m.group('type').strip().lower())
                self.parse_line('descrip', next_descrip.strip())
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
                self.parse_line(m.group('fullkey'), value)
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
                self.parse_line(m.group('halfkey'), bib_data[start:end-1])
                pos = end
            else:
                raise ValueError(f"Unmatched expression: {m}")
        if self.next_item is not None:
            yield self.next_item
            self.next_item = None

    def write_file(self, entry, fp, comment=False):
        """ Write a single entry in a BibTex file.

        Args:
            fp (file object): Reference to an open (writable) BibTex file.

            entry (BibEntry): A bibliography entry to write.

            comment (bool, optional): Print the description field as a comment
                at the top of the bib entry when True. Defaults to False.

        """

        fp.write(entry.to_bib(comment=comment))
        fp.write("\n\n")
