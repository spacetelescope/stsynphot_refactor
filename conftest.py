try:
    from pytest_astropy_header.display import (PYTEST_HEADER_MODULES,
                                               TESTED_VERSIONS)
except ImportError:
    PYTEST_HEADER_MODULES = {}
    TESTED_VERSIONS = {}

try:
    from stsynphot import __version__ as version
except ImportError:
    version = 'unknown'

from astropy.utils import minversion
NUMPY_LT_2_0 = not minversion("numpy", "2.0.dev")
if not NUMPY_LT_2_0:
    import numpy as np
    np.set_printoptions(legacy="1.25")

# Uncomment and customize the following lines to add/remove entries
# from the list of packages for which version numbers are displayed
# when running the tests.
PYTEST_HEADER_MODULES['beautifulsoup4'] = 'bs4'
PYTEST_HEADER_MODULES['astropy'] = 'astropy'
PYTEST_HEADER_MODULES['synphot'] = 'synphot'
PYTEST_HEADER_MODULES.pop('h5py', None)
PYTEST_HEADER_MODULES.pop('Pandas', None)

TESTED_VERSIONS['stsynphot'] = version
