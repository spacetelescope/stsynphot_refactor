.. _synphot_observationmode:

************
Observations
************

Spectra
=======

`stsynphot.spectrum` and `stsynphot.obsbandpass`.


Observation Modes
=================

`stsynphot.observationmode` uses:

    * ``rootdir``
    * ``datadir``
    * ``wavecat``
    * ``CLEAR``


Parser Language
===============

Language is parsed using `stsynphot.spparser`, which uses:

    * ``syfunctions``
    * ``synforms``
    * ``syredlaws``

Language parser uses `stsynphot.spark`.

Spark Version
-------------

.. autodata:: stsynphot.spark.__version__
