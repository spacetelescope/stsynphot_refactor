.. include:: appb_ref.txt

.. _stsynphot-appendixb-legacy:

Legacy Instruments
==================

The instruments which had previously flown on HST but had been
replaced by more modern detectors are included here for completeness.


.. _stsynphot-appendixb-foc:

FOC
---

The FOC keywords consist of a list of detectors, filters, and
miscellaneous keywords. The ``f/48`` detector has 2 filter wheels and the
``f/96`` detector has 4. Some of the filters have aliases. For instance,
``fuvop`` is an alias for ``prism1``, ``nuvop`` for ``prism2``,
``fopcd`` for ``prism3``, ``g450m`` for F305LP,
``g225m`` for F220W, and ``g150m`` for F140W.
The miscellaneous keywords include the :ref:`stsynphot-costar` and
the occulting fingers. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('foc,costar,f/96,f410m')  # doctest: +SKIP

+--------------+--------------------------------------------------+
|Description   |Keywords                                          |
+==============+==================================================+
|Detector      |f/48 f/96 f/288 spec                              |
+------+-------+--------------------------------------------------+
|f/48  |Wheel 1|f140w (g130m) f150w (g150m) f175w f195w f220w     |
|      |       |(g225m) f305lp (g450m) prism3 (fopcd) (grat-prism)|
|      +-------+--------------------------------------------------+
|      |Wheel 2|f130lp f180lp f275w f342w f430w prism1 (fuvop)    |
|      |       |prism2 (nuvop)                                    |
+------+-------+--------------------------------------------------+
|f/96  |Wheel 1|f600m f630m f2nd f4nd f6nd f8nd pol0 pol0_par     |
|      |       |pol0_per pol0_unp pol60 pol60_par pol60_per       |
|      |       |pol60_unp pol120 pol120_par pol120_per pol120_unp |
|      |       |prism1 (fuvop) prism2 (nuvop)                     |
|      +-------+--------------------------------------------------+
|      |Wheel 2|f140w f175w f220w f275w f320w f342w f370lp f430w  |
|      |       |f480lp f486n f501n                                |
|      +-------+--------------------------------------------------+
|      |Wheel 3|f120m f130m f140m f152m f165w f170m f190m f195w   |
|      |       |f210m f231m f1nd                                  |
|      +-------+--------------------------------------------------+
|      |Wheel 4|f130lp f253m f278m f307m f346m f372m f410m f437m  |
|      |       |f470m f502m f550m                                 |
+------+-------+--------------------------------------------------+
|Image |f/48   |x48n256 x48n256d x48n512 x48nlrg x48zlrg x48zrec  |
|Format+-------+--------------------------------------------------+
|      |f/96   |x96n128 x96n256 x96n512 x96nlrg x96z512 x96zlrg   |
+------+-------+--------------------------------------------------+
|Spectral Order|order1 order2 order3 order4                       |
+--------------+--------------------------------------------------+
|Occulting     |occ0p23 occ0p4 occ0p8                             |
|FIngers       |                                                  |
+--------------+--------------------------------------------------+
|Detector      |x48n256 x48n256d x48n512 x48nlrg x48zlrg x48zrec  |
|Format        |x96n128 x96n256 x96n512 x96z512 x96nlrg x96zlrg   |
+--------------+--------------------------------------------------+

Note that the spectroscopic capabilities, and hence the related
keywords ``spec``, ``order1``, ``order2``, ``order3``, and ``order4``,
are only available for the ``f/48`` camera. Furthermore, the ``occ0p23``
keyword is only available with the ``f/48`` camera, and the ``occ0p4`` and
``occ0p8`` keywords are only available with the ``f/96`` camera.

The ``x48*`` and ``x96*`` keywords are used to account for the known dependency
of DQE on the detector format (see the FOC Instrument Handbook for
more details). These keywords invoke throughput tables that contain
the (wavelength-independent) relative sensitivities for each format,
where the 512x512 format (``x48n512`` and ``x96n512``) is set to 1.0.
The associations between formats and keywords are listed below.

+------+-------+-------------+
|Camera|Keyword|Camera Format|
+======+=======+=============+
|f/96  |x96n128|128 x 128    |
|      +-------+-------------+
|      |x96n256|256 x 256    |
|      +-------+-------------+
|      |x96n512|512 x 512    |
|      +-------+-------------+
|      |x96z512|512z x 512   |
|      +-------+-------------+
|      |x96zlrg|512z x 1024  |
+------+-------+-------------+
|f/48  |x48n256|256 x 256    |
|      +-------+-------------+
|      |x48n512|512 x 512    |
|      +-------+-------------+
|      |x48zrec|256z x 1024  |
|      +-------+-------------+
|      |x48nlrg|512 x 1024   |
|      +-------+-------------+
|      |x48zlrg|512z x 1024  |
+------+-------+-------------+


