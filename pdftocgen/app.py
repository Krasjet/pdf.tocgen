"""The executable of pdftocgen"""

import toml
import sys
import getopt
import pdftocgen

from getopt import GetoptError
from typing import TextIO
from fitzutils import open_pdf, dump_toc, pprint_toc
from .tocgen import gen_toc

usage_s = """
usage: pdftocgen [options] doc.pdf < recipe.toml
""".strip()

help_s = """
usage: pdftocgen [options] doc.pdf < recipe.toml

Generate PDF table of contents from a recipe file.

This command automatically generates a table of contents for doc.pdf based on
the font attributes and position of headings specified in a TOML recipe file.
See [1] for an introduction to recipe files.

To generate the table of contents for a pdf, use input redirection or pipes to
supply a recipe file

    $ pdftocgen in.pdf < recipe.toml

or alternatively use the -r flag

    $ pdftocgen -r recipe.toml in.pdf

The output of this command can be directly piped into pdftocio to generate a
new pdf file using the generated table of contents

    $ pdftocgen -r recipe.toml in.pdf | pdftocio -o out.pdf in.pdf

or you could save the output of this command to a file for further tweaking
using output redirection

    $ pdftocgen -r recipe.toml in.pdf > toc

or the -o flag:

    $ pdftocgen -r recipe.toml -o toc in.pdf

If you only need a readable format of the table of contents, use the -H flag

    $ pdftocgen -r recipe.toml -H in.pdf

This format cannot be parsed by pdftocio, but it is slightly more readable.

arguments
  doc.pdf                   path to the input PDF document

options
  -h, --help                show help
  -r, --recipe=recipe.toml  path to the recipe file. if this flag is not
                            specified, the default is stdin
  -H, --human-readable      print the toc in a readable format
  -v, --vpos                if this flag is set, the vertical position of each
                            heading will be generated in the output
  -o, --out=file            path to the output file. if this flag is not
                            specified, the default is stdout
  -g, --debug               enable debug mode
  -V, --version             show version number

[1]: https://krasjet.com/voice/pdf.tocgen/#step-1-build-a-recipe
""".strip()


def main():
    # parse arguments
    try:
        opts, args = getopt.gnu_getopt(
            sys.argv[1:],
            "hr:Hvo:gV",
            ["help", "recipe=", "human-readable", "vpos", "out=", "debug", "version"]
        )
    except GetoptError as e:
        print(e, file=sys.stderr)
        print(usage_s, file=sys.stderr)
        sys.exit(2)

    recipe_file: TextIO = sys.stdin
    readable: bool = False
    vpos: bool = False
    out: TextIO = sys.stdout
    debug: bool = False

    for o, a in opts:
        if o in ("-H", "--human-readable"):
            readable = True
        elif o in ("-v", "--vpos"):
            vpos = True
        elif o in ("-r", "--recipe"):
            try:
                recipe_file = open(a, "r")
            except IOError as e:
                print("error: can't open file for reading", file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
        elif o in ("-o", "--out"):
            try:
                out = open(a, "w")
            except IOError as e:
                print("error: can't open file for writing", file=sys.stderr)
                print(e, file=sys.stderr)
                sys.exit(1)
        elif o in ("-g", "--debug"):
            debug = True
        elif o in ("-V", "--version"):
            print("pdftocgen", pdftocgen.__version__, file=sys.stderr)
            sys.exit()
        elif o in ("-h", "--help"):
            print(help_s, file=sys.stderr)
            sys.exit()

    if len(args) < 1:
        print("error: no input pdf is given", file=sys.stderr)
        print(usage_s, file=sys.stderr)
        sys.exit(1)

    path_in: str = args[0]
    # done parsing arguments

    try:
        with open_pdf(path_in) as doc:
            recipe = toml.load(recipe_file)
            toc = gen_toc(doc, recipe)
            if readable:
                print(pprint_toc(toc), file=out)
            else:
                print(dump_toc(toc, vpos), end="", file=out)
    except ValueError as e:
        if debug:
            raise e
        print("error:", e, file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        if debug:
            raise e
        print("error: unable to open file", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt as e:
        if debug:
            raise e
        print("error: interrupted", file=sys.stderr)
        sys.exit(1)
