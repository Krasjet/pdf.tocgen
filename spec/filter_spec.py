import os

from mamba import description, it, before
from pdftocgen.filter import Font

with description("Font") as self:
    with before.all:
        self.fnt_dict1 = {
            'name': "CMBX12",
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        }

        self.fnt_dict2 = {
            'name': "CMR10",
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': False
        }

        self.fnt_dict3 = {
            'superscript': False,
            'italic': False,
            'serif': True,
            'monospace': False,
            'bold': True
        }

        self.fnt_dict4 = {
            'name': "CMBX12",
        }

        self.fnt_dict5 = {
            'serif': True,
            'bold': True
        }

        self.fnt_dict6 = {
            'serif': True,
        }

        self.fnt_dict7 = {
            'serif': False,
        }

        self.fnt_dict8 = {
            'serif': True,
            'monospace': True,
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
        fnt = Font(self.fnt_dict1)
        assert fnt.name.search("TZOLRB+CMBX12")
        assert fnt.name.search("CMBX12")
        assert not fnt.name.search("CMBX10")
        assert fnt.flags == 0b10100
        assert fnt.ign_mask == 0b11111

    with it("can construct if None is given in the constructor"):
        fnt = Font(None)
        assert fnt.name.match("anything")
        assert fnt.flags == 0
        assert fnt.ign_mask == 0

    with it("admits matching spans"):
        fnt_title = Font(self.fnt_dict1)
        fnt_text = Font(self.fnt_dict2)
        assert fnt_title.admits(self.spn_title)
        assert fnt_text.admits(self.spn_text)

    with it("rejects non-matching spans"):
        fnt_title = Font(self.fnt_dict1)
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_title2)

        fnt_text = Font(self.fnt_dict2)
        assert not fnt_text.admits(self.spn_title)
        assert not fnt_text.admits(self.spn_title2)

    with it("admits correctly without font name"):
        fnt_title = Font(self.fnt_dict3)
        assert fnt_title.admits(self.spn_title)

    with it("rejects correctly without font name"):
        fnt_title = Font(self.fnt_dict3)
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_title2)

    with it("admits correctly without flags"):
        fnt_title = Font(self.fnt_dict4)
        assert fnt_title.admits(self.spn_title)
        assert fnt_title.admits(self.spn_title2)

    with it("rejects correctly without flags"):
        fnt_title = Font(self.fnt_dict4)
        assert not fnt_title.admits(self.spn_text)

    with it("admits correctly with partial flags"):
        fnt_title = Font(self.fnt_dict5)
        fnt_serif = Font(self.fnt_dict6)
        fnt_sans = Font(self.fnt_dict7)
        fnt_mono = Font(self.fnt_dict8)
        assert fnt_title.admits(self.spn_title)
        assert fnt_serif.admits(self.spn_title)
        assert fnt_serif.admits(self.spn_text)
        assert fnt_sans.admits({'flags': 0b11011})
        assert fnt_mono.admits({'flags': 0b11111})

    with it("rejects correctly with partial flags"):
        fnt_title = Font(self.fnt_dict5)
        fnt_serif = Font(self.fnt_dict6)
        fnt_sans = Font(self.fnt_dict7)
        fnt_mono = Font(self.fnt_dict8)
        assert not fnt_title.admits(self.spn_text)
        assert not fnt_title.admits(self.spn_title2)
        assert not fnt_sans.admits(self.spn_title)
        assert not fnt_sans.admits(self.spn_text)
        assert not fnt_mono.admits(self.spn_title)
        assert not fnt_mono.admits(self.spn_text)
