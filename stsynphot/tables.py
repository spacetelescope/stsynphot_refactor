# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module handles graph and component (optical or thermal) tables."""

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import log

# LOCAL
from . import exceptions, stio
from .config import conf
from .stio import get_latest_file, irafconvert

__all__ = ['GraphTable', 'CompTable']


class GraphTable:
    """Class to handle graph table.

    Table is parsed with :func:`~stsynphot.stio.read_graphtable`.
    All string entries will be converted to lower case.
    Comment column is ignored.

    Parameters
    ----------
    graphfile : str
        Graph table name.

    ext : int, optional
        FITS extension index of the data table.

    Attributes
    ----------
    keywords : array of str
        Keyword names.

    compnames, thcompnames : array of str
        Components names (optical and thermal).

    innodes, outnodes : array of int
        Input and output nodes.

    primary_area : `astropy.units.quantity.Quantity` or `None`
        Value of PRIMAREA keyword in primary header.

    """
    def __init__(self, graphfile, ext=1):
        self.primary_area, data = stio.read_graphtable(
            get_latest_file(
                irafconvert(graphfile),
                err_msg=('No graph tables found; functionality will be '
                         'SEVERELY crippled.')),
            tab_ext=ext)

        # Convert all strings to lowercase
        self.keywords = np.array([s.lower() for s in data['KEYWORD']])
        self.compnames = np.array([s.lower() for s in data['COMPNAME']])
        self.thcompnames = np.array([s.lower() for s in data['THCOMPNAME']])

        # Already int
        self.innodes = data['INNODE']
        self.outnodes = data['OUTNODE']

    def get_next_node(self, modes, innode):
        """Return the output node that matches an element from
        given list of modes, starting at the given input node.

        If no match found for the given modes, output node
        corresponding to default mode is used.
        If multiple matches are found, only the result for the
        latest matched mode is stored.

        .. note::

            This is only used for debugging.

        Parameters
        ----------
        modes : list of str
            List of modes.

        innode : int
            Starting input node.

        Returns
        -------
        outnode : int
            Matching output node, or -1 if given input node not found.

        """
        nodes = np.where(self.innodes == innode)[0]

        # No match
        if len(nodes) == 0:
            return -1

        # Output node for default mode
        defaultindex = np.where(self.keywords[nodes] == 'default')[0]

        if len(defaultindex) != 0:
            outnode = self.outnodes[nodes[defaultindex]]

        for mode in modes:
            index = np.where(self.keywords[nodes] == mode)[0]
            if len(index) > 0:
                outnode = self.outnodes[nodes[index]]

        return outnode[0]

    def get_comp_from_gt(self, modes, innode):
        """Return component names for the given modes by traversing
        the graph table, starting at the given input node.

        .. note::

            Extra debug messages available by setting logger to
            debug mode.

        Parameters
        ----------
        modes : list of str
            List of modes.

        innode : int
            Starting input node.

        Returns
        -------
        components, thcomponents : list of str
            Optical and thermal components.

        Raises
        ------
        stsynphot.exceptions.AmbiguousObsmode
            Ambiguous mode.

        stsynphot.exceptions.IncompleteObsmode
            Incomplete mode.

        stsynphot.exceptions.UnusedKeyword
            Unused keyword in mode.

        """
        components = []
        thcomponents = []
        outnode = 0
        inmodes = set(modes)
        used_modes = set()
        count = 0

        while outnode >= 0:
            if outnode < 0:  # pragma: no cover
                log.debug(f'outnode={outnode} (stop condition).')

            previous_outnode = outnode
            nodes = np.where(self.innodes == innode)

            # If there are no entries with this innode, we're done
            if len(nodes[0]) == 0:
                log.debug(f'innode={innode} not found (stop condition).')
                break

            # Find the entry corresponding to the component named
            # 'default', because thats the one we'll use if we don't
            # match anything in the modes list
            if 'default' in self.keywords[nodes]:
                dfi = np.where(self.keywords[nodes] == 'default')[0][0]
                outnode = self.outnodes[nodes[0][dfi]]
                component = self.compnames[nodes[0][dfi]]
                thcomponent = self.thcompnames[nodes[0][dfi]]
                used_default = True
            else:
                # There's no default, so fail if nothing found in the
                # keyword matching step.
                outnode = -2
                component = thcomponent = None

            # Match something from the modes list
            for mode in modes:
                if mode in self.keywords[nodes]:
                    used_modes.add(mode)
                    index = np.where(self.keywords[nodes] == mode)
                    n_match = len(index[0])
                    if n_match > 1:
                        raise exceptions.AmbiguousObsmode(
                            f'{n_match} matches found for {mode}')
                    idx = index[0][0]
                    component = self.compnames[nodes[0][idx]]
                    thcomponent = self.thcompnames[nodes[0][idx]]
                    outnode = self.outnodes[nodes[0][idx]]
                    used_default = False

            log.debug(f'innode={innode} outnode={outnode} '
                      f'compname={component}')
            components.append(component)
            thcomponents.append(thcomponent)
            innode = outnode

            if outnode == previous_outnode:
                log.debug(f'innode={innode} outnode={outnode} '
                          f'used_default={used_default}')
                count += 1
                if count > 3:
                    log.debug(f'Same outnode={outnode} over 3 times (stop '
                              'condition)')
                    break

        if outnode < 0:
            log.debug(f'outnode={outnode} (stop condition)')
            raise exceptions.IncompleteObsmode(
                f'{modes}, choose from {self.keywords[nodes]}')

        if inmodes != used_modes:
            raise exceptions.UnusedKeyword(
                f'{str(inmodes.difference(used_modes))}')

        return components, thcomponents


class CompTable:
    """Class to handle component table (optical or thermal).

    Table is parsed with :func:`~stsynphot.stio.read_comptable`.
    Only component names and filenames are kept.
    Component throughput filenames are parsed with
    :func:`~stsynphot.stio.irafconvert`.

    Parameters
    ----------
    compfile : str
        Component table filename.

    ext : int, optional
        FITS extension index of the data table.

    Attributes
    ----------
    name : str
        Component table filename.

    compnames, filenames : array of str
        Component names and corresponding filenames.

    """
    def __init__(self, compfile, ext=1):
        data = stio.read_comptable(
            get_latest_file(
                irafconvert(compfile),
                err_msg=('No component tables found; functionality will be '
                         'SEVERELY crippled.')),
            tab_ext=ext)
        self.name = compfile
        self.compnames = np.array([s.lower() for s in data['COMPNAME']])
        self.filenames = np.array(
            list(map(stio.irafconvert, data['FILENAME'])))

    def get_filenames(self, compnames):
        """Get filenames of given component names.

        For multiple matches, only the first match is kept.

        Parameters
        ----------
        compnames : list of str
            List of component names to search. Case-sensitive.

        Returns
        -------
        files : list of str
            List of matched filenames.

        Raises
        ------
        stsynphot.exceptions.GraphtabError
            Unmatched component name.

        """
        files = []

        for compname in compnames:
            if compname not in (None, '', conf.clear_filter):
                index = np.where(self.compnames == compname)[0]
                if len(index) < 1:
                    raise exceptions.GraphtabError(
                        f'Cannot find {compname} in {self.name}.')
                files.append(self.filenames[index[0]].lstrip())
            else:
                files.append(conf.clear_filter)

        return files
