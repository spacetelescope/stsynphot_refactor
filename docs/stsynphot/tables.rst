.. doctest-skip-all

.. _synphot_tables:

******
Tables
******

Graph Lookup Tables
===================

`stsynphot.tables` handles graph lookup tables.

Software uses `astropy.config` for the following;
also overwrites ``synphot.config`` file locations with ``rootdir``:

    * ``stsynphot.config.conf.rootdir``
    * ``stsynphot.config.conf.graphtable``
    * ``stsynphot.config.conf.comptable``
    * ``stsynphot.config.conf.thermtable``
    * ``stsynphot.config.conf.area``
    * ``stsynphot.config.conf.waveset_array``
    * ``stsynphot.config.conf.waveset``
    * ``stsynphot.config.conf.clear_filter``
    * ``stsynphot.config.conf.wavecatfile``
    * ``stsynphot.config.conf.detectorfile``
    * ``stsynphot.config.conf.irafshortcutfile``

Software caches the following:

    * ``stsynphot.catalog._CACHE``
    * ``stsynphot.observationmode._GRAPHDICT``
    * ``stsynphot.observationmode._COMPDICT``
    * ``stsynphot.observationmode._THERMDICT``
    * ``stsynphot.observationmode._DETECTORDICT``
    * ``stsynphot.spectrum._REDLAWS``
    * ``stsynphot.spectrum.Vega``
    * ``stsynphot.stio._irafconvdata``
    * ``stsynphot.wavetable.WAVECAT``

These are not used anymore:

    * ``setref``
    * ``CAT_TEMPLATE``
    * ``KUR_TEMPLATE``

Maybe use a table to map ``stsynphot`` to ASTROLIB PYSYNPHOT?
Need to reorganize sections in this doc.


Wave Tables
===========

`stsynphot.wavetable` uses:

    * ``stsynphot.config.conf.wavecatfile``
    * ``stsynphot.wavetable.WAVECAT``
