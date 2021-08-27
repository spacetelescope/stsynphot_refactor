"""``stsynphot`` constants."""

from astropy import units as u
from astropy.constants import Constant

__all__ = ['hst_area', 'jwst_area']

hst_area = Constant(
    'hst_area', "HST primary mirror area", 45238.93416, u.cm * u.cm, 0.0,
    "HST", system='cgs')
"""HST primary mirror area"""

jwst_area = Constant(
    'jwst_area', "JWST primary mirror area", 254308.2, u.cm * u.cm, 0.0,
    '2022.04.01 Area X Transmission Budget - Rev J (post launch) by Lightsey et al',  # noqa
    system='cgs')
"""JWST primary mirror area"""
