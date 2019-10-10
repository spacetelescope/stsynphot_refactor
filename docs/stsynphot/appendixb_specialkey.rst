.. include:: appb_ref.txt

.. _stsynphot-appendixb-special-keywords:

Special Keywords
================

This section contains special keywords that apply to multiple instruments.


.. _stsynphot-ota:

OTA
---

The HST OTA transmissivity is included by default in the calculation of
all HST-related observation modes. It can be included or excluded explicitly by
adding the keywords ``ota`` or ``noota``, respectively; For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('stis,ccd,f25srf2,noota')  # doctest: +SKIP


.. _stsynphot-costar:

COSTAR
------

An observation mode that involves a first-generation instrument
(:ref:`stsynphot-appendixb-foc`, :ref:`stsynphot-appendixb-fos`, or
:ref:`stsynphot-appendixb-ghrs`) also automatically accounts for the effects of
COSTAR on its wavelength-dependent sensitivity. This includes the product of
the reflectivity curves for each pair of the COSTAR mirrors for each of these
instruments, as well as the effects on instrument throughput and
sensitivity due to the improved point-spread function that is achieved
with COSTAR.

Like the :ref:`stsynphot-ota`, the COSTAR effects on bandpass and
count rates are included by default for these instruments when using versions
of the HST graph table created on or after February 24, 1995. In earlier
versions of the graph table, ``nocostar`` is the default. To explicitly include
or exclude COSTAR, use the keywords ``costar`` and ``nocostar``, respectively,
anywhere within your observation mode string; For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('fos,red,4.3,g270h,costar')  # doctest: +SKIP

All current HST instruments (except :ref:`stsynphot-appendixb-fgs`) have
built-in corrective optics to compensate for the spherical aberration of the
primary mirror. It is not necessary to explicitly exclude COSTAR for the
current generation instruments, as it is excluded by default.
Inclusion of COSTAR for these instruments are not allowed.


.. _stsynphot-parameterized-mjd:

MJD
---

In the case of :ref:`stsynphot-appendixb-acs`, :ref:`stsynphot-appendixb-cos`,
:ref:`stsynphot-appendixb-stis`, and :ref:`stsynphot-appendixb-wfc3`,
the ``mjd`` keyword is used to handle time-dependent sensitivity of certain
detectors. To use this capability in simulations, include ``mjd#ddddd`` in the
``obsmode`` string, where ``ddddd`` is the desired Modified Julian Date (MJD)
value, which could be an integer or a floating point.

**stsynphot** interpolates between the dates for which data exist in the table
to arrive at an estimate of the throughput on the requested date
(see :ref:`stsynphot-parameterized`). For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('acs,wfc1,f555w,mjd#49486')  # doctest: +SKIP

If not specified, the default is to use
the latest set of throughput values in the ``THROUGHPUT`` column without any
interpolation or extrapolation.
This default column is expected to be updated by the relevant instrument team
whenever significant changes to the current trend are identified, such that the
throughput should not differ by more than 2% from the one obtained by using the
current date.


.. _stsynphot-parameterized-aper:

Encircled Energy
----------------

For :ref:`stsynphot-appendixb-acs` and :ref:`stsynphot-appendixb-wfc3`,
the ``aper`` keyword is used to specify a circular aperture, given by its
radius in arcseconds, to calculate the source counts within.
If no aperture is given, calculations are done for an infinite aperture, which
is also 5.5 arcsec or larger for ACS, and 2 arcsec or larger for WFC3.

This enables **stsynphot** to be more flexible and accurate, particularly for
cases where red targets are observed at long wavelengths.
At wavelengths greater than 7500 Angstrom (for ACS/HRC) and about
9000 Angstrom (for ACS/WFC), the observations are affected by a
red halo due to light scattered off the CCD substrate. An increasing
fraction of the light as a function of wavelength is scattered
from the center of the PSF into the wings. This problem affects
particularly the very broad *z*-band F850LP filter, for which the
encircled energy (EE) depends on the underlying spectral energy
distribution the most.

