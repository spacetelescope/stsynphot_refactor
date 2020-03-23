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
