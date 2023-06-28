SHELL := /bin/bash

serve:
	. .venv/bin/activate && flask --app index run
.PHONY: serve


dump-requirements:
	. .venv/bin/activate && pip freeze > requirements.txt
.PHONY: dump-requirements
