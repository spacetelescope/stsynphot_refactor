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
# ASTROPY
from astropy import log
from astropy import units as u

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import units
from synphot.models import (BlackBodyNorm1D, Box1D, ConstFlux1D,
                            GaussianFlux1D, PowerLawFlux1D)
from synphot.spectrum import SourceSpectrum, SpectralElement

# LOCAL
from . import exceptions, spectrum
from .catalog import grid_to_spec
from .config import conf
from .spark import GenericScanner, GenericASTBuilder, GenericASTMatcher
from .stio import irafconvert

__all__ = ['Token', 'AST', 'BaseScanner', 'Scanner', 'BaseParser',
           'Interpreter', 'tokens_info', 'scan', 'parse', 'interpret',
           'parse_spec']

# IRAF SYNPHOT functions
_SYFUNCTIONS = ('band', 'bb', 'box', 'ebmvx', 'em', 'icat', 'pl', 'rn', 'spec',
                'unit', 'z')

# IRAF SYNPHOT flux units
_SYFORMS = ('abmag', 'counts', 'flam', 'fnu', 'jy', 'mjy', 'obmag', 'photlam',
            'photnu', 'stmag', 'vegamag')


def _convertstr(value):
    """Convert given filename to source spectrum or passband.

    This is used by the interpreter to do the conversion from
    string to spectrum object.

    """
    if not isinstance(value, str):
        return value
    value = irafconvert(value)
    try:
        sp = SourceSpectrum.from_file(value)
    except KeyError:
        sp = SpectralElement.from_file(value)
    return sp


class Token:
    # Class to handle token.
    def __init__(self, token_type=None, attr=None):
        self.type = token_type
        self.attr = attr

    def __cmp__(self, o):  # pragma: py2
        return cmp(self.type, o)

    def __eq__(self, o):  # pragma: py3
        return self.type == o

    def __lt__(self, o):  # pragma: py3
        return self.type < o

    def __repr__(self):
        if self.attr is not None:
            return str(self.attr)
        else:
            return self.type


class AST:
    # Class to handle Abstract Syntax Tree (AST).
    def __init__(self, ast_type):
        self.type = ast_type
        self._kids = []

    def __getitem__(self, i):
        return self._kids[i]

    def __setitem__(self, i, seq):  # pragma: py3
        self._kids[i] = seq

    def __len__(self):
        return len(self._kids)

    def __setslice__(self, low, high, seq):  # pragma: py2
        self._kids[low:high] = seq

    def __cmp__(self, o):  # pragma: py2
        return cmp(self.type, o)

    def __eq__(self, o):  # pragma: py3
        return self.type == o

    def __lt__(self, o):  # pragma: py3
        return self.type < o


class BaseScanner(GenericScanner):
    # Base class to handle language scanner.
    def tokenize(self, s):
        # Tokenize string.
        self.rv = []
        GenericScanner.tokenize(self, s)
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
        self.rv.append(Token(token_type='LPAREN'))  # nosec

    def t_rparens(self, s):
        # Right parenthesis regular expression.
        r' \) '
        self.rv.append(Token(token_type='RPAREN'))  # nosec

    def t_comma(self, s):
        # Comma regular expression.
        r' , '
        self.rv.append(Token(token_type=s))

    def t_integer(self, s):
        # Integer regular expression.
        r' \d+ '
        self.rv.append(Token(token_type='INTEGER', attr=s))  # nosec

    def t_identifier(self, s):
        # Identifier regular expression.
        r' [$a-z_A-Z/\//][\w/\.\$:#]*'
        self.rv.append(Token(token_type='IDENTIFIER', attr=s))  # nosec

    def t_filelist(self, s):
        # File list regular expression.
        r' @\w+'
        self.rv.append(Token(token_type='FILELIST', attr=s[1:]))  # nosec


class Scanner(BaseScanner):
    # Class to handle language scanner.
    def t_float(self, s):
        # Float regular expression.
        r' ((\d*\.\d+)|(\d+\.d*)|(\d+)) ([eE][-+]?\d+)?'
        self.rv.append(Token(token_type='FLOAT', attr=s))  # nosec

    def t_divop(self, s):
        # Division operation regular expression.
        r' \s/\s '
        self.rv.append(Token(token_type='/'))  # nosec


class BaseParser(GenericASTBuilder):
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
            rv = GenericASTBuilder.nonterminal(self, intype, args)
        return rv


