SHELL := /bin/bash

venv-create:
	python -m venv .venv
.PHONY: venv-create

venv-activate:
	. .venv/bin/activate
.PHONY: venv-activate

serve:
	flask --app index run
.PHONY: serve

next:
	flask --app next run --debug
.PHONY: next

dump-requirements:
	pip freeze > requirements.txt
.PHONY: dump-requirements

unit-coverage:
	python -m coverage run -m unittest
	python -m coverage report
	python -m coverage html
.PHONY: unit-coverage