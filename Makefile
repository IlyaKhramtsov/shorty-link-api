PYTHON = python3

.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To run the project type make run"
	@echo "To test the project type make test"
	@echo "------------------------------------"

run:
	${PYTHON} manage.py runserver
test:
	${PYTHON} manage.py test shortener.tests

.PHONY: help test run