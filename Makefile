# As a workaround to [1], we will use a makefile instead
# [1]: https://github.com/python-poetry/poetry/issues/241

.PHONY: install test

test: # run tests
	poetry run python -m unittest discover

install: # set up dependencies
	poetry install
