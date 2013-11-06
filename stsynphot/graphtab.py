# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module handles graph table look-up as discussed in
:ref:`Laidler et al. 2005 <stsynphot-ref-laidler2005>` and
:ref:`Diaz 2012 <stsynphot-ref-diaz2012>`.

Data structure and traversal algorithm suggested by Alex Martelli in
`this discussion <http://stackoverflow.com/questions/844505/is-a-graph-library-eg-networkx-the-right-solution-for-my-python-problem>`_.

.. warning::

    This module is incomplete but will replace `stsynphot.tables` someday.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import collections

# ASTROPY
from astropy import log
from astropy.io import fits

# LOCAL
from . import exceptions, io


__all__ = ['extract_keywords', 'GraphNode', 'GraphPath', 'GraphTable',
           'CompTable']


def extract_keywords(icss):
    """Extract keywords from the given comma-separated string.

    Parameters
    ----------
    icss : str
        Comma-separated string in the format of 'key1,key2#val2,...'.

    Returns
    -------
    kws : list of str
        Extracted keywords.

    paramdict : dict
        Dictionary of ``{parameterized_keyword: parameter_value}``.

    """
    # Force to lower case and split into keywords
    kws = set(icss.lower().split(','))

    # Parameterized keywords require special handling
    paramdict = {}
    parlist = [k for k in kws if '#' in k]
    for k in parlist:
        key, val = k.split('#')
        # Take the parameterized value off the keyword...
        kws.remove(k)
        kws.add(key+'#')
        # ...and save it in the dictionary
        paramdict[key+'#'] = val

    return kws, paramdict


class GraphNode(object):
    """Class to hold all the information associated with a single
    input node of `GraphTable`.

    The constructor produces an empty node, which must be filled later.
    This structure will be the value associated with the `GraphTable`
    dictionary.

    """
    def __init__(self):
        self._default = (None, None, None)
        self._named = {}
        self._entry = (self.default, self.named)

    def __repr__(self):
        return str(self.entry)

    @property
    def default(self):
        """Tuple of ``(default_outnode, compname, thcompname)``."""
        return self._default

    @default.setter
    def default(self, value):
        """Set default.

        Parameters
        ----------
        value : tuple
            Tuple of ``(outnode, compname, thcompname)``.

        """
        self._default = value
        self._entry = (self.default, self.named)

    @property
    def named(self):
        """Dictionary that maps each keyword to
        ``(outnode, compname, thcompname)``.

        """
        return self._named

    def add_named(self, key, value):
        """Add new entry to ``self.named`` dictionary.

        Parameters
        ----------
        key : str
            New keyword.

        value : dict
            Corresponding value in the form of
            ``(outnode, compname, thcompname)``.

        Raises
        ------
        stsynphot.exceptions.GraphtabError
            If keyword already exists in the dictionary.

        """
        if kwd in self.named:
            raise exceptions.GraphtabError(
                '{0} already exists for this node.'.format(kwd))

        self._named[kwd] = value
        self._entry = (self.default, self.named)

    @property
    def entry(self):
        """Tuple of ``(default, named)``."""
        return self._entry


class GraphPath(object):
    """Class to handle the result of a `GraphTable` traversal.

    Parameters
    ----------
    obsmode_string : str
        Observation mode in parser language form.

    optical : list of str
        Optical component names.

    thermal : list of str
        Thermal component names.

    params : dict
        Dictionary of ``{compname: parameterized_value}`` for
        any parameterized keywords used in ``obsmode_string``.

    tname : str
        Grapth table name.

    Attributes
    ----------
    obsmode : str
        Observation mode in parser language form.

    optical : list of str
        Optical component names.

    thermal : list of str
        Thermal component names.

    params : dict
        Dictionary of ``{compname: parameterized_value}`` for
        any parameterized keywords used in ``obsmode``.

    gtable : str
        Grapth table name.

    """
    def __init__(self, obsmode_string, optical, thermal, params, tname):
        self.obsmode = obsmode_string
        self.optical = optical
        self.thermal = thermal
        self.params = params
        self.gtable = tname

    def __repr__(self):
        return str((self.optical, self.thermal, self.params, self.gtable))

    def __len__(self):
        return max(len(self.optical), len(self.thermal))


