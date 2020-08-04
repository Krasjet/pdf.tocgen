"""The executable of pdftocgen"""

import argparse
import toml
import sys
import pdftocgen

from argparse import Namespace
from fitzutils import open_pdf, dump_toc, pprint_toc
from .tocgen import gen_toc
from textwrap import dedent


def getargs() -> Namespace:
    """parse commandline arguments"""

    app_desc = dedent("""
    pdftocgen: generate pdf table of contents from a recipe file.

    This command automatically generates a table of contents for a pdf file
    based on the font attributes and position of headings, which are specified
    in a TOML recipe file. See the README for an introduction to the recipe
    file.

    To generate the table of contents for a pdf, use input redirection or pipes
    to supply the recipe file

        $ pdftocgen in.pdf < recipe.toml

    or alternatively use the -r flag

        $ pdftocgen -r recipe.toml in.pdf

    The output of this command can be directly piped into pdftocio to generate
    a new pdf file using the generated table of contents

        $ pdftocgen -r recipe.toml in.pdf | pdftocio -o out.pdf in.pdf

    or you could save the output of this command to a file for further
    tweaking using output redirection

        $ pdftocgen -r recipe.toml in.pdf > toc

    or the -o flag

        $ pdftocgen -r recipe.toml -o toc in.pdf

    If you only need a readable format of the table of contents, use the -H
    flag

        $ pdftocgen -r recipe.toml -H in.pdf

    This format cannot be parsed by pdftocio, but it is slightly more readable.

    """)
    parser = argparse.ArgumentParser(
        description=app_desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('input',
                        metavar='in.pdf',
                        help="path to the input pdf document")
    parser.add_argument('-r', '--recipe',
                        metavar='recipe.toml',
                        type=argparse.FileType('r'),
                        default='-',
                        help="""path to the recipe file,
                        if this flag is not specified,
                        the default is stdin""")
    parser.add_argument('-H', '--human-readable',
                        action='store_true',
                        help="print the toc in a readable format")
    parser.add_argument('-v', '--vpos',
                        action='store_true',
                        help="if this flag is set, "
                        "the vertical position of each header "
                        "will be generated in the output")
    parser.add_argument('-o', '--out',
                        metavar="file",
                        type=argparse.FileType('w'),
                        default='-',
                        help="""path to the output file.
                        if this flag is not specified,
                        the default is stdout""")
    parser.add_argument('-g', '--debug',
                        action='store_true',
                        help="enable debug mode")
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + pdftocgen.__version__)

    return parser.parse_args()


def main():
    args = getargs()
    try:
        with open_pdf(args.input) as doc:
            recipe = toml.load(args.recipe)
            toc = gen_toc(doc, recipe)
            if args.human_readable:
                print(pprint_toc(toc), file=args.out)
            else:
                print(dump_toc(toc, args.vpos), end="", file=args.out)
    except ValueError as e:
        if args.debug:
            raise e
        print("error:", e, file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        if args.debug:
            raise e
        print("error: unable to open file", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt as e:
        if args.debug:
            raise e
        print("error: interrupted", file=sys.stderr)
        sys.exit(1)
