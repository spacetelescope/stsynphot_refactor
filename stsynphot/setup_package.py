# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals


def get_package_data():
    return {
        str('stsynphot'): [
            str('data/*.txt'), str('data/*.dat'), str('data/wavecats/*.dat'),
            str('data/wavecats/*.txt')],
        str('stsynphot.tests'): [
            str('data/*.txt'), str('data/*.dat'), str('data/*.fits'),
            str('data/extinction/*fits')]}


def requires_2to3():
    return True
