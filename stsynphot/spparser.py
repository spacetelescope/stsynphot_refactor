# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Synthetic photometry language parser.

See :ref:`stsynphot-parser` for more details and
:func:`BaseParser.p_top` for language definition.

.. note::

    Like `stsynphot.spark`, parser docstrings in this module
    are used by the parser itself, so modify any docstring in
    this module with care.

    In `Interpreter`, the docstring of every function named with ``p_*``
    is part of the instructions to the parser.

    IRAF SYNPHOT extinction names are obsolete and no longer supported.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

# ASTROPY
from astropy import log
from astropy import units as u
from astropy.extern import six

# SYNPHOT
from synphot import analytic, reddening
from synphot import exceptions as synexceptions
from synphot import spectrum as synspectrum

# LOCAL
from . import catalog, config, exceptions, stio, spark, spectrum


__all__ = ['Token', 'AST', 'BaseScanner', 'Scanner', 'BaseParser',
           'Interpreter', 'tokens_info', 'scan', 'parse', 'interpret',
           'parse_spec']

# IRAF SYNPHOT functions
_SYFUNCTIONS = ('band', 'bb', 'box', 'ebmvx', 'em', 'icat', 'pl', 'rn', 'spec',
                'unit', 'z')

# IRAF SYNPHOT flux units
_SYFORMS = ('abmag', 'counts', 'flam', 'fnu', 'jy', 'mjy', 'obmag', 'photlam',
             'photnu', 'stmag', 'vegamag')

# Filelist is not supported yet. Should be handled in :func:`interpret`.
#_ZZZ = """ top ::= FILELIST """


def _convertstr(value):
    """Convert given filename to source spectrum or passband.

    This is used by the interpreter to do the conversion from
    string to spectrum object.

    """
    if not isinstance(value, six.string_types):
        return value
    value = stio.irafconvert(value)
    try:
        sp = synspectrum.SourceSpectrum.from_file(value)
    except KeyError:
        sp = synspectrum.SpectralElement.from_file(value)
    return sp


class Token(object):
    # Class to handle token.
    def __init__(self, token_type=None, attr=None):
        self.type = token_type
        self.attr = attr

    def __cmp__(self, o):
        return cmp(self.type, o)

    def __repr__(self):
        if self.attr is not None:
            return str(self.attr)
        else:
            return self.type


class AST(object):
    # Class to handle Abstract Syntax Tree (AST).
    def __init__(self, ast_type):
        self.type = ast_type
        self._kids = []

    def __getitem__(self, i):
        return self._kids[i]

    def __len__(self):
        return len(self._kids)

    def __setslice__(self, low, high, seq):
        self._kids[low:high] = seq

    def __cmp__(self, o):
        return cmp(self.type, o)


class BaseScanner(spark.GenericScanner):
    # Base class to handle language scanner.
    def tokenize(self, s):
        # Tokenize string.
        self.rv = []
        spark.GenericScanner.tokenize(self, s)
        return self.rv

    def t_whitespace(self, s):
        # Whitespace regular expression.
        r' \s+ '

    def t_op(self, s):
        # Addition, multiplication, and subtraction operations
        # regular expression.
        r' \+ | \* | - '
        self.rv.append(Token(token_type=s))

    def t_lparens(self, s):
        # Left parenthesis regular expression.
        r' \( '
        self.rv.append(Token(token_type='LPAREN'))

    def t_rparens(self, s):
        # Right parenthesis regular expression.
        r' \) '
        self.rv.append(Token(token_type='RPAREN'))

    def t_comma(self, s):
        # Comma regular expression.
        r' , '
        self.rv.append(Token(token_type=s))

    def t_integer(self, s):
        # Integer regular expression.
        r' \d+ '
        self.rv.append(Token(token_type='INTEGER', attr=s))

    def t_identifier(self, s):
        # Identifier regular expression.
        r' [$a-z_A-Z/\//][\w/\.\$:#]*'
        self.rv.append(Token(token_type='IDENTIFIER', attr=s))

    def t_filelist(self, s):
        # File list regular expression.
        r' @\w+'
        self.rv.append(Token(token_type='FILELIST', attr=s[1:]))


class Scanner(BaseScanner):
    # Class to handle language scanner.
    def t_float(self, s):
        # Float regular expression.
        r' ((\d*\.\d+)|(\d+\.d*)|(\d+)) ([eE][-+]?\d+)?'
        self.rv.append(Token(token_type='FLOAT', attr=s))

    def t_divop(self, s):
        # Division operation regular expression.
        r' \s/\s '
        self.rv.append(Token(token_type='/'))


