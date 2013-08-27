This module was part of the legacy PYSYNPHOT that deals with HST/JWST specific 
functionalities.

It is intended to be used with http://www.github.com/spacetelescope/pysynphot
for synthetic photometry as observed through HST or JWST.

It is designed to work with the HST and JWST SYNPHOT database.
The HST data files can be downloaded from http://www.stsci.edu/resources/software_hardware/stsdas/synphot .

You must define the environment variable ``PYSYN_CDBS`` to point
to the top level directory where you have installed these files.

If you have questions about this module, send email to ``help[at]stsci.edu``.

**Dependencies:**
  - astropy 0.2 or higher
  - numpy 1.5.1 or higher
  - pysynphot 3.0.0.dev or higher
