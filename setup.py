#!/usr/bin/env python
'''
Sentry-Pivotal
=============
A Sentry plugin to add stories to Pivotal Tracker.

License
-------
Copyright 2012 Labbler, Inc

This file is part of Sentry-Pivotal.

Sentry-Pivotal is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sentry-Pivotal is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sentry-Pivotal.  If not, see <http://www.gnu.org/licenses/>.
'''
from setuptools import setup, find_packages

setup(
    name='sentry-pivotal',
    version='0.3.3',
    author='Labbler',
    author_email='dev@labbler.com',
    url='https://github.com/Labblersd/sentry-pivotal',
    description='Pivatal Tracker and Sentry friendship plugin.',
    long_description=__doc__,
    license='GPL',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pyvotal',
    ],
    entry_points={
        'sentry.plugins': [
            'pivotal = sentry_pivotal.plugin:PivotalStory'
        ]
    },
    include_package_data=True,
)
