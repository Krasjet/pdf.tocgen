import os

from mamba import description, it, before
from pdftocgen.filter import (
    ToCFilter,
    admits_float,
    FontFilter,
    BoundingBoxFilter
)

dirpath = os.path.dirname(os.path.abspath(__file__))

with description("admits_float") as self:
    with it("admits if difference is below tol"):
        assert admits_float(1, 1.05, 0.1)
        assert admits_float(1, 0.95, 0.1)

    with it("does not admit if difference is too large"):
        assert not admits_float(1, 1.5, 0.1)
        assert not admits_float(1, 0.5, 0.1)

    with it("admits anything if expect is unset"):
        assert admits_float(None, 1, 0.1)
        assert admits_float(None, None, 0.1)

    with it("does not admit if expect is set but actual is None"):
        assert not admits_float(1, None, 0.1)

with description("ToCFilter") as self:
    with before.all:
        self.title_exact = {
            'level': 1,
            'font': {
                'name': "CMBX12",
                'size': 14.346199989318848,
                'size_tolerance': 0,
                'color': 0,
                'superscript': False,
                'italic': False,
                'serif': True,
                'monospace': False,
                'bold': True
            },
            'bbox': {
                'left': 157.98439025878906,
                'top': 567.3842163085938,
                'right': 245.18057250976562,
                'bottom': 581.7447509765625,
                'tolerance': 0
            }
        }

        self.text_exact = {
            'level': 2,
            'font': {
                'name': "CMR10",
                'size': 9.962599754333496,
                'size_tolerance': 0,
                'color': 0,
                'superscript': False,
                'italic': False,
                'serif': True,
                'monospace': False,
                'bold': False
            },
            'bbox': {
                'left': 133.76800537109375,
                'top': 592.492919921875,
                'right': 477.537353515625,
                'bottom': 602.4555053710938,
                'tolerance': 0
            }
        }

        self.spn_title = {
            'size': 14.346199989318848,
            'flags': 20,
            'font': 'TZOLRB+CMBX12',
            'color': 0,
            'text': 'Section Two',
            'bbox': (157.98439025878906,
                     567.3842163085938,
                     245.18057250976562,
                     581.7447509765625)
        }

        self.spn_text = {
            'size': 9.962599754333496,
            'flags': 4,
            'font': 'MJDLZY+CMR10',
            'color': 0,
            'text': 'text',
            'bbox': (133.76800537109375,
                     592.492919921875,
                     477.537353515625,
                     602.4555053710938)
        }

    with it("raises error if no toc level is specified"):
        try:
            fltr = ToCFilter({})
        except ValueError:
            pass
        except:
            assert False, "must raise error"

    with it("raises error if toc level is invalid"):
        try:
            fltr = ToCFilter({'level': 0})
            fltr = ToCFilter({'level': -1})
        except ValueError:
            pass
        except:
            assert False, "must raise error"

    with it("does not raise error if toc level is valid"):
        try:
            fltr = ToCFilter({'level': 1})
            fltr = ToCFilter({'level': 2})
        except ValueError:
            assert False, "must not raise error"

    with it("admits exact matches"):
        filter_title = ToCFilter(self.title_exact)
        filter_text = ToCFilter(self.text_exact)
        assert filter_title.admits(self.spn_title)
        assert filter_text.admits(self.spn_text)

    with it("rejects unmatched spans"):
        filter_title = ToCFilter(self.title_exact)
        filter_text = ToCFilter(self.text_exact)
        assert not filter_title.admits(self.spn_text)
        assert not filter_text.admits(self.spn_title)

    with it("admits correctly without bbox"):
        filter_title = ToCFilter({
            'level': 1,
            'font': {
                'name': "CMBX12",
            }
        })
        assert filter_title.admits(self.spn_title)

        filter_text = ToCFilter({
            'level': 2,
            'font': {
                'size': 9.962599754333496,
            }
        })
        assert filter_text.admits(self.spn_text)

    with it("rejects correctly without bbox"):
        filter_title = ToCFilter({
            'level': 1,
            'font': {
                'name': "CMBX12",
            }
        })
        assert not filter_title.admits(self.spn_text)

        filter_text = ToCFilter({
            'level': 2,
            'font': {
                'size': 9.962599754333496,
            }
        })
        assert not filter_text.admits(self.spn_title)

    with it("admits correctly without font"):
        filter_title = ToCFilter({
            'level': 1,
            'bbox': {
                'left': 157.98439025878906,
            }
        })
        assert filter_title.admits(self.spn_title)

        filter_text = ToCFilter({
            'level': 2,
            'bbox': {
                'top': 592.492919921875,
            }
        })
        assert filter_text.admits(self.spn_text)

    with it("rejects correctly without font"):
        filter_title = ToCFilter({
            'level': 1,
            'bbox': {
                'left': 157.98439025878906,
            }
        })
        assert not filter_title.admits(self.spn_text)

        filter_text = ToCFilter({
            'level': 2,
            'bbox': {
                'top': 592.492919921875,
            }
        })
        assert not filter_text.admits(self.spn_title)


