import os
import io

from mamba import description, it, before
from fitzutils import (
    open_pdf,
    ToCEntry,
    dump_toc
)
from pdftocio.tocparser import parse_toc

dirpath = os.path.dirname(os.path.abspath(__file__))

valid_file = os.path.join(dirpath, "files/level2.pdf")
invalid_file = os.path.join(dirpath, "files/nothing.pdf")

with description("open_pdf:") as self:
    with it("opens pdf file for reading"):
        with open_pdf(valid_file, False) as doc:
            assert doc is not None
            assert doc.page_count == 6

    with it("returns None if pdf file is invalid"):
        with open_pdf(invalid_file, False) as doc:
            assert doc is None

    with it("exits if pdf file is invalid and exit_on_error is true"):
        try:
            with open_pdf(invalid_file, True) as doc:
                assert False, "should have exited"
        except AssertionError as err:
            raise err
        except:
            pass

with description("ToCEntry") as self:
    with it("matches fitz's representation"):
        fitz_entry = [1, "title", 2]
        fitz_entry2 = [1, "title", 2, 100.0]

        toc_entry = ToCEntry(level=1, title="title", pagenum=2)
        toc_entry2 = ToCEntry(level=1, title="title", pagenum=2, vpos=100.0)

        assert toc_entry.to_fitz_entry() == fitz_entry
        assert toc_entry2.to_fitz_entry() == fitz_entry2

        assert ToCEntry(*fitz_entry) == toc_entry
        assert ToCEntry(*fitz_entry2) == toc_entry2

    with it("is sorted correctly"):
        entries = [
            ToCEntry(level=1, title="title4", pagenum=2, vpos=150.0),
            ToCEntry(level=1, title="title3", pagenum=2, vpos=90.0),
            ToCEntry(level=1, title="title5", pagenum=3, vpos=0.0),
            ToCEntry(level=1, title="title2", pagenum=1, vpos=150.0),
            ToCEntry(level=1, title="title1", pagenum=1, vpos=100.0),
            ToCEntry(level=1, title="title6", pagenum=5, vpos=200.0)
        ]

        expected = [
            ToCEntry(level=1, title="title1", pagenum=1, vpos=100.0),
            ToCEntry(level=1, title="title2", pagenum=1, vpos=150.0),
            ToCEntry(level=1, title="title3", pagenum=2, vpos=90.0),
            ToCEntry(level=1, title="title4", pagenum=2, vpos=150.0),
            ToCEntry(level=1, title="title5", pagenum=3, vpos=0.0),
            ToCEntry(level=1, title="title6", pagenum=5, vpos=200.0)
        ]
        assert sorted(entries, key=ToCEntry.key) == expected


with description("dump_toc") as self:
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
