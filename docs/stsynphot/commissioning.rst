.. _stsynphot_comm_report:

Commissioning Report
====================

.. |comm_ver| replace:: 0.1b2

.. note::

    Some results may change as codes (be it this package, ASTROLIB, or their
    dependencies) change. It is recommended that the commissioning tests be
    re-run from time to time and this report updated accordingly, as needed.

This report covers the commissioning tests of **stsynphot** against
ASTROLIB PYSYNPHOT. Given that ASTROLIB PYSYNPHOT was tested against
IRAF SYNPHOT in :ref:`TSR 2009-01 (Laidler 2009) <stsynphot-ref-laidler2009>`,
we can infer that any agreement to ASTROLIB PYSYNPHOT is also an agreement
with IRAF SYNPHOT.

As **stsynphot** is not a straight port from ASTROLIB nor IRAF, but rather
a new implementation designed to use `astropy.modeling`, a 100% agreement
between the difference software is impossible. However, an extensive
commissioning process was performed to verify that the results
produced by **stsynphot** are either as good as, or better than, the results
obtained using ASTROLIB PYSYNPHOT for the same calculations.

This runs all the commissioning tests in addition to regular unit tests::

    pytest --pyargs stsynphot docs --remote-data --slow --html=/path/to/report.html

Since this involves detail comparison with ASTROLIB PYSYNPHOT using various
spectra and observing modes, it is important that the tests have access to the
ASTROLIB software and :ref:`stsynphot-crds-overview`.
Here are the
`commissioning test results <http://ssb.stsci.edu/stsynphot/report.html>`_
(might take time to load as it contains results for over 10,000 tests) for the
following software versions:

* **stsynphot** |comm_ver|
* **synphot** |comm_ver|
* ASTROLIB PYSYNPHOT 0.9.8.5
* Astropy 1.3
* Scipy 0.17.1
* Numpy 1.11.1
* Python 3.5.2
* pytest (version not recorded)
* pytest-html (version not recorded)

To ensure repeatability, the graph and component tables are fixed at a specific
version, as follows. Since we are only testing for software agreement, the fact
that these tables might be outdated is irrelevant:

* 07r1502mm_tmg.fits
* 07r1502nm_tmc.fits
* tae17277m_tmt.fits

Tests were only written for HST instruments that are currently active, i.e,
ACS (HRC, SBC, and WFC), STIS (CCD, FUV-MAMA, and NUV-MAMA), and WFC3 (IR,
UVIS-1, and UVIS-2). The specific observing modes tested were ported directly
from ASTROLIB's commissioning tests against IRAF. Reddening laws that are no
longer supported (e.g., ``gal1``) were replaced with something else that were
similar (e.g., ``gal3``); This should not affect the integrity of the tests as
both software under test use the same reddening law anyway.

For each observing mode, the wavelength set and flux/throughput in internal
units (Angstrom and PHOTLAM) were compared for all bandpass, source spectrum,
and observation involved. Exceptions are made for known differences,
for instance, when ASTROLIB uses an arbitrary default ``waveset`` while Astropy
does not (those comparisons are skipped).
For an observation, its count rate and effective wavelength were also compared.
When applicable, bandpass thermal source and background count rate were
compared as well.

For **stysnphot** |comm_ver|, a total of 10,026 tests were run and only 160
(1.6%) failures found. All the failures are understood and explained below:

* Astropy models computed very small flux values, while ASTROLIB set those to
  zeroes. This is especially true for blackbody source, for which ASTROLIB
  has some IRAF-like (32-bit) "rounding to zero" behaviors.
* Both Astropy and ASTROLIB models computed very small flux values
  (anywhere from 1.8E-26 to 2E-311 PHOTLAM) but they are not within 1%
  agreement. This is not surprising given that 1% of such small values is
  too small to be realistic for comparison.
* Expected source spectrum ``waveset`` differences between Astropy and ASTROLIB
  for blackbody and flat source spectra. In **stynphot**, the former model
  includes more "tail" region, while the latter does not use arbitrary default
  ``waveset`` anymore.
* Thermal source calculations in **stsynphot** has a different (and arguably
  better) sampling, resulting in flux values that do not agree with ASTROLIB
  within 1%. Despite this, thermal background results still agree.

In conclusion, these commissioning tests have shown that **synphot** and
**stsynphot** are robust enough to replace ASTROLIB PYSYNPHOT and IRAF SYNPHOT
for most cases.


Future Work
-----------

Here are some possible follow-up action items for this commissioning test
report:

#. Instrument teams, who wish to utilize **stsynphot** for their
   Exposure Time Calculators, should independently run comparison tests
   for the observing modes and the source spectra that are relevant to them.
   Using those results and the information provided here, they should decide
   for themselves whether this software is good enough for their needs.
#. The known failures reported here may be revisited so that they could be
   quantified and understood further. More understanding could result in code
   changes that would lead to even better agreement.
