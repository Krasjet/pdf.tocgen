pdf.tocgen
==========

```
                          in.pdf
                            |
                            |
     +----------------------+--------------------+
     |                      |                    |
     V                      V                    V
+----------+          +-----------+         +----------+
|          |  recipe  |           |   ToC   |          |
| pdfxmeta +--------->| pdftocgen +-------->| pdftocio +---> out.pdf
|          |          |           |         |          |
+----------+          +-----------+         +----------+
```

[pdf.tocgen][tocgen] is a set of command-line tools for automatically
extracting and generating the table of contents (ToC) of a PDF file. It uses
the embedded font attributes and position of headings to deduce the basic
outline of a PDF file.

It works best for PDF files produces from a TeX document using `pdftex` (and
its friends `pdflatex`, `pdfxetex`, etc.), but it's designed to work with any
**software-generated** PDF files (i.e. you shouldn't expect it to work with
scanned PDFs). Some examples include `troff`/`groff`, Adobe InDesign, Microsoft
Word, and probably more.

Please see the [**homepage**][tocgen] for a detailed introduction.

Installation
------------

`pdf.tocgen` written in Python 3. It is known to work with Python 3.8 under
Linux, but Python 3.7 should be the minimum. Use

```sh
$ pip install -U pdf.tocgen
```
to install the latest version systemwide, or use

```sh
$ pip install -U --user pdf.tocgen
```
to install it for the current user. I would recommend the latter approach to
avoid messing up the package manager on your system.

Workflow
--------

The design of pdf.tocgen is influenced by the [Unix philosophy][unix]. I
intentionally separated pdf.tocgen to 3 separate programs. They work together,
but each of them is useful on their own.

1. `pdfxmeta`: extract the metadata (font attributes, positions) of headings to
    build a **recipe** file.
2. `pdftocgen`: generate a table of contents from the recipe.
3. `pdftocio`: import the table of contents to the PDF document.

You should read [the example][ex] on the homepage for a proper introduction,
but the basic workflow follows like this.

First, use `pdfxmeta` to search for metadata of headings

```sh
$ pdfxmeta -p page in.pdf pattern >> recipe.toml
$ pdfxmeta -p page in.pdf pattern2 >> recipe.toml
```

Edit the `recipe.toml` file to pick out the attributes you need and specify the
heading levels.

```sh
$ vim recipe.toml # edit
```

An example recipe would look like this:

```toml
[[filter]]
level = 1
font.name = "Times-Bold"
font.size = 19.92530059814453

[[filter]]
level = 2
font.name = "Times-Bold"
font.size = 11.9552001953125
```

Then pass the recipe to `pdftocgen` to generate a table of contents,

```console
$ pdftocgen in.pdf < recipe.toml
"Preface" 5
    "Bottom-up Design" 5
    "Plan of the Book" 7
    "Examples" 9
    "Acknowledgements" 9
"Contents" 11
"The Extensible Language" 14
    "1.1 Design by Evolution" 14
    "1.2 Programming Bottom-Up" 16
    "1.3 Extensible Software" 18
    "1.4 Extending Lisp" 19
    "1.5 Why Lisp (or When)" 21
"Functions" 22
    "2.1 Functions as Data" 22
    "2.2 Defining Functions" 23
    "2.3 Functional Arguments" 26
    "2.4 Functions as Properties" 28
    "2.5 Scope" 29
    "2.6 Closures" 30
    "2.7 Local Functions" 34
    "2.8 Tail-Recursion" 35
    "2.9 Compilation" 37
    "2.10 Functions from Lists" 40
"Functional Programming" 41
    "3.1 Functional Design" 41
    "3.2 Imperative Outside-In" 46
    "3.3 Functional Interfaces" 48
    "3.4 Interactive Programming" 50
[--snip--]
```
which can be directly imported to the PDF file using `pdftocio`,

```sh
$ pdftocgen in.pdf < recipe.toml | pdftocio -o out.pdf in.pdf
```

Or if you want to edit the table of contents before importing it,

```sh
$ pdftocgen in.pdf < recipe.toml > toc
$ vim toc # edit
$ pdftocio in.pdf < toc
```

Each of the three programs has some extra functionalities. Use the `-h` option
to see all the options you could pass in.

Development
-----------

If you want to modify the source code or contribute anything, first install
[`poetry`][poetry], which is a dependency and package manager for Python used
by pdf.tocgen. Then run

```sh
$ poetry install
```
in the root directory of this repository to set up development dependencies.

If you want to test the development version of pdf.tocgen, use the `poetry run` command:

```sh
$ poetry run pdfxmeta in.pdf "pattern"
```
Alternatively, you could also use the

```sh
$ poetry shell
```
command to open up a virtual environment and run the development version
directly:

```sh
(pdf.tocgen) $ pdfxmeta in.pdf "pattern"
```

Before you send a patch or pull request, make sure the unit test passes by
running:

```sh
$ make test
```

License
-------

pdf.tocgen is free software. The source code of pdf.tocgen is licensed under
the GNU GPLv3 license.

pdf.tocgen is based on [PyMuPDF][pymupdf], licensed under the GNU GPLv3
license, which is again based on [MuPDF][mupdf], licensed under the GNU AGPLv3
license. A copy of the AGPLv3 license is included in the repository.

If you want to make any derivatives based on this project, please follow the
terms of the GNU GPLv3 license.

[tocgen]: https://krasjet.com/voice/pdf.tocgen/
[unix]: https://en.wikipedia.org/wiki/Unix_philosophy
[ex]: https://krasjet.com/voice/pdf.tocgen/#a-worked-example
[poetry]: https://python-poetry.org/
[pymupdf]: https://github.com/pymupdf/PyMuPDF
[mupdf]: https://mupdf.com/docs/index.html
