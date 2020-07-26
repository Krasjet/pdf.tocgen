"""Filters on span dictionary

This module contains the internal representation of filters, which are used to
test if a span should be included in the ToC.
"""

import re

from typing import Optional
from re import Pattern

class Font:
    """Filter on font attributes"""
    name: Pattern
    flags: int
    # besides the usual true (1) and false (0), we have another state--unset (x),
    # where the truth table would be
    # a b
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

    def __init__(self, font_dict: Optional[dict]):
        if font_dict is None:
            self.name = re.compile("")
            self.flags = 0
            self.ign_mask = 0
            return
        self.name = re.compile(font_dict.get('name', ""))
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
          False if the spn doesn't match current font attribute
        """
        if not self.name.search(spn.get("font", "")):
            return False

        flags = spn.get('flags', ~self.flags)
        # see above for explanation
        return not (flags ^ self.flags) & self.ign_mask



class BoundingBox:
    """Filter on bounding box"""
    left: Optional[float]
    top: Optional[float]
    right: Optional[float]
    bottom: Optional[float]
    tolerance: float

    def __init__(self, bbox_dict: Optional[dict], tolerance: float):
        if bbox_dict is None:
            return
        self.left = bbox_dict.get('left')
        self.top = bbox_dict.get('top')
        self.right = bbox_dict.get('right')
        self.bottom = bbox_dict.get('bottom')
        self.tolerance = tolerance


class ToCFilter:
    """The overall filter on span dictionary"""
    level: int
    size: Optional[float]
    size_tolerance: Optional[float]
    color: Optional[int]
    font: Font
    bbox: BoundingBox

    def __init__(self, fltr_dict: dict):
        self.level = fltr_dict.get('level')

        if self.level is None:
            raise ValueError("level is not set")
        if self.level < 1:
            raise ValueError("level must be >= 1")

        tol = fltr_dict.get('tolerance', {})

        self.size = fltr_dict.get('size')
        self.size_tolerance = tol.get('size', 1e-5)
        self.color = fltr_dict.get('color')
        self.font = Font(fltr_dict.get('font'))
        self.bbox = BoundingBox(fltr_dict.get('bbox'), tol.get('bbox', 1e-5))