Supported apertures are instrument-dependent, as listed below.
Arbitrary aperture sizes are permitted, but not recommended.
This is because **stsynphot** only provides a linear interpolation between
supported apertures (see :ref:`stsynphot-parameterized`), which is a poor
approximation, especially at small apertures.

For ACS, the following apertures are supported:

* every 0.1 arcsec between 0 and 0.6 arcsec
* 0.8 arcsec
* 1.0 arcsec
* 1.5 arcsec
* 2.0 arcsec
* 4.0 arcsec

For WFC3, the following apertures are supported:

* every 0.05 arcsec between 0.1 and 0.3 arcsec
* every 0.1 arcsec between 0.3 and 0.6 arcsec
* 0.8 arcsec
* 1.0 arcsec
* 1.5 arcsec
* 2.0 arcsec

To use this capability in simulations, include ``aper#value`` in the
``obsmode`` string, where ``value`` is the radius in arcseconds.
When "aper#0" is specified, the user will obtain the number of counts in the
brightest pixel (i.e., the peak counts of the source centered at that pixel).
For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('acs,wfc1,f850lp,aper#0.2')  # doctest: +SKIP


.. _stsynphot-parameterized-temperature:

Temperature
-----------

For :ref:`stsynphot-appendixb-nicmos` and :ref:`stsynphot-appendixb-wfc3`
IR detectors, :ref:`thermal background <stsynphot-command-therm>`
can be calculated by **stsynphot**. If no temperature is specified, the default
value for each component is used (see :ref:`stsynphot_thermal_em` and
:ref:`stsynphot-parameterized`).

For WFC3, the calculation can only be done at the default temperature
(not yet parameterized). For observation modes using a grism, the ``bkg``
keyword is used to perform throughput and emission calculations pertaining to
the associated background signal. This is because in grism observations,
a given detector pixel will receive source signal from only a small wavelength
interval of the dispersed source spectrum, but it will receive background
signal from the entire bandpass of the grism. Therefore, a special throughput
table is used to correctly compute the detected signal from a background
spectrum, which gives the transmission of the grism over its entire bandpass.
The ``bkg`` keyword cannot be used with non-grism observations. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfc3,ir,g102,bkg')  # doctest: +SKIP

For NICMOS, all keywords except the detector are parameterized for
temperature. This includes OTA components that are opaque but thermally
emitting. Most of the its optical elements (``reimag``, ``pupil``, ``image``,
``para1``, ``para2``, ``bend``, ``dewar``, and ``cmask``) are contained in the
dewar, and are therefore at the same temperature. However, **stsynphot** does
not enforce this, so the user must specify any non-default temperature for each
component individually. For example, to specify a primary mirror temperature of
290 K and then calculate the thermal background:

    >>> bp = stsyn.band('nicmos,3,f222m,primary#290.0')  # doctest: +SKIP
    >>> bp.thermback()  # doctest: +SKIP
    <Quantity 82.29150427454572 ct / (pix s)>


.. _stsynphot-parameterized-contamination:

Contamination
-------------

The ``cont#`` keyword for :ref:`stsynphot-appendixb-wfpc1` and
:ref:`stsynphot-appendixb-wfpc2` references the Modified Julian Date,
which is used to account for the gradual decline in throughput between
decontamination events, as well as for the sudden increase in throughput
immediately after a decontamination.

For WF/PC-1, data exists for dates between May 8, 1991 (MJD 48384) and
December 8, 1993 (MJD 49329), non-inclusive, in the intervals of 20-30 days.
For WFPC2, data currently exists from December 26, 1993 (MJD 49347) until SM4,
in intervals of approximately 30 days.

**stsynphot** interpolates between the dates for which data exist in the table
to arrive at an estimate of the throughput on the requested date
(see :ref:`stsynphot-parameterized`). For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfpc2,3,f555w,cont#49800')  # doctest: +SKIP
