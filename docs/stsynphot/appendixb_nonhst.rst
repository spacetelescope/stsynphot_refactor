.. include:: appb_ref.txt

.. _stsynphot-appendixb-nonhst:

Non-HST Filter Systems
======================

In addition to the HST instruments, filters, and gratings, the
graph table also contains entries for various
standard bandpass from photometric systems that are not specific to HST.
Actively supported systems (i.e., their data files are updated on CRDS as
needed) are as tabulated below.
Non-HST filters are specified using the name of the filter system,
followed by the desired band name. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('cousins,i')  # doctest: +SKIP
    >>> bp = stsyn.band('stromgren,u')  # doctest: +SKIP

If the name of the filter system is omitted for any of the common *UBVRIJHK*
filters, the defaults are Johnson *UBV*, Cousins *RI*, and Bessell *JHK*.
For example, the following are equivalent:

    >>> bp = stsyn.band('v')  # doctest: +SKIP
    >>> bp = stsyn.band('johnson,v')  # doctest: +SKIP

+------------------+-------------+
|System Name       |Band Name    |
+==================+=============+
||nonhst_cousins|  |r i          |
+------------------+-------------+
||nonhst_galex|    |nuv fuv      |
+------------------+-------------+
||nonhst_johnson|  |u v b r i j k|
+------------------+-------------+
||nonhst_landolt|  |u v b r i    |
+------------------+-------------+
||nonhst_sdss|     |u g r i z    |
+------------------+-------------+
||nonhst_stromgren||u v b y      |
+------------------+-------------+


.. _appb_nonhst_observed:

Comparison with Observed Non-HST Photometry
-------------------------------------------

There are two issues that are sometimes overlooked when comparing
synthetic photometry from **stsynphot** with observed photometry using a
non-HST system.

Firstly, one should be careful whether the throughput data have been
defined for a photon-counting or an energy-integrating detector.
**stsynphot** always assumes that a throughput are of the former.
In particular, some authors in the past have defined throughput curves
for photomultipliers as if these detectors were energy integrators,
which they are not. Such curves have to be converted into photon-counting
form before they can be correctly used by **stsynphot**
(:ref:`Maiz Apellaniz 2006 <stsynphot-ref-maiz2006>`).
Using the wrong definition can lead to errors of a few percent for
broad-band filters.

Secondly, many systems (e.g., Johnson *UBV*) use Vega
as a reference spectrum, but have been calibrated using secondary standards,
leading to the existence of finite zero points. In some systems
(e.g. Stromgren), those zero points are not even
close to 0.0 for some filters. The table below defines the zero point
corrections for ground-based filter systems from measurements of zero points
collected from the respective literature; These values should be added to the
VEGAMAG magnitude in **stsynphot** before they are compared with the
observed data:

+-------------------+-------------+----------+-------------+
|System             |Color/Index  |Zero point|References   |
|                   |             |(mag)     |             |
+===================+=============+==========+=============+
||nonhst_johnson2|  |:math:`V`    |0.026     ||bohlin2004| |
|and                +-------------+----------+-------------+
||nonhst_landolt2|  |:math:`B-V`  |0.010     ||maiz2006|   |
|                   +-------------+----------+-------------+
|                   |:math:`U-B`  |0.020     ||maiz2006|   |
+-------------------+-------------+----------+-------------+
||nonhst_cousins2|  |:math:`V-R`  |-0.012    ||holberg2006||
|and                +-------------+----------+-------------+
||nonhst_landolt2|  |:math:`V-I`  |-0.002    ||holberg2006||
+-------------------+-------------+----------+-------------+
||nonhst_stromgren2||:math:`y`    |0.038     ||holberg2006||
|                   +-------------+----------+-------------+
|                   |:math:`b-y`  |0.007     ||maiz2006|   |
|                   +-------------+----------+-------------+
|                   |:math:`m_{1}`|0.154     ||maiz2006|   |
|                   +-------------+----------+-------------+
|                   |:math:`c_{1}`|1.092     ||maiz2006|   |
+-------------------+-------------+----------+-------------+

The existence of these issues has led CRDS to divide the non-HST photometric
systems into supported (as mentioned above) and
:ref:`not supported <stsynphot-nonhst-deprecated>`.

Systems for which there are analyses in the literature that deal with
the issues mentioned above are as follow. CRDS Team is reasonably confident
that the possible systematic errors in the **stsynphot** results for these
systems are small:

