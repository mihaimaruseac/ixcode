# IxCode - app for code spelunking :: block diagram
# Data for parsing C code.

# Construct lang_lex_dict dictionary
lang_parse_dict = {}

# start symbol
lang_parse_dict['start'] = 'foo'

def p_foo(self, p):
    'foo    :   PPHASH'
    raise SyntaxError
lang_parse_dict['p_foo'] = p_foo