class GraphTable(object):
    """Class to handle graph table.

    Table is parsed with :func:`~stsynphot.io.read_graphtable`.
    Component names that match 'clear' (case-insensitive) will
    be converted to `None`. All string entries will be converted
    to lower case. Comment column is ignored.

    Parameters
    ----------
    fname : str
        Graph table name.

    ext : int, optional
        FITS extension index of the data table.

    Attributes
    ----------
    tname : str
        Graph table name.

    primary_area : float or `None`
        Value of PRIMAREA keyword in primary header in :math:`cm^{2}`.

    tab : dict
        Dictionary of `GraphNode`.

    all_nodes : set
        All the nodes in the table.

    problemset : set
        Stores ambiguous nodes for reporting.

    """
    def __init__(self, fname, ext=1):
        self.primary_area, data = io.read_graphtable(fname, tab_ext=ext)
        self.tname = fname
        self.tab = collections.defaultdict(GraphNode)
        self.problemset = set()

        for row in data:
            compname = self._parse_filter(row['COMPNAME'])
            kwd = row['KEYWORD'].lower()
            innode = row['INNODE']  # Already int
            outnode = row['OUTNODE']  # Already int
            thcomp = self._parse_filter(row['THCOMPNAME'])
            val = (outnode, compname, thcomp)

            # Now create the GraphNode defined by this row,
            # and add it to the table. Default nodes are special.
            if kwd == 'default':
                self.tab[innode].default = val
            else:
                try:
                    self.tab[innode].add_named(kwd, val)
                except exceptions.GraphtabError:
                    old = self.tab[innode].named[kwd]
                    self.problemset.add((innode, kwd, old, val))

        n_bad = len(self.problemset)
        if n_bad > 0:
            warn_str = 'Ambiguous nodes encountered\n'
            warn_str += '(innode, kwd, (outnode, compname, thcompname))\n'
            for i, k in enumerate(self.problemset):
                warn_str += '{0}'.format(k)
                if i < n_bad - 1:
                    warn_str += '\n'
            log.warn(warn_str)

        self.all_nodes = set()
        for node in self.tab:
            self.all_nodes.add(node)
            self._add_descendants(node, self.all_nodes)

    @staticmethod
    def _parse_filter(x):
        """Change filter CLEAR (case-insensitive) to `None`.
        Always return lowercase.

        """
        y = x.lower()
        if y == 'clear':
            y = None
        return y

    def _add_descendants(self, node, updateset):
        """Add all descendants of node to given set."""
        someset = set()
        startnode = self.tab[node]
        defout = startnode.default[0]

        if defout is not None:
            someset.add(defout)

        for kwd, matchnode in startnode.named.items():
            if matchnode[0] is not None:
                someset.add(matchnode[0])

        updateset.update(someset)

    def traverse(self, icss, verbose=False):
        """Traverse the graph table.

        Parameters
        ----------
        icss : str
            Comma-separated string in the format of 'key1,key2#val2,...'.

        verbose : bool, optional
            Verbose output that is useful for debugging.

        Returns
        -------
        path : `GraphPath`

        Raises
        ------
        stsynphot.exceptions.AmbiguousObsmode
            Ambiguous observation mode.

        stsynphot.exceptions.IncompleteObsmode
            Incomplete observation mode.

        stsynphot.exceptions.UnusedKeyword
            Unused keyword in observation mode.

        """
        opt = []
        thm = []
        used = set()
        paramcomp = dict()
        nodelist = list()

        # Returns a list of keywords and a dict of paramkeys
        kws, paramdict = extract_keywords(icss)
        if verbose:
            log.info(kws)
            log.info(paramdict)

        # Always start from 1
        nextnode = 1

        # Keep going as long as the next node is in this table
        while nextnode in self.tab:
            defnode = self.tab[nextnode].default
            othernodes = self.tab[nextnode].named

            # Check if the keywords match a named option
            found = kws & set(othernodes)

            if found:
                if verbose:
                    log.info(found)
                # Check for ambiguity
                if len(found) == 1:
                    used.update(found)
                    matchkey = found.pop()
                    matchnode = othernodes[matchkey]
                else:
                    raise exceptions.AmbiguousObsmode(
                        'Cannot use {0} together'.format(found))
            else:
                # fall back to default
                matchnode = defnode

            # Having picked out the matching node, also pick up
            # the optical & thermal components from it
            nodelist.append(matchnode)
            nextnode, ocomp, tcomp = matchnode
            if ocomp is not None:
                opt.append(ocomp)
            if tcomp is not None:
                thm.append(tcomp)

            # Special handling of paramterization
            if matchkey in paramdict:
                paramcomp[ocomp] = float(paramdict[matchkey])
                paramcomp[tcomp] = float(paramdict[matchkey])

            if verbose:
                log.info(matchnode)

            if nextnode is None:
                raise exceptions.IncompleteObsmode(
                    'Legal possibilities {0}'.format(str(othernodes.keys())))

        # We're done with the table. If there are any keywords left over,
        # raise an exception.
        if kws != used:
            raise exceptions.UnusedKeyword(
                '{0}'.format(str([k for k in (kws - used)])))

        # The results are returned as a simple class
        path = GraphPath(icss, opt, thm, paramcomp, self.tname)

        return path

    def validate(self):
        """Simulataneously checks for loops and unreachable nodes.

        Returns
        -------
        msg : `True` or str
            `True` if validation is successful, error messages otherwise.

        """
        msg = list()
        previously_seen = set()
        currently_seen = set([1])
        problemset = set()

        while currently_seen:
            node = currently_seen.pop()
            if node in previously_seen:
                problemset.add(node)
            else:
                previously_seen.add(node)
                self.add_descendants(node, currently_seen)

        unreachable = self.all_nodes - previously_seen
        if unreachable:
            msg.append('{0} unreachable nodes: '.format(len(unreachable)))
            for node in unreachable:
                msg.append(str(node))

        if problemset:
            msg.append('Loop involving {0} nodes'.format(len(problemset)))
            for node in problemset:
                msg.append(str(node))

        if msg:
            return msg
        else:
            return True


class CompTable(object):
    """Class to handle component table (optical or thermal).

    Table is parsed with :func:`~stsynphot.io.read_comptable`.
    Only component names and filenames are kept.
    Component throughput filenames are parsed with
    :func:`~stsynphot.io.irafconvert`.

    This class is used with `GraphPath` to produce a realized
    list of files.

    Parameters
    ----------
    fname : str
        Component table filename.

    ext : int, optional
        FITS extension index of the data table.

    Attributes
    ----------
    tname : str
        Component table filename.

    tab : dict
        Dictionary that maps component name to corresponding throughput file.

    """
    def __init__(self, fname, ext=1):
        data = io.read_comptable(fname, tab_ext=ext)
        self.tname = fname
        self.tab = dict()

        for row in data:
            compname = row['COMPNAME'].lower()
            compfile = row['FILENAME']
            self.tab[compname] = io.irafconvert(compfile)

    def __getitem__(self, key):
        """Return throughput filename for given component name."""
        return self.tab[key]