* |nonhst_cousins2| *RI*
* |nonhst_johnson2| *UBV* (but not *RIJK*)
* |nonhst_landolt2| *UBVRI*
* :ref:`stsynphot-nonhst-sdss` *ugriz*
* |nonhst_stromgren2| *uvby*


.. _stsynphot-nonhst-2mass:

2MASS
-----

The 2MASS *JHK*:math:`_s` throughputs are taken from :ref:`Cohen et al. (2003) <stsynphot-ref-cohen2003>`.
These are normalized relative spectral response curves and include the throughputs of all of the 
appropriate optics from the 2MASS optical system, as well as the atmosphere above the two 2MASS
telescopes. 

Zero point reference fluxes for 2MASS reproduced from the 
`IPAC 2MASS website <https://old.ipac.caltech.edu/2mass/releases/allsky/doc/sec6_4a.html>`_ 
are included here for reference (pay special attention to the units):

+-----+--------------------+-----------------+---------------+-----------------------+
|Band |λ (µm)              |Bandwidth        |Fnu ref        |Flambda ref            |
|     |                    |(µm)             |(Jy)           |(W/cm^2/µm)            |
+=====+====================+=================+===============+=======================+
|J    |   1.235 ± 0.006    | 0.162 ± 0.001   | 1594 ± 27.8   | 3.129E-13 ± 5.464E-15 |
+-----+--------------------+-----------------+---------------+-----------------------+
|H    |   1.662 ± 0.009    | 0.251 ± 0.002   | 1024 ± 20.0   | 1.133E-13 ± 2.212E-15 |
+-----+--------------------+-----------------+---------------+-----------------------+
|Ks   |   2.159 ± 0.011    | 0.262 ± 0.002   | 666.7 ± 12.6  | 4.283E-14 ± 8.053E-16 |
+-----+--------------------+-----------------+---------------+-----------------------+

To use the 2MASS throughputs:

>>> import stsynphot as stsyn
>>> bp = stsyn.band('2mass,j')  # doctest: +SKIP
>>> bp = stsyn.band('2mass,h')  # doctest: +SKIP
>>> bp = stsyn.band('2mass,ks')  # doctest: +SKIP

(Note: 2MASS throughput curves were added to the TMG file in January 2020. Users must use
a TMG/TMC file and associated throughput tables delivered after this date to use the 
2MASS OBSMODEs.)



.. _stsynphot-nonhst-cousins:

Cousins
-------

The Cousins *RI* throughputs are taken from
:ref:`Bessell (1983) <stsynphot-ref-bessell1983>`. They have been transformed
into photon-counting form. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('cousins,i')  # doctest: +SKIP


.. _stsynphot-nonhst-galex:

GALEX
-----

The GALEX FUV and NUV throughputs were provided by Tom Barlow on
behalf of the `GALEX <http://www.galex.caltech.edu/>`_ project, as described in
:ref:`Morrissey et al. (2007) <stsynphot-ref-morrissey2007>`.
They were measured on the ground in units of effective area,
and were divided by the full area of the GALEX primary mirror
(:math:`1963.495 \; \text{cm}^{2}`) to convert them to the dimensionless
transmission values required by **stsynphot**. Therefore, these curves
represent the true total throughput, including obscuration by the secondary
mirror, reflectivity of the mirrors, sensitivity of the detector, and so forth.
For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('galex,fuv')  # doctest: +SKIP


.. _stsynphot-nonhst-johnson:

Johnson
-------

The throughput data for the Johnson *UBV* bands were obtained from
:ref:`Maiz Apellaniz (2006) <stsynphot-ref-maiz2006>`, while the *RIJK* bands
from :ref:`Johnson (1965) <stsynphot-ref-johnson1965>`. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('johnson,v')  # doctest: +SKIP


.. _stsynphot-nonhst-landolt:

Landolt
-------

The :ref:`Landolt (1983) <stsynphot-ref-landolt1983>` *UBVRI* system is made up
of the :ref:`stsynphot-nonhst-johnson` *UBV* and the
:ref:`stsynphot-nonhst-cousins` *RI* bandpass. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('landolt,v')  # doctest: +SKIP


.. _stsynphot-nonhst-sdss:

SDSS
----

The `Sloan Digital Sky Survey (SDSS) <https://www.sdss.org/>`_ *ugriz* filter
throughputs were provided by Sebastian Jester on behalf of the SDSS team,
as described in :ref:`Gunn et al. (2001) <stsynphot-ref-gunn2001>`.
The filter curves are shown in the
`SDSS filter response plot <http://classic.sdss.org/dr1/instruments/imager/index.html#filters>`_. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('sdss,g')  # doctest: +SKIP

