# As a workaround to [1], we will use a makefile instead
# [1]: https://github.com/python-poetry/poetry/issues/241

.PHONY: install test xmeta-demo lint

test: # run tests
	@poetry run mamba --format=documentation ./spec

lint: # run lint
	@poetry run pylint ./spec ./pdfxmeta ./pdftocgen ./fitzutils

xmeta-demo: # a demo of pdfxmeta
	@poetry run pdfxmeta ./spec/files/level2.pdf "Section"

install: # set up dependencies
	poetry install --no-dev
