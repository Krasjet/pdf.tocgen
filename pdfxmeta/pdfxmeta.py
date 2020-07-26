import fitz
from toml.encoder import _dump_str, _dump_float

from fitz import Document, Page, TextPage
from typing import Optional, List, Tuple


def extract_meta( doc: Document
                , needle: str
                , page: Optional[int] = None
                , ign_case: bool = False
                ) -> List[Tuple[str, dict]]:
    """Extract meta for `needle` on `page` in a pdf document

    Arguments
      doc: document from pymupdf
      needle: the text to search for
      page: page number (1-based index), if None is given, search for the
            entire document, but this is highly discouraged.
      ign_case: ignore case?
    """
    result = []

    if page is None:
        pages = doc.pages()
    elif 1 <= page <= doc.pageCount:
        pages = [doc[page-1]]
    else: # page out of range
        return result

    # we could parallelize this, but I don't see a reason
    # to *not* specify a page number
    for p in pages:
        result = result + search_in_page(needle, p, ign_case)

    return result

def search_in_page( needle: str
                  , page: Page
                  , ign_case: bool = False
                  ) -> List[Tuple[str, dict]]:
    """Search for `text` in `page` and extract meta

    Arguments
      needle: the text to search for
      page: page number (1-based index)
      ign_case: ignore case?
    Returns
      a list of (text, meta)
    """
    result = []
    if ign_case:
        needle = needle.casefold()

    page_meta = page.getTextPage().extractDICT()

    # we are using get(key, {}) to bypass any missing key errors
    for blk in page_meta.get('blocks', {}):
        for ln in blk.get('lines', {}):
            for spn in ln.get('spans', {}):
                text = spn.get('text', "")
                if ign_case:
                    text = text.casefold()
                # the current search algorithm is very naive and doesn't handle
                # line breaks and more complex layout. might want to take a
                # look at `page.searchFor`, but the current algorithm should be
                # enough for TeX-generated pdf
                if needle in text:
                    result.append((spn['text'], spn))

    return result

def to_bools(var: int) -> str:
    """Convert int to lowercase bool string"""
    return str(var != 0).lower()

def dump_meta(spn: dict) -> str:
    """Dump the span dict from PyMuPDF to TOML compatible string"""
    result = []

    result.append(f"size = {_dump_float(spn['size'])}")
    result.append(f"color = {spn['color']:#08x}")
    result.append(f"font.name = {_dump_str(spn['font'])}")

    flags = spn['flags']

    result.append(f"font.superscript = {to_bools(flags & 0b00001)}")
    result.append(f"font.italic = {to_bools(flags & 0b00010)}")
    result.append(f"font.serif = {to_bools(flags & 0b00100)}")
    result.append(f"font.monospace = {to_bools(flags & 0b01000)}")
    result.append(f"font.bold = {to_bools(flags & 0b10000)}")

    bbox = spn['bbox']

    result.append(f"bbox.left = {_dump_float(bbox[0])}")
    result.append(f"bbox.top = {_dump_float(bbox[1])}")
    result.append(f"bbox.right = {_dump_float(bbox[2])}")
    result.append(f"bbox.bottom = {_dump_float(bbox[3])}")

    return '\n'.join(result)

