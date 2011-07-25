# IxCode - app for code spelunking :: block diagram
# Data for parsing C code.

import ast

# Construct lang_lex_dict dictionary
lang_parse_dict = {}

# start symbol
lang_parse_dict['start'] = 'file'

# debug
import sys
def _p(msg):
    print >> sys.stderr, msg

def p_file_0(self, p):
    'file   :   empty'
    _p(p.slice)
lang_parse_dict['p_file_0'] = p_file_0

def p_file_1(self, p):
    'file   :   file PPHASH'
    """
    Raise error if encountering this token.
    """
    raise SyntaxError
lang_parse_dict['p_file_1'] = p_file_1

def p_file_2(self, p):
    'file   :   file decl'
    _p(p.slice)
lang_parse_dict['p_file_2'] = p_file_2

def p_decl_1(self, p):
    'decl   :   decl_specs type_spec varlist SEMI'
    _p(p.slice)
lang_parse_dict['p_decl_1'] = p_decl_1

def p_decl_specs_1(self, p):
    'decl_specs :   empty'
    _p(p.slice)
lang_parse_dict['p_decl_specs_1'] = p_decl_specs_1

def p_decl_specs_2(self, p):
    'decl_specs :   decl_specs type_qualifier'
    _p(p.slice)
lang_parse_dict['p_decl_specs_2'] = p_decl_specs_2

#def p_decl_specs_3(self, p):
#    'decl_specs :   decl_specs type_spec'
#    _p(p.slice)
#lang_parse_dict['p_decl_specs_3'] = p_decl_specs_3

def p_decl_specs_4(self, p):
    'decl_specs :   decl_specs storage_class'
    _p(p.slice)
lang_parse_dict['p_decl_specs_4'] = p_decl_specs_4

def p_decl_specs_5(self, p):
    'decl_specs :   decl_specs func_spec'
    _p(p.slice)
lang_parse_dict['p_decl_specs_5'] = p_decl_specs_5

def p_type_qualifier(self, p):
    """
    type_qualifier  :   CONST
                    |   RESTRICT
                    |   VOLATILE
    """
    _p(p.slice)
lang_parse_dict['p_type_qualifier'] = p_type_qualifier

def p_type_spec_1(self, p):
    """
    type_spec   :   VOID
                |   CHAR
                |   SHORT
                |   INT
                |   LONG
                |   FLOAT
                |   DOUBLE
                |   SIGNED
                |   UNSIGNED
                |   ID
    """
#                |   enum_spec
#                |   struct_spec
#                |   union_spec
    _p(p.slice)
lang_parse_dict['p_type_spec_1'] = p_type_spec_1

def p_type_spec_2(self, p):
    'type_spec  :   LONG LONG'
    _p(p.slice)
lang_parse_dict['p_type_spec_2'] = p_type_spec_2

def p_type_spec_3(self, p):
    'type_spec  :   LONG INT'
    _p(p.slice)
lang_parse_dict['p_type_spec_3'] = p_type_spec_3

def p_type_spec_4(self, p):
    'type_spec  :   LONG LONG INT'
    _p(p.slice)
lang_parse_dict['p_type_spec_4'] = p_type_spec_4

def p_storage_class(self, p):
    """
    storage_class   :   AUTO
                    |   REGISTER
                    |   STATIC
                    |   EXTERN
                    |   TYPEDEF
    """
    _p(p.slice)
lang_parse_dict['p_storage_class'] = p_storage_class

def p_func_spec(self, p):
    'func_spec  :   INLINE'
    _p(p.slice)
lang_parse_dict['p_func_spec'] = p_func_spec

def p_varlist_1(self, p):
    'varlist    :   variable'
    _p(p.slice)
lang_parse_dict['p_varlist_1'] = p_varlist_1

def p_varlist_2(self, p):
    'varlist    :   varlist COMMA variable'
    _p(p.slice)
lang_parse_dict['p_varlist_2'] = p_varlist_2

def p_variable_1(self, p):
    'variable   :   var_name'
    _p(p.slice)
lang_parse_dict['p_variable_1'] = p_variable_1

def p_variable_2(self, p):
    'variable   :   pointer variable'
    _p(p.slice)
lang_parse_dict['p_variable_2'] = p_variable_2

def p_variable_3(self, p):
    'variable   :   var_name LBRACKET expression RBRACKET'
    _p(p.slice)
lang_parse_dict['p_variable_3'] = p_variable_3

def p_pointer_1(self, p):
    'pointer    :   TIMES decl_specs'
    _p(p.slice)
lang_parse_dict['p_pointer_1'] = p_pointer_1

#def p_pointer_2(self, p):
#    'pointer    :   TIMES CONST'
#    _p(p.slice)
#lang_parse_dict['p_pointer_2'] = p_pointer_2

def p_var_name_1(self, p):
    'var_name   :   ID'
    _p(p[1])
    _p(p.slice)
lang_parse_dict['p_var_name_1'] = p_var_name_1

def p_expression(self, p):
    'expression :   ID'
    _p(p[1])
    _p(p.slice)
lang_parse_dict['p_expression'] = p_expression

