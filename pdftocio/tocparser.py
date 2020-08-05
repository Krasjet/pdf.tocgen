"""Parser for table of content csv file"""

import csv
import sys

from typing import IO, List
from fitzutils import ToCEntry
from itertools import takewhile


def parse_entry(entry: List) -> ToCEntry:
    """parse a row in csv to a toc entry"""

    # a somewhat weird hack, csv reader would read spaces as an empty '', so we
    # only need to count the number of '' before an entry to determined the
    # heading level
    indent = len(list(takewhile(lambda x: x == '', entry)))
    try:
        toc_entry = ToCEntry(
            int(indent / 4) + 1,     # 4 spaces = 1 level
            entry[indent],           # heading
            int(entry[indent + 1]),  # pagenum
            *entry[indent + 2:]      # vpos
        )
        return toc_entry
    except IndexError as e:
        print(f"Unable to parse toc entry {entry};",
              f"Need at least {indent + 2} parts but only have {len(entry)}.",
              "Make sure the page number is present.",
              file=sys.stderr)
        raise e


def parse_toc(file: IO) -> List[ToCEntry]:
    """Parse a toc file to a list of toc entries"""
    reader = csv.reader(file, lineterminator='\n',
                        delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
    return list(map(parse_entry, reader))
