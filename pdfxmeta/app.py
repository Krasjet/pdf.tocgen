"""The executable of pdfxmeta"""

import argparse
import sys
import pdfxmeta

from argparse import Namespace
from fitzutils import open_pdf
from textwrap import indent, dedent
from pdfxmeta import dump_meta, dump_toml, extract_meta


def getargs() -> Namespace:
    """parse commandline arguments"""

    app_desc = dedent("""
    pdfxmeta: extract metadata for a string in a pdf document.

    To use this command, first open up the pdf file your favorite pdf reader
    and find the string you want to search for. Then use

        $ pdfxmeta -p 1 in.pdf "Subsection One"

    to find the metadata, mainly the font attributes and bounding box, of lines
    containing the pattern "Subsection One" on page 1. Specifying a page number
    is optional but highly recommended, since it greatly reduces the ambiguity
    of matches and execution time.

    The output of this command can be directly copy-pasted to build a recipe
    file for pdftocgen. Alternatively, you could also use the --auto or -a flag
    to output a valid heading filter directly

        $ pdfxmeta -p 1 -a 2 in.pdf "Subsection One" >> recipe.toml

    where the argument of -a is the level of the heading filter, which in this
    case is 2.
    """)
    parser = argparse.ArgumentParser(
        description=app_desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input',
                        metavar='in.pdf',
                        help="path to the input pdf file")
    parser.add_argument('pattern',
                        help="the pattern to search for (python regex)")
    parser.add_argument('-p', '--page',
                        type=int,
                        help="""specify the page in which the string occurs
                        (1-based index)""")
    parser.add_argument('-i', '--ignore-case',
                        action='store_true',
                        help="""when flag is set, search will be
                        case-insensitive""")
    parser.add_argument('-a', '--auto',
                        metavar='level',
                        type=int,
                        const=1,
                        nargs='?',
                        help="""when flag is set, the output would be a valid
                        heading filter of the specified level with the most
                        common settings, directly usable by pdftocgen. the
                        default level is 1""")
    parser.add_argument('-o', '--out',
                        metavar="file",
                        type=argparse.FileType('w'),
                        default='-',
                        help="""path to the output file.  if this flag is not
                        specified, the default is stdout""")
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + pdfxmeta.__version__)

    return parser.parse_args()


def print_result(meta: str) -> str:
    """pretty print results in a structured manner"""
    return f"{meta.get('text', '')}:\n{indent(dump_meta(meta), '    ')}"


def main():
    args = getargs()

    with open_pdf(args.input) as doc:
        meta = extract_meta(doc, args.pattern, args.page, args.ignore_case)

        # nothing found
        if len(meta) == 0:
            sys.exit(1)

        # should we add \n between each output?
        addnl = not args.out.isatty()

        if args.auto:
            print('\n'.join(
                [dump_toml(m, args.auto, addnl) for m in meta]
            ), file=args.out)
        else:
            print('\n'.join(map(print_result, meta)), file=args.out)
