.. include:: appb_ref.txt

.. _stsynphot-appendixb-inflight:

In-Flight Instruments
=====================

This section contains science instruments that are currently installed on HST.


.. _stsynphot-appendixb-acs:

ACS
---

.. note:: HRC is currently not operational.

The ACS keywords consist of a list of detectors, filters,
:ref:`extraction apertures <stsynphot-parameterized-aper>`, and
|mjd_par| specifications. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('acs,wfc1,f555w')  # doctest: +SKIP

+---------------+-----------------------------------------------------------------+
|Description    |Keywords                                                         |
+===============+=================================================================+
|Detector       |hrc sbc wfc1 wfc2                                                |
+-----------+---+-----------------------------------------------------------------+
|Filter     |HRC|f220w f250w f330w f344n f435w f475w f502n f550m f555w f606w f625w|
|           |   |f658n f660n f775w f814w f850lp f892n pol_uv pol_v                |
|           +---+-----------------------------------------------------------------+
|           |WFC|f435w f475w f502n f550m f555w f606w f625w f658n f660n f775w f814w|
|           |   |f850lp f892n pol_uv pol_v                                        |
|           +---+-----------------------------------------------------------------+
|           |SBC|f115lp f125lp f140lp f150lp f165lp f122m                         |
+-----------+---+-----------------------------------------------------------------+
||acs_ramp| |HRC|fr388n fr459m fr505n fr656n fr914m                               |
|           +---+-----------------------------------------------------------------+
|           |WFC|fr1016n fr388n fr423n fr459m fr462n fr505n fr551n fr601n fr647m  |
|           |   |fr656n fr716n fr782n fr853n fr914m fr931n                        |
+-----------+---+-----------------------------------------------------------------+
|Disperser  |HRC|g800l pr200l                                                     |
|           +---+-----------------------------------------------------------------+
|           |WFC|g800l                                                            |
|           +---+-----------------------------------------------------------------+
|           |SBC|pr110l pr130l                                                    |
+-----------+---+-----------------------------------------------------------------+
||aper_par|     |aper#0.0 aper#0.1 aper#0.2 aper#0.3 aper#0.4 aper#0.5 aper#0.6   |
|               |aper#0.8 aper#1.0 aper#1.5 aper#2.0 aper#4.0                     |
+---------------+-----------------------------------------------------------------+
||mjd_par|      |mjd#                                                             |
+---------------+-----------------------------------------------------------------+
|Coronographic  |coron                                                            |
|(HRC only)     |                                                                 |
+---------------+-----------------------------------------------------------------+


.. _stsynphot_acs_parameterized_ramp:

Ramp Filter
^^^^^^^^^^^

The WFC detector has 15 ramp filters available for use, while the HRC has 6.
To use a ramp filter in simulations, use the keyword syntax
``filtername#cenwave``, where ``filtername`` is the name of the ramp filter
and ``cenwave`` the desired central wavelength in Angstrom.
Also see :ref:`stsynphot-parameterized` for more information. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('acs,wfc1,fr388n#3880')  # doctest: +SKIP


.. _stsynphot-appendixb-cos:

COS
---

The COS keywords consist of a list of detectors, apertures,
mirrors, gratings, central wavelengths, and |mjd_par| specifications.

FUV spectral simulations are performed by specifying one of the FUV gratings
along with a central wavelength. NUV spectral simulations are
performed by specifying one of the NUV gratings along with a
central wavelength. In both cases, only first-order light is
included in the calculation, and the resulting spectrum will
include all three stripes on the detector.

Imaging simulations are performed by specifying one of the mirrors
(``mirrorb`` for bright objects) with the NUV detector.

Either the Primary Science Aperture (``psa``) or the Bright Object
Aperture (``boa``) may be specified with any simulation; the Primary
Science Aperture will be included by default if neither is specified.

For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('cos,nuv,g185m,c1786')  # doctest: +SKIP

