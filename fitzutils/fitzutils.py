from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, ContextManager, List, Tuple
from fitz import Document

import sys
import fitz
import io
import csv


@contextmanager
def open_pdf(path: str,
             exit_on_error: bool = True
             ) -> ContextManager[Optional[Document]]:
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
    vpos: Optional[float] = None

    @staticmethod
    def key(e) -> Tuple[int, float]:
        """Key used for sorting"""
        return (e.pagenum, 0 if e.vpos is None else e.vpos)

    def to_fitz_entry(self) -> list:
        return ([self.level, self.title, self.pagenum] +
                [self.vpos] * (self.vpos is not None))


def dump_toc(entries: List[ToCEntry], dump_vpos: bool = False) -> str:
    """Dump table of contents as a CSV dialect

    We will use indentations to represent the level of each entry, except that,
    everything should be similar to the normal CSV.

    Argument
      entries: a list of ToC entries
      dump_vpos: if true, the vertical position of a page is also dumped
    Returns
      a multiline string
    """
    with io.StringIO(newline='\n') as out:
        writer = csv.writer(out, lineterminator='\n',
                            delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
        for entry in entries:
            out.write((entry.level - 1) * '    ')
            writer.writerow(
                [entry.title, entry.pagenum] +
                ([entry.vpos] * (dump_vpos and entry.vpos is not None))
            )
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
