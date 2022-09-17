.DEFAULT_GOAL := test

test:
	black .
	coverage run -m pytest
	coverage report -m
.PHONY:test