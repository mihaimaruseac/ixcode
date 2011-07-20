# IxCode - app for code spelunking :: block diagram
# Data for parsing C code.

import ast

# Construct lang_lex_dict dictionary
lang_parse_dict = {}

# start symbol
lang_parse_dict['start'] = 'external_decl'

def p_external_decl_1(self, p):
    'external_decl  :   empty'
    print p.slice
lang_parse_dict['p_external_decl_1'] = p_external_decl_1

def p_external_decl_2(self, p):
    'external_decl  :   pp_directive external_decl'
    print p.slice
lang_parse_dict['p_external_decl_2'] = p_external_decl_2

def p_pp_directive(self, p):
    'pp_directive   :   PPHASH INCLUDE LT included GT'
    p[0] = ast.Include(p[4])
    print p[0]
lang_parse_dict['p_pp_directive'] = p_pp_directive

def p_included_1(self, p):
    'included   :   empty'
    p[0] = ""
lang_parse_dict['p_included_1'] = p_included_1

def p_included_2(self, p):
    'included   :   PERIOD included'
    p[0] = p[1] + p[2]
lang_parse_dict['p_included_2'] = p_included_2

def p_included_3(self, p):
    'included   :   DIVIDE included'
    p[0] = p[1] + p[2]
lang_parse_dict['p_included_3'] = p_included_3

def p_included_4(self, p):
    'included   :   LINECONT included'
    p[0] = p[1] + p[2]
lang_parse_dict['p_included_4'] = p_included_4

def p_included_5(self, p):
    'included   :   ID included'
    p[0] = p[1] + p[2]
lang_parse_dict['p_included_5'] = p_included_5

