# django-reports-admin

A Django Admin add-on which adds functionality to export data in customized forms of output,

## Requirements

Django Reports Admin requires Django 1.10 or later, and is written for Python 3.5 or later.

## Installation

    pip install django-reports-admin

Then, amend your Django `settings.py` file:

    INSTALLED_APPS = (
      ...
      'reports',
      ...
    )

Although enabled by default, you'll want to ensure
`django.contrib.contenttypes`` is within `INSTALLED_APPS`.

## Testing

Tests are run using `pytest`, and the test suite can be executed using the
MakeFile

    make test
