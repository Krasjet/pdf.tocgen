from dataclasses import dataclass
from typing import Optional, List, Dict
from .filter import ToCFilter
from fitzutils import ToCEntry
from itertools import chain
from collections import defaultdict
from fitz import Document


class FoundGreedy(Exception):
    """A hacky solution to do short-circuiting in Python.

    The main reason to do this short-circuiting is to untangle the logic of
    greedy filter with normal execution, which makes the typing and code much
    cleaner, but it can also save some unecessary comparisons.

    Probably similar to call/cc in scheme or longjump in C
    c.f. https://ds26gte.github.io/tyscheme/index-Z-H-15.html#node_sec_13.2
    """
    level: int

    def __init__(self, level):
        """
        Argument
          level: level of the greedy filter
        """
        super().__init__()
        self.level = level


def blk_to_str(blk: dict) -> str:
    """Extract all the text inside a block"""
    return " ".join([
        spn.get('text', "").strip()
        for line in blk.get('lines', [])
        for spn in line.get('spans', [])
    ])


@dataclass
class Fragment:
    """A fragment of the extracted heading"""
    text: str
    level: int


def concatFrag(frags: List[Optional[Fragment]], sep: str = " ") -> Dict[int, str]:
    """Concatenate fragments to strings

    Returns
      a dictionary (level -> title) that contains the title for each level.
    """
    # accumulate a list of strings for each level of heading
    acc = defaultdict(list)
    for frag in frags:
        if frag is not None:
            acc[frag.level].append(frag.text)

    result = {}
    for level, strs in acc.items():
        result[level] = sep.join(strs)
    return result


class Recipe:
    """The internal representation of a recipe"""
    filters: List[ToCFilter]

    def __init__(self, recipe_dict: dict):
        fltr_dicts = recipe_dict.get('heading', [])

        if len(fltr_dicts) == 0:
            raise ValueError("no filters found in recipe")
        self.filters = [ToCFilter(fltr) for fltr in fltr_dicts]

    def _extract_span(self, spn: dict) -> Optional[Fragment]:
        """Extract text from span along with level

        Argument
          spn: a span dictionary
          {
            'bbox': (float, float, float, float),
            'color': int,
            'flags': int,
            'font': str,
            'size': float,
            'text': str
          }
        Returns
          a fragment of the heading or None if no match
        """
        for fltr in self.filters:
            if fltr.admits(spn):
                text = spn.get('text', "").strip()

                if not text:
                    # don't match empty spaces
                    return None

                if fltr.greedy:
                    # propagate all the way back to extract_block
                    raise FoundGreedy(fltr.level)

                return Fragment(text, fltr.level)
        return None

    def _extract_line(self, line: dict) -> List[Optional[Fragment]]:
        """Extract matching heading fragments in a line.

        Argument
          line: a line dictionary
          {
            'bbox': (float, float, float, float),
            'wmode': int,
            'dir': (float, float),
            'spans': [dict]
          }
        Returns
          a list of fragments concatenated from result in a line
        """
        return [self._extract_span(spn) for spn in line.get('spans', [])]

    def extract_block(self, block: dict, page: int) -> List[ToCEntry]:
        """Extract matching headings in a block.

        Argument
          block: a block dictionary
          {
            'bbox': (float, float, float, float),
            'lines': [dict],
            'type': int
          }
        Returns
          a list of toc entries, concatenated from the result of lines
        """
        if block.get('type') != 0:
            # not a text block
            return []

        vpos = block.get('bbox', (0, 0))[1]

        try:
            frags = chain.from_iterable([
                self._extract_line(ln) for ln in block.get('lines')
            ])
            titles = concatFrag(frags)

            return [
                ToCEntry(level, title, page, vpos)
                for level, title in titles.items()
            ]
        except FoundGreedy as e:
            # return the entire block as a single entry
            return [ToCEntry(e.level, blk_to_str(block), page, vpos)]


def extract_toc(doc: Document, recipe: Recipe) -> List[ToCEntry]:
    """Extract toc entries from a document

    Arguments
      doc: a pdf document
      recipe: recipe from user
    Returns
      a list of toc entries in the document
    """
    result = []

    for page in doc.pages():
        for blk in page.getTextPage().extractDICT().get('blocks', []):
            result.extend(
                recipe.extract_block(blk, page.number + 1)
            )

    return result
