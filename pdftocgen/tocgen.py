import io
import csv

from fitz import Document
from typing import List
from fitzutils import ToCEntry, get_pages
from multiprocessing import Pool
from itertools import repeat, chain
from .filter import ToCFilter, extract_toc


def gen_toc(doc: Document, recipe: dict) -> List[ToCEntry]:
    """Generate the table of content for a document from recipe

    Argument
      doc: a pdf document
      recipe: the recipe used to generate the toc
    Returns
      a list of ToC entries
    """
    fltr_dicts = recipe.get('filter', [])

    if len(fltr_dicts) == 0:
        raise ValueError("no filter found")

    filters = [ToCFilter(fltr) for fltr in fltr_dicts]
    pages = get_pages(doc)

    with Pool() as pool:
        result = chain.from_iterable(
            pool.starmap(extract_toc, zip(repeat(pages), filters))
        )
        return sorted(result, key=ToCEntry.key)


def dump_toc(entries: List[ToCEntry]) -> str:
    """Dump table of contents as a CSV dialect

    We will use indentations to represent the level of each entry, except that,
    everything should be similar to the normal CSV.

    Argument
      entries: a list of ToC entries
    Returns
      a multiline string
    """
    with io.StringIO(newline='\n') as out:
        writer = csv.writer(out, lineterminator='\n',
                            delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        for entry in entries:
            out.write((entry.level - 1) * '    ')
            writer.writerow([entry.title, entry.pagenum])
        return out.getvalue()


def pprint_toc(entries: List[ToCEntry]) -> str:
    """Pretty print table of contents

    Argument
      entries: a list of ToC entries
    Returns
      a multiline string
    """
    return '\n'.join([
        f"{(entry.level - 1) * '    '}{entry.title} ··· {entry.pagenum}"
        for entry in entries
    ])