The throughput data give the system photon response to point sources of the
2.5-m SDSS survey telescope, including extinction through an airmass of 1.3 at
`Apache Point Observatory <https://www.apo.nmsu.edu/>`_ (to which all SDSS
photometry is referenced).
Originally, the *ugriz* system was intended to be identical to the
:math:`u^{\prime} g^{\prime} r^{\prime} i^{\prime} z^{\prime}`
system described in :ref:`Fukugita et al. (1996) <stsynphot-ref-fukugita1996>`
and defined by the standard star system in
:ref:`Smith et al. (2002) <stsynphot-ref-smith2002>`. However, in the course
of processing the SDSS data, an unpleasant discovery was made that
the filters in the 2.5-m telescope have significantly different
effective wavelengths from the filters in the
`USNO <https://en.wikipedia.org/wiki/United_States_Naval_Observatory>`_ telescope, which was used to observe
the :math:`u^{\prime} g^{\prime} r^{\prime} i^{\prime} z^{\prime}`
standards; The difference originates from the USNO filters being exposed to
ambient air, while the survey-telescope filters live in the vacuum of the
survey camera. Therefore, it became necessary to distinguish between the primed
and unprimed SDSS filter sets.

The response curves in *r* and *i* are slightly different for
large extended sources (larger than about 80 pixels in size)
because the extended IR scattering wings in these bands,
which do not affect the photometry of point sources, begin to be
included. The modified curves are shown in an
`updated SDSS system response plot <http://classic.sdss.org/dr3/instruments/imager/#filters>`_.

The SDSS photometry is intended to be on the AB system
(:ref:`Oke & Gunn 1983 <stsynphot-ref-oke1983>`), by which a 0-magnitude object
should have the same counts as a source of
:math:`F_{\nu} = 3631 \; \text{Jy}` (except that it used the so-called
"asinh" magnitudes defined by
:ref:`Lupton et al. 1999 <stsynphot-ref-lupton1999>` instead of conventional
Pogson magnitudes). However, this is known not to be exactly true, such that
the photometric zero points are slightly off the AB standard. The SDSS team
continues to work to pin down these shifts. Their estimate, based on comparison
to the STIS standards of :ref:`Bohlin et al. (2001) <stsynphot-ref-bohlin2001>`
and confirmed by SDSS photometry and spectroscopy of fainter hot white dwarfs,
is that the *u* band zero point is in error by 0.04 mag,
:math:`u_{\text{AB}} = u_{\text{SDSS}} - 0.04 \; \text{mag}`,
and that *g*, *r*, and *i* are close to AB; These statements are certainly not
precise to better than 0.01 mag. The *z* band zero point is not as certain
(as of January 2005), but there is mild evidence that it may be shifted by
about 0.02 mag in the sense that
:math:`z_{\text{AB}} = z_{\text{SDSS}} + 0.02 \; \text{mag}`.

See :ref:`Holberg & Bergeron (2006) <stsynphot-ref-holberg2006>` for a
calibration of SDSS magnitudes using Vega as a reference spectrum.
Further information about SDSS photometric calibration and the "asinh"
magnitude system can be found at
`SDSS Photometric Flux Calibration webpage <http://classic.sdss.org/dr3/algorithms/fluxcal.html>`_.


.. _stsynphot-nonhst-stromgren:

Stromgren
---------

The Stromgren *uvby* throughputs are taken from
:ref:`Maiz Apellaniz (2006) <stsynphot-ref-maiz2006>`. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('stromgren,y')  # doctest: +SKIP


.. _stsynphot-nonhst-wfirst:

WFIRST
------

Phase B estimates of the WFIRST integrated system throughputs have been taken from
the `WFIRST Reference Information <https://wfirst.gsfc.nasa.gov/science/WFIRST_Reference_Information.html>`_ page at GSFC. For example:

>>> import stsynphot as stsyn
>>> bp = stsyn.band('wfirst,wfi,f062')  # doctest: +SKIP

Only the Wide Field Instrument (WFI) is currently supported with the following modes:

+------------+-----------------------------------------+
|Description |Keywords                                 |
+============+=========================================+
|Filter      |f062, f087, f106, f129, f146, f158, f184 |
+------------+-----------------------------------------+
|Grating     |grism, prism                             |
+------------+-----------------------------------------+

