"""The executable of pdfxmeta"""

import pdfxmeta
import fitz
import argparse
import sys

from argparse import Namespace
from typing import List
from fitzutils import open_pdf


def getargs() -> Namespace:
    """parse commandline arguments"""

    app_desc = "pdfxmeta: extract metadata for a string in a pdf document."
    parser = argparse.ArgumentParser(description=app_desc)

    parser.add_argument('fname',
                        metavar='doc.pdf',
                        help="name of the input pdf file")
    parser.add_argument('needle',
                        help="the string to search for")
    parser.add_argument('-p', '--page',
                        action='store',
                        type=int,
                        help="specify the page in which the string occurs (1-based index)")
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help="when flag is set, search will be case-insensitive")

    return parser.parse_args()


def main():
    args = getargs()

    with open_pdf(args.fname) as doc:
        meta = pdfxmeta.extract_meta(doc, args.needle, args.page, args.ignore_case)

        # nothing found
        if len(meta) == 0:
            sys.exit(1)

        for m in meta:
            # TODO print in a readable format
            print(m)

