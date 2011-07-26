# IxCode - app for code spelunking :: block diagram
# Data for parsing C code.

import ast

# debug
import sys
def _p(msg):
    print >> sys.stderr, msg

start = 'file'

precedence = (
        ('right', 'ID'),
        )

def p_file_0(self, p):
    'file   :   empty'
    _p(p.slice)

def p_file_1(self, p):
    'file   :   file PPHASH'
    """
    Raise error if encountering this token.
    """
    raise SyntaxError

def p_file_2(self, p):
    'file   :   file decl'
    _p(p.slice)

def p_file_3(self, p):
    'file   :   file function'
    _p(p.slice)

def p_decl(self, p):
    'decl   :   decl_specs type_spec varlist SEMI'
    _p(p.slice)

def p_decl_specs_1(self, p):
    'decl_specs :   empty'
    _p(p.slice)

def p_decl_specs_2(self, p):
    'decl_specs :   decl_specs type_qualifier'
    _p(p.slice)

def p_decl_specs_3(self, p):
    'decl_specs :   decl_specs storage_class'
    _p(p.slice)

def p_decl_specs_4(self, p):
    'decl_specs :   decl_specs func_spec'
    _p(p.slice)

def p_type_qualifier(self, p):
    """
    type_qualifier  :   CONST
                    |   RESTRICT
                    |   VOLATILE
    """
    _p(p.slice)

def p_storage_class(self, p):
    """
    storage_class   :   AUTO
                    |   REGISTER
                    |   STATIC
                    |   EXTERN
                    |   TYPEDEF
    """
    _p(p.slice)

def p_func_spec(self, p):
    'func_spec  :   INLINE'
    _p(p.slice)

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
    _p(p.slice)

def p_type_spec_2(self, p):
    'type_spec  :   LONG LONG'
    _p(p.slice)

def p_type_spec_3(self, p):
    'type_spec  :   LONG INT'
    _p(p.slice)

def p_type_spec_4(self, p):
    'type_spec  :   LONG LONG INT'
    _p(p.slice)

def p_varlist_1(self, p):
    'varlist    :   variable'
    _p(p.slice)

def p_varlist_2(self, p):
    'varlist    :   varlist COMMA variable'
    _p(p.slice)

def p_variable_1(self, p):
    'variable   :   var_name'
    _p(p.slice)

def p_variable_2(self, p):
    'variable   :   pointer variable'
    _p(p.slice)

def p_variable_3(self, p):
    'variable   :   var_name array'
    _p(p.slice)

def p_var_name(self, p):
    'var_name   :   ID'
    _p(p[1])
    _p(p.slice)

def p_pointer(self, p):
    'pointer    :   TIMES decl_specs'
    _p(p.slice)

def p_array_1(self, p):
    'array  :   LBRACKET array_expression RBRACKET'
    _p(p.slice)

def p_array_2(self, p):
    'array  :   array LBRACKET array_expression RBRACKET'
    _p(p.slice)

def p_array_expression_1(self, p):
    'array_expression   :   expression'
    _p(p.slice)

def p_array_expression_2(self, p):
    'array_expression   :   TIMES'
    _p(p.slice)

def p_array_expression_3(self, p):
    'array_expression   :   empty'
    _p(p.slice)

def p_expression(self, p):
    'expression :   ID'
    # TODO: fill
    _p(p[1])
    _p(p.slice)

def p_function_0(self, p):
    'function   :   decl_specs type_spec func_name LPAREN f_arg_list RPAREN SEMI'
    _p(p.slice)

def p_function_1(self, p):
    'function   :   decl_specs type_spec func_name LPAREN f_arg_list RPAREN block'
    _p(p.slice)

def p_func_name(self, p):
    'func_name  :   ID'
    _p(p.slice)

def p_f_arg_list(self, p):
    'f_arg_list :   empty'
    # TODO: fill
    _p(p.slice)

def p_block(self, p):
    'block  :   LBRACE block_content RBRACE'
    _p(p.slice)

def p_block_content_0(self, p):
    'block_content  :   empty'
    _p(p.slice)

def p_block_content_1(self, p):
    'block_content  :   decl'
    # TODO: fill
    _p(p.slice)

