.PHONY: clean-dist clean-pyc clean

# version variable
VERSION := $(shell python setup.py --version)

all: version help

version:
	@echo " gapipy.__version__ == $(VERSION)"
	@echo

help:
	@echo " Make targets"
	@echo
	@echo " * clean-dist - remove dist artifacts"
	@echo " * clean-pyc   - remove Python file artifacts"
	@echo " * dist        - package"
	@echo " * help        - print this targets list"
	@echo " * release     - package and upload a release"
	@echo " * test        - run tests quickly with the default Python"
	@echo " * version     - print the current value of reports.__version__"
	@echo

clean: clean-dist clean-pyc

clean-dist:
	@rm -fr dist/
	@rm -fr *.egg-info

clean-pyc:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +

test:
	pytest --ds=tests.testapp.settings -v

dist: clean
	@python setup.py -q sdist
	@ls -l dist
	@twine check dist/django-reports-admin-${VERSION}.tar.gz

release: clean
	@python setup.py -q sdist
	@twine upload dist/django-reports-admin-$(VERSION).tar.gz
