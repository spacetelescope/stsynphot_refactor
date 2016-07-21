# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This sub-package is for commisioning tests.

.. note::

    Tests require ASTROLIB PYSYNPHOT to be installed.
    Specifically, install the version to be compared against ``stsynphot``.

To run the tests from source checkout::

    cd ../..
    python setup.py test -P commissioning --remote-data

To run the tests from a Python session::

    >>> import stsynphot
    >>> stsynphot.test('commissioning', remote_data=True)

"""

try:
    import pysynphot  # ASTROLIB
except ImportError:
    HAS_PYSYNPHOT = False
else:
    HAS_PYSYNPHOT = True
