"""Filter on span dictionaries

This module contains the internal representation of heading filters, which are
used to test if a span should be included in the ToC.
"""

import re

from typing import Optional
from re import Pattern

DEF_TOLERANCE: float = 1e-5


def admits_float(expect: Optional[float],
                 actual: Optional[float],
                 tolerance: float) -> bool:
    """Check if a float should be admitted by a filter"""
    return (expect is None) or \
           (actual is not None and abs(expect - actual) <= tolerance)


class FontFilter:
    """Filter on font attributes"""
    name: Pattern
    size: Optional[float]
    size_tolerance: float
    color: Optional[int]
    flags: int
    # besides the usual true (1) and false (0), we have another state,
    # unset (x), where the truth table would be
    # a b diff?
    # 0 0 0
    # 0 1 1
    # 1 0 1
    # 1 1 0
    # x 0 0
    # x 1 0
    # it's very inefficient to compare bit by bit, which would take 5 bitwise
    # operations to compare, and then 4 to combine the results, we will use a
    # trick to reduce it to 2 ops.
    # step 1: use XOR to find different bits. if unset, set bit to 0, we will
    #         take care of false positives in the next step
    # a b a^b
    # 0 0 0
    # 0 1 1
    # 1 0 1
    # 1 1 0
    # step 2: use AND with a ignore mask, (0 for ignored) to eliminate false
    #         positives
    # a b a&b
    # 0 1 0           <- no diff
    # 0 0 0           <- no diff
    # 1 1 1           <- found difference
    # 1 0 0           <- ignored
    ign_mask: int

    def __init__(self, font_dict: dict):
        self.name = re.compile(font_dict.get('name', ""))
        self.size = font_dict.get('size')
        self.size_tolerance = font_dict.get('size_tolerance', DEF_TOLERANCE)
        self.color = font_dict.get('color')
        # some branchless trick
        # x * True = x
        # x * False = 0
        self.flags = (0b00001 * font_dict.get('superscript', False) |
                      0b00010 * font_dict.get('italic', False) |
                      0b00100 * font_dict.get('serif', False) |
                      0b01000 * font_dict.get('monospace', False) |
                      0b10000 * font_dict.get('bold', False))

        self.ign_mask = (0b00001 * ('superscript' in font_dict) |
                         0b00010 * ('italic' in font_dict) |
                         0b00100 * ('serif' in font_dict) |
                         0b01000 * ('monospace' in font_dict) |
                         0b10000 * ('bold' in font_dict))

    def admits(self, spn: dict) -> bool:
        """Check if the font attributes admit the span

        Argument
          spn: the span dict to be checked
        Returns
          False if the span doesn't match current font attribute
        """
        if not self.name.search(spn.get('font', "")):
            return False

        if self.color is not None and self.color != spn.get('color'):
            return False

        if not admits_float(self.size, spn.get('size'), self.size_tolerance):
            return False

        flags = spn.get('flags', ~self.flags)
        # see above for explanation
        return not (flags ^ self.flags) & self.ign_mask


class BoundingBoxFilter:
    """Filter on bounding boxes"""
    left: Optional[float]
    top: Optional[float]
    right: Optional[float]
    bottom: Optional[float]
    tolernace: float

    def __init__(self, bbox_dict: dict):
        self.left = bbox_dict.get('left')
        self.top = bbox_dict.get('top')
        self.right = bbox_dict.get('right')
        self.bottom = bbox_dict.get('bottom')
        self.tolerance = bbox_dict.get('tolerance', DEF_TOLERANCE)

    def admits(self, spn: dict) -> bool:
        """Check if the bounding box admit the span

        Argument
          spn: the span dict to be checked
        Returns
          False if the span doesn't match current bounding box setting
        """
        bbox = spn.get('bbox', (None, None, None, None))
        return (admits_float(self.left, bbox[0], self.tolerance) and
                admits_float(self.top, bbox[1], self.tolerance) and
                admits_float(self.right, bbox[2], self.tolerance) and
                admits_float(self.bottom, bbox[3], self.tolerance))


class ToCFilter:
    """Filter on span dictionary to pick out headings in the ToC"""
    # The level of the title, strictly > 0
    level: int
    # When set, the filter will be more *greedy* and extract all the text in a
    # block even when at least one match occurs
    greedy: bool
    font: FontFilter
    bbox: BoundingBoxFilter

    def __init__(self, fltr_dict: dict):
        self.level = fltr_dict.get('level')

        if self.level is None:
            raise ValueError("filter's 'level' is not set")
        if self.level < 1:
            raise ValueError("filter's 'level' must be >= 1")

        self.greedy = fltr_dict.get('greedy', False)
        self.font = FontFilter(fltr_dict.get('font', {}))
        self.bbox = BoundingBoxFilter(fltr_dict.get('bbox', {}))

    def admits(self, spn: dict) -> bool:
        """Check if the filter admits the span

        Arguments
          spn: the span dict to be checked
        Returns
          False if the span doesn't match the filter
        """
        return self.font.admits(spn) and self.bbox.admits(spn)
