"""The executable of pdfxmeta"""

import argparse
import pdfxmeta
import sys

from argparse import Namespace
from fitzutils import open_pdf
from textwrap import indent, dedent


def getargs() -> Namespace:
    """parse commandline arguments"""

    app_desc = dedent("""
    pdfxmeta: extract metadata for a string in a pdf document.

    To use this command, first open up the pdf file your favorite pdf reader
    and find the string you want to search for. Then use

        $ pdfxmeta -p 1 in.pdf "Subsection One"

    to find the metadata, mainly the font attributes and bounding box, of lines
    containing the query "Subsection One" on page 1. Specifying a page number
    is optional but highly recommended, since it greatly reduces the ambiguity
    of matches and execution time.

    The output of this command can be directly copy-pasted to build a recipe
    file for pdftocgen.
    """)
    parser = argparse.ArgumentParser(
        description=app_desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input',
                        metavar='in.pdf',
                        help="path to the input pdf file")
    parser.add_argument('needle',
                        help="the query string to search for")
    parser.add_argument('-p', '--page',
                        type=int,
                        help="""specify the page in which the string
                             occurs (1-based index)""")
    parser.add_argument('-i', '--ignore-case',
                        action='store_true',
                        help="""when flag is set, search will be
                        case-insensitive""")
    parser.add_argument('-o', '--out',
                        metavar="file",
                        type=argparse.FileType('w'),
                        default='-',
                        help="""path to the output file.
                        if this flag is not specified,
                        the default is stdout""")

    return parser.parse_args()


def print_result(text: str, meta: str) -> str:
    """pretty print results in a structured manner"""
    return f"{text}:\n{indent(pdfxmeta.dump_meta(meta), '    ')}"


def uncurry(f):
    """(a -> b -> c) -> (a, b) -> c"""
    def h(args):
        return f(*args)
    return h


def main():
    args = getargs()

    with open_pdf(args.input) as doc:
        meta = pdfxmeta.extract_meta(doc, args.needle,
                                     args.page, args.ignore_case)
        # nothing found
        if len(meta) == 0:
            sys.exit(1)

        print('\n'.join(map(uncurry(print_result), meta)), file=args.out)
