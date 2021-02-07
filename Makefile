.PHONY: clean-dev clean-dist clean-pyc clean

# other variables
VERSION := $(shell python setup.py --version)
VENV_DIR := ./.venv

all: version help

version:
	@echo "reports.__version__ == $(VERSION)"
	@echo

help:
	@echo " Make targets"
	@echo
	@echo " * clean-dev  - remove $(VENV_DIR)"
	@echo " * clean-dist - remove dist artifacts"
	@echo " * clean-pyc  - remove Python file artifacts"
	@echo " * dev        - setup the dev environment"
	@echo " * dist       - package"
	@echo " * help       - print this targets list"
	@echo " * release    - package and upload a release"
	@echo " * test       - run tests quickly with the default Python"
	@echo " * version    - print the current value of reports.__version__"
	@echo

clean: clean-dist clean-pyc

clean-dev:
	@rm -fr $(VENV_DIR)

clean-dist:
	@rm -fr dist/
	@rm -fr *.egg-info

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

dev:
	@python3 -m venv $(VENV_DIR)
	@. $(VENV_DIR)/bin/activate
	@pip install -r requirements-dev.txt

dist: clean
	@python setup.py -q sdist
	@ls -l dist
	@twine check dist/django-reports-admin-${VERSION}.tar.gz

release: clean
	@python setup.py -q sdist
	@twine upload dist/django-reports-admin-$(VERSION).tar.gz

test:
	pytest --ds=tests.testapp.settings -v
