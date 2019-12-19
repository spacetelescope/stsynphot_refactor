# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This sub-package is for commisioning tests.

.. note::

    Tests require ASTROLIB PYSYNPHOT to be installed.
    Specifically, install the version to be compared against ``stsynphot``.

To run only the commissioning tests from source checkout::

    cd ../..
    pytest --pyargs stsynphot/commissioning --remote-data --slow

Like above, but also use ``pytest-html`` plugin for a detail HTML report::

    pytest --pyargs stsynphot/commissioning --remote-data --slow --html=/full/path/report.html

To rerun only failed tests from the last run, add ``--lf`` in the list of
``args`` above. This option requires ``pytest-cache`` (enabled by default)
and is useful for debugging.

"""  # noqa

from . import utils  # noqa
