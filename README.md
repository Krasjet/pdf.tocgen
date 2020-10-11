[pdf.tocgen][tocgen]
==========

[![PyPI](https://img.shields.io/pypi/v/pdf.tocgen)](https://pypi.org/project/pdf.tocgen/)
[![build](https://github.com/Krasjet/pdf.tocgen/workflows/build/badge.svg?branch=master)](https://github.com/Krasjet/pdf.tocgen/actions?query=workflow%3Abuild)

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

pdf.tocgen is written in Python 3. It is known to work with Python 3.7 to 3.9
on Linux, Windows, and macOS (On BSDs, you probably need to build PyMuPDF
yourself). Use

```sh
$ pip install -U pdf.tocgen
```
to install the latest version systemwide. Alternatively, use [pipx][pipx] or

```sh
$ pip install -U --user pdf.tocgen
```
to install it for the current user. I would recommend the latter approach to
avoid messing up the package manager on your system.

If you are using an Arch-based Linux distro, the package is also available on
[AUR][aur]. It can be installed using any AUR helper, for example [`yay`][yay]:

```{.console .codein}
$ yay -S pdf.tocgen
```

[pipx]: https://pipxproject.github.io/pipx/
[aur]: https://aur.archlinux.org/packages/pdf.tocgen/
[yay]: https://github.com/Jguer/yay

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

First, use `pdfxmeta` to search for the metadata of headings, and generate
**heading filters** using the automatic setting

```sh
$ pdfxmeta -p page -a 1 in.pdf "Section" >> recipe.toml
$ pdfxmeta -p page -a 2 in.pdf "Subsection" >> recipe.toml
```
The output `recipe.toml` file would contain several heading filters, each of
which specifies the attribute of a heading at a particular level should have.

An example recipe file would look like this:

```toml
[[heading]]
level = 1
greedy = true
font.name = "Times-Bold"
font.size = 19.92530059814453

[[heading]]
level = 2
greedy = true
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

Command examples
----------------

Because of the modularity of design, each program is useful on its own, despite
being part of the pipeline. This section will provide some more examples on how
you could use them. Feel free to come up with more.

### `pdftocio`

`pdftocio` should best demonstrate this point, this program can do a lot on its
own.

To display existing table of contents in a PDF to `stdout`:

```console
$ pdftocio doc.pdf
"Level 1 heading 1" 1
    "Level 2 heading 1" 1
        "Level 3 heading 1" 2
        "Level 3 heading 2" 3
    "Level 2 heading 2" 4
"Level 1 heading 2" 5
```

To write existing table of contents in a PDF to a file named `toc`:

```console
$ pdftocio doc.pdf > toc
```

To write a `toc` file back to `doc.pdf`:

```console
$ pdftocio doc.pdf < toc
```

To specify the name of output PDF:

```console
$ pdftocio -o out.pdf doc.pdf < toc
```

To copy the table of contents from `doc1.pdf` to `doc2.pdf`:

```console
$ pdftocio doc1.pdf | pdftocio doc2.pdf
```

To print the table of contents for reading:

```console
$ pdftocio -H doc.pdf
Level 1 heading 1 ··· 1
    Level 2 heading 1 ··· 1
        Level 3 heading 1 ··· 2
        Level 3 heading 2 ··· 3
    Level 2 heading 2 ··· 4
Level 1 heading 2 ··· 5
```

### `pdftocgen`

If you have obtained an existing recipe `rcp.toml` for `doc.pdf`, you could
apply it and print the outline to `stdout` by

```console
$ pdftocio doc.pdf < rcp.toml
"Level 1 heading 1" 1
    "Level 2 heading 1" 1
        "Level 3 heading 1" 2
        "Level 3 heading 2" 3
    "Level 2 heading 2" 4
"Level 1 heading 2" 5
```

To output the table of contents to a file called `toc`:

```console
$ pdftocgen doc.pdf < rcp.toml > toc
```

To import the generated table of contents to the PDF file, and output
to `doc_out.pdf`:

```console
$ pdftocgen doc.pdf < rcp.toml | pdftocio -o doc_out.pdf doc.pdf
```

To print the generated table of contents for reading:

```console
$ pdftocgen -H doc.pdf < rcp.toml
Level 1 heading 1 ··· 1
    Level 2 heading 1 ··· 1
        Level 3 heading 1 ··· 2
        Level 3 heading 2 ··· 3
    Level 2 heading 2 ··· 4
Level 1 heading 2 ··· 5
```

If you want to include the vertical position in a page for each heading, use the
`-v` flag

```console
$ pdftocgen -v doc.pdf < rcp.toml
"Level 1 heading 1" 1 306.947998046875
    "Level 2 heading 1" 1 586.3488159179688
        "Level 3 heading 1" 2 586.5888061523438
        "Level 3 heading 2" 3 155.66879272460938
    "Level 2 heading 2" 4 435.8687744140625
"Level 1 heading 2" 5 380.78875732421875
```

`pdftocio` can understand the vertical position in the output to generate table
of contents entries that link to the exact position of the heading, instead of
the top of the page.

```console
$ pdftocgen -v doc.pdf < rcp.toml | pdftocio doc.pdf
```

Note that the default output of `pdftocio` here is `doc_out.pdf`.

### `pdfxmeta`

To search for `Anaphoric` in the entire PDF:

```console
$ pdfxmeta onlisp.pdf "Anaphoric"
14. Anaphoric Macros:
    font.name = "Times-Bold"
    font.size = 9.962599754333496
    font.color = 0x000000
    font.superscript = false
    font.italic = false
    font.serif = true
    font.monospace = false
    font.bold = true
    bbox.left = 308.6400146484375
    bbox.top = 307.1490478515625
    bbox.right = 404.33282470703125
    bbox.bottom = 320.9472351074219
[--snip--]
```

To output the result as a heading filter with the automatic settings,

```console
$ pdfxmeta -a 1 onlisp.pdf "Anaphoric"
[[heading]]
# 14. Anaphoric Macros
level = 1
greedy = true
font.name = "Times-Bold"
font.size = 9.962599754333496
# font.size_tolerance = 1e-5
# font.color = 0x000000
# font.superscript = false
# font.italic = false
# font.serif = true
# font.monospace = false
# font.bold = true
# bbox.left = 308.6400146484375
# bbox.top = 307.1490478515625
# bbox.right = 404.33282470703125
# bbox.bottom = 320.9472351074219
# bbox.tolerance = 1e-5
[--snip--]
```
which can be directly write to a recipe file:

```console
$ pdfxmeta -a 1 onlisp.pdf "Anaphoric" >> recipe.toml
```

To case-insensitive search for `Anaphoric` in the entire PDF:

```console
$ pdfxmeta -i onlisp.pdf "Anaphoric"
to compile-time. Chapter 14 introduces anaphoric macros, which allow you to:
    font.name = "Times-Roman"
    font.size = 9.962599754333496
    font.color = 0x000000
    font.superscript = false
    font.italic = false
    font.serif = true
    font.monospace = false
    font.bold = false
    bbox.left = 138.60000610351562
    bbox.top = 295.6583557128906
    bbox.right = 459.0260009765625
    bbox.bottom = 308.948486328125
[--snip--]
```

Use regular expression to case-insensitive search search for `Anaphoric` in the
entire PDF:

```console
$ pdfxmeta onlisp.pdf "[Aa]naphoric"
to compile-time. Chapter 14 introduces anaphoric macros, which allow you to:
    font.name = "Times-Roman"
    font.size = 9.962599754333496
    font.color = 0x000000
    font.superscript = false
    font.italic = false
    font.serif = true
    font.monospace = false
    font.bold = false
    bbox.left = 138.60000610351562
    bbox.top = 295.6583557128906
    bbox.right = 459.0260009765625
    bbox.bottom = 308.948486328125
[--snip--]
```

To search only on page 203:

```console
$ pdfxmeta -p 203 onlisp.pdf "anaphoric"
anaphoric if, called:
    font.name = "Times-Roman"
    font.size = 9.962599754333496
    font.color = 0x000000
    font.superscript = false
    font.italic = false
    font.serif = true
    font.monospace = false
    font.bold = false
    bbox.left = 138.60000610351562
    bbox.top = 283.17822265625
    bbox.right = 214.81094360351562
    bbox.bottom = 296.4683532714844
[--snip--]
```

To dump the entire page of 203:

```console
$ pdfxmeta -p 203 onlisp.pdf
190:
    font.name = "Times-Roman"
    font.size = 9.962599754333496
    font.color = 0x000000
    font.superscript = false
    font.italic = false
    font.serif = true
    font.monospace = false
    font.bold = false
    bbox.left = 138.60000610351562
    bbox.top = 126.09941101074219
    bbox.right = 153.54388427734375
    bbox.bottom = 139.38951110839844
[--snip--]
```

To dump the entire PDF document:

```console
$ pdfxmeta onlisp.pdf
i:
    font.name = "Times-Roman"
    font.size = 9.962599754333496
    font.color = 0x000000
    font.superscript = false
    font.italic = false
    font.serif = true
    font.monospace = false
    font.bold = false
    bbox.left = 458.0400085449219
    bbox.top = 126.09941101074219
    bbox.right = 460.8096008300781
    bbox.bottom = 139.38951110839844
[--snip--]
```

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

GUI front end
-------------

If you are a Emacs user, you could install Daniel Nicolai's [toc-mode][tocmode]
package as a GUI front end for pdf.tocgen, though it offers many more
functionalities, such as extracting (printed) table of contents from a PDF
file. Note that it uses pdf.tocgen under the hood, so you still need to install
pdf.tocgen before using toc-mode as a front end for pdf.tocgen.

License
-------

pdf.tocgen itself a is free software. The source code of pdf.tocgen is licensed
under the GNU GPLv3 license. However, the recipes in the `recipes` directory is
separately licensed under the [CC BY-NC-SA 4.0 License][cc] to prevent any
commercial usage, and thus not included in the distribution.

pdf.tocgen is based on [PyMuPDF][pymupdf], licensed under the GNU GPLv3
license, which is again based on [MuPDF][mupdf], licensed under the GNU AGPLv3
license. A copy of the AGPLv3 license is included in the repository.

If you want to make any derivatives based on this project, please follow the
terms of the GNU GPLv3 license.

Support
-------

Even though pdf.tocgen is free to use and free to tinker with, I do accept
[donations][donate] if you find this tool useful and want to support me and
this project in any means, though I won't promise to prioritize your feature
requests or suggestions.

[tocgen]: https://krasjet.com/voice/pdf.tocgen/
[unix]: https://en.wikipedia.org/wiki/Unix_philosophy
[ex]: https://krasjet.com/voice/pdf.tocgen/#a-worked-example
[poetry]: https://python-poetry.org/
[pymupdf]: https://github.com/pymupdf/PyMuPDF
[mupdf]: https://mupdf.com/docs/index.html
[cc]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[donate]: https://krasjet.com/life.sustainer/
[tocmode]: https://github.com/dalanicolai/toc-mode
