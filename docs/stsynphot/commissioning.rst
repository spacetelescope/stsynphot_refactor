.. doctest-skip-all

.. _stsynphot_comm_report:

Commissioning Report
====================

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

Here are the
`commissioning test results <http://ssb.stsci.edu/stsynphot/report.html>`_
(might take time to load as it contains results for over 9800 tests).

TODO: Re-run tests using latest stable versions, state the versions tested,
explain the process and results, and update the link above to point to the
new report.
