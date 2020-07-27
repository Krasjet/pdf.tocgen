from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, ContextManager

import sys
import fitz


@contextmanager
def open_pdf(path: str,
             exit_on_error: bool = True
             ) -> ContextManager[Optional[fitz.Document]]:
    """A context manager for fitz Document

    This context manager will take care of the error handling when creating a
    fitz Document.

    Arguments
      path: the path of the pdf file
      exit_on_error: if true, exit with error code 1 when error occurs
    """
    try:
        doc = fitz.open(path)
    except:
        # mupdf will print an error message here
        if exit_on_error:
            sys.exit(1)
        else:
            yield None
    else:
        try:
            yield doc
        finally:
            doc.close()

@dataclass
class ToCEntry:
    """A single entry in the table of contents"""
    level: int
    title: str
    pagenum: int
    # vpos == bbox.top, used for sorting
    vpos: float

    def to_fitz_entry(self) -> list:
        return [self.level, self.title, self.pagenum]

