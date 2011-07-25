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
    'decl   :   decl_specs varlist SEMI'
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

def p_decl_specs_3(self, p):
    'decl_specs :   decl_specs type_spec'
    _p(p.slice)
lang_parse_dict['p_decl_specs_3'] = p_decl_specs_3

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

def p_type_spec(self, p):
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
lang_parse_dict['p_type_spec'] = p_type_spec

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

def p_var_name_1(self, p):
    'var_name   :   ID'
    _p(p[1])
    _p(p.slice)
lang_parse_dict['p_var_name_1'] = p_var_name_1

#def p_decl_1(self, p):
#    'decl  :   empty'
#    print p.slice
#lang_parse_dict['p_decl_1'] = p_decl_1
#
#def p_decl_2(self, p):
#    'decl   :   SEMI'
#    print p.slice
#lang_parse_dict['p_decl_2'] = p_decl_2
#
#def p_decl_3(self, p):
#    'decl  :   decl external_decl'
#    """
#    global vars, forward defs
#    """
#    print p.slice
#lang_parse_dict['p_decl_3'] = p_decl_3
#
#def p_external_decl(self, p):
#    'external_decl  :   var_declaration SEMI'
#    p[0] = p[1]
#lang_parse_dict['p_external_decl'] = p_external_decl
#
#def p_var_declaration_1(self, p):
#    'var_declaration    :   decl_specs'
#    """
#    struct something; /* forward decl */
#    """
#    print p.slice
#lang_parse_dict['p_var_declaration_1'] = p_var_declaration_1
#
#def p_var_declaration_2(self, p):
#    'var_declaration    :   decl_specs var_list'
#    print p.slice
#lang_parse_dict['p_var_declaration_2'] = p_var_declaration_2

#def p_enum_spec(self, p):
#    'enum_spec  :   ENUM ID'
#    print p.slice
#lang_parse_dict['p_enum_spec'] = p_enum_spec
#
#def p_struct_spec(self, p):
#    'struct_spec    :   STRUCT ID'
#    print p.slice
#lang_parse_dict['p_struct_spec'] = p_struct_spec
#
#def p_union_spec(self, p):
#    'union_spec :   UNION ID'
#    print p.slice
#lang_parse_dict['p_union_spec'] = p_union_spec