.. _stsynphot-appendixb-fos:

FOS
---

The FOS keywords consist of a list of detectors, apertures, gratings, and
polarimeter waveplates and waveplate position angles.
:ref:`stsynphot-costar` keyword is also accepted. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('fos,costar,blue,g160l')  # doctest: +SKIP

The waveplate keywords indicate whether Waveplate A or  B is being used and
the angle of the waveplate. The waveplate keyword syntax is ``POLpa-wp``,
where ``pa`` is the position angle in degrees, and ``wp`` is the A or B
waveplate::

    >>> bp = stsyn.band('fos,blue,g130h,pol135-a')  # doctest: +SKIP

The ``upper`` and ``lower`` aperture keywords are only recognized when used
in conjunction with one of the paired apertures::

    >>> bp = stsyn.band('fos,blue,g130h,upper,1.0-pair')  # doctest: +SKIP

The ``order0`` keyword is only available in conjunction with the ``g160l``
grating and the ``blue`` detector::

    >>> bp = stsyn.band('fos,blue,g160l,order0')  # doctest: +SKIP

+-----------+--------------------------------------------------+
|Description|Keywords                                          |
+===========+==================================================+
|Detector   |blue red                                          |
+-----------+--------------------------------------------------+
|Aperture   |0.3 0.5 1.0 4.3 0.1-pair 0.25-pair 0.5-pair       |
|           |1.0-pair upper lower 0.25x2.0 0.7x2.0-bar 2.0-bar |
|           |blank failsafe                                    |
+-----------+--------------------------------------------------+
|Grating    |g130h g190h g270h g400h g570h g780h g160l g650l   |
|           |mirror prism order0                               |
+-----------+--------------------------------------------------+
|Waveplate  |pol0-a pol0-b pol22.5-a pol22.5-b pol45-a pol45-b |
|           |pol67.5-a pol67.5-b pol90-a pol90-b pol112.5-a    |
|           |pol112.5-b pol135-a pol135-b pol157.5-a pol157.5-b|
|           |pol180-a pol180-b pol202.5-a pol202.5-b pol235-a  |
|           |pol235-b pol257.5-a pol257.5-b pol270-a pol270-b  |
|           |pol292.5-a pol292.5-b pol315-a pol315-b pol337.5-a|
|           |pol337.5-b                                        |
+-----------+--------------------------------------------------+


.. _stsynphot-appendixb-ghrs:

GHRS
----

The GHRS keywords consist of a list of detectors, apertures, gratings
or mirrors, and Echelle mode orders. :ref:`stsynphot-costar` keyword
is also accepted. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('hrs,costar,lsa,g160m')  # doctest: +SKIP

The Echelle mode orders are used with the keywords ``echa`` and ``echb``.
Orders 18 to 33 are valid with Echelle mode B, while orders 33 to 53 with
mode A. For example::

    >>> bp = stsyn.band('hrs,costar,lsa,echa,33')  # doctest: +SKIP

+-----------+--------------------------------------------------+
|Description|Keywords                                          |
+===========+==================================================+
|Aperture   |lsa ssa                                           |
+-----------+--------------------------------------------------+
|Grating    |echa echb g140l g140m g160m g200m g270m           |
+-----------+--------------------------------------------------+
|Mirror     |a1 a2 n1 n2                                       |
+-----------+--------------------------------------------------+
|Echelle    |18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34|
|Order      |35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51|
|           |52 53 all                                         |
+-----------+--------------------------------------------------+


.. _stsynphot-appendixb-hsp:

HSP
---

The HSP keywords consist of a list of detectors, filters,
apertures, and beams. The beams refer to the two beams that
come out of the beam splitter. Not all apertures can be used
with all detectors; Refer to the HSP Instrument Handbook for
further information. The polarization detector also has angle
and type keywords. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('hsp,uv1,f220w,c')  # doctest: +SKIP