At this time, the estimated throughputs do not differentiate between the different sensor chip assemblies (SCAs).
SCA-dependent throughputs will be delivered at a later time.

(Note: WFIRST throughput curves were added to the TMG file in January 2020. Users must use
a TMG/TMC file and associated throughput tables delivered after this date to use the 
WFIRST OBSMODEs.)



.. _stsynphot-nonhst-deprecated:

Deprecated Systems
------------------

As of March 2006, some non-HST bandpass systems were deprecated, as tabulated
below. They remain accessible by **stsynphot**, but mostly for backward
compatibility. There will be no updates from CRDS, so use these at your own
risk.

+-----------------+-----------------------------------------------+
|System Name      |Band Name                                      |
+=================+===============================================+
||nonhst_ans|     |1550 1550n 1800 2200 2500 3300                 |
+-----------------+-----------------------------------------------+
||nonhst_baum|    |f336w f439w f547m f555w f569w f606w f622w f675w|
|                 |f702w f725lp f785lp f791w f814w f850lp f1042m  |
+-----------------+-----------------------------------------------+
||nonhst_bessell| |j h k                                          |
+-----------------+-----------------------------------------------+
||nonhst_eso|     |88 97 100-102 104-106 109-119 121 122 125      |
|                 |127-130 132 136 140 141 145 149 152 154-157    |
|                 |159-161 163-166 168-170 172-179 181-183 185 186|
|                 |189 192-194 196-199 201-207 209-234 236-242 244|
|                 |247 248 253 254 260 264 265 537 538            |
+-----------------+-----------------------------------------------+
||nonhst_kpno|    |j h k                                          |
+-----------------+-----------------------------------------------+
||nonhst_steward| |j h k                                          |
+-----------------+-----------------------------------------------+
||nonhst_walraven||v b l u w                                      |
+-----------------+-----------------------------------------------+


.. _stsynphot-nonhst-ans:

ANS
^^^

The Astronomical Netherlands Satellite (ANS) system is a set of UV filters used
by the satellite, as described in
:ref:`van Duinen et al. (1975) <stsynphot-ref-vanduinen1975>`. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('ans,1550')  # doctest: +SKIP


.. _stsynphot-nonhst-baum:

Baum
^^^^

The Baum filter set is a set of 15 broadband and intermediate-band
filters that are copies the ones onboard :ref:`stsynphot-appendixb-wfpc1` that
were used as part of a ground-based calibration campaign for the instrument.
In order to match the response of the in-flight bandpass as closely as
possible, the throughputs for the Baum filters have been multiplied
by the spectral response curve of the ground-based CCD (measured
in the laboratory) and twice by the spectral reflectance of aluminum
(:ref:`Harris et al. 1991 <stsynphot-ref-harris1991>`). For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('baum,f336w')  # doctest: +SKIP


.. _stsynphot-nonhst-bessell:

Bessell
^^^^^^^

The Bessell *JHK* filter curves are taken from
:ref:`Bessell & Brett (1988) <stsynphot-ref-bessell1988>`, Table IV.
These curves include the mean atmospheric transmission equivalent to 1.2
air masses of a standard `KPNO <https://www.noao.edu/kpno/>`_  atmosphere.
For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('bessell,k')  # doctest: +SKIP


.. _stsynphot-nonhst-eso:

ESO
^^^

The 530 ESO band throughput tables were received from Jan Koornneef in 1990.
For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('eso,198')  # doctest: +SKIP


.. _stsynphot-nonhst-kpno:

KPNO
^^^^

The `Kitt Peak National Observatory (KPNO) <https://www.noao.edu/kpno/>`_ *JHK*
filter curves are taken from the tracings of the Simultaneous Quad Infrared
Image Device (SQIID) filter set, which were provided by Richard Joyce from the
observatory. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('kpno,k')  # doctest: +SKIP


.. _stsynphot-nonhst-steward:

Steward
^^^^^^^

The `Steward Observatory <https://www.as.arizona.edu/observing>`_ *JHK* filter
curves are from data provided by Marcia Rieke from the observatory.
For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('steward,k')  # doctest: +SKIP


.. _stsynphot-nonhst-walraven:

Walraven
^^^^^^^^

The throughput data for the Walraven *VBLUW* bands are from
:ref:`Lub & Pel (1977) <stsynphot-ref-lub1977>`, Table 6. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('walraven,v')  # doctest: +SKIP
