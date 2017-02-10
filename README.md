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

## Usage

Creating reports requires subclassing the `ModelReport` class and identifying a
report. This can be done with a few lines of code if you simply want to extract
the admin list view for verbatim. For example:

    # This file can be named anything, but it lives well within the admin.py or
    # models.py as it'll ensure your register() command is run.
    # yourapp/reports.py -- This file can be named anything

    from reports.base import ModelReport

    class MyReport(ModelReport)
        name = "Report - My Report"

Then, register the `ModelReport` against a model:

    # yourapp/admin.py

    from .reports import MyReport
    from .models import MyModel

    reports.register(MyModel, MyReport)

Upon registration, you'll see a new action with the Django Admin for that Model,
with whatever name you've provided in the `name` attribute.

For advanced report modification, subclass the following functions within your
`ModelReport` class:

`get_field_lookups` returns a list of column name-value/callback tuples. This
function is a great way to modify the columns of the report, and the exact
output of each field. It is useful if you wish to create a calculated field, or
format a date field.

`get_row_data` returns a dictionary of the data to be entered for each row.
Generally you should not need to modify this as `get_field_lookups` will be
sufficient.

`generate_output` can be modified to adjust the type of output. By default, a
CSV file is generated.


## Testing

Tests are run using `pytest`, and the test suite can be executed using the
MakeFile

    make test
