import unittest
from pdfxmeta import extract_meta
import fitz


class ExtractMetaTest(unittest.TestCase):
    def test_extract_meta_basic(self):
        doc = fitz.open('./tests/files/level2.pdf')
        meta = extract_meta(doc, "Section One", 1)
        self.assertEqual(len(meta), 1)
        self.assertIn('font', meta[0])
        self.assertIn('CMBX12', meta[0]['font'])

    def test_extract_meta_ign_case(self):
        doc = fitz.open('./tests/files/level2.pdf')
        #
        meta = extract_meta(doc, "section one", 1, True)
        self.assertEqual(len(meta), 1, "ignore case should match lowercase")
        self.assertIn('font', meta[0])
        self.assertIn('CMBX12', meta[0]['font'])

        meta = extract_meta(doc, "sEcTIoN OnE", 1, True)
        self.assertEqual(len(meta), 1, "ignore case should match mixed case")
        self.assertIn('font', meta[0])
        self.assertIn('CMBX12', meta[0]['font'])

        meta = extract_meta(doc, "section one", 1, False)
        self.assertEqual(len(meta), 0,
                         "without ignore case, lowercase shouldn't match anything")

    def test_extract_meta_multiple(self):
        doc = fitz.open('./tests/files/level2.pdf')

        meta = extract_meta(doc, "Section", 1)
        self.assertEqual(len(meta), 2, "should match 2 instances")

        self.assertIn('font', meta[0])
        self.assertIn('CMBX12', meta[0]['font'])

        self.assertIn('font', meta[1])
        self.assertIn('CMBX12', meta[1]['font'])

    def test_extract_meta_none(self):
        doc = fitz.open('./tests/files/level2.pdf')

        meta = extract_meta(doc, "Sectoin", 1)
        self.assertEqual(len(meta), 0, "should match none")

    def test_extract_meta_outofrange(self):
        doc = fitz.open('./tests/files/level2.pdf')

        meta = extract_meta(doc, "Section One", 0)
        self.assertEqual(len(meta), 0)

        meta = extract_meta(doc, "Section One", 7)
        self.assertEqual(len(meta), 0)

    def test_extract_meta_all(self):
        doc = fitz.open('./tests/files/level2.pdf')

        meta = extract_meta(doc, "The End")
        self.assertEqual(len(meta), 1)
        self.assertIn('font', meta[0])
        self.assertIn('CMBX12', meta[0]['font'])
