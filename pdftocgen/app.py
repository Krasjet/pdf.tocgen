"""The executable of pdftocgen"""

import argparse
import toml
import sys

from argparse import Namespace
from fitzutils import open_pdf
from .tocgen import gen_toc, dump_toc, pprint_toc


def getargs() -> Namespace:
    """parse commandline arguments"""

    app_desc = "pdftocgen: generate pdf table of contents from a recipe file."
    parser = argparse.ArgumentParser(description=app_desc)

    parser.add_argument('fname',
                        metavar='doc.pdf',
                        help="path to the input pdf document")
    parser.add_argument('recipe',
                        metavar='recipe.toml',
                        help="path to the recipe file")
    parser.add_argument('-r', '--readable',
                        action='store_true',
                        help="print the toc in a readable format")
    parser.add_argument('-g', '--debug',
                        action='store_true',
                        help="enable debug mode")

    return parser.parse_args()


def main():
    args = getargs()
    try:
        with open(args.recipe, "r") as recipe_file:
            recipe = toml.load(recipe_file)
            with open_pdf(args.fname) as doc:
                toc = gen_toc(doc, recipe)
                # print(dump_toc(gen_toc(doc, recipe)))
                if args.readable:
                    print(pprint_toc(toc))
                else:
                    print(dump_toc(toc), end="")
    except ValueError as e:
        if args.debug:
            raise e
        print("error:", e)
    except IOError as e:
        if args.debug:
            raise e
        print("error: unable to open file", file=sys.stderr)
        print(e, file=sys.stderr)