+------------------+-------------------------------------------------+
|Description       |Keywords                                         |
+==================+=================================================+
|Detector          |pmt pol uv1 uv2 vis                              |
+------------------+-------------------------------------------------+
|Relay mirror      |norelay relay                                    |
+------------------+-------------------------------------------------+
|Aperture          |a b c d e f h j s t                              |
+------------------+-------------------------------------------------+
|Beam              |blue red                                         |
+------------+-----+-------------------------------------------------+
|Filter      |POL  |f160lp f216m f237m f277m f327m                   |
|            +-----+-------------------------------------------------+
|            |UV1  |f122m f135w f140lp f145m f152m f184w f218m f220w |
|            |     |f240w f248m f278n prism                          |
|            +-----+-------------------------------------------------+
|            |UV2  |f122m f140lp f145m f152m f160lp f179m f184w f218m|
|            |     |f248m f262m f278n f284m prism                    |
|            +-----+-------------------------------------------------+
|            |VIS  |f160lp f184w f240w f262m f355m f400lp f419n f450w|
|            |     |f551w f620w prism                                |
+------------+-----+-------------------------------------------------+
|Polarization|Angle|0 45 90 135                                      |
|            +-----+-------------------------------------------------+
|            |Type |ext ord par per                                  |
+------------+-----+-------------------------------------------------+


.. _stsynphot-appendixb-wfpc1:

WF/PC-1
-------

The WF/PC-1 keywords consist of a list of filters, detectors,
and miscellaneous keywords.
The ``cal`` keyword accounts for the flat-field correction.
The ``cont#`` keyword accounts for changes in sensitivity between
:ref:`decontamination <stsynphot-parameterized-contamination>` events.

WF/PC-1 has 12 independently positionable filter wheels,
each of which has 5 positions, including a "clear" position.
Detectors 1-4 correspond to the Wide Field Camera; They are only valid
when used in conjunction with the ``wf``, ``wfc``, or ``wfpc`` keywords.
Meanwhile, Detectors 5-8 correspond to the Planetary Camera;
They are only valid when used with the ``pc`` keyword.
If a detector number is not specified, the default detector for ``wf`` is 2,
and ``pc`` is 6.

For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfpc,4,f194w,dn')  # doctest: +SKIP

+---------------+-------------------------------+
|Decription     |Keywords                       |
+===============+===============================+
|Instrument     |wfpc wfc wf (all equivalent) pc|
+---------------+-------------------------------+
|Detector       |1 2 3 4 5 6 7 8                |
+--------+------+-------------------------------+
|Filter  |  1   |f673n f8nd g450 g800           |
|Wheel   +------+-------------------------------+
|        |  2   |f122m f336w f439w g200 g200m2  |
|        +------+-------------------------------+
|        |  3   |pol0 pol60 pol120 f1083n       |
|        +------+-------------------------------+
|        |  4   |f157w f194w f230w f284w        |
|        +------+-------------------------------+
|        |  5   |f569w f658n f675w f791w        |
|        +------+-------------------------------+
|        |  6   |f631n f656n f664n f702w        |
|        +------+-------------------------------+
|        |  7   |f375n f437n f502n f588n        |
|        +------+-------------------------------+
|        |  8   |f368m f413m f492m f622w        |
|        +------+-------------------------------+
|        |  9   |f547m f555w f648m f718m        |
|        +------+-------------------------------+
|        | 10   |f785lp f814w f875m f1042m      |
|        +------+-------------------------------+
|        | 11   |f128lp f469n f487n f517n       |
|        +------+-------------------------------+
|        | 12   |f606w f725lp f850lp f889n      |
+--------+------+-------------------------------+
|ADC gain       |dn                             |
+---------------+-------------------------------+
|Baum spot      |baum                           |
+---------------+-------------------------------+
||cont_par|     |cont#                          |
+---------------+-------------------------------+
|Flat-field     |cal                            |
+---------------+-------------------------------+


.. _stsynphot-appendixb-wfpc2:

WFPC2
-----

The WFPC2 keywords consist of a list of detectors, filters, ADC gain, and
miscellaneous keywords. The ``cal`` keyword accounts for the flat-field
response. Meanwhile, the ``cont#`` keyword accounts for changes in throughput
between :ref:`decontamination <stsynphot-parameterized-contamination>` events;
Due to the removal of WFPC2 during SM4, this time-dependent effect is only
valid for dates prior to SM4.

