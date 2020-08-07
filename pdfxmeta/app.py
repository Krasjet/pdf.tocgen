"""The executable of pdfxmeta"""

import getopt
import sys
import pdfxmeta

from getopt import GetoptError
from typing import Optional, TextIO
from fitzutils import open_pdf
from textwrap import indent
from pdfxmeta import dump_meta, dump_toml, extract_meta


usage_s = """
usage: pdfxmeta [options] doc.pdf [pattern]
""".strip()

help_s = """
usage: pdfxmeta [options] doc.pdf [pattern]

Extract the metadata for pattern in doc.pdf.

To use this command, first open up the pdf file your favorite pdf reader and
find the text you want to search for. Then use

    $ pdfxmeta -p 1 in.pdf "Subsection One"

to find the metadata, mainly the font attributes and bounding box, of lines
containing the pattern "Subsection One" on page 1. Specifying a page number is
optional but highly recommended, since it greatly reduces the ambiguity of
matches and execution time.

The output of this command can be directly copy-pasted to build a recipe file
for pdftocgen. Alternatively, you could also use the --auto or -a flag to
output a valid heading filter directly

    $ pdfxmeta -p 1 -a 2 in.pdf "Subsection One" >> recipe.toml

where the argument of -a is the level of the heading filter, which in this case
is 2.

arguments
  doc.pdf            path to the input PDF document
  [pattern]          the pattern to search for (python regex). if not given,
                     dump the entire document

options
  -h, --help         show help
  -p, --page=PAGE    specify the page to search for (1-based index)
  -i, --ignore-case  when flag is set, search will be case-insensitive
  -a, --auto=LEVEL   when flag is set, the output would be a valid heading
                     filter of the specified heading level in default
                     settings. it is directly usable by pdftocgen.
  -o, --out=FILE     path to the output file. if this flag is not
                     specified, the default is stdout
  -V, --version      show version number
""".strip()


def print_result(meta: str) -> str:
    """pretty print results in a structured manner"""
    return f"{meta.get('text', '')}:\n{indent(dump_meta(meta), '    ')}"


def main():
    # parse arguments
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "hiVp:a:o:",
            ["help", "ignore-case", "version", "page=", "auto=", "out="]
        )
    except GetoptError as e:
        print(e, file=sys.stderr)
        print(usage_s, file=sys.stderr)
        sys.exit(2)

    ignore_case: bool = False
    page: Optional[int] = None
    auto_level: Optional[int] = None
    out: TextIO = sys.stdout

    for o, a in opts:
        if o in ("-i", "--ignore-case"):
            ignore_case = True
        elif o in ("-p", "--page"):
            page = int(a)
        elif o in ("-a", "--auto"):
            auto_level = int(a)
        elif o in ("-o", "--out"):
            try:
                out = open(a, "w")
            except IOError as e:
                print("error: can't open file for writing", file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
        elif o in ("-V", "--version"):
            print("pdfxmeta", pdfxmeta.__version__, file=sys.stderr)
            sys.exit()
        elif o in ("-h", "--help"):
            print(help_s, file=sys.stderr)
            sys.exit()

    argc = len(args)

    if argc < 1:
        print("error: no input pdf is given", file=sys.stderr)
        print(usage_s, file=sys.stderr)
        sys.exit(1)

    path_in: str = args[0]
    pattern: str = ""

    if argc >= 2:
        pattern = args[1]

    # done parsing arguments

    with open_pdf(path_in) as doc:
        meta = extract_meta(doc, pattern, page, ignore_case)

        # nothing found
        if len(meta) == 0:
            sys.exit(1)

        # should we add \n between each output?
        addnl = not out.isatty()

        if auto_level:
            print('\n'.join(
                [dump_toml(m, auto_level, addnl) for m in meta]
            ), file=out)
        else:
            print('\n'.join(map(print_result, meta)), file=out)
