.DEFAULT_GOAL := test

test:
	black .
	PYTHONPATH=./src coverage run -m pytest
	PYTHONPATH=./src coverage report -m
.PHONY:test