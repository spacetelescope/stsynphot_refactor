# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os
from astropy.tests.runner import TestRunner

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''

# Create the test function for self test
test = TestRunner.make_test_runner_in(os.path.dirname(__file__))
test.__test__ = False

# STSYNPHOT UI
from .config import getref, showref, conf  # noqa
from .spectrum import band, ebmvx, Vega  # noqa
from .catalog import grid_to_spec  # noqa
from .spparser import parse_spec  # noqa

# Clean up namespace
del os
del TestRunner
