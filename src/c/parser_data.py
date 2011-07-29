# IxCode - app for code spelunking :: block diagram
# Data for parsing C code.

import src.ast as ast

# debug
import sys
def _p(msg):
    print >> sys.stderr, msg

start = 'file'

precedence = (
        ('right', 'CONDOP', 'COLON'),
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('nonassoc', 'NE', 'EQ'),
        ('nonassoc', 'LT', 'LE', 'GE', 'GT'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('right', 'POINTER', 'UMINUS', 'PLUSPLUS', 'MINUSMINUS', 'NOT',
            'LNOT', 'SIZEOF'),
        ('right', 'ID'),
        )

def p_file_0(self, p):
    'file   :   empty'
    p[0] = ast.File()

def p_file_1(self, p):
    'file   :   file PPHASH'
    """
    Raise error if encountering this token.
    """
    raise SyntaxError

def p_file_2(self, p):
    'file   :   file decl'
    p[0] = p[1] # ignore global decls

def p_file_3(self, p):
    'file   :   file function'
    p[0] = p[1]
    p[0].add(p[2])

def p_decl(self, p):
    'decl   :   decl_specs type_spec varlist SEMI'
    p[0] = None # ignore global decls

def p_decl_specs_1(self, p):
    'decl_specs :   empty'
    p[0] = ast.TextNode('')

def p_decl_specs_2(self, p):
    'decl_specs :   decl_specs type_qualifier'
    p[0] = ast.TextNode('%s %s' % (p[1], p[2]))

def p_decl_specs_3(self, p):
    'decl_specs :   decl_specs storage_class'
    p[0] = ast.TextNode('%s %s' % (p[1], p[2]))

def p_decl_specs_4(self, p):
    'decl_specs :   decl_specs func_spec'
    p[0] = ast.TextNode('%s %s' % (p[1], p[2]))

def p_type_qualifier(self, p):
    """
    type_qualifier  :   CONST
                    |   RESTRICT
                    |   VOLATILE
    """
    p[0] = ast.TextNode('%s' % p[1])

def p_storage_class(self, p):
    """
    storage_class   :   AUTO
                    |   REGISTER
                    |   STATIC
                    |   EXTERN
                    |   TYPEDEF
    """
    p[0] = ast.TextNode('%s' % p[1])

def p_func_spec(self, p):
    'func_spec  :   INLINE'
    p[0] = ast.TextNode('%s' % p[1])

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
    p[0] = ast.TextNode('%s' % p[1])

def p_type_spec_2(self, p):
    """
    type_spec   :   LONG LONG
                |   LONG INT
    """
    p[0] = ast.TextNode('long %s' % p[2])

def p_type_spec_3(self, p):
    'type_spec  :   LONG LONG INT'
    p[0] = ast.TextNode('long long int')

def p_varlist_1(self, p):
    'varlist    :   variable'
    p[0] = ast.TextNode('%s' % p[1])

def p_varlist_2(self, p):
    'varlist    :   varlist COMMA variable'
    p[0] = ast.TextNode('%s, %s' % (p[1], p[2]))

def p_variable_1(self, p):
    'variable   :   var_name'
    p[0] = ast.TextNode('%s' % p[1])

def p_variable_2(self, p):
    'variable   :   pointer variable'
    p[0] = ast.TextNode('%s %s' % (p[1], p[2]))

def p_variable_3(self, p):
    'variable   :   var_name array'
    p[0] = ast.TextNode('%s%s' % (p[1], p[2]))

def p_var_name(self, p):
    'var_name   :   ID'
    p[0] = ast.TextNode('%s' % p[1])

def p_pointer(self, p):
    'pointer    :   TIMES decl_specs %prec POINTER'
    p[0] = ast.TextNode('*%s' % p[2])

def p_array_1(self, p):
    'array  :   LBRACKET array_expression RBRACKET'
    p[0] = ast.TextNode('[%s]' % p[2])

def p_array_2(self, p):
    'array  :   array LBRACKET array_expression RBRACKET'
    p[0] = ast.TextNode('%s[%s]' % (p[1], p[3]))

def p_array_expression_1(self, p):
    'array_expression   :   expression'
    p[0] = p[1]

def p_array_expression_2(self, p):
    'array_expression   :   TIMES'
    p[0] = ast.TextNode('%s' % p[1])

def p_array_expression_3(self, p):
    'array_expression   :   empty'
    p[0] = ast.TextNode('')

def p_expression_1(self, p):
    'expression :   arg'
    p[0] = ast.Expression("%s" % p[1])

def p_expression_2(self, p):
    """
    expression  :   expression LT expression
                |   expression LE expression
                |   expression EQ expression
                |   expression GE expression
                |   expression GT expression
                |   expression NE expression
                |   expression PLUS expression
                |   expression MINUS expression
                |   expression TIMES expression
                |   expression DIVIDE expression
                |   expression MOD expression
                |   expression LSHIFT expression
                |   expression RSHIFT expression
                |   expression XOR expression
                |   expression LOR expression
                |   expression LAND expression
                |   expression AND expression
                |   expression OR expression
    """
    p[0] = ast.Expression("%s %s %s" % (p[1], p[2], p[3]))

def p_expression_3(self, p):
    'expression  :   MINUS arg %prec UMINUS'
    p[0] = ast.Expression("-%s" % p[2])

def p_expression_4(self, p):
    """
    expression  :   arg PLUSPLUS
                |   arg MINUSMINUS
                |   PLUSPLUS arg
                |   MINUSMINUS arg
    """
    p[0] = ast.TextNode("%s%s" % (p[1], p[2]))

def p_expression_5(self, p):
    """
    expression  :   NOT expression
                |   LNOT expression
    """
    p[0] = ast.TextNode("%s%s" % (p[1], p[2]))

def p_expression_6(self, p):
    'expression :   LPAREN expression RPAREN'
    p[0] = ast.TextNode("(%s)" % p[2])

def p_expression_7(self, p):
    'expression :   SIZEOF expression'
    p[0] = ast.TextNode('%s %s' % (p[1], p[2]))

def p_expression_8(self, p):
    'expression :   expression CONDOP expression COLON expression'
    p[0] = ast.TextNode('%s ? %s : %s' % (p[1], p[3], p[5]))

def p_arg_1(self, p):
    'arg   :   arg_name'
    p[0] = ast.TextNode('%s' % p[1])

def p_arg_2(self, p):
    'arg   :   TIMES arg %prec POINTER'
    p[0] = ast.TextNode('*%s' % p[2])

def p_arg_3(self, p):
    'arg   :   arg_name array'
    p[0] = ast.TextNode('%s%s' % (p[1], p[2]))

def p_arg_4(self, p):
    'arg    :   function_call'
    p[0] = p[1]

def p_arg_name_1(self, p):
    'arg_name   :   ID'
    p[0] = ast.TextNode('%s' % p[1])

def p_arg_name_2(self, p):
    'arg_name   :   constant'
    p[0] = p[1]

def p_constant_1(self, p):
    """
    constant    :   STRING_LITERAL
                |   INT_CONST_DEC
                |   INT_CONST_HEX
                |   INT_CONST_OCT
                |   FLOAT_CONST
                |   CHAR_CONST
    """
    p[0] = ast.TextNode('%s' % p[1])

def p_function_call(self, p):
    'function_call  :   func_name LPAREN arglist RPAREN'
    p[0] = ast.TextNode('%s(%s)' % (p[1], p[3]))

def p_func_name(self, p):
    'func_name  :   ID'
    p[0] = ast.TextNode('%s' % p[1])

def p_arglist_0(self, p):
    'arglist    :   empty'
    p[0] = ast.TextNode('')

def p_arglist_1(self, p):
    'arglist    :   arg'
    p[0] = ast.TextNode('%s' % p[1])

def p_arglist_2(self, p):
    'arglist    :   arglist COMMA arg'
    p[0] = ast.TextNode('%s, %s' % (p[1], p[3]))

def p_function_0(self, p):
    'function   :   decl_specs type_spec func_name LPAREN f_arg_list RPAREN SEMI'
    p[0] = None # ignoring prototypes

def p_function_1(self, p):
    'function   :   decl_specs type_spec func_name LPAREN f_arg_list RPAREN block'
    p[0] = ast.Function(p[3], '%s %s' % (p[1], p[2]), '%s' % p[5], p[7])

def p_f_arg_list_1(self, p):
    'f_arg_list :   empty'
    p[0] = ast.TextNode('')

def p_f_arg_list_2(self, p):
    'f_arg_list :   decl_specs type_spec variable'
    p[0] = ast.TextNode('%s%s %s' % (p[1], p[2], p[3]))

def p_f_arg_list_3(self, p):
    'f_arg_list :   f_arg_list COMMA decl_specs type_spec variable'
    p[0] = ast.TextNode('%s, %s%s %s' % (p[1], p[3], p[4], p[5]))

def p_f_arg_list_4(self, p):
    'f_arg_list :   f_arg_list COMMA ELLIPSIS'
    p[0] = ast.TextNode('%s, ...' % p[1])

def p_block(self, p):
    'block  :   LBRACE block_content RBRACE'
    p[0] = ast.BlockInstruction(p[2])

def p_block_0(self, p):
    'block_content  :   empty'
    p[0] = ast.Block()

def p_block_content_1(self, p):
    'block_content  :   block_content decl'
    p[0] = p[1] # ignore decls

def p_block_content_2(self, p):
    'block_content  :   block_content instruction'
    p[0] = p[1]
    p[0].add(p[2])

def p_instruction_1(self, p):
    'instruction    :   block'
    p[0] = ast.BlockInstruction(p[1])

def p_instruction_2(self, p):
    'instruction    :   function_call instruction'
    p[0] = ast.MacroLoopInstruction(p[1], p[2])

def p_instruction_3(self, p):
    'instruction    :   expression SEMI'
    p[0] = ast.Instruction("%s;" % p[1])

def p_instruction_4(self, p):
    'instruction    :   label'
    p[0] = ast.LabelInstruction(p[1])

def p_instruction_5(self, p):
    'instruction    :   GOTO ID SEMI'
    p[0] = ast.GoToInstruction(p[2])

def p_instruction_6(self, p):
    'instruction    :   FOR for_header instruction'
    p[0] = ast.ForInstruction(p[2], p[3])

def p_instruction_7(self, p):
    'instruction    :   initializer SEMI'
    p[0] = ast.Instruction("%s;" % p[1])

def p_instruction_8(self, p):
    'instruction    :   RETURN  expression SEMI'
    p[0] = ast.RetInstruction("return %s;" % p[2])

def p_instruction_9(self, p):
    'instruction    :   IF LPAREN expression RPAREN instruction'
    p[0] = ast.IfInstruction(p[3], p[5], None)

def p_instruction_10(self, p):
    'instruction    :   IF LPAREN expression RPAREN instruction ELSE instruction'
    p[0] = ast.IfInstruction(p[3], p[5], p[7])

def p_label(self, p):
    'label  :   ID COLON'
    p[0] = ast.TextNode("%s" % p[1])

def p_for_header_1(self, p):
    'for_header :   LPAREN initializer SEMI expression SEMI expression RPAREN'
    p[0] = ast.TextNode("(%s; %s; %s)" % (p[2], p[4], p[6]))
    # TODO: other for expressions

def p_initializer(self, p):
    """
    initializer :   arg EQUALS expression
                |   arg PLUSEQUAL expression
                |   arg MINUSEQUAL expression
                |   arg TIMESEQUAL expression
                |   arg MODEQUAL expression
                |   arg DIVEQUAL expression
                |   arg LSHIFTEQUAL expression
                |   arg RSHIFTEQUAL expression
                |   arg ANDEQUAL expression
                |   arg OREQUAL expression
                |   arg XOREQUAL expression
    """
    p[0] = ast.Expression('%s %s %s' % (p[1], p[2], p[3]))

