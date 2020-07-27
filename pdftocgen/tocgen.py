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