class Interpreter(GenericASTMatcher):
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
        tree.svalue = f'({str(tree[1].value):s})'

    def p_arglist(self, tree):
        """ V ::= arglist ( V , V ) """
        if isinstance(tree[0].value, list):
            tree.value = tree[0].value + [tree[2].value]
        else:
            tree.value = [tree[0].value, tree[2].value]
        try:
            tree.svalue = f'{tree[0].svalue:s},{tree[2].svalue:s}'
        except AttributeError:
            pass  # We only care about this for relatively simple constructs.

    @staticmethod
    def _get_names_from_tree_values(args):
        names = []
        for arg in args:
            if hasattr(arg, 'meta') and 'expr' in arg.meta:
                names.append(arg.meta['expr'])
            else:
                names.append(str(arg))
        return f"({','.join(names)})"

    def p_functioncall(self, tree):
        # Where all the real interpreter action is.
        # Note that things that should only be done at the top level
        # are performed in :func:`interpret` defined below.
        """ V ::= function_call ( V LPAREN V RPAREN ) """
        if not isinstance(tree[2].value, list):
            args = [tree[2].value]
        else:
            args = tree[2].value

        fname = tree[0].value
        metadata = {'expr': f'{fname}{self._get_names_from_tree_values(args)}'}

        if fname not in _SYFUNCTIONS:
            log.error(f'Unknown function: {fname}')
            self.error(fname)

        else:
            # Constant spectrum
            if fname == 'unit':
                if args[1] not in _SYFORMS:
                    log.error(f'Unrecognized unit: {args[1]}')
                    self.error(fname)
                try:
                    fluxunit = units.validate_unit(args[1])
                    tree.value = SourceSpectrum(
                        ConstFlux1D, amplitude=args[0]*fluxunit, meta=metadata)
                except NotImplementedError as e:
                    log.error(str(e))
                    self.error(fname)

            # Black body
            elif fname == 'bb':
                tree.value = SourceSpectrum(
                    BlackBodyNorm1D, temperature=args[0]*u.K)

            # Power law
            elif fname == 'pl':
                if args[2] not in _SYFORMS:
                    log.error(f'Unrecognized unit: {args[2]}')
                    self.error(fname)
                try:
                    fluxunit = units.validate_unit(args[2])
                    tree.value = SourceSpectrum(
                        PowerLawFlux1D, amplitude=1*fluxunit, x_0=args[0]*u.AA,
                        alpha=-args[1], meta=metadata)
                except (synexceptions.SynphotError, NotImplementedError) as e:
                    log.error(str(e))
                    self.error(fname)

            # Box throughput
            elif fname == 'box':
                tree.value = SpectralElement(
                    Box1D, amplitude=1, x_0=args[0]*u.AA, width=args[1]*u.AA,
                    meta=metadata)

            # Source spectrum from file
            elif fname == 'spec':
                tree.value = SourceSpectrum.from_file(irafconvert(args[0]))
                tree.value.meta.update(metadata)

            # Passband
            elif fname == 'band':
                tree.value = spectrum.band(tree[2].svalue)  # string value
                tree.value.meta.update(metadata)

            # Gaussian emission line
            elif fname == 'em':
                if args[3] not in _SYFORMS:
                    log.error(f'Unrecognized unit: {args[3]}')
                    self.error(fname)
                x0 = args[0] * u.AA
                fluxunit = units.validate_unit(args[3])
                totflux = args[2] * (fluxunit * u.AA)
                tree.value = SourceSpectrum(
                    GaussianFlux1D, total_flux=totflux, mean=x0,
                    fwhm=args[1]*u.AA)

            # Catalog interpolation
            elif fname == 'icat':
                tree.value = grid_to_spec(*args)

            # Renormalize source spectrum
            elif fname == 'rn':
                sp = args[0]
                bp = args[1]
                fluxunit = units.validate_unit(args[3])
                rnval = args[2] * fluxunit

                if not isinstance(sp, SourceSpectrum):
                    sp = SourceSpectrum.from_file(irafconvert(sp))

                if not isinstance(bp, SpectralElement):
                    bp = SpectralElement.from_file(irafconvert(bp))

                # Always force the renormalization to occur: prevent exceptions
                # in case of partial overlap. Less robust but duplicates
                # IRAF SYNPHOT. Force the renormalization in the case of
                # partial overlap, but raise an exception if the spectrum and
                # bandpass are entirely disjoint.
                try:
                    tree.value = sp.normalize(
                        rnval, band=bp, area=conf.area, vegaspec=spectrum.Vega)
                except synexceptions.PartialOverlap:
                    tree.value = sp.normalize(
                        rnval, band=bp, area=conf.area, vegaspec=spectrum.Vega,
                        force=True)
                    tree.value.warnings = {
                        'force_renorm': ('Renormalization exceeds the limit '
                                         'of the specified passband.')}
                tree.value.meta.update(metadata)

            # Redshift source spectrum (flat spectrum if fails)
            elif fname == 'z':
                sp = args[0]

                # ETC generates junk (i.e., 'null') sometimes
                if isinstance(sp, str) and sp != 'null':
                    sp = SourceSpectrum.from_file(irafconvert(sp))

                if isinstance(sp, SourceSpectrum):
                    tree.value = sp
                    tree.value.z = args[1]
                else:
                    tree.value = SourceSpectrum(
                        ConstFlux1D, amplitude=1*units.PHOTLAM)

                tree.value.meta.update(metadata)

            # Extinction
            elif fname == 'ebmvx':
                try:
                    tree.value = spectrum.ebmvx(args[1], args[0])
                except synexceptions.SynphotError as e:
                    log.error(str(e))
                    self.error(fname)
                tree.value.meta.update(metadata)

            # Default
            else:
                tree.value = (f'would call {fname} with the following args: '
                              f'{repr(args)}')


def tokens_info(tlist):  # pragma: no cover
    """Print tokens for debugging.

    Parameters
    ----------
    tlist : list
        List of tokens.

    """
    for token in tlist:
        log.info(f'{token.type} {token.attr}')


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
