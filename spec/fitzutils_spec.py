import os

from mamba import description, it
from fitzutils import open_pdf

dirpath = os.path.dirname(os.path.abspath(__file__))

valid_file = os.path.join(dirpath, "files/level2.pdf")
invalid_file = os.path.join(dirpath, "files/nothing.pdf")

with description("open_pdf:") as self:
    with it("opens pdf file for reading"):
        with open_pdf(valid_file, False) as doc:
            assert doc is not None
            assert doc.pageCount == 6

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
