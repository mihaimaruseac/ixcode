# IxCode - app for code spelunking :: block diagram
# Overmind

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
    ast = get_ast(filename, opts)

def get_ast(filename, opts):
    """
    Returns the AST for a file

        filename - filename to parse
        opts - user options
        --
        returns: ast
    """
    if opts.type == 'C':
        from c.ixcode import (lang_lex_dict, lang_parse_dict)
        lex = lexer.lex(filename, lang_lex_dict)
        return parser.parse(lex, filename, lang_parse_dict)
    elif opts.type == 'Python':
        from python.ixcode import (lang_lex_dict, lang_parse_dict)
        lex = lexer.lex(filename, python.lang_lex_dict)
        return parser.parse(lex, filename, python.lang_parse_dict)
    arg_err("Unable to parse %s language files." % opts.type)

