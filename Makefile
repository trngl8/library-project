SHELL := /bin/bash

serve:
	flask --app index run
.PHONY: serve
