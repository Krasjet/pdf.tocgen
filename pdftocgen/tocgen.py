from fitz import Document
from typing import List
from fitzutils import ToCEntry
from .recipe import Recipe, extract_toc

def gen_toc(doc: Document, recipe_dict: dict) -> List[ToCEntry]:
    """Generate the table of content for a document from recipe

    Argument
      doc: a pdf document
      recipe_dict: the recipe dictionary used to generate the toc
    Returns
      a list of ToC entries
    """
    return extract_toc(doc, Recipe(recipe_dict))
