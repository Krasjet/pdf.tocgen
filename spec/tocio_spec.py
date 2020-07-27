import os
import io
import fitz

from mamba import description, it, before
from fitzutils import ToCEntry
from pdftocio.tocio import read_toc, write_toc

dirpath = os.path.dirname(os.path.abspath(__file__))

level2 = os.path.join(dirpath, "files/level2.pdf")
hastoc = os.path.join(dirpath, "files/hastoc.pdf")

with description("read_toc") as self:
    with before.all:
        self.doc = fitz.open(level2)
        self.reference = fitz.open(hastoc)
        self.expect = [
            ToCEntry(level=1, title='Section One', pagenum=1),
            ToCEntry(level=1, title='Section Two', pagenum=1),
            ToCEntry(level=2, title='Subsection Two.One', pagenum=2),
            ToCEntry(level=1,
                     title='Section Three, with looong loooong looong title',
                     pagenum=3),
            ToCEntry(level=2,
                     title='Subsection Three.One, '
                     'with even loooooooooooonger title, and probably even more',
                     pagenum=3),
            ToCEntry(level=2, title='Subsection Three.Two',
                     pagenum=4),
            ToCEntry(level=2, title='Subsection Three.Three',
                     pagenum=5),
            ToCEntry(level=1, title='The End', pagenum=5)
        ]

    with it("reads pdf toc correctly"):
        assert self.expect == read_toc(self.reference)

    with it("makes (read_toc -> write_toc -> read_toc) an identity operation"):
        toc = read_toc(self.reference)
        write_toc(self.doc, toc)
        assert read_toc(self.doc) == self.expect

with description("write_toc") as self:
    with before.all:
        self.doc = fitz.open(level2)
        self.reference = fitz.open(hastoc)
        self.toc = [
            ToCEntry(level=1, title='Section One', pagenum=1),
            ToCEntry(level=1, title='Section Two', pagenum=1),
            ToCEntry(level=2, title='Subsection Two.One', pagenum=2),
            ToCEntry(level=1,
                     title='Section Three, with looong loooong looong title',
                     pagenum=3),
            ToCEntry(level=2,
                     title='Subsection Three.One, '
                     'with even loooooooooooonger title, and probably even more',
                     pagenum=3),
            ToCEntry(level=2, title='Subsection Three.Two',
                     pagenum=4),
            ToCEntry(level=2, title='Subsection Three.Three',
                     pagenum=5),
            ToCEntry(level=1, title='The End', pagenum=5)
        ]

    with it("makes (write_toc -> read_toc) an identity operation"):
        write_toc(self.doc, self.toc)
        assert self.toc == read_toc(self.doc)
