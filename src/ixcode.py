# IxCode - app for code spelunking :: block diagram
# Overmind

import c.ixcode as c
import python.ixcode as python

import lexer
import parser

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
    lex = get_lexer(filename, opts)
    ast = get_ast(lex, filename, opts)

def get_lexer(filename, opts):
    """
    Returns the lexer for a language.

        filename - filename to parse
        opts - user options
        --
        returns: lexer
    """
    if opts.type == 'C':
        return lexer.lex(filename, c.lang_lex_dict)
    elif opts.type == 'Python':
        return lexer.lex(filename, python.lang_lex_dict)
    arg_err("Unable to get lexer for %s files." % opts.type)

def get_ast(lex, filename, opts):
    """
    Returns the AST for a file

        lex - lexer for that file
        filename - filename to parse
        opts - user options
        --
        returns: ast
    """
    if opts.type == 'C':
        return parser.parse(lex, filename, c.lang_parse_dict)
    elif opts.type == 'Python':
        return parser.parse(lex, filename, python.lang_parse_dict)
    arg_err("Unable to parse %s language files." % opts.type)

