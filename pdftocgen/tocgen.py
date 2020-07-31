from fitz import Document
from typing import List
from fitzutils import ToCEntry, get_pages
from multiprocessing import Pool
from itertools import repeat, chain
# from .filter import ToCFilter
from .recipe import extract_toc, Recipe


def gen_toc(doc: Document, recipe_dict: dict) -> List[ToCEntry]:
    """Generate the table of content for a document from recipe

    Argument
      doc: a pdf document
      recipe_dict: the recipe dictionary used to generate the toc
    Returns
      a list of ToC entries
    """
    recipe = Recipe(recipe_dict)
    pages = get_pages(doc)

    # TODO split pages array then distribute to multiple processors
    return extract_toc(pages, 1, recipe)

    # with Pool() as pool:
    #     result = chain.from_iterable(
    #         pool.starmap(extract_toc, zip(repeat(pages), filters))
    #     )
    #     return result
