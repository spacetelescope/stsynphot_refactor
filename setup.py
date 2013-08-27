#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    use_2to3=True,
    zip_safe=False
)
