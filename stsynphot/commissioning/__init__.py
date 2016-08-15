# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This sub-package is for commisioning tests.

.. note::

    Tests require ASTROLIB PYSYNPHOT to be installed.
    Specifically, install the version to be compared against ``stsynphot``.

To run only the commissioning tests from source checkout::

    cd ../..
    python setup.py test -P commissioning --args="--slow" --remote-data

To run only the commissioning tests from a Python session::

    >>> import stsynphot
    >>> stsynphot.test('commissioning', args='--slow', remote_data=True)

"""
from __future__ import absolute_import, division, print_function

from . import utils  # noqa