#def p_var_list_1(self, p):
#    'var_list   :   var_decl'
#    """
#    a in int a;
#    """
#    print p.slice
#lang_parse_dict['p_var_list_1'] = p_var_list_1
#
#def p_var_list_2(self, p):
#    'var_list   :   var_list COMMA var_decl'
#    """
#    a, b, c in int a, b, c;
#    """
#    print p.slice
#lang_parse_dict['p_var_list_2'] = p_var_list_2
#
#def p_var_decl_1(self, p):
#    'var_decl   :   declarator'
#    """
#    a in int a;
#    """
#    print p.slice
#lang_parse_dict['p_var_decl_1'] = p_var_decl_1
#
#def p_var_decl_2(self, p):
#    'var_decl   :   declarator EQUALS init'
#    """
#    a = 3 in int a = 3;
#    """
#    print p.slice
#lang_parse_dict['p_var_decl_2'] = p_var_decl_2
#
#def p_declarator_1(self, p):
#    'declarator :   direct_declarator'
#    print p.slice
#lang_parse_dict['p_declarator_1'] = p_declarator_1
#
#def p_declarator_2(self, p):
#    'declarator :   pointer direct_declarator'
#    print p.slice
#lang_parse_dict['p_declarator_2'] = p_declarator_2
#
#def p_pointer_1(self, p):
#    'pointer    :   TIMES'
#    print p.slice
#lang_parse_dict['p_pointer_1'] = p_pointer_1
#
#def p_pointer_2(self, p):
#    'pointer    :   TIMES type_qualifier_list'
#    print p.slice
#lang_parse_dict['p_pointer_2'] = p_pointer_2
#
#def p_pointer_3(self, p):
#    'pointer    :   TIMES pointer'
#    print p.slice
#lang_parse_dict['p_pointer_3'] = p_pointer_3
#
#def p_pointer_4(self, p):
#    'pointer    :   TIMES type_qualifier_list pointer'
#    print p.slice
#lang_parse_dict['p_pointer_4'] = p_pointer_4
#
#def p_direct_declarator_1(self, p):
#    'direct_declarator  :   ID'
#    print p.slice
#lang_parse_dict['p_direct_declarator_1'] = p_direct_declarator_1
#
#def p_direct_declarator_2(self, p):
#    'direct_declarator  :   LPAREN declarator RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_declarator_2'] = p_direct_declarator_2
#
#def p_direct_declarator_3(self, p):
#    'direct_declarator  :   direct_declarator LBRACKET RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_declarator_3'] = p_direct_declarator_3
#
#def p_direct_declarator_4(self, p):
#    'direct_declarator  :   direct_declarator LBRACKET assignment_expression RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_declarator_4'] = p_direct_declarator_4
#
#def p_direct_declarator_5(self, p):
#    'direct_declarator  :   direct_declarator LBRACKET TIMES RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_declarator_5'] = p_direct_declarator_5
#
#def p_direct_declarator_6(self, p):
#    'direct_declarator  :   direct_declarator LPAREN parameter_type_list RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_declarator_6'] = p_direct_declarator_6
#
#def p_direct_declarator_7(self, p):
#    'direct_declarator  :   direct_declarator LPAREN RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_declarator_7'] = p_direct_declarator_7
#
#def p_direct_declarator_8(self, p):
#    'direct_declarator  :   direct_declarator LPAREN identifier_list RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_declarator_8'] = p_direct_declarator_8
#
#def p_init_1(self, p):
#    'init   :   assignment_expression'
#    print p.slice
#lang_parse_dict['p_init_1'] = p_init_1
#
#def p_init_2(self, p):
#    'init   :   LBRACE initializer_list RBRACE'
#    print p.slice
#lang_parse_dict['p_init_2'] = p_init_2
#
#def p_init_3(self, p):
#    'init   :   LBRACE initializer_list COMMA RBRACE'
#    print p.slice
#lang_parse_dict['p_init_3'] = p_init_3
#
#def p_type_qualifier_list_1(self, p):
#    'type_qualifier_list    :   type_qualifier'
#    print p.slice
#lang_parse_dict['p_type_qualifier_list_1'] = p_type_qualifier_list_1
#
#def p_type_qualifier_list_2(self, p):
#    'type_qualifier_list    :   type_qualifier_list type_qualifier'
#    print p.slice
#lang_parse_dict['p_type_qualifier_list_2'] = p_type_qualifier_list_2
#
#def p_assignment_expression_1(self, p):
#    'assignment_expression  :   conditional_expression'
#    print p.slice
#lang_parse_dict['p_assignment_expression_1'] = p_assignment_expression_1
#
#def p_assignment_expression_2(self, p):
#    'assignment_expression  :   unary_expression assignment_operator assignment_expression'
#    print p.slice
#lang_parse_dict['p_assignment_expression_2'] = p_assignment_expression_2
#
#def p_parameter_type_list_1(self, p):
#    'parameter_type_list    :   parameter_list'
#    print p.slice
#lang_parse_dict['p_parameter_type_list_1'] = p_parameter_type_list_1
#
#def p_parameter_type_list_2(self, p):
#    'parameter_type_list    :   parameter_list COMMA ELLIPSIS'
#    """
#    f (int a, int b, ...)
#    """
#    print p.slice
#lang_parse_dict['p_parameter_type_list_2'] = p_parameter_type_list_2
#
#def p_identifier_list_1(self, p):
#    'identifier_list    :   ID'
#    print p.slice
#lang_parse_dict['p_identifier_list_1'] = p_identifier_list_1
#
#def p_identifier_list_2(self, p):
#    'identifier_list    :   identifier_list COMMA ID'
#    print p.slice
#lang_parse_dict['p_identifier_list_2'] = p_identifier_list_2
#
#def p_initializer_list_1(self, p):
#    'initializer_list   :   initializer'
#    print p.slice
#lang_parse_dict['p_initializer_list_1'] = p_initializer_list_1
#
#def p_initializer_list_2(self, p):
#    'initializer_list   :   designation initializer'
#    print p.slice
#lang_parse_dict['p_initializer_list_2'] = p_initializer_list_2
#
#def p_initializer_list_3(self, p):
#    'initializer_list   :   initializer_list COMMA initializer'
#    print p.slice
#lang_parse_dict['p_initializer_list_3'] = p_initializer_list_3
#
#def p_initializer_list_4(self, p):
#    'initializer_list   :   initializer_list COMMA designation initializer'
#    print p.slice
#lang_parse_dict['p_initializer_list_4'] = p_initializer_list_4
#
#def p_conditional_expression_1(self, p):
#    'conditional_expression :   binary_expression'
#    print p.slice
#lang_parse_dict['p_conditional_expression_1'] = p_conditional_expression_1
#
#def p_conditional_expression_2(self, p):
#    'conditional_expression :   binary_expression CONDOP expression COLON conditional_expression'
#    print p.slice
#lang_parse_dict['p_conditional_expression_2'] = p_conditional_expression_2
#
#def p_unary_expression_1(self, p):
#    'unary_expression   :   postfix_expression'
#    print p.slice
#lang_parse_dict['p_unary_expression_1'] = p_unary_expression_1
#
#def p_unary_expression_2(self, p):
#    """
#    unary_expression    :   PLUSPLUS unary_expression
#                        |   MINUSMINUS  unary_expression
#                        |   unary_operator cast_expression
#    """
#    print p.slice
#lang_parse_dict['p_unary_expression_2'] = p_unary_expression_2
#
#def p_unary_expression_3(self, p):
#    """
#    unary_expression    :   SIZEOF unary_expression
#                        |   SIZEOF LPAREN type_name RPAREN
#    """
#    print p.slice
#lang_parse_dict['p_unary_expression_3'] = p_unary_expression_3
#
#def p_assignment_operator(self, p):
#    """
#    assignment_operator : EQUALS
#                        | XOREQUAL
#                        | TIMESEQUAL
#                        | DIVEQUAL
#                        | MODEQUAL
#                        | PLUSEQUAL
#                        | MINUSEQUAL
#                        | LSHIFTEQUAL
#                        | RSHIFTEQUAL
#                        | ANDEQUAL
#                        | OREQUAL
#    """
#    print p.slice
#lang_parse_dict['p_assignment_operator'] = p_assignment_operator
#
#def p_parameter_list_1(self, p):
#    'parameter_list :   parameter_declaration'
#    print p.slice
#lang_parse_dict['p_parameter_list_1'] = p_parameter_list_1
#
#def p_parameter_list_2(self, p):
#    'parameter_list :   parameter_list COMMA parameter_declaration'
#    print p.slice
#lang_parse_dict['p_parameter_list_2'] = p_parameter_list_2
#
#def p_designation(self, p):
#    'designation    :   designator_list EQUALS'
#    print p.slice
#lang_parse_dict['p_designation'] = p_designation
#
#def p_initializer_1(self, p):
#    'initializer    :   assignment_expression'
#    print p.slice
#lang_parse_dict['p_initializer_1'] = p_initializer_1
#
#def p_initializer_2(self, p):
#    'initializer    :   LBRACE initializer_list RBRACE'
#    print p.slice
#lang_parse_dict['p_initializer_2'] = p_initializer_2
#
#def p_initializer_3(self, p):
#    'initializer    :   LBRACE initializer_list COMMA RBRACE'
#    print p.slice
#lang_parse_dict['p_initializer_3'] = p_initializer_3
#
#def p_binary_expression(self, p):
#    """
#    binary_expression   : cast_expression
#                        | binary_expression TIMES binary_expression
#                        | binary_expression DIVIDE binary_expression
#                        | binary_expression MOD binary_expression
#                        | binary_expression PLUS binary_expression
#                        | binary_expression MINUS binary_expression
#                        | binary_expression RSHIFT binary_expression
#                        | binary_expression LSHIFT binary_expression
#                        | binary_expression LT binary_expression
#                        | binary_expression LE binary_expression
#                        | binary_expression GE binary_expression
#                        | binary_expression GT binary_expression
#                        | binary_expression EQ binary_expression
#                        | binary_expression NE binary_expression
#                        | binary_expression AND binary_expression
#                        | binary_expression OR binary_expression
#                        | binary_expression XOR binary_expression
#                        | binary_expression LAND binary_expression
#                        | binary_expression LOR binary_expression
#    """
#    print p.slice
#lang_parse_dict['p_binary_expression'] = p_binary_expression
#
#def p_expression_1(self, p):
#    'expression :   assignment_expression'
#    print p.slice
#lang_parse_dict['p_expression_1'] = p_expression_1
#
#def p_expression_2(self, p):
#    'expression :   expression COMMA assignment_expression'
#    print p.slice
#lang_parse_dict['p_expression_2'] = p_expression_2
#
#def p_postfix_expression_1(self, p):
#    'postfix_expression :   primary_expression'
#    print p.slice
#lang_parse_dict['p_postfix_expression_1'] = p_postfix_expression_1
#
#def p_postfix_expression_2(self, p):
#    'postfix_expression :   postfix_expression LBRACKET expression RBRACKET'
#    print p.slice
#lang_parse_dict['p_postfix_expression_2'] = p_postfix_expression_2
#
#def p_postfix_expression_3(self, p):
#    'postfix_expression :   postfix_expression LPAREN argument_expression_list RPAREN'
#    print p.slice
#lang_parse_dict['p_postfix_expression_3'] = p_postfix_expression_3
#
#def p_postfix_expression_4(self, p):
#    'postfix_expression :   postfix_expression LPAREN RPAREN'
#    print p.slice
#lang_parse_dict['p_postfix_expression_4'] = p_postfix_expression_4
#
#def p_postfix_expression_5(self, p):
#    'postfix_expression :   postfix_expression PERIOD ID'
#    print p.slice
#lang_parse_dict['p_postfix_expression_5'] = p_postfix_expression_5
#
#def p_postfix_expression_6(self, p):
#    'postfix_expression :   postfix_expression ARROW ID'
#    print p.slice
#lang_parse_dict['p_postfix_expression_6'] = p_postfix_expression_6
#
#def p_postfix_expression_7(self, p):
#    """
#    postfix_expression  :   postfix_expression PLUSPLUS
#                        |   postfix_expression MINUSMINUS
#    """
#    print p.slice
#lang_parse_dict['p_postfix_expression_7'] = p_postfix_expression_7
#
#def p_postfix_expression_8(self, p):
#    'postfix_expression :   LPAREN type_name RPAREN LBRACE initializer_list RBRACE'
#    print p.slice
#lang_parse_dict['p_postfix_expression_8'] = p_postfix_expression_8
#
#def p_postfix_expression_9(self, p):
#    'postfix_expression :   LPAREN type_name RPAREN LBRACE initializer_list COMMA RBRACE'
#    print p.slice
#lang_parse_dict['p_postfix_expression_9'] = p_postfix_expression_9
#
#def p_cast_expression_1(self, p):
#    'cast_expression    :   unary_expression'
#    print p.slice
#lang_parse_dict['p_cast_expression_1'] = p_cast_expression_1
#
#def p_cast_expression_2(self, p):
#    'cast_expression    :   LPAREN type_name RPAREN cast_expression'
#    print p.slice
#lang_parse_dict['p_cast_expression_2'] = p_cast_expression_2
#
#def p_unary_operator(self, p):
#    """
#    unary_operator  :   AND
#                    |   OR
#                    |   PLUS
#                    |   MINUS
#                    |   NOT
#                    |   LNOT
#    """
#    print p.slice
#lang_parse_dict['p_unary_operator'] = p_unary_operator
#
#def p_type_name_1(self, p):
#    'type_name  :   specifier_qualifier_list'
#    print p.slice
#lang_parse_dict['p_type_name_1'] = p_type_name_1
#
#def p_type_name_2(self, p):
#    'type_name  :   specifier_qualifier_list abstract_declarator'
#    print p.slice
#lang_parse_dict['p_type_name_2'] = p_type_name_2
#
#def p_parameter_declaration_1(self, p):
#    'parameter_declaration  :   decl_specs declarator'
#    print p.slice
#lang_parse_dict['p_parameter_declaration_1'] = p_parameter_declaration_1
#
#def p_parameter_declaration_2(self, p):
#    'parameter_declaration  :   decl_specs'
#    print p.slice
#lang_parse_dict['p_parameter_declaration_2'] = p_parameter_declaration_2
#
#def p_parameter_declaration_3(self, p):
#    'parameter_declaration  :   decl_specs abstract_declarator'
#    print p.slice
#lang_parse_dict['p_parameter_declaration_3'] = p_parameter_declaration_3
#
#def p_designator_list_1(self, p):
#    'designator_list    :   designator'
#    print p.slice
#lang_parse_dict['p_designator_list_1'] = p_designator_list_1
#
#def p_designator_list_2(self, p):
#    'designator_list    :   designator_list designator'
#    print p.slice
#lang_parse_dict['p_designator_list_2'] = p_designator_list_2
#
#def p_primary_expression_1(self, p):
#    'primary_expression :   ID'
#    print p.slice
#lang_parse_dict['p_primary_expression_1'] = p_primary_expression_1
#
#def p_primary_expression_2(self, p):
#    'primary_expression :   constant'
#    print p.slice
#lang_parse_dict['p_primary_expression_2'] = p_primary_expression_2
#
#def p_primary_expression_3(self, p):
#    'primary_expression :   string'
#    print p.slice
#lang_parse_dict['p_primary_expression_3'] = p_primary_expression_3
#
#def p_primary_expression_4(self, p):
#    'primary_expression :   LPAREN expression RPAREN'
#    print p.slice
#lang_parse_dict['p_primary_expression_4'] = p_primary_expression_4
#
#def p_argument_expression_list_1(self, p):
#    'argument_expression_list   :   assignment_expression'
#    print p.slice
#lang_parse_dict['p_argument_expression_list_1'] = p_argument_expression_list_1
#
#def p_argument_expression_list_2(self, p):
#    'argument_expression_list   :   argument_expression_list COMMA assignment_expression'
#    print p.slice
#lang_parse_dict['p_argument_expression_list_2'] = p_argument_expression_list_2
#
#def p_specifier_qualifier_list_1(self, p):
#    'specifier_qualifier_list   :   type_qualifier'
#    print p.slice
#lang_parse_dict['p_specifier_qualifier_list_1'] = p_specifier_qualifier_list_1
#
#def p_specifier_qualifier_list_2(self, p):
#    'specifier_qualifier_list   :   type_spec'
#    print p.slice
#lang_parse_dict['p_specifier_qualifier_list_2'] = p_specifier_qualifier_list_2
#
#def p_specifier_qualifier_list_3(self, p):
#    'specifier_qualifier_list   :   specifier_qualifier_list type_qualifier'
#    print p.slice
#lang_parse_dict['p_specifier_qualifier_list_3'] = p_specifier_qualifier_list_3
#
#def p_specifier_qualifier_list_4(self, p):
#    'specifier_qualifier_list   :   specifier_qualifier_list type_spec'
#    print p.slice
#lang_parse_dict['p_specifier_qualifier_list_4'] = p_specifier_qualifier_list_4
#
#def p_abstract_declarator_1(self, p):
#    'abstract_declarator    :   pointer'
#    print p.slice
#lang_parse_dict['p_abstract_declarator_1'] = p_abstract_declarator_1
#
#def p_abstract_declarator_2(self, p):
#    'abstract_declarator    :   pointer direct_abstract_declarator'
#    print p.slice
#lang_parse_dict['p_abstract_declarator_2'] = p_abstract_declarator_2
#
#def p_abstract_declarator_3(self, p):
#    'abstract_declarator    :   direct_abstract_declarator'
#    print p.slice
#lang_parse_dict['p_abstract_declarator_3'] = p_abstract_declarator_3
#
#def p_designator_1(self, p):
#    'designator :   LBRACKET conditional_expression LBRACKET'
#    """
#    constant expression in fact but we don't bother checking
#    """
#    print p.slice
#lang_parse_dict['p_designator_1'] = p_designator_1
#
#def p_designator_2(self, p):
#    'designator :   PERIOD ID'
#    print p.slice
#lang_parse_dict['p_designator_2'] = p_designator_2
#
#def p_constant(self, p):
#    """
#    constant    :   INT_CONST_DEC
#                |   INT_CONST_OCT
#                |   INT_CONST_HEX
#                |   FLOAT_CONST
#                |   CHAR_CONST
#    """
#    print p.slice
#lang_parse_dict['p_constant'] = p_constant
#
#def p_string_1(self, p):
#    'string :   STRING_LITERAL'
#    print p.slice
#lang_parse_dict['p_string_1'] = p_string_1
#
#def p_string_2(self, p):
#    'string :   string STRING_LITERAL'
#    print p.slice
#lang_parse_dict['p_string_2'] = p_string_2
#
#def p_direct_abstract_declarator_1(self, p):
#    'direct_abstract_declarator :   LPAREN abstract_declarator  RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_1'] = p_direct_abstract_declarator_1
#
#def p_direct_abstract_declarator_2(self, p):
#    'direct_abstract_declarator :   LBRACKET RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_2'] = p_direct_abstract_declarator_2
#
#def p_direct_abstract_declarator_3(self, p):
#    'direct_abstract_declarator :   LBRACKET assignment_expression RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_3'] = p_direct_abstract_declarator_3
#
#def p_direct_abstract_declarator_4(self, p):
#    'direct_abstract_declarator :   direct_abstract_declarator LBRACKET RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_4'] = p_direct_abstract_declarator_4
#
#def p_direct_abstract_declarator_5(self, p):
#    'direct_abstract_declarator :   direct_abstract_declarator LBRACKET assignment_expression RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_5'] = p_direct_abstract_declarator_5
#
#def p_direct_abstract_declarator_6(self, p):
#    'direct_abstract_declarator :   LBRACKET TIMES RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_6'] = p_direct_abstract_declarator_6
#
#def p_direct_abstract_declarator_7(self, p):
#    'direct_abstract_declarator :   direct_abstract_declarator LBRACKET TIMES RBRACKET'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_7'] = p_direct_abstract_declarator_7
#
#def p_direct_abstract_declarator_8(self, p):
#    'direct_abstract_declarator :   LPAREN RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_8'] = p_direct_abstract_declarator_8
#
#def p_direct_abstract_declarator_9(self, p):
#    'direct_abstract_declarator :   LPAREN parameter_type_list RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_9'] = p_direct_abstract_declarator_9
#
#def p_direct_abstract_declarator_10(self, p):
#    'direct_abstract_declarator :   direct_abstract_declarator LPAREN RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_10'] = p_direct_abstract_declarator_10
#
#def p_direct_abstract_declarator_11(self, p):
#    'direct_abstract_declarator :   direct_abstract_declarator LPAREN parameter_type_list RPAREN'
#    print p.slice
#lang_parse_dict['p_direct_abstract_declarator_11'] = p_direct_abstract_declarator_11
#








