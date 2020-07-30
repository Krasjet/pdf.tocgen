"""Reading and writing table of contents from/to a pdf"""

from typing import List
from fitz import Document
from fitzutils import ToCEntry


def write_toc(doc: Document, toc: List[ToCEntry]):
    """Write table of contents to a document"""
    fitz_toc = list(map(lambda e: e.to_fitz_entry(), toc))
    doc.setToC(fitz_toc)


def read_toc(doc: Document) -> List[ToCEntry]:
    """Read table of contents from a document"""
    return [ToCEntry(*entry) for entry in doc.getToC()]
