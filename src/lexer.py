# IxCode - app for code spelunking :: block diagram
# Generic lexer

import sys

import ply.lex

class Lexer():
    """
    The actual lexer. It is instantiated in the lex method below (used for
    testing it) or by the parser. Returns an iterator over a stream of tokens.
    """
    def __init__(self, filename, lex_err, debug=False):
        """
        Inits the lexer.
        """
        self._err = lex_err
        self._file = filename
        self._built = False
        self._debug = debug

    def __iter__(self):
        """
        Returns itself as an iterator.
        """
        if not self._built:
            self.__build()
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

    def token(self):
        """
        Required by parser.py. Do not call, use the above iterator methods
        instead.
        """
        if not self._built:
            self.__build()
        return self._lex.token()

    def input(self, text):
        """
        Required by parser.py. Do not call, use the above iterator methods
        instead.
        """
        if not self._built:
            self.__build()
        self._lex.input(text)

    def __build(self):
        """
        Builds the lexer. To be called only from the inside.
        """
        if self._debug:
            self._lex = ply.lex.lex(self)
        else:
            self._lex = ply.lex.lex(self, optimize=True,
                    lextab='%slextab' % self.language)
        self._built = True

    def t_error(self, t):
        """
        Called when an erroneous token is encountered.
        """
        msg = 'Illegal character %s' % repr(t.value[0])
        self.error(msg, t)
        self._lex.skip(1) # if we get here, skip err token

    def error(self, msg, t):
        """
        Called to report an error.
        """
        location = self.__get_location(t)
        self._err(msg, *location)

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
    Reports a lexer error. Stops lexing.

        msg - message to print
        line - line of error
        column - column of error
        --
        returns: None
    """
    print >> sys.stderr, msg, 'at %d:%d' % (line, column)
    print >> sys.stderr, '\nIf you think this is an IxCode error report it.'
    sys.exit(-1)

def lex(filename, lang_dict={}, debug=False):
    """
    Constructs a lexer for a filename.

        filename - filename to lex
        lang_dict - dictionary with extensions for a specific language
        --
        returns: lexer
    """
    lex = Lexer(filename, lex_err, debug)

    # Inject language specific tokens and definitions here
    for k in lang_dict:
        Lexer.__dict__[k] = lang_dict[k]

    return lex