+----------------+------------------------------------+
|Description     |Keywords                            |
+================+====================================+
|Detector        |fuv nuv                             |
+----------------+------------------------------------+
|Aperture        |boa psa                             |
+----------------+------------------------------------+
|Mirror          |mirrora mirrorb                     |
+----------+-----+------------------------------------+
|Grating   |FUV  |g130m g140l g160m                   |
|          +-----+------------------------------------+
|          |NUV  |g185m g225m g230l g285m             |
+----------+-----+------------------------------------+
|Central   |g130m|c1291 c1300 c1309 c1318 c1327       |
|wavelength+-----+------------------------------------+
|          |g140l|c1105 c1230                         |
|          +-----+------------------------------------+
|          |g160m|c1577 c1589 c1600 c1611 c1623       |
|          +-----+------------------------------------+
|          |g185m|c1786 c1817 c1835 c1850 c1864 c1882 |
|          |     |c1890 c1900 c1913 c1921 c1941 c1953 |
|          |     |c1971 c1986 c2010                   |
|          +-----+------------------------------------+
|          |g225m|c2186 c2217 c2233 c2250 c2268 c2283 |
|          |     |c2306 c2325 c2339 c2357 c2373 c2390 |
|          |     |c2410                               |
|          +-----+------------------------------------+
|          |g230l|c2635 c2950 c3000 c3360             |
|          +-----+------------------------------------+
|          |g285m|c2617 c2637 c2657 c2676 c2695 c2709 |
|          |     |c2719 c2739 c2850 c2952 c2979 c2996 |
|          |     |c3018 c3035 c3057 c3074 c3094       |
+----------+-----+------------------------------------+
||mjd_par|       |mjd#                                |
+----------+-----+------------------------------------+


.. _stsynphot-appendixb-fgs:

FGS
---

The FGS instrument keywords consist of a list of filters plus a coordinate
axis. Some of the filter names are aliases for other filters. For instance,
``astroclear`` is an alias for F605W, ``clear`` for F583W, ``red`` for
F650W, and ``yellow`` for 550W. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('fgs,f583w,y')  # doctest: +SKIP

+-----------+-----------------------------------------------------------+
|Description|Keywords                                                   |
+===========+===========================================================+
|Filter     |f550w (yellow) f583w (clear) f605w (astroclear) f650w (red)|
|           |nd5 pupil                                                  |
+-----------+-----------------------------------------------------------+
|Axis       |x y                                                        |
+-----------+-----------------------------------------------------------+


.. _stsynphot-appendixb-nicmos:

NICMOS
------

.. note:: NICMOS is currently not operational.

The NICMOS keywords consist of a list of filters, grisms, polarizers, and
detectors.

Both the filter name and camera number are required in the observation mode.
The detector keyword ``tacq`` is another way to specify Detector 2.
For thermal calculations, all component keywords, except the detector, may be
:ref:`parameterized for temperature <stsynphot-parameterized-temperature>`.

For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('nicmos,1,f090m,dn,primary#270')  # doctest: +SKIP

+-----------------+-----------------------------------------------------------------+
|Description      |Keywords                                                         |
+=================+=================================================================+
|Detector         |1 2 3 tacq                                                       |
+------+----------+-----------------------------------------------------------------+
|Filter|Detector 1|blank f090m f095n f097n f108n f110m f110w f113n f140w f145m f160w|
|      |          |f164n f165m f166n f170m f187n f190n pol0s pol120s pol240s        |
|      +----------+-----------------------------------------------------------------+
|      |Detector 2|blank f100w f160w f165m f171m f180m f187n f187w f190n f204m f205w|
|      +----------+f207m f212n f215n f216n f222m f237m pol0l pol120l pol240l        |
|      |tacq      |                                                                 |
|      +----------+-----------------------------------------------------------------+
|      |Detector 3|blank f108n f110w f113n f150w f160w f164n f166n f175w f187n f190n|
|      |          |f196n f200n f212n f215n f222m f240m g096 g141 g206               |
+------+----------+-----------------------------------------------------------------+
|ADC gain         |dn                                                               |
+-----------------+-----------------------------------------------------------------+
||nic_therm|      |spider primary pads hole sec edge bend1 reimag pupil image para1 |
|                 |para2 bend dewar cmask dqe                                       |
+-----------------+-----------------------------------------------------------------+


.. _stsynphot-appendixb-stis:

STIS
----

The STIS keywords consist of filters, apertures, gratings, central wavelengths,
and ADC gains.

In the STIS instrument, imaging mirrors and gratings are contained in the
Mode Select Mechanism (MSM) while filters and slits are in the aperture wheel.
Each grating or imaging mirror can be used with only one of the 3 STIS
detectors (CCD, NUVMAMA, or FUVMAMA); Therefore, specifying the grating
automatically determines the detector.

