"""This module contains ACS/SBC commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/acs/test3.py``
(last few tests).

.. note::

    ``astrolib/pysynphot/from_commissioning/acs/test4.py`` was disabled.
    Therefore, Test622 to Test 657 were not ported over.

"""

# LOCAL
from ..utils import CommCase


class Test619(CommCase):
    obsmode = 'acs,sbc,f115lp'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test620(Test619):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.5e-16,flam)'


class Test621(Test619):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'
