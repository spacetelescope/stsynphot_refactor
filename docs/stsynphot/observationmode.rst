.. _synphot_observationmode:

************
Observations
************

Spectra
=======

`stsynphot.spectrum`


.. _synphot-obsmode:

Observation Modes
=================

:func:`stsynphot.spectrum.band` supports either:

    * Observation mode string
        * ``'acs,hrc,f555w'`` - Produce a set of chained throughput files.
        * ``'johnson,v'`` - Produce a single throughput file.
    * Filename, e.g., ``'crnonhstcomp$johnson_v_004_syn.fits'``

`stsynphot.observationmode` uses:

    * ``rootdir``
    * ``datadir``
    * ``wavecat``
    * ``CLEAR``

Examples
--------
>>> from stsynphot.spectrum import band
>>> obsband = band('acs,hrc,f555w')


.. _stsynphot-parser:

Language Parser
===============

Synthetic photometry uses a special language that can be parsed with
`stsynphot.spparser` based on SPARK by John Aycock (`stsynphot.spark`),
which utilizes the Earley parser
(:ref:`Earley 1968 <stsynphot-spark-earley1968>`, page 27;
:ref:`Earley 1970 <stsynphot-spark-earley1970>`). The language
is described in :ref:`Laidler et al. (2005) <stsynphot-ref-laidler2005>`.

Examples
--------
>>> from ststynphot import spparser

Return a list of tokens for the given text:

>>> l = spparser.scan('bb(5000)')

Convert the list of tokens into an Abstract Syntax Tree (AST):

>>> t = spparser.parse(l)

Convert the AST into an object (or a tree of objects), based
on the conversion rules in `~stsynphot.spparser.Interpreter`:

>>> r = spparser.interpret(t)

Parse a classic SYNPHOT command and obtain the resulting spectrum:

>>> sp = spparser.parse_spec('bb(5000)')

Spark Version
-------------

.. autodata:: stsynphot.spark.__version__