Each central wavelength is intended for use with a particular grating.
See the STIS Instrument Handbook for a listing of which central wavelengths are
allowed with each grating. The low order gratings (G140L, G230L, G230LB, G430L,
and G750L) have only one allowed setting; Thus, central wavelength should not
be specified for those. If no central wavelength is specified,
results will be calculated for the entire bandpass of the grating.

In principle, any filter or slit (aperture) could be used with any grating or
mirror, although in practice, certain combinations are restricted or forbidden.
Since the slits and filters are in the same wheel, it is not possible to use
both a slit and a filter at the same time. Some small slits also contain
built-in neutral density filters.
In addition to the aperture names listed, those used for HST Phase 2 proposals
are also acceptable. For example, the ``52X0.05`` is equivalent to ``s52x005``
listed in the table below.
If no aperture or filter is specified, the calculation is done for the "clear"
aperture.

The |mjd_par| keyword only applies to FUV and NUV MAMAs.
The ADC gain keyword only applies to CCD; It is used to convert results from
units of electrons to DN.

These ``obsmode`` strings are all equivalent, with 50CCD being the unobstructed
full-field aperture for the CCD detector::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('stis,g430l')  # doctest: +SKIP
    >>> bp = stsyn.band('stis,ccd,g430l')  # doctest: +SKIP
    >>> bp = stsyn.band('stis,ccd,g430l,50ccd')  # doctest: +SKIP

This assumes that an imaging mirror is being used because the detector name is
specified without a grating::

    >>> bp = stsyn.band('stis,ccd,f28x50lp')  # doctest: +SKIP

This will calculate results for the entire bandpass of the instrument because
no central wavelength is specified::

    >>> bp = stsyn.band('stis,ccd,g430m,52X0.2')  # doctest: +SKIP

This will only calculate results for the wavelength range covered by the
specified wavelength setting::

    >>> bp = stsyn.band('stis,ccd,g430m,52X0.2,c4451')  # doctest: +SKIP

+-----------+---------------------------------------------------------------------+
|Description|Keywords                                                             |
+===========+=====================================================================+
|Filter     |25mama 50ccd 50coron f25ciii f25cn182 f25cn270 f25lya f25mgii f25nd3 |
|           |f25nd5 f25ndq1 f25ndq2 f25ndq3 f25ndq4 f25qtz f25srf2 f28x50lp       |
|           |f28x50oii f28x50oiii                                                 |
+-----------+---------------------------------------------------------------------+
|Aperture   |s005x29 s005x31nda s005x31ndb s009x29 s01x003 s01x006 s01x009 s01x02 |
|           |s02x005nd s02x006 s02x006fpa s02x006fpb s02x006fpc s02x006fpd        |
|           |s02x006fpe s02x009 s02x02 s02x02fpa s02x02fpb s02x02fpc s02x02fpd    |
|           |s02x02fpe s02x05 s02x29 s03x005nd s03x006 s03x009 s03x02 s05x05      |
|           |s10x006 s10x02 s2x2 s31x005nda s31x005ndb s31x005ndc s36x005n45      |
|           |s36x005p45 s36x06n45 s36x06p45 s52x005 s52x01 s52x02 s52x05 s52x2    |
|           |s6x006 s6x02 s6x05 s6x6                                              |
+-----------+---------------------------------------------------------------------+
|Grating    |e140h e140hb e140m e140mb e230h e230m g140l g140lb g140m g140mb g230l|
|           |g230lb g230m g230mb g430l g430m g750l g750m prism x140 x140m x230    |
|           |x230h                                                                |
+-----------+---------------------------------------------------------------------+
|Mirror     |acq ccd fuvmama nuvmama                                              |
+-----------+---------------------------------------------------------------------+
|Central    |all c1687 c1769 c1851 c1933 c2014 c2095 c2176 c2257 c2338 c2419 c2499|
|wavelength |c2579 c2659 c2739 c2818 c2898 c2977 c3055 c3134 i1884 i2600 i2800    |
|           |i2828 c1713 c1854 c1995 c2135 c2276 c2416 c2557 c2697 c2836 c2976    |
|           |c3115 i2794 c1978 c2707 i2124 i2269 i2415 i2561 c1763 c2013 c2263    |
|           |c2513 c2762 c3012 i1813 i1863 i1913 i1963 i2063 i2113 i2163 i2213    |
|           |i2313 i2363 i2413 i2463 i2563 i2613 i2663 i2713 i2812 i2862 i2912    |
|           |i2962 c3165 c3423 c3680 c3936 c4194 c4451 c4706 c4961 c5216 c5471    |
|           |i3305 i3843 i4781 i5093 c1173 c1222 c1272 c1321 c1371 c1420 c1470    |
|           |c1518 c1567 c1616 c1665 c1714 i1218 i1387 i1400 i1540 i1550 i1640    |
|           |c1425 c1234 c1416 c1598 i1271 i1307 i1343 i1380 i1453 i1489 i1526    |
|           |i1562 c7751 c8975 c10363 c10871 c5734 c6252 c6768 c7283 c7795        |
|           |c8311 c8825 c9336 c9851 i6094 i6581 i8561 i9286 i9806                |
+-----------+---------------------------------------------------------------------+
|ADC gain   |a2d1 a2d2 a2d3 a2d4                                                  |
+-----------+---------------------------------------------------------------------+
||mjd_par|  |mjd#                                                                 |
+-----------+---------------------------------------------------------------------+


