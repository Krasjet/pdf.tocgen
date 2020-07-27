"""A collection of utility functions to work with PyMuPDF"""

__version__ = '0.1.0'

from .fitzutils import *

__all__ = [
    'open_pdf',
    'get_pages',
    'ToCEntry',
    'dump_toc',
    'pprint_toc',
]