class BaseParser(spark.GenericASTBuilder):
    # Base class to handle language parser.
    def __init__(self, ASTclass, start='top'):
        super(BaseParser, self).__init__(ASTclass, start)

    def p_top(self, args):
        """
            top ::= expr
            top ::= FILELIST
            expr ::= expr + term
            expr ::= expr - term
            expr ::= term
            term ::= term * factor
            term ::= term / factor
            value ::= LPAREN expr RPAREN
            term ::= factor
            factor ::= unaryop value
            factor ::= value
            unaryop ::= +
            unaryop ::= -
            value ::= INTEGER
            value ::= FLOAT
            value ::= IDENTIFIER
            value ::= function_call
            function_call ::= IDENTIFIER LPAREN arglist RPAREN
            arglist ::= arglist , expr
            arglist ::= expr
        """

    def terminal(self, token):
        # Return terminal element.
        rv = AST(token.type)
        rv.attr = token.attr
        return rv

    def nonterminal(self, intype, args):
        # Return non-terminal element.
        if len(args) == 1:
            rv = args[0]
        else:
            rv = spark.GenericASTBuilder.nonterminal(self, intype, args)
        return rv


class Interpreter(spark.GenericASTMatcher):
    # Class to handle language interpreter.
    def __init__(self, ast):
        super(Interpreter, self).__init__('V', ast)

    def error(self, token):
        # Raise en exception.
        raise exceptions.ParserError('Cannot interpret AST.')

    def p_int(self, tree):
        """ V ::= INTEGER """
        tree.value = int(tree.attr)
        tree.svalue = tree.attr

    def p_float(self, tree):
        """ V ::= FLOAT """
        tree.value = float(tree.attr)
        tree.svalue = tree.attr

    def p_identifier(self, tree):
        """ V ::= IDENTIFIER """
        tree.value = tree.attr
        tree.svalue = tree.attr

    def p_factor_unary_plus(self, tree):
        """ V ::= factor ( + V ) """
        tree.value = _convertstr(tree[1].value)

    def p_factor_unary_minus(self, tree):
        """ V ::= factor ( - V ) """
        tree.value = - _convertstr(tree[1].value)

    def p_expr_plus(self, tree):
        """ V ::= expr ( V + V ) """
        tree.value = _convertstr(tree[0].value) + _convertstr(tree[2].value)

    def p_expr_minus(self, tree):
        """ V ::= expr ( V - V ) """
        tree.value = _convertstr(tree[0].value) - _convertstr(tree[2].value)

    def p_term_mult(self, tree):
        """ V ::= term ( V * V ) """
        tree.value = _convertstr(tree[0].value) * _convertstr(tree[2].value)

    def p_term_div(self, tree):
        """ V ::= term ( V / V ) """
        tree.value = _convertstr(tree[0].value) / tree[2].value

    def p_value_paren(self, tree):
        """ V ::= value ( LPAREN V RPAREN ) """
        tree.value = _convertstr(tree[1].value)
        tree.svalue = "(%s)" % str(tree[1].value)

    def p_arglist(self, tree):
        """ V ::= arglist ( V , V ) """
        if isinstance(tree[0].value, list):
            tree.value = tree[0].value + [tree[2].value]
        else:
            tree.value = [tree[0].value, tree[2].value]
        try:
            tree.svalue = "%s,%s" % (tree[0].svalue, tree[2].svalue)
        except AttributeError:
            pass  # We only care about this for relatively simple constructs.

    def p_functioncall(self, tree):
        # Where all the real interpreter action is.
        # Note that things that should only be done at the top level
        # are performed in :func:`interpret` defined below.
        """ V ::= function_call ( V LPAREN V RPAREN ) """
        if type(tree[2].value)!=type([]):
            args = [tree[2].value]
        else:
            args = tree[2].value

        fname = tree[0].value

        if fname not in _SYFUNCTIONS:
            log.error('Unknown function: {0}'.format(fname))
            self.error(fname)

        else:
            area = config.PRIMARY_AREA()

            # Constant spectrum
            if fname == 'unit':
                if args[1] not in _SYFORMS:
                    log.error('Unrecognized unit: {0}'.format(args[1]))
                    self.error(fname)
                tree.value = analytic.Const1DSpectrum(
                    args[0], flux_unit=args[1], area=area)

            # Black body
            elif fname == 'bb':
                tree.value = analytic.BlackBody1DSpectrum(args[0], area=area)

            # Power law
            elif fname == 'pl':
                if args[2] not in _SYFORMS:
                    log.error('Unrecognized unit: {0}'.format(args[2]))
                    self.error(fname)
                tree.value = analytic.PowerLaw1DSpectrum(
                    1.0, args[0], -1.0 * args[1], flux_unit=args[2], area=area)

            # Box throughput
            elif fname == 'box':
                tree.value = analytic.Box1DSpectrum(
                    1.0, args[0], args[1], area=area)

            # Source spectrum from file
            elif fname == 'spec':
                tree.value = synspectrum.SourceSpectrum.from_file(
                    stio.irafconvert(args[0]), area=area)

            # Passband
            elif fname == 'band':
                tree.value = spectrum.band(tree[2].svalue)

            # Gaussian emission line
            elif fname == 'em':
                if args[3] not in _SYFORMS:
                    log.error('Unrecognized unit: {0}'.format(args[3]))
                    self.error(fname)
                totflux = u.Quantity(args[2], args[3])
                tree.value = analytic.gaussian_spectrum(
                    totflux, args[0], args[1], area=area)

            # Catalog interpolation
            elif fname == 'icat':
                tree.value = catalog.grid_to_spec(*args, area=area)

            # Renormalize source spectrum
            elif fname == 'rn':
                sp = args[0]
                bp = args[1]
                rnval = u.Quantity(args[2], args[3])

                if isinstance(sp, analytic.BaseMixinAnalytic):
                    sp = sp.to_spectrum(config._DEFAULT_WAVESET())
                elif not isinstance(sp, synspectrum.SourceSpectrum):
                    sp = synspectrum.SourceSpectrum.from_file(
                        stio.irafconvert(sp), area=area)

                if isinstance(bp, analytic.BaseMixinAnalytic):
                    bp = bp.to_spectrum(config._DEFAULT_WAVESET())
                elif not isinstance(bp, synspectrum.SpectralElement):
                    bp = synspectrum.SpectralElement.from_file(
                        stio.irafconvert(bp), area=area)

                # Always force the renormalization to occur: prevent exceptions
                # in case of partial overlap. Less robust but duplicates
                # IRAF SYNPHOT. Force the renormalization in the case of partial
                # overlap, but raise an exception if the spectrum and bandpass
                # are entirely disjoint.
                try:
                    tree.value = sp.renorm(rnval, bp, vegaspec=spectrum.Vega)
                except synexceptions.PartialOverlap:
                    tree.value = sp.renorm(rnval, bp, vegaspec=spectrum.Vega,
                                           force=True)
                    tree.value.warnings['force_renorm'] = \
                        'Renormalization of {0}, to {1} and {2}, ' \
                        'exceeds the limit of the specified passband.'.format(
                        str(sp), rnval, str(bp))

            # Redshift source spectrum (flat spectrum if fails)
            elif fname == 'z':
                sp = args[0]

                # ETC generates junk (i.e., 'null') sometimes
                if isinstance(sp, six.string_types) and sp != 'null':
                    sp = synspectrum.SourceSpectrum.from_file(
                        stio.irafconvert(sp), area=area)
                elif isinstance(sp, analytic.BaseMixinAnalytic):
                    sp = sp.to_spectrum(config._DEFAULT_WAVESET())

                if isinstance(sp, synspectrum.SourceSpectrum):
                    tree.value = sp.apply_redshift(args[1])
                else:
                    tree.value = analytic.flat_spectrum('photlam', area=area)

            # Extinction
            elif fname == 'ebmvx':
                try:
                    tree.value = spectrum.ebmvx(args[1], args[0], area=area)
                except synexceptions.SynphotError as e:
                    log.error(str(e))
                    self.error(fname)

            # Default
            else:
                tree.value = 'would call {0} with the following args: ' \
                    '{1}'.format(fname, repr(args))


def tokens_info(tlist):  # pragma: no cover
    """Print tokens for debugging.

    Parameters
    ----------
    tlist : list
        List of tokens.

    """
    for token in tlist:
        log.info('{0} {1}'.format(token.type, token.attr))


def scan(input_str):
    """Scan language string."""
    scanner = Scanner()
    input_str = input_str.replace('%2b', '+')
    return scanner.tokenize(input_str)


def parse(tokens):
    """Parse tokens."""
    parser = BaseParser(AST)
    return parser.parse(tokens)


def interpret(ast):
    """Interpret AST."""
    interpreter = Interpreter(ast)
    interpreter.match()
    value = ast.value
    return _convertstr(value)


def parse_spec(syncommand):
    """Parse a classic SYNPHOT command and return the resulting spectrum.

    Parameters
    ----------
    syncommand : str
        SYNPHOT command string.

    Returns
    -------
    sp : obj
        Spectrum object.

    """
    return interpret(parse(scan(syncommand)))
