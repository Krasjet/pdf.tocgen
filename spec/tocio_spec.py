import os
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
            ToCEntry(level=1, title='Section One', pagenum=1, vpos=234.65998),
            ToCEntry(level=1, title='Section Two', pagenum=1, vpos=562.148),
            ToCEntry(level=2, title='Subsection Two.One', pagenum=2, vpos=449.522),
            ToCEntry(level=1,
                     title='Section Three, with looong loooong looong title',
                     pagenum=3,
                     vpos=330.333),
            ToCEntry(level=2,
                     title='Subsection Three.One, '
                     'with even loooooooooooonger title, and probably even more',
                     pagenum=3,
                     vpos=616.444),
            ToCEntry(level=2, title='Subsection Three.Two',
                     pagenum=4, vpos=509.298),
            ToCEntry(level=2, title='Subsection Three.Three',
                     pagenum=5, vpos=124.802),
            ToCEntry(level=1, title='The End', pagenum=5, vpos=361.387)
        ]

    with it("reads pdf toc correctly"):
        assert self.expect == read_toc(self.reference)

    with it("makes (read_toc -> write_toc -> read_toc) an identity operation (except vpos)"):
        toc = read_toc(self.reference)
        write_toc(self.doc, toc)
        toc2 = read_toc(self.doc)

        assert len(toc2) == len(toc)
        for e1, e2 in zip(toc, toc2):
            assert e1.level == e2.level
            assert e1.title == e2.title
            assert e1.pagenum == e2.pagenum

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

    with it("makes (write_toc -> read_toc) an identity operation (except vpos)"):
        write_toc(self.doc, self.toc)
        toc2 = read_toc(self.doc)

        assert len(toc2) == len(self.toc)
        for e1, e2 in zip(self.toc, toc2):
            assert e1.level == e2.level
            assert e1.title == e2.title
            assert e1.pagenum == e2.pagenum
