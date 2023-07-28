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

requirements:
	pip freeze > requirements.txt
.PHONY: requirements

unit:
	python -m coverage run -m unittest
	python -m coverage report
	python -m coverage html
.PHONY: unit

integration-coverage:
	coverage run -m pytest
	coverage html
.PHONY: integration-coverage
