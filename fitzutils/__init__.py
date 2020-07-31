"""A collection of utility functions to work with PyMuPDF"""

__version__ = '0.1.0'

from .fitzutils import (
    open_pdf,
    ToCEntry,
    dump_toc,
    pprint_toc
)

__all__ = [
    'open_pdf',
    'ToCEntry',
    'dump_toc',
    'pprint_toc',
]
