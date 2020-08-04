"""Parser for table of content csv file"""

import csv

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
        print ("Unable to parse toc entry %s; Need at least %s parts but only have %s -> %s" % (entry, indent + 2 + 1, len(entry), e))
        raise e


def parse_toc(file: IO) -> List[ToCEntry]:
    """Parse a toc file to a list of toc entries"""
    reader = csv.reader(file, lineterminator='\n',
                        delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
    return list(map(parse_entry, reader))
