.DEFAULT_GOAL := test

test:
	black .
	pytest
.PHONY:test