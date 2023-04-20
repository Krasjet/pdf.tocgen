Change log
==========

pdf.tocgen 1.3.1
----------------

Released April 20, 2023

- Fix file encoding problems on Windows

pdf.tocgen 1.3.0
----------------

Released November 10, 2021

- Fix deprecation warning from PyMuPDF

pdf.tocgen 1.2.3
----------------

Released January 7, 2021

- Compatibility with PyMuPDF 1.18.6

pdf.tocgen 1.2.2
----------------

Released October 11, 2020

- Compatibility with Python 3.9

pdf.tocgen 1.2.1
----------------

Released August 7, 2020

- Fix a typo in the help message of `pdftocgen`.

pdf.tocgen 1.2.0
----------------

Released August 7, 2020

- Swap out argparse in favor of getopt, which is much simpler and more
  flexible.
- Now we could use `pdfxmeta doc.pdf` to dump an entire document, without the
  empty pattern `""`.

pdf.tocgen 1.1.3
----------------

Released August 4, 2020

- Usefully complain when tocparser can't parse an entry

pdf.tocgen 1.1.2
----------------

Released August 3, 2020

- Add `--print` flag for `pdftocio` to force printing ToC.
- Add spec for cli commands.

pdf.tocgen 1.1.1
----------------

Released July 31, 2020

- Add a `--auto` option for `pdfxmeta` to output a valid heading filter directly.

pdf.tocgen 1.1.0
----------------

Released July 31, 2020

- Add a new option for a heading filter to be "greedy", which makes it extract
  all the text in a block when at least one match occurs. This is extremely
  useful for math-heavy documents.
- fixes the sorting problem with two column layout.

pdf.tocgen 1.0.1
----------------

Released July 29, 2020

- Update documentations
- Fix some linter warnings
- Fix unicode problem in tests
- Some prep work for the next major release

pdf.tocgen 1.0.0
----------------

Released July 28, 2020

- The first stable version
