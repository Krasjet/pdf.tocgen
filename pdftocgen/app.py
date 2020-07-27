"""The executable of pdftocgen"""

import argparse
import toml
import sys

from argparse import Namespace
from fitzutils import open_pdf, dump_toc, pprint_toc
from .tocgen import gen_toc


def getargs() -> Namespace:
    """parse commandline arguments"""

    app_desc = "pdftocgen: generate pdf table of contents from a recipe file."
    parser = argparse.ArgumentParser(description=app_desc)

    parser.add_argument('input',
                        metavar='doc.pdf',
                        help="path to the input pdf document")
    parser.add_argument('-r', '--recipe',
                        metavar='recipe.toml',
                        type=argparse.FileType('r'),
                        default='-',
                        help="path to the recipe file, "
                        "if this flag is not specified, "
                        "the default is stdin")
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
                        help="path to the output file. "
                        "if this flag is not specified, "
                        "the default is stdout")
    parser.add_argument('-g', '--debug',
                        action='store_true',
                        help="enable debug mode")

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
        print("error:", e)
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