WFPC2 has 12 filter wheels, each of which has 5 positions, including the "clear"
position. Wheel 11 contains :ref:`quad filters <stsynphot-wfpc2-quad>`, while
Wheel 12 contains :ref:`linear ramp filters <stsynphot-wfpc2-ramp>`.
Detector 1 is the Planetary Camera. Meanwhile, Detectors 2-4 correspond to the
Wide Field Camera. If a detector is not specified, the default is Detector 4.

For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfpc2,2,f450w,a2d7,cont#50180')  # doctest: +SKIP

+---------------+------------------------------------------------------+
|Description    |Keywords                                              |
+===============+======================================================+
|Detector       |1 2 3 4                                               |
+----------+----+------------------------------------------------------+
|Filter    |  1 |f122m f157w f160bw f953n                              |
|Wheel     +----+------------------------------------------------------+
|          |  2 |f130lp f165lp f785lp f850lp                           |
|          +----+------------------------------------------------------+
|          |  3 |f336w f410m f467m f547m                               |
|          +----+------------------------------------------------------+
|          |  4 |f439w f569w f675w f791w                               |
|          +----+------------------------------------------------------+
|          |  5 |f343n f375n f390n f437n                               |
|          +----+------------------------------------------------------+
|          |  6 |f469n f487n f502n f588n                               |
|          +----+------------------------------------------------------+
|          |  7 |f631n f656n f658n f673n                               |
|          +----+------------------------------------------------------+
|          |  8 |f170w f185w f218w f255w                               |
|          +----+------------------------------------------------------+
|          |  9 |f300w f380w f555w f622w                               |
|          +----+------------------------------------------------------+
|          | 10 |f450w f606w f702w f814w                               |
|          +----+------------------------------------------------------+
|          | 11 |f1042m |wfpc2_quad|                                   |
|          +----+------------------------------------------------------+
|          | 12 ||wfpc2_lrf|                                           |
+----------+----+------------------------------------------------------+
|ADC gain       |a2d7 a2d15                                            |
+---------------+------------------------------------------------------+
||cont_par|     |cont#                                                 |
+---------------+------------------------------------------------------+
|Flat-field     |cal                                                   |
+---------------+------------------------------------------------------+


.. _stsynphot-wfpc2-quad:

Quad Filter
^^^^^^^^^^^

Filter Wheel 11 contains 3 specialized quadrant (quad) filters.
Each quadrant corresponds to a facet of the pyramid, and therefore to a
distinct camera relay:

* FQUVN contains 4 narrow-band, redshifted [O II] filters
* FQCH4N contains 4 methane (CH4) band filters
* POLQ contains 4 polarizing elements

For FQUVN and FQCH4N filters, the :ref:`graph table <stsynphot-graph>` is
constructed such that distinct throughput values are automatically selected
for a given quadrant based on the selected detector. For POLQ filter, it can
also be specified by the direction its polarization; i.e., ``polq_perp`` for
perpendicular polarization, and ``polq_par`` for parallel.

The quad filters were designed to map onto a 4-faceted WFC configuration.
However, in the final design of the instrument, with WF Quadrant 1 replaced
by the PC, it is necessary to rotate the quad filters as follow
(see the WFPC2 Instrument Handbook for more details):

* ``fquvn33``, ``fqch4n33``, and ``polqn33`` represent the respective filters
  rotated by :math:`-33^{\circ}` in order to bring Filter Quadrant 1 into the
  WF2 and WF3 relays
* ``fqch4p15`` and ``fqch4n15`` represent FQCH4N partially rotated by
  :math:`\pm15^{\circ}` in order to bring 2 of its quadrants into the PC relay
* ``polqp15`` and ``polqn18`` represent POLQ partially rotated by
  :math:`+15^{\circ}` and :math:`-18^{\circ}`, respectively, in order to allow
  observations with different polarization angles

The nominal positions are represented as ``fquvn``, ``fqch4n``, and ``polq``
keywords. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfpc2,2,fqch4n')  # doctest: +SKIP


.. _stsynphot-wfpc2-ramp:

Ramp Filter
^^^^^^^^^^^

Filter Wheel 12 contains 4 linearly variable narrow-band ramp filters,
which together cover a total wavelength range of 3700 to 9800 Angstrom.
The FWHM of the throughput at a given wavelength is typically about 1% of
the central wavelength. To use a WFPC2 ramp filter in simulations, use the
keyword syntax ``lrf#cenwave``, where ``cenwave`` is the desired central
wavelength in Angstrom. For example::

    >>> import stsynphot as stsyn
    >>> bp = stsyn.band('wfpc2,3,lrf#4861')  # doctest: +SKIP
