import os
import fitz
import toml

from mamba import description, it, before
from pdfxmeta import extract_meta, dump_meta

dirpath = os.path.dirname(os.path.abspath(__file__))

with description("extract_meta:") as self:
    with before.all:
        self.doc = fitz.open(os.path.join(dirpath, "files/level2.pdf"))

    with it("extracts metadata from pdf"):
        meta = extract_meta(self.doc, "Section One", 1)
        assert len(meta) == 1

        txt, m = meta[0]
        assert txt == "Section One"
        assert 'font' in m
        assert 'CMBX12' in m['font']

    with it("matches lowercase when ignore case is set"):
        meta = extract_meta(self.doc, "section one", 1, True)
        assert len(meta) == 1

        txt, m = meta[0]
        assert txt == "Section One"
        assert 'font' in m
        assert 'CMBX12' in m['font']

    with it("matches mixed case when ignore case is set"):
        meta = extract_meta(self.doc, "sEcTIoN OnE", 1, True)
        assert len(meta) == 1

        txt, m = meta[0]
        assert txt == "Section One"
        assert 'font' in m
        assert 'CMBX12' in m['font']

    with it("matches nothing if ignore case is not set"):
        meta = extract_meta(self.doc, "section one", 1, False)
        assert len(meta) == 0

    with it("can match multiple instances of needle"):
        meta = extract_meta(self.doc, "Section", 1)
        assert len(meta) == 2

        txt, m = meta[0]
        assert txt == "Section One"
        assert 'font' in m
        assert 'CMBX12' in m['font']

        txt, m = meta[1]
        assert txt == "Section Two"
        assert 'font' in m
        assert 'CMBX12' in m['font']

    with it("returns [] when nothing is matched"):
        meta = extract_meta(self.doc, "Sectoin", 1, False)
        assert len(meta) == 0

    with it("returns [] when page number is out of range"):
        meta = extract_meta(self.doc, "Section One", 0)
        assert len(meta) == 0

        meta = extract_meta(self.doc, "Section One", 7)
        assert len(meta) == 0

    with it("can match text on any page when page number is not specified"):
        meta = extract_meta(self.doc, "The End")
        assert len(meta) == 1

        txt, m = meta[0]
        assert txt == "The End"
        assert 'font' in m
        assert 'CMBX12' in m['font']

with description("dump_meta:") as self:
    with before.all:
        self.doc = fitz.open(os.path.join(dirpath, "files/level2.pdf"))
        self.expected_meta = {
            'size': 14.346199989318848,
            'color': 0x000000,
            'font': {
                'name': 'TZOLRB+CMBX12',
                'superscript': False,
                'italic': False,
                'serif': True,
                'monospace': False,
                'bold': True
            },
            'bbox': {
                'left': 157.98439025878906,
                'top': 237.6484375,
                'right': 243.12905883789062,
                'bottom': 252.00897216796875
            }
        }

    with it("produces valid toml"):
        meta = extract_meta(self.doc, "Section One", 1)
        assert len(meta) == 1

        txt, m = meta[0]
        try:
            meta_dict = toml.loads(dump_meta(m))
            assert meta_dict == self.expected_meta
        except AssertionError as err:
            raise err
        except:
            pass
