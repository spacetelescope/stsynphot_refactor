.. include:: appb_ref.txt

.. _stsynphot-appendixb:

Appendix B: OBSMODE Keywords
============================

In this section, we describe the keywords available for
:ref:`stsynphot-obsmode`.

.. note::

    OBSMODE is currently not yet available for JWST.

For HST, the following are supported:

+-----------+----------------------------------+
|Description|Keywords                          |
+===========+==================================+
|Telescope  |ota noota                         |
+-----------+----------------------------------+
|COSTAR     |costar nocostar                   |
+-----------+----------------------------------+
|Instrument |acs cos fgs foc fos hrs hsp nicmos|
|           |pc stis wf wfc wfc3 wfpc wfpc2    |
+-----------+----------------------------------+

.. toctree::
   :maxdepth: 3

   appendixb_inflight
   appendixb_legacy
   appendixb_specialkey

Some non-HST filter systems are also available:

.. toctree::
   :maxdepth: 3

   appendixb_nonhst
