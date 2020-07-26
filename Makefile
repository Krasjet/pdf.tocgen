# As a workaround to [1], we will use a makefile instead
# [1]: https://github.com/python-poetry/poetry/issues/241

.PHONY: install test

test: # run tests
	@poetry run mamba --format=documentation ./spec

xmeta-demo: # a demo of pdfxmeta
	poetry run pdfxmeta ./tests/files/level2.pdf "Section"

install: # set up dependencies
	poetry install --no-dev
