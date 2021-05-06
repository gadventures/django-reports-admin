#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import reports

readme = open("README.rst").read()
history = open("HISTORY.rst").read()

test_requirements = [
    "Django==2.2.21",
    "pytest==6.2.4",
    "pytest-django==4.2.0",
]

setup(
    name="django-reports-admin",
    version=reports.__version__,
    author=reports.__author__,
    description="A Django Admin add-on which adds functionality to export data in customized forms of output.",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author_email="software@gadventures.com",
    url="https://github.com/gadventures/django-reports-admin",
    packages=find_packages(),
    package_dir={"reports": "reports"},
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords="django reports admin",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    tests_require=test_requirements,
)