with description("FontFilter") as self:
    with before.all:
        self.title_exact = {
            'name': "CMBX12",
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'color': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        }

        self.text_exact = {
            'name': "CMR10",
            'size': 9.962599754333496,
            'size_tolerance': 0,
            'color': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': False
        }

        self.spn_title = {
            'size': 14.346199989318848,
            'flags': 20,
            'font': 'TZOLRB+CMBX12',
            'color': 0,
            'text': 'Section Two',
            'bbox': (157.98439025878906,
                     567.3842163085938,
                     245.18057250976562,
                     581.7447509765625)
        }

        self.spn_small_title = {
            'size': 9.962599754333496,
            'flags': 4,
            'font': 'TZOLRB+CMBX12',
            'color': 0,
            'text': 'text',
            'bbox': (133.76800537109375,
                     592.492919921875,
                     477.537353515625,
                     602.4555053710938)
        }

        self.spn_text = {
            'size': 9.962599754333496,
            'flags': 4,
            'font': 'MJDLZY+CMR10',
            'color': 0,
            'text': 'text',
            'bbox': (133.76800537109375,
                     592.492919921875,
                     477.537353515625,
                     602.4555053710938)
        }

    with it("has a working constructor"):
        fnt = FontFilter(self.title_exact)
        assert fnt.name.search("TZOLRB+CMBX12")
        assert fnt.name.search("CMBX12")
        assert not fnt.name.search("CMBX10")
        assert fnt.flags == 0b10100
        assert fnt.ign_mask == 0b11111
        assert fnt.color == 0x000000
        assert fnt.size == 14.346199989318848
        assert fnt.size_tolerance == 0

    with it("can construct if empty dict is given in the constructor"):
        fnt = FontFilter({})
        assert fnt.name.search("anything")
        assert fnt.flags == 0
        assert fnt.ign_mask == 0
        assert fnt.color is None
        assert fnt.size is None
        assert fnt.size_tolerance == 1e-5

    with it("admits exact matches"):
        fnt_title = FontFilter(self.title_exact)
        fnt_text = FontFilter(self.text_exact)
        assert fnt_title.admits(self.spn_title)
        assert fnt_text.admits(self.spn_text)

    with it("rejects unmatched spans"):
        fnt_title = FontFilter(self.title_exact)
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

        fnt_text = FontFilter(self.text_exact)
        assert not fnt_text.admits(self.spn_title)
        assert not fnt_text.admits(self.spn_small_title)

    with it("admits correctly without font name"):
        fnt_title = FontFilter({
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'color': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly without font name"):
        fnt_title = FontFilter({
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'color': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

    with it("admits correctly with only font name"):
        fnt_title = FontFilter({
            'name': "CMBX12"
        })
        assert fnt_title.admits(self.spn_title)
        assert fnt_title.admits(self.spn_small_title)

    with it("rejects correctly with only font name"):
        fnt_title = FontFilter({
            'name': "CMBX12"
        })
        assert not fnt_title.admits(self.spn_text)

    with it("admits correctly without size"):
        fnt_title = FontFilter({
            'name': "CMBX12",
            'size_tolerance': 0,
            'color': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly without size"):
        fnt_title = FontFilter({
            'name': "CMBX12",
            'size_tolerance': 0,
            'color': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

    with it("admits correctly with only size"):
        fnt_title = FontFilter({
            'size': 14.346199989318848,
            'size_tolerance': 0
        })
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly with only size"):
        fnt_title = FontFilter({
            'size': 14.346199989318848,
            'size_tolerance': 0
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

    with it("admits correctly without color"):
        fnt_title = FontFilter({
            'name': "CMBX12",
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly without color"):
        fnt_title = FontFilter({
            'name': "CMBX12",
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

    with it("admits correctly with only color"):
        fnt_title = FontFilter({
            'color': 0x000000,
        })
        assert fnt_title.admits(self.spn_title)
        assert fnt_title.admits(self.spn_text)
        assert fnt_title.admits(self.spn_small_title)

    with it("rejects correctly with only color"):
        fnt_title = FontFilter({
            'color': 0x000000,
        })
        spn_blue = {
            'size': 14.346199989318848,
            'flags': 20,
            'font': 'TZOLRB+CMBX12',
            'color': 0x0000ff,
            'text': 'Section Two',
            'bbox': (157.98439025878906,
                     567.3842163085938,
                     245.18057250976562,
                     581.7447509765625)
        }
        assert not fnt_title.admits(spn_blue)

    with it("admits correctly with only flags"):
        fnt_title = FontFilter({
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly with only flags"):
        fnt_title = FontFilter({
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

    with it("admits correctly without flags"):
        fnt_title = FontFilter({
            'name': "CMBX12",
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'color': 0,
        })
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly without flags"):
        fnt_title = FontFilter({
            'name': "CMBX12",
            'size': 14.346199989318848,
            'size_tolerance': 0,
            'color': 0,
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)

    with it("admits correctly with partial flags"):
        fnt_title = FontFilter({
            'serif': True,
            'bold': True
        })
        fnt_serif = FontFilter({
            'serif': True
        })
        fnt_sans = FontFilter({
            'serif': False
        })
        fnt_mono = FontFilter({
            'monospace': True
        })
        assert fnt_title.admits(self.spn_title)
        assert fnt_serif.admits(self.spn_title)
        assert fnt_serif.admits(self.spn_text)
        assert fnt_sans.admits({'flags': 0b11011})
        assert fnt_mono.admits({'flags': 0b11111})

    with it("rejects correctly with partial flags"):
        fnt_title = FontFilter({
            'serif': True,
            'bold': True
        })
        fnt_serif = FontFilter({
            'serif': True
        })
        fnt_sans = FontFilter({
            'serif': False
        })
        fnt_mono = FontFilter({
            'monospace': True
        })
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_small_title)
        assert not fnt_sans.admits(self.spn_title)
        assert not fnt_sans.admits(self.spn_text)
        assert not fnt_mono.admits(self.spn_title)
        assert not fnt_mono.admits(self.spn_text)


with description("BoundingBoxFilter") as self:
    with before.all:
        self.title_exact = {
            'left': 157.98439025878906,
            'top': 567.3842163085938,
            'right': 245.18057250976562,
            'bottom': 581.7447509765625,
            'tolerance': 0
        }

        self.text_exact = {
            'left': 133.76800537109375,
            'top': 592.492919921875,
            'right': 477.537353515625,
            'bottom': 602.4555053710938,
            'tolerance': 0
        }

        self.spn_title = {
            'size': 14.346199989318848,
            'flags': 20,
            'font': 'TZOLRB+CMBX12',
            'color': 0,
            'text': 'Section Two',
            'bbox': (157.98439025878906,
                     567.3842163085938,
                     245.18057250976562,
                     581.7447509765625)
        }

        self.spn_title2 = {
            'size': 14.346199989318848,
            'flags': 20,
            'font': 'TZOLRB+CMBX12',
            'color': 0,
            'text': 'Section One',
            'bbox': (157.98439025878906,
                     335.569580078125,
                     477.66058349609375,
                     349.93011474609375)
        }

        self.spn_text = {
            'size': 9.962599754333496,
            'flags': 4,
            'font': 'MJDLZY+CMR10',
            'color': 0,
            'text': 'text',
            'bbox': (133.76800537109375,
                     592.492919921875,
                     477.537353515625,
                     602.4555053710938)
        }
    with it("has a working constructor"):
        bbox = BoundingBoxFilter(self.title_exact)
        assert bbox.left is not None
        assert bbox.right is not None
        assert bbox.top is not None
        assert bbox.bottom is not None
        assert bbox.tolerance == 0

    with it("can construct if empty dict is given in the constructor"):
        bbox = BoundingBoxFilter({})
        assert bbox.left is None
        assert bbox.right is None
        assert bbox.top is None
        assert bbox.bottom is None
        assert bbox.tolerance == 1e-5

    with it("admits exact matches"):
        bbox_title = BoundingBoxFilter(self.title_exact)
        bbox_text = BoundingBoxFilter(self.text_exact)
        assert bbox_title.admits(self.spn_title)
        assert bbox_text.admits(self.spn_text)

    with it("rejects unmatched spans"):
        bbox_title = BoundingBoxFilter(self.title_exact)
        assert not bbox_title.admits(self.spn_text)
        assert not bbox_title.admits(self.spn_title2)

        bbox_text = BoundingBoxFilter(self.text_exact)
        assert not bbox_text.admits(self.spn_title)
        assert not bbox_text.admits(self.spn_title2)

    with it("admits correctly with partial bbox"):
        bbox_title = BoundingBoxFilter({
            'left': 157.98439025878906
        })
        assert bbox_title.admits(self.spn_title)
        assert bbox_title.admits(self.spn_title2)

        bbox_top = BoundingBoxFilter({
            'top': 567.3842163085938
        })
        assert bbox_top.admits(self.spn_title)

        bbox_right = BoundingBoxFilter({
            'right': 245.18057250976562
        })
        assert bbox_right.admits(self.spn_title)

        bbox_bottom = BoundingBoxFilter({
            'bottom': 581.7447509765625
        })
        assert bbox_bottom.admits(self.spn_title)

    with it("rejects correctly with partial bbox"):
        bbox_title = BoundingBoxFilter({
            'left': 157.98439025878906
        })
        assert not bbox_title.admits(self.spn_text)

        bbox_top = BoundingBoxFilter({
            'top': 567.3842163085938
        })
        assert not bbox_top.admits(self.spn_title2)

        bbox_right = BoundingBoxFilter({
            'right': 245.18057250976562
        })
        assert not bbox_right.admits(self.spn_title2)

        bbox_bottom = BoundingBoxFilter({
            'bottom': 581.7447509765625
        })
        assert not bbox_bottom.admits(self.spn_title2)
