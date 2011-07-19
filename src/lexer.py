# IxCode - app for code spelunking :: block diagram
# Generic lexer

import sys

import ply.lex

class Lexer():
    """
    The actual lexer. It is instantiated in the lex method below (used for
    testing it) or by the parser. Returns an iterator over a stream of tokens.
    """
    def __init__(self, filename, lex_err):
        """
        Inits the lexer.
        """
        self._err = lex_err
        self._file = filename

    def __iter__(self):
        """
        Returns iteself as an iterator.
        """
        self._lex = ply.lex.lex(self)
        with open(self._file) as f:
            self._lex.input(f.read())
        return self

    def next(self):
        """
        Returns next token from the stream.
        """
        t = self._lex.token()
        if t:
            return t
        raise StopIteration

    def t_error(self, t):
        """
        Called when an erroneous token is encountered.
        """
        msg = 'Illegal character %s' % repr(t.value[0])
        self.error(msg, t)

    def error(self, msg, t):
        """
        Called to report an error.
        """
        location = self.__get_location(t)
        self._err(msg, *location)
        self._lex.skip(1) # if we get here, skip err token

    def __get_location(self, t):
        """
        Returns the location of a token as a tuple (line, col).
        """
        column = t.lexpos
        while column > 0:
            if self._lex.lexdata[column] == '\n':
                break
            column -= 1
        column = t.lexpos - column
        return (t.lineno, column + 1)

def lex_err(msg, line, column):
    """
    Reports a lexer error. Doesn't stop lexing.

        msg - message to print
        line - line of error
        column - column of error
        --
        returns: None
    """
    print >> sys.stderr, msg, 'at %d:%d' % (line, column)
    print >> sys.stderr, 'If you think this is an IxCode error report it.'
    sys.exit(-1)

def lex(filename, lang_dict={}):
    """
    Lexes a filename.

        filename - filename to lex
        --
        returns: None
    """
    lex = Lexer(filename, lex_err)

    # Inject language specific tokens and definitions here
    for k in lang_dict:
        Lexer.__dict__[k] = lang_dict[k]

    for tok in lex:
        print "-", tok.value, tok.type, tok.lineno, tok.lexpos


