.. doctest-skip-all

.. include:: appb_ref.txt

.. _stsynphot-appendixb:

Appendix B: OBSMODE Keywords
============================

.. note:: OBSMODE is currently only available for HST.

In this section, we describe the keywords available for
:ref:`stsynphot-obsmode`. **stsynphot** supports
:ref:`science instruments currently installed on HST <stsynphot-appendixb-inflight>`
as of Servicing Mission 4 (SM4) performed in May 2009,
:ref:`legacy HST instruments <stsynphot-appendixb-legacy>`, and
:ref:`non-HST filter systems <stsynphot-appendixb-nonhst>`.
:ref:`Cross-instrument keywords <stsynphot-appendixb-special-keywords>` are
also listed.

In all the following tables, the |mjd_par| keyword is used to account for
time-dependent sensitivity, while the ADC (Analog-to-Digital Converter) gain
keyword is used to convert flux unit from electrons to data number (DN).
The keywords are also further explained in the
following sections. More instrument-specific details
can be obtained from their respective Instrument Handbooks.

The complete list of allowed component names that represent the
telescope (:ref:`stsynphot-ota`), Corrective Optics Space Telescope Axial
Replacement (:ref:`stsynphot-costar`), and science instruments is as tabulated
below:

+-----------+-----------------------------------------------------------------+
|Description|Keywords                                                         |
+===========+=================================================================+
|Telescope  |ota noota                                                        |
+-----------+-----------------------------------------------------------------+
|COSTAR     |costar nocostar                                                  |
+-----------+-----------------------------------------------------------------+
|Instrument |acs cos fgs foc fos hrs hsp nicmos pc stis wf wfc wfc3 wfpc wfpc2|
+-----------+-----------------------------------------------------------------+

As of September 1993, the default modes for the telescope and COSTAR components
are ``ota`` and ``nocostar``, respectively. Soon after COSTAR was installed in
the telescope, the default mode was changed to ``costar`` for original
instruments. Once the second-generation instruments were installed, with their
built-in optical corrections, the default mode for ``costar`` or ``nocostar``
became instrument-specific. Note that for the :ref:`stsynphot-appendixb-wfpc1`
instrument, the names ``wf``, ``wfc``, and ``wfpc`` are all equivalent and
correspond to the Wide Field Camera.

.. toctree::
   :maxdepth: 1

   appendixb_inflight
   appendixb_legacy
   appendixb_specialkey
   appendixb_nonhst
