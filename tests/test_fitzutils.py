import unittest
from fitzutils import open_pdf
import fitz
import os


dirpath = os.path.dirname(os.path.abspath(__file__))
valid_file = os.path.join(dirpath, "files/level2.pdf")
invalid_file = os.path.join(dirpath, "files/nothing.pdf")

class FitzUtilsTest(unittest.TestCase):
    def test_open_pdf(self):
        with open_pdf(valid_file, False) as doc:
            self.assertIsNot(doc, None)
            self.assertEqual(doc.pageCount, 6)

        with open_pdf(invalid_file, False) as doc:
            self.assertIs(doc, None)

        try:
            with open_pdf(invalid_file, True) as doc:
                self.fail("should have exited")
        except AssertionError as e:
            raise e
        except:
            pass
