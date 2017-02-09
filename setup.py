#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import reports

readme = open('README.md').read()
history = open('HISTORY.md').read()

test_requirements = [
    'Django',
    'pytest',
    'pytest-django',
]

setup(
    name='django-reports-admin',
    version=reports.__version__,
    description='A Django Admin add-on which adds functionality to export data in customized forms of output.',
    long_description=readme + '\n\n' + history,
    author='G Adventures',
    author_email='software@gadventures.com',
    url='https://github.com/gadventures/django-reports-admin',
    packages=find_packages(),
    package_dir={'reports': 'reports'},
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='django reports admin',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=test_requirements,
)
