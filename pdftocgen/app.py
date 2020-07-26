"""The executable of pdftocgen"""

import argparse

from argparse import Namespace


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

    return parser.parse_args()


def main():
    args = getargs()
    print(args)
