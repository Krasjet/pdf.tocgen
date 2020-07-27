import os
import io

from mamba import description, it, before
from fitzutils import *
from pdftocio.tocparser import parse_toc

dirpath = os.path.dirname(os.path.abspath(__file__))

valid_file = os.path.join(dirpath, "files/level2.pdf")
invalid_file = os.path.join(dirpath, "files/nothing.pdf")

with description("parse_toc") as self:
    with before.all:
        self.toc = [
            ToCEntry(level=1, title="title1", pagenum=1, vpos=100.0),
            ToCEntry(level=2, title="title2", pagenum=1, vpos=150.0),
            ToCEntry(level=3, title="title3", pagenum=2, vpos=90.0),
            ToCEntry(level=2, title="title4", pagenum=2, vpos=150.0),
            ToCEntry(level=2, title="title5", pagenum=3, vpos=0.0),
            ToCEntry(level=1, title="title6", pagenum=5, vpos=200.0)
        ]

        self.toc_novpos = [
            ToCEntry(level=1, title="title1", pagenum=1),
            ToCEntry(level=2, title="title2", pagenum=1),
            ToCEntry(level=3, title="title3", pagenum=2),
            ToCEntry(level=2, title="title4", pagenum=2),
            ToCEntry(level=2, title="title5", pagenum=3),
            ToCEntry(level=1, title="title6", pagenum=5)
        ]

    with it("can recover the result from dump_toc"):
        toc_s = dump_toc(self.toc, True)
        f = io.StringIO(toc_s)
        assert parse_toc(f) == self.toc
        assert parse_toc(f) != self.toc_novpos

        toc_s = dump_toc(self.toc_novpos, False)
        f = io.StringIO(toc_s)
        assert parse_toc(f) == self.toc_novpos
        assert parse_toc(f) != self.toc

    with it("won't print vpos if vpos is False"):
        toc_s = dump_toc(self.toc, False)
        f = io.StringIO(toc_s)
        assert parse_toc(f) == self.toc_novpos
        assert parse_toc(f) != self.toc

    with it("won't print vpos if vpos is missing"):
        toc_s = dump_toc(self.toc_novpos, True)
        f = io.StringIO(toc_s)
        assert parse_toc(f) == self.toc_novpos
        assert parse_toc(f) != self.toc