.. _stsynphot-appendixb-wfc3:

WFC3
----

The WFC3 keywords consist of a list of detectors, filters, |mjd_par|, and
:ref:`extraction apertures <stsynphot-parameterized-aper>`
for each of its 2 channels (UVIS and IR), in addition to other special keyword,
as tabulated below. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfc3,uvis1,f218w')  # doctest: +SKIP

+------------------------+-------------------------------------------------+
|Description             |Keywords                                         |
+========================+=================================================+
|Detector                |uvis1 uvis2 ir                                   |
+--------+---------------+-------------------------------------------------+
|Filter  |UVIS           |f200lp f218w f225w f275w f280n f300x f336w f343n |
|        |               |f350lp f373n f390m f390w f395n f410m f438w f467m |
|        |               |f469n f475w f475x f487n f502n f547m f555w f600lp |
|        |               |f606w f621m f625w f631n f645n f656n f657n f658n  |
|        |               |f665n f673n f680n f689m f763m f775w f814w f845m  |
|        |               |f850lp f953n fq232n fq243n fq378n fq387n fq422m  |
|        |               |fq436n fq437n fq492n fq508n fq575n fq619n fq634n |
|        |               |fq672n fq674n fq727n fq750n fq889n fq906n fq924n |
|        |               |fq937n                                           |
|        +---------------+-------------------------------------------------+
|        |IR             |f098m f105w f110w f125w f126n f127m f128n f130n  |
|        |               |f132n f139m f140w f153m f160w f164n f167n        |
+--------+---------------+-------------------------------------------------+
|Grism   |UVIS           |g280                                             |
|        +---------------+-------------------------------------------------+
|        |IR             |g102 g141                                        |
+--------+---------------+-------------------------------------------------+
|ADC gain                |dn                                               |
+------------------------+-------------------------------------------------+
||wfc3_qyc|              |qyc                                              |
+------------------------+-------------------------------------------------+
||wfc3_bkg|              |bkg                                              |
+------------------------+-------------------------------------------------+
||aper_par|              |aper#0.00 aper#0.10 aper#0.15 aper#0.20          |
|                        |aper#0.25a aper#0.30 aper#0.40 aper#0.50         |
|                        |aper#0.60 aper#0.80 aper#1.00 aper#1.50 aper#2.00|
+------------------------+-------------------------------------------------+
||mjd_par|               |mjd#                                             |
+------------------------+-------------------------------------------------+


.. _stsynphot-wfc3-qyc:

Quantum Yield Correction
^^^^^^^^^^^^^^^^^^^^^^^^

The ``qyc`` keyword is used to apply a wavelength-dependent
quantum yield correction.
At short wavelengths, the UVIS detector has a finite chance of
producing two elections for one incoming photon. By default,
**stsynphot** reports the count rate in electrons if the
``dn`` keyword is not specified, or data numbers otherwise.

However, the appropriate count rate for SNR calculations should be in
electrons with a correction for this quantum yield effect; That is,
users should specify the ``qyc`` keyword but not ``dn``. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfc3,uvis1,f218w,qyc')  # doctest: +SKIP
