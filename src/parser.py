# IxCode - app for code spelunking :: block diagram
# Generic parser

import sys

import ply.yacc

class Parser():
    """
    The generic parser. It is instantiated in the parse method below this
    class. Call build to get the AST.
    """
    def __init__(self, lex, filename, parse_err, debug=False):
        self._lex = lex
        self.tokens = self._lex.tokens
        self._file = filename
        self._err = parse_err
        self._debug = debug

    def __build(self):
        """
        Constructs the actual parser (after language specific rules are
        injected).
        """
        if self._debug:
            self._parser = ply.yacc.yacc(module=self, write_tables=0)
        else:
            self._parser = ply.yacc.yacc(module=self, optimize=True)

    def parse(self):
        """
        Returns a generic AST as given by the ast.py module.
        """
        self.__build()
        dbg = 1 if self._debug else 0
        with open(self._file) as f:
            ast = self._parser.parse(lexer=self._lex, input=f.read(),
                    debug=dbg)
        return ast

    def p_error(self, p):
        """
        Called when encountering a non expected token. If p is None then end
        of input was reached, otherwise we have a valid error.

        Do no recovery, let PLY handle it.
        """
        if p:
            self._err("Parse error near line %d: ``%s''" % (p.lineno, p.value))
        else:
            self._err("Parse error at end of input (incomplete input): " + \
                    "``%s''" % p.value)

    def p_empty(self, p):
        'empty  :'
        """
        Empty production
        """
        pass # don't do anything with the stack

def parse_err(msg, line=None):
    """
    Reports a parse error. Doesn't stop parsing.

        msg - message to print
        line - line of error (if known)
        --
        returns: None
    """
    print >> sys.stderr, msg
    print >> sys.stderr, '\nIf you think this is an IxCode error report it.'

def parse(lex, filename, lang_dict={}, debug=False):
    """
    Constructs an AST for a filename.

        lex - lexer used to lex target source
        filename - filename to parse
        lang_dict - dictionary with extensions for a specific language
        --
        returns: AST representation of filename
    """
    parser = Parser(lex, filename, parse_err, debug)

    # Inject language specific tokens and definitions here
    for k in lang_dict:
        Parser.__dict__[k] = lang_dict[k]

    return parser.parse()

