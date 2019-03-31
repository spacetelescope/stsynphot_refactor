# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This sub-package is for commisioning tests.

.. note::

    Tests require ASTROLIB PYSYNPHOT to be installed.
    Specifically, install the version to be compared against ``stsynphot``.

To run only the commissioning tests from source checkout::

    cd ../..
    python setup.py test -P commissioning --remote-data --args="--slow"

Like above, but also use ``pytest-html`` plugin for a detail HTML report::

    python setup.py test -P commissioning --remote-data \
    --args="--slow --html=/full/path/report.html"

To generate the HTML report using ``py.test`` directly::

    py.test stsynphot/commissioning/tests/ --remote-data \
    --slow --html=report.html

To run only the commissioning tests from a Python session::

    >>> import stsynphot
    >>> stsynphot.test('commissioning', remote_data=True, args='--slow')

Like above, but also use ``pytest-html`` plugin for a detail HTML report::

    >>> stsynphot.test('commissioning', remote_data=True,
    ...                args='--slow --html="report.html"')

To rerun only failed tests from the last run, add ``--lf`` in the list of
``args`` above. This option requires ``pytest-cache`` (enabled by default)
and is useful for debugging.

"""

from . import utils  # noqa
