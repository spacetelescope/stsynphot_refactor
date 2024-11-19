1.4.0 (2024-11-19)
==================

- Bumped minimum supported versions for Python to 3.10,
  ``numpy`` to 1.23, ``astropy`` to 6.0, and ``scipy`` to 1.9. [#201]

1.3.0 (2023-11-28)
==================

- Compatibility with ``numpy`` 2.0. [#181]

- Bumped minimum supported versions for Python to 3.9,
  ``numpy`` to 1.20, ``astropy`` to 5.0, ``scipy`` to 1.6,
  and ``synphot`` to 1.1. [#181]

1.2.0 (2023-03-20)
==================

- Dropped support for Python 3.6 and 3.7. Minimum supported Python
  version is now 3.8. [#161]
- Bumped minimum supported versions for ``numpy`` to 1.18,
  ``astropy`` to 4.3, and ``scipy`` to 1.3. [#167]
- Bumped minimum supported version for ``synphot`` to 1. [#167]

1.1.0 (2021-06-23)
==================

This version is compatible with ``synphot`` 1.1.0.

- Compatibility with ``astropy`` 4.3. [#128]
- ``~/.astropy/config/stsynphot.cfg`` is no longer updated on import. [#145]

1.0.0 (2020-07-31)
==================

- CDBS is TRDS now. [#121]
- This release works with ``synphot`` 1.0.

0.3.0 (2020-03-23)
==================

- New ``catalog.plot_phoenix`` function to visualize the Phoenix catalog
  parameters. [#111]
- Fix compatibility with Windows in regards to path handling. [#107]
- Fix a bug in ``stio.get_latest_file`` to recognize file in current directory.
  [#108]
- Dropped support for Python 3.5. This package now requires Python 3.6 or
  later. It also now requires ``astropy`` 3 or later. [#109]

0.2.2 (2020-01-29)
==================

- Fix total flux unit handling for ``em`` spectrum generated from
  ``parse_spec``. [#102]
- Fix ``.meta['expr']`` value for normalized spectrum generated from
  ``parse_spec``. [#102]

0.2.1 (2019-12-20)
==================

- Infrastructure update in accordance to Astropy APE 17. [#96]

0.2.0 (2019-11-19)
==================

- Removed Python 2 support. This version is only compatible with Python 3.5
  or later. [#67]
- Compatibility with ``astropy`` 4.0 models. [#81]
- Invalid ``pixscale`` in ``thermback`` calculation now raises
  ``PixscaleNotFoundError`` instead of ``SynphotError``. [#88]
- Invalid filename lookup by component in ``tables`` now raises
  ``GraphtabError`` instead of ``SynphotError``. [#89]

0.1.1 (2018-07-18)
==================

- Raise error when catalog gap (e.g., Phoenix) is used in interpolation. [#48]
- ``astropy-helpers`` updated to v2.0.6. [#51]
- Wavelength catalog updated for HST/COS. [#53]
- Added support for JWST/NIRISS path shortcut. [#55]
- Removed deprecation warning from ``np.issubdtype``. [#56]

0.1.0 (2018-01-19)
==================

First release.
