django-reports-admin
====================

.. image:: https://badge.fury.io/py/django-reports-admin.svg
    :target: http://badge.fury.io/py/django-reports-admin

A Django Admin add-on which adds functionality to export data in customised
forms of output.

Requirements
------------

Django Reports Admin requires ``Django 2.2.21`` or later, and is written
for ``Python 3.6`` or later.

Installation
------------

**NOTE:** Although enabled by default, you’ll want to ensure that
``django.contrib.contenttypes`` is within ``INSTALLED_APPS``.

.. code:: sh

   pip install django-reports-admin

Then, amend your Django ``settings.INSTALLED_APPS``:

.. code:: python

   INSTALLED_APPS = (
       ...
       'reports',
       ...
   )

Usage
-----

Creating reports requires subclassing the ``ModelReport`` class and
identifying a report. This can be done with a few lines of code if you
simply want to extract the admin list view for verbatim. For example:

.. code:: python

   # This file can be named anything, but it lives well within the admin.py or
   # models.py as it'll ensure your register() command is run.
   # yourapp/reports.py -- This file can be named anything

   from reports.base import ModelReport

   class MyReport(ModelReport)
       name = "Report - My Report"

Then, register the ``ModelReport`` against a model:

.. code:: python

   # yourapp/admin.py

   from .reports import MyReport
   from .models import MyModel

   reports.register(MyModel, MyReport)

Upon registration, you’ll see a new action with the Django Admin for
that Model, with whatever name you’ve provided in the ``name``
attribute.

For advanced report modification, subclass the following functions
within your ``ModelReport`` class:

``get_field_lookups`` returns a list of column name-value/callback
tuples. This function is a great way to modify the columns of the
report, and the exact output of each field. It is useful if you wish to
create a calculated field, or format a date field.

``get_row_data`` returns a dictionary of the data to be entered for each
row. Generally you should not need to modify this as
``get_field_lookups`` will be sufficient.

``generate_output`` can be modified to adjust the type of output. By
default, a CSV file is generated.

Usage In Shell And Tests
------------------------

It may be useful for you to test a report via code, either as a test or
a quick shell script. This is done without much stress:

.. code:: python

   # Assuming a defined ModelReport
   from reports.base import ModelReport
   from .models import MyModel

   class MyReport(ModelReport):
       queryset = MyModel.objects.all()

   # Instantiate the report, and run it through various means

   report = MyReport()

   # Create a SavedReport instance
   report.run_report()

   # Raw output of the report (as CSV, by default)
   report.generate_output()

   # Output list of OrderedDicts
   report.collect_data()

Testing
-------

Tests are run using ``pytest``, and the test suite can be executed using
the MakeFile

.. code:: sh

   make test
