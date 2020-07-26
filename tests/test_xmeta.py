from pdfxmeta import extract_meta

import unittest
import fitz
import os

dirpath = os.path.dirname(os.path.abspath(__file__))
level2_path = os.path.join(dirpath, "files/level2.pdf")


class ExtractMetaTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ExtractMetaTest, self).__init__(*args, **kwargs)
        self.doc = fitz.open(level2_path)

    def test_extract_meta_basic(self):
        meta = extract_meta(self.doc, "Section One", 1)
        self.assertEqual(len(meta), 1)

        txt, m = meta[0]
        self.assertEqual(txt, "Section One")
        self.assertIn('font', m)
        self.assertIn('CMBX12', m['font'])

    def test_extract_meta_ign_case(self):
        meta = extract_meta(self.doc, "section one", 1, True)
        self.assertEqual(len(meta), 1, "ignore case should match lowercase")
        txt, m = meta[0]
        self.assertEqual(txt, "Section One")
        self.assertIn('font', m)
        self.assertIn('CMBX12', m['font'])

        meta = extract_meta(self.doc, "sEcTIoN OnE", 1, True)
        self.assertEqual(len(meta), 1, "ignore case should match mixed case")
        txt, m = meta[0]
        self.assertEqual(txt, "Section One")
        self.assertIn('font', m)
        self.assertIn('CMBX12', m['font'])

        meta = extract_meta(self.doc, "section one", 1, False)
        self.assertEqual(len(meta), 0,
                         "without ignore case, lowercase shouldn't match anything")

    def test_extract_meta_multiple(self):
        meta = extract_meta(self.doc, "Section", 1)
        self.assertEqual(len(meta), 2, "should match 2 instances")

        txt, m = meta[0]
        self.assertEqual(txt, "Section One")
        self.assertIn('font', m)
        self.assertIn('CMBX12', m['font'])

        txt, m = meta[1]
        self.assertEqual(txt, "Section Two")
        self.assertIn('font', m)
        self.assertIn('CMBX12', m['font'])

    def test_extract_meta_none(self):
        meta = extract_meta(self.doc, "Sectoin", 1)
        self.assertEqual(len(meta), 0, "should match none")

    def test_extract_meta_outofrange(self):
        meta = extract_meta(self.doc, "Section One", 0)
        self.assertEqual(len(meta), 0)

        meta = extract_meta(self.doc, "Section One", 7)
        self.assertEqual(len(meta), 0)

    def test_extract_meta_all(self):
        meta = extract_meta(self.doc, "The End")

        txt, m = meta[0]
        self.assertEqual(txt, "The End")
        self.assertIn('font', m)
        self.assertIn('CMBX12', m['font'])
