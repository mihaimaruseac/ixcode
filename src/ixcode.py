# IxCode - app for code spelunking :: block diagram
# Overmind

import c.ixcode as c
import python.ixcode as python

import lexer

def main(filename, functions, opts, arg_err):
    """
    Gets the ASTs for each of the required methods (all functions in file if
    functions == []) then dumps it to a DOT formatted file calling dot to
    obtain the required diagram.

    Each AST is obtained by a dispatch to that specific language's parser.

        filename - filename to parse
        functions - list of functions to parse
        arg_err - callback for errors caused by a command line argument
        opts - user options
        --
        returns: None
    """
    if opts.type == 'C':
        lexer.lex(filename, c.lang_lex_dict)
    elif opts.type == 'Python':
        lexer.lex(filename, python.lang_lex_dict)

